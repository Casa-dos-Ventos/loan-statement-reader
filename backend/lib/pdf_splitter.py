# backend/lib/funcs.py (or directly in your streamlit script)
import pypdf
import re
import io
from typing import List, Optional, Tuple

def find_page_numbering(text: str) -> Optional[Tuple[int, int]]:
    """
    Searches for 'Pág X de Y' or similar patterns in the text.
    Returns (page_number, total_pages) if found, otherwise None.
    Handles variations like Pág/Pag./Pagina, accents, and spacing.
    """
    # Regex:
    # (?:P[aá]g|Pagina) - Matches "Pag", "Pág", or "Pagina" (non-capturing group)
    # \.?              - Matches an optional dot
    # \s*               - Matches zero or more whitespace characters
    # (\d+)             - Captures the current page number (Group 1)
    # \s*de\s*          - Matches " de " with flexible spacing
    # (\d+)             - Captures the total pages (Group 2)
    # re.IGNORECASE     - Makes the search case-insensitive
    pattern = re.compile(r"(?:P[aá]g|Pagina)\.?\s*(\d+)\s*de\s*(\d+)", re.IGNORECASE)
    match = pattern.search(text)
    if match:
        try:
            page_num = int(match.group(1))
            total_pages = int(match.group(2))
            return page_num, total_pages
        except (ValueError, IndexError):
            return None
    return None

def split_pdf_in_memory(pdf_bytes: bytes) -> List[io.BytesIO]:
    """
    Splits a PDF (provided as bytes) based on finding 'Page 1 of Y' patterns.

    Args:
        pdf_bytes (bytes): The content of the concatenated input PDF file.

    Returns:
        List[io.BytesIO]: A list of BytesIO streams, each containing a sub-document.
                          Returns a list with a single BytesIO stream containing the
                          original PDF if no splitting boundaries are found or on error.
    """
    sub_documents = []
    original_stream = io.BytesIO(pdf_bytes)

    try:
        reader = pypdf.PdfReader(original_stream)
        num_pages_total = len(reader.pages)
        # print(f"Total pages found: {num_pages_total}") # Optional: for debugging

        boundaries = [0] # Start index of the first sub-document

        for i in range(num_pages_total):
            try:
                page = reader.pages[i]
                text = page.extract_text()
                if not text:
                    # print(f"Warning: Could not extract text from page {i + 1}.") # Optional
                    continue

                numbering = find_page_numbering(text)

                if numbering:
                    page_num, total_pages = numbering
                    if page_num == 1 and i > 0:
                        # print(f"  Found boundary marker 'Page 1 of {total_pages}' on page {i + 1}.") # Optional
                        boundaries.append(i)

            except Exception as e:
                print(f"Warning: Error processing page {i + 1} for splitting: {e}")
                continue # Continue to next page

        boundaries.append(num_pages_total)
        # print(f"Identified boundaries (start page indices): {boundaries}") # Optional

        # --- Splitting and Creating In-Memory Streams ---
        num_subdocs = len(boundaries) - 1

        # If only one document is found (or no boundaries after page 1)
        if num_subdocs <= 1:
            print("Info: No effective split boundaries found. Returning original PDF content.")
            original_stream.seek(0) # Ensure stream is at the beginning
            return [original_stream]

        print(f"Splitting into {num_subdocs} sub-document(s)...") # Optional

        for i in range(num_subdocs):
            start_page = boundaries[i]
            end_page = boundaries[i + 1]

            if start_page >= end_page:
                # print(f"Warning: Skipping empty sub-document range starting at page {start_page + 1}.") # Optional
                continue

            writer = pypdf.PdfWriter()
            # print(f"  Creating sub-document {i + 1} (Pages {start_page + 1} to {end_page})...") # Optional
            for page_index in range(start_page, end_page):
                writer.add_page(reader.pages[page_index])

            # Write to an in-memory stream
            output_stream = io.BytesIO()
            writer.write(output_stream)
            output_stream.seek(0) # Rewind stream to the beginning for reading
            sub_documents.append(output_stream)
            writer.close() # Good practice to close writer

        print("Splitting complete.") # Optional
        return sub_documents

    except pypdf.errors.PdfReadError as e:
        print(f"Error: Failed to read PDF for splitting. It might be corrupted. Details: {e}")
        original_stream.seek(0)
        return [original_stream] # Return original on read error
    except Exception as e:
        print(f"An unexpected error occurred during splitting: {e}")
        original_stream.seek(0)
        return [original_stream] # Return original on other errors