import streamlit as st
import pandas as pd

st.markdown(
    "<h1 style='text-align: center;'>🏦 Loan statement reader</h1>", unsafe_allow_html=True
)

st.write("Instruções...")
uploaded_files = st.file_uploader(
    "Adicionar extratos dos finaciamentos", accept_multiple_files=True,type="pdf",key = "files"
)

# if arquivo enviado: ativar botão
if st.button("Extrair saldos dos extratos", use_container_width=True):
    if uploaded_files:
        st.session_state["uploaded_files"] = uploaded_files
        st.switch_page("frontend/text_extraction.py")
    else:
        st.warning("Por favor, adicione pelo menos um arquivo antes de continuar.")