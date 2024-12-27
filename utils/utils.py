import streamlit
from pathlib import Path

 
def start_chatbot(st: streamlit , directory: Path, function: callable):
    """
    Inicializa um chatbot dentro de uma aplicação Streamlit confirmando a presença de arquivos PDF e invocando uma função de callback fornecida.

    Parâmetros:
        st (streamlit): A instância do Streamlit usada para avisos, mensagens e notificações toast.
        directory (Path): Caminho para o diretório que deve conter os arquivos PDF necessários para a inicialização do chatbot.
        function (callable): Função de callback para iniciar o chatbot uma vez que os PDFs sejam validados.

    Retorna:
        None
    """
    # Verifica PDFs, mostra avisos e inicializa a conversa
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
    for existing_file in directory.glob("*.pdf"):
        existing_file.unlink()
    for new_file in pdf_list:
        with open(directory / new_file.name, "wb") as fp:
            fp.write(new_file.read())
        st.success("Arquivo(s) importado(s) com sucesso!", icon="✔️")