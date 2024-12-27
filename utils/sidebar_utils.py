import streamlit
from utils.langchain import create_chain_conversation, ARQUIVOS
from utils.config_utils import get_config
from utils.utils import start_chatbot, manage_pdfs


def sidebar_home(st: streamlit, ARQUIVOS=ARQUIVOS):
    st.sidebar.title("Importar Documento PDF")
    uploaded_pdfs = st.file_uploader(
        "Escolha um arquivo PDF",
        type="pdf",
        accept_multiple_files=True,
        help="Arraste e solte o arquivo PDF aqui"
    )
    if uploaded_pdfs:
        manage_pdfs(st, ARQUIVOS, uploaded_pdfs)
    label_botao = "Inicializar ChatBot"
    if "chain" in st.session_state:
        label_botao = "Atualizar ChatBot"
    if st.button(
        label_botao,
        use_container_width=True,
        key="botao_chatbot"
    ):
        start_chatbot(st, ARQUIVOS, create_chain_conversation)
    st.info("Para alterar as configurações, acesse a página de configurações")


def sidebar_config(st: streamlit):
    """
    Configura a barra lateral para as configurações do ChatBot em uma aplicação Streamlit.
    Esta função cria um expansor na barra lateral do Streamlit onde os usuários podem visualizar e verificar 
    as configurações atuais do ChatBot. Ela recupera e exibe o nome do modelo, tipo de busca, 
    parâmetros de recuperação e prompt da configuração.
    Args:
        st (streamlit): A instância do Streamlit usada para renderizar os componentes da barra lateral.
    Returns:
        None
    """
    with st.expander(label="Configurações do ChatBot"):
        model_name = get_config("model_name", st)
        search_type = get_config("retrieval_search_type", st)
        retrieval_kwargs = get_config("retrieval_kwargs", st)
        prompt = get_config("prompt", st)

        st.markdown(f"Modelo: `{model_name}`")
        st.markdown(f"Search Type: `{search_type}`")
        st.write("Retrieval Kwargs:", retrieval_kwargs)
        st.text_area("Prompt:", value=prompt, height=400, disabled=True)
    st.info("Verifique se as configurações estão corretas antes de iniciar ou atualizar o ChatBot.")
