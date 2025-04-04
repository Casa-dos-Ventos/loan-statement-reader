import pypdf
import re
import os
import argparse
from pathlib import Path


def find_page_numbering(text):
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


def split_pdf_by_page_numbering(input_pdf_path, output_dir):
    """
    Splits a PDF based on finding 'Page 1 of Y' patterns.

    Args:
        input_pdf_path (str or Path): Path to the concatenated input PDF file.
        output_dir (str or Path): Directory where the split PDF files will be saved.
    """
    input_path = Path(input_pdf_path)
    output_path = Path(output_dir)

    if not input_path.is_file():
        print(f"Error: Input file not found at '{input_path}'")
        return

    output_path.mkdir(
        parents=True, exist_ok=True
    )  # Create output dir if it doesn't exist

    print(f"Processing '{input_path.name}'...")

    try:
        reader = pypdf.PdfReader(str(input_path))
        num_pages_total = len(reader.pages)
        print(f"Total pages found: {num_pages_total}")

        boundaries = [0]  # Start index of the first sub-document is always page 0

        for i in range(num_pages_total):
            page = reader.pages[i]
            try:
                text = page.extract_text()
                if not text:  # Handle cases where text extraction fails for a page
                    print(f"Warning: Could not extract text from page {i + 1}.")
                    continue

                numbering = find_page_numbering(text)

                if numbering:
                    page_num, total_pages = numbering
                    # Found "Page 1 of Y" on a page *other* than the very first page (index 0)
                    # This indicates the start of a new logical document.
                    if page_num == 1 and i > 0:
                        print(
                            f"  Found boundary marker 'Page 1 of {total_pages}' on page {i + 1}. Starting new sub-document."
                        )
                        boundaries.append(i)
                # else:
                # Optional: Print if no numbering found on a page
                # print(f"  No 'Page X of Y' pattern found on page {i+1}.")

            except Exception as e:
                print(f"Warning: Error processing page {i + 1}: {e}")
                # Decide if you want to continue or stop on error
                continue  # Continue to next page

        # Add the final boundary (the total number of pages)
        boundaries.append(num_pages_total)
        print(f"Identified boundaries (start page indices): {boundaries}")

        # --- Splitting and Writing ---
        num_subdocs = len(boundaries) - 1
        if num_subdocs == 0:
            print("Warning: No 'Page 1 of Y' boundaries found. Cannot split.")
            # Optionally copy the whole file if no split needed?
            # import shutil
            # output_filename = output_path / f"{input_path.stem}_full.pdf"
            # shutil.copy(str(input_path), str(output_filename))
            # print(f"Copied original file as '{output_filename.name}'")
            return
        elif (
            num_subdocs == 1 and boundaries[0] == 0 and boundaries[1] == num_pages_total
        ):
            print(
                "Info: Only one logical document detected (or no 'Page 1 of Y' found after page 1). Result will be same as input."
            )
            # Fall through to write the single document below

        print(f"\nSplitting into {num_subdocs} sub-document(s)...")

        for i in range(num_subdocs):
            start_page = boundaries[i]
            end_page = boundaries[i + 1]  # Exclusive index

            if start_page >= end_page:
                print(
                    f"Warning: Skipping empty sub-document range starting at page {start_page + 1}."
                )
                continue

            output_filename = output_path / f"{input_path.stem}_subdoc_{i + 1}.pdf"
            writer = pypdf.PdfWriter()

            print(
                f"  Creating '{output_filename.name}' (Pages {start_page + 1} to {end_page})..."
            )
            for page_index in range(start_page, end_page):
                writer.add_page(reader.pages[page_index])

            try:
                with open(output_filename, "wb") as output_pdf:
                    writer.write(output_pdf)
            except Exception as e:
                print(f"  Error writing file '{output_filename.name}': {e}")

        print("\nSplitting complete.")

    except pypdf.errors.PdfReadError as e:
        print(
            f"Error: Failed to read PDF file '{input_path}'. It might be corrupted or password-protected."
        )
        print(f"Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

