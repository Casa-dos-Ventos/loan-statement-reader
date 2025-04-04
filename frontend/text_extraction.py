from collections import defaultdict
import streamlit as st
import io
from backend.prompts import PROMPTS
from backend.schemas import SCHEMAS, LIST_KEYS
from backend.lib.funcs import recursive_expand_rows, split_pdf_in_memory
from backend.connectors.gemini_connector import generate_response
import pandas as pd


def classify_document(document):
    """
    Classify a document into one of three categories using the AI model.
    """
    model = "gemini-2.0-flash-lite"
    prediction = generate_response(
        model, PROMPTS["classifier"], SCHEMAS["classifier"], document
    )
    return prediction


def extract_text(document, doc_source):
    model = "gemini-2.0-flash-lite"
    prediction = generate_response(
        model, PROMPTS["extractor"], SCHEMAS[doc_source], document
    )
    return prediction


# @st.cache_data(show_spinner=False)
def classify_uploaded_files(files):
    """
    Classify each uploaded file, split if necessary (for 'BNB'),
    and extract text from the resulting document(s).
    Returns results grouped by original file name.
    """

    my_bar = st.progress(0, text="Processando arquivos...")
    num_files = len(files)
    processed_results = defaultdict(list)
    for id_file, file in enumerate(files):
        with st.spinner(
            f"Processando arquivo {id_file + 1} de {num_files}: {file.name}"
        ):
            # Classify the document
            classification = classify_document(file.getvalue())
            source = classification["Fonte_documento"]

            if source == "BNB":
                # Split the document into multiple sub-documents
                sub_documents = split_pdf_in_memory(file.getvalue())

                for id_subdoc, sub_doc in enumerate(sub_documents):
                    # Extract text based on the classification
                    extracted_text = extract_text(sub_doc.read(), source)

                    processed_results[file.name].append(
                        {
                            "Fonte": source,
                            "Conteúdo": extracted_text,
                            "Parte": f"{id_subdoc + 1} de {len(sub_documents)}",
                        }
                    )
            else:
                # Extract text based on the classification
                extracted_text = extract_text(file.getvalue(), source)

                processed_results[file.name].append(
                    {
                        "Fonte": source,
                        "Conteúdo": extracted_text,
                    }
                )

            my_bar.progress(
                (id_file + 1) / num_files,
                text="Processando arquivos...",
            )

    my_bar.empty()  # Remove the progress bar after processing is complete
    return processed_results


if "uploaded_files" in st.session_state:
    results = classify_uploaded_files(st.session_state["uploaded_files"])
else:
    results = None
    st.warning("Nenhum arquivo foi enviado.")
    st.markdown("[Voltar para a página inicial](./)")

if results is not None:
    st.write(results)
    """# group the results by source
    grouped_results = defaultdict(list)

    for file_name, result in results.items():
        st.subheader(f"Arquivo: {file_name}")
        st.write(f"Fonte: {result['Fonte']}")

        # Perform recursive expansion once per file
        expanded_file = pd.DataFrame(
            recursive_expand_rows(result["Conteúdo"], LIST_KEYS[result["Fonte"]])
        )
        st.dataframe(expanded_file, hide_index=True)

        # Group the extractions by source
        source = result["Fonte"]
        grouped_results[source].append(expanded_file)

    # Create an Excel file with each source as a separate sheet
    with io.BytesIO() as output:
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            for source, tables in grouped_results.items():
                combined_table = pd.concat(tables, ignore_index=True)
                combined_table.to_excel(writer, sheet_name=source, index=False)
        output.seek(0)

        # Provide the file for download
        st.download_button(
            label="Baixar extrações agrupadas",
            data=output,
            file_name="extracted_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )"""
