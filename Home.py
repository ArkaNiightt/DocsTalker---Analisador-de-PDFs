import streamlit as st
from utils.sidebar_utils import sidebar_home
from utils.chat_utils import get_chat_mensage


def chat_window():
    st.header(
        "📝 DocsTalker: Seu bate-papo com PDFs",
        help="Chatbot para leitura de documentos PDF",
        divider=True
    )

    if not "chain" in st.session_state:
        st.warning("Inicialize o ChatBot para começar", icon="⚠️")
        st.stop()

    chain = st.session_state["chain"]
    memory = chain.memory

    mensagens = memory.load_memory_variables({})["chat_history"]

    container = st.container()
    for mensagem in mensagens:
        get_chat_mensage(st, mensagem, container)

    input_mensagem = st.chat_input(
        placeholder="Converse com os seus documentos pdfs...", key="input_mensagem")
    if input_mensagem:
        get_chat_mensage(
            st,
            input_mensagem,
            container,
            input_mensagem,
            chain,
            is_input=True
        )

def app():
    st.set_page_config(
        page_title="DocsTalker - Chatbot para PDFs",
        page_icon="📝",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={"Get Help": "https://www.streamlit.io/docs"}
    )
    with st.sidebar:
        sidebar_home(st)
    chat_window()


if __name__ == "__main__":
    app()
