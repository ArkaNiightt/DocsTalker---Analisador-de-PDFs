import streamlit
from pathlib import Path

def start_chatbot(st, directory, function):
    directory = Path(directory) if isinstance(directory, str) else directory
    if len(list(directory.glob("*.pdf"))) == 0:
        st.warning("Nenhum arquivo PDF importado")
        st.toast("Adicione arquivos .pdf para inicializar o chatbot", icon="❌")
    else:
        with st.spinner("Inicializando ChatBot..."):
            function()
            st.toast("Chatbot inicializado com sucesso!", icon="✔️")

def manage_pdfs(st: streamlit, directory: Path, pdf_list: list):
    """
    Gerencia arquivos PDF excluindo os existentes no diretório especificado e salvando novos da lista fornecida.
    Parâmetros:
        st (streamlit): A instância do Streamlit usada para exibir mensagens de sucesso.
        directory (Path): O diretório onde os arquivos PDF são gerenciados.
        pdf_list (list): Uma lista de novos arquivos PDF a serem salvos no diretório.
    Retorna:
        None
    """
    directory = Path(directory) if isinstance(directory, str) else directory
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)
    for existing_file in directory.glob("*.pdf"):
        existing_file.unlink()
    for new_file in pdf_list:
        with open(directory / new_file.name, "wb") as fp:
            fp.write(new_file.read())