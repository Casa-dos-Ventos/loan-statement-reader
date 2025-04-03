from io import BytesIO
import json
from pathlib import Path
from typing import List

import google.auth
from loguru import logger
from pypdf import PdfReader
from pypdf import PdfWriter
import vertexai
from vertexai.preview.generative_models import GenerationConfig
from vertexai.preview.generative_models import GenerativeModel
from vertexai.preview.generative_models import Part

from lib import utils
from lib.custom_types import DocumentIO

# Initialize Vertex AI
_, PROJECT_ID = google.auth.default()
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

MODEL_NAME = "gemini-1.5-pro"
model = GenerativeModel(MODEL_NAME)

with open("./data/gemini_instructions_split.txt", "r") as f:
    SPLIT_PROMPT_INSTRUCTIONS = f.read()


def get_pdf_split_points(document_io: DocumentIO) -> List[int]:
    blob, mimetype = document_io
    document = Part.from_data(
        mime_type=mimetype,
        data=blob,
    )
    contents = [document, SPLIT_PROMPT_INSTRUCTIONS]
    with utils.timeit(f"Gemini [{MODEL_NAME}] - OCR - Extract breakpoints"):
        generation_config = GenerationConfig(
            response_mime_type="application/json",
            temperature=0,
        )
        response = model.generate_content(
            contents, generation_config=generation_config, stream=False
        )
        raw_response = response.text  # type: ignore
    logger.debug("[BREAKPOINTS] Raw response: {}", raw_response)
    results = json.loads(raw_response.strip().strip('"'))
    start_pages = [int(page) - 1 for page in results]
    logger.debug("[BREAKPOINTS] Gemini returned {start_pages}", start_pages=start_pages)
    return start_pages


def split_pdf(document_io: DocumentIO) -> List[DocumentIO]:
    start_pages = get_pdf_split_points(document_io)
    blob, _ = document_io
    # read into pdfreader
    bytes_io = BytesIO(blob)
    bytes_io.seek(0)
    pdfreader = PdfReader(bytes_io)
    # assert gemini result makes sense
    total_pages = len(pdfreader.pages)
    assert all(0 <= i < total_pages for i in start_pages)
    # build page ranges
    page_ranges = list(zip(start_pages, start_pages[1:] + [total_pages]))
    # write splitted pdfs as document io list
    splitted_document_io_list = []
    for page_range in page_ranges:
        assert len(page_range) == 2
        start, end = page_range
        pdfwriter = PdfWriter()
        # TODO improve this
        for idx in range(start, end):
            pdfwriter.add_page(pdfreader.pages[idx])
        # write to bytesio
        pdf_stream = BytesIO()
        pdfwriter.write(pdf_stream)
        pdf_stream.seek(0)
        splitted_document_io_list.append((pdf_stream.read(), "application/pdf"))
    return splitted_document_io_list


if __name__ == "__main__":
    filepath = Path("../scripts/test-invoices/unified.pdf")
    with open(filepath, "rb") as pdf_file:
        blob = pdf_file.read()

    mimetype = "application/pdf"
    document_io = (blob, mimetype)

    splitted_document_io_list = split_pdf(document_io=document_io)

    # document = Part.from_data(mime_type="application/pdf", data=pdf_content_binary)

    # with open(filepath, "rb") as f:
    #     blob = BytesIO(f.read())
    #     blob.seek(0)