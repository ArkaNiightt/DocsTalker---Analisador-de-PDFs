import streamlit as st
from utils.config_utils import get_config, MODEL_OPTIONS, SEARCH_TYPES
from utils.langchain import create_chain_conversation, ARQUIVOS
from utils.sidebar_utils import sidebar_config
from utils.utils import start_chatbot


def config_window() -> None:
    """Configure the Streamlit window and chatbot parameters."""
    st.set_page_config(
        page_title="Configurações do Chatbot",
        page_icon="⚙️",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={"Get Help": "https://www.streamlit.io/docs"}
    )
    st.header(
        "⚙️ Configurações de Parâmetros do Chatbot",
        help="Configurações do ChatBot para leitura de documentos PDF",
        divider=True
    )

    model_name = st.selectbox(
        "Modelo de Linguagem",
        MODEL_OPTIONS,
        index=MODEL_OPTIONS.index(get_config("model_name")),
        key="model_name_input",
        help="Modelo de linguagem a ser utilizado pelo ChatBot"
    )

    retrieval_search_type = st.selectbox(
        "Tipo de Busca",
        options=SEARCH_TYPES,
        index=SEARCH_TYPES.index(get_config("retrieval_search_type")),
        key="retrieval_search_type_selectbox",
        help="Tipo de busca a ser utilizado pelo ChatBot"
    )
    retrieval_kwargs: dict = {}

    retrieval_kwargs['k'] = st.select_slider(
        "Número de Documentos Retornados (k) - Recomendado: 5",
        options=list(range(1, 101)),
        value=get_config("retrieval_kwargs")['k'],
        key="retrieval_kwargs_k_slider",
        help="Número de documentos mais relevantes a serem retornados",
        on_change=lambda: st.session_state.update(
            {"retrieval_kwargs": retrieval_kwargs})
    )

    retrieval_kwargs['fetch_k'] = st.select_slider(
        "Número de Documentos Buscados (fetch_k) - Recomendado: 20",
        options=list(range(1, 101)),
        value=get_config("retrieval_kwargs")['fetch_k'],
        key="retrieval_kwargs_fetch_k_slider",
        help="Número total de documentos a serem buscados antes da filtragem",
        on_change=lambda: st.session_state.update(
            {"retrieval_kwargs": retrieval_kwargs})
    )

    prompt = st.text_area(
        label="Prompt Template - Modelo de Prompt",
        value=get_config("prompt"),
        height=400,
        key="prompt_slider",
        help="Template de prompt a ser utilizado pelo ChatBot"

    )

    if st.button(
        "Salvar Configurações",
        key="salvar_config",
        help="Salva as configurações do ChatBot",
        use_container_width=True
    ):
        st.session_state["model_name"] = model_name
        st.session_state["retrieval_search_type"] = retrieval_search_type
        st.session_state["retrieval_kwargs"] = retrieval_kwargs
        st.session_state["prompt"] = prompt
        st.toast("Configurações Salvas com Sucesso!", icon="✔️")
        st.rerun()

    if st.button(
        "Atualizar ChatBot", 
        key="atualizar_chatbot",
        help="Atualiza o ChatBot com as novas configurações",
        type="primary",
        use_container_width=True
        ):
        start_chatbot(st, ARQUIVOS, create_chain_conversation)

def app() -> None:
    """Main Streamlit application."""
    config_window()
    with st.sidebar:
        sidebar_config(st)


app()