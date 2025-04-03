import streamlit as st
import io
from backend.prompts import PROMPTS
from backend.schemas import SCHEMAS
from backend.connectors.gemini_connector import generate_response


def classify_document(document):
    """
    Classify a document into one of three categories using the AI model.
    """
    # Replace with actual prediction logic
    prediction = generate_response(
        PROMPTS["classifier"], SCHEMAS["classifier"], document
    )
    return prediction


def extract_text(document, doc_source):
    prediction = generate_response(PROMPTS["extractor"], SCHEMAS[doc_source], document)
    return prediction


def classify_uploaded_files():
    """
    Classify each uploaded file in the session state into three categories and extract text based on the classification.
    """
    if "uploaded_files" in st.session_state:
        my_bar = st.progress(0, text="Processando arquivos...")
        processed_results = {}
        for i, file in enumerate(st.session_state["uploaded_files"]):
            with st.spinner(f"Processando arquivo: {file.name}"):
                # Classify the document
                classification = classify_document(file.getvalue())
                source = classification["Fonte_documento"]

                # Extract text based on the classification
                extracted_text = extract_text(file.getvalue(), source)

            processed_results[file.name] = {
                "Fonte": source,
                "Conteúdo": extracted_text,
            }
            my_bar.progress(
                (i + 1) / len(st.session_state["uploaded_files"]),
                text="Processando arquivos...",
            )
        return processed_results
    else:
        st.warning("Nenhum arquivo foi enviado.")
        st.markdown("[Voltar para a página inicial](./)")


results = classify_uploaded_files()
if results is not None:
    st.write("Classification Results:", results)
