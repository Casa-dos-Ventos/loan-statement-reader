import pandas as pd
import pypdf
import re
import io
from typing import List, Optional, Tuple

def flatten_json(y, parent_key="", sep="."):
    """Recursively flattens a nested dictionary into a single dictionary with compound keys."""
    items = []
    if isinstance(y, dict):
        for k, v in y.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.extend(flatten_json(v, new_key, sep=sep).items())
    elif isinstance(y, list):
        # If it's a list of dicts, we keep it as a list and handle it later
        items.append((parent_key, y))
    else:
        items.append((parent_key, y))
    return dict(items)


def recursive_expand_rows(data, list_keys, sep="."):
    """
    Recursively expands nested lists in a JSON object into a flat list of rows.

    Parameters:
    - data: The JSON data to expand
    - list_keys: A list of paths to the lists to expand, in order of expansion
    - sep: The separator to use for compound keys

    Returns:
    - A list of flattened rows
    """
    if not list_keys:
        return [data]

    current_key = list_keys[0]
    remaining_keys = list_keys[1:]

    # First flatten to access the nested list by path
    flat_data = flatten_json(data, sep=sep)

    # Get the list to expand safely
    list_to_expand = flat_data.get(current_key, [])

    # Create a copy of flat_data without the current_key
    base_data = {k: v for k, v in flat_data.items() if k != current_key}

    # If the list is empty or not found, return the data as is
    if not list_to_expand or not isinstance(list_to_expand, list):
        return [flat_data]

    rows = []
    for item in list_to_expand:
        # Create a new row combining base data and item
        row_data = {**base_data}

        # Add the item properties to the row with prefixed keys
        item_dict = item if isinstance(item, dict) else {current_key: item}
        for k, v in flatten_json(item_dict, sep=sep).items():
            row_data[f"{current_key}{sep}{k}"] = v

        # Recursively expand any remaining lists
        expanded_rows = recursive_expand_rows(row_data, remaining_keys, sep)
        rows.extend(expanded_rows)

    return rows



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