import streamlit as st


st.set_page_config(
    page_title="Loan statement reader",
    page_icon=":bank:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Report a bug": "mailto:murilo.moura@casadosventos.com.br",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)

pages = {
    "Loan reader": [
        st.Page("frontend/home.py", title="Upload de fatura"),
        st.Page("frontend/text_extraction.py", title="Resultado da leitura"),
    ]
}

pg = st.navigation(pages)
pg.run()
