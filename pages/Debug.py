import streamlit as st
from langchain.prompts import PromptTemplate
from utils.config_utils import get_config


def debug_window():
    st.set_page_config(
        page_title="Debug Window",
        page_icon="🐞",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://www.streamlit.io/docs",
            "Report a bug": "https://github.com/ArkaNiightt"
        },
    )
    st.header(
        "Visualização de Dados e Depuração",
        help="Esta página é destinada a depuração e teste de funcionalidades.",
        divider=True
    )

    prompt_template = get_config("prompt")
    prompt_template = PromptTemplate.from_template(prompt_template)

    if not "ultima_resposta" in st.session_state:
        st.warning("Nenhuma resposta foi gerada ainda.", icon="⚠️")
        st.stop()

    ultima_resposta = st.session_state['ultima_resposta']

    contexto_docs = ultima_resposta['source_documents']
    contexto_list = [doc.page_content for doc in contexto_docs]
    contexto_str = '\n\n'.join(contexto_list)

    chain = st.session_state['chain']
    memory = chain.memory
    chat_history = memory.buffer_as_str

    with st.container(border=True):
        prompt = prompt_template.format(
            chat_history=chat_history,
            context=contexto_str,
            question=''
        )
        st.code(prompt)


debug_window()
