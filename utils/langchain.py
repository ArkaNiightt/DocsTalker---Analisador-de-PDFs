import streamlit as st
from pathlib import Path
from utils.config_utils import get_config
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

ARQUIVOS = Path(__file__).parent.parent / "arquivos"


def documents_loader():
    """
    Carrega e processa documentos PDF de um diretório especificado.

    Esta função procura por todos os arquivos PDF no diretório especificado pela 
    variável global ARQUIVOS, usa o PyPDFLoader para carregar cada arquivo PDF, e 
    agrega o conteúdo de todos os documentos PDF carregados em uma única lista.

    Retorna:
        list: Uma lista contendo o conteúdo de todos os documentos PDF carregados.
    """
    documentos = []
    for arquivo in ARQUIVOS.glob("*.pdf"):
        loader = PyPDFLoader(str(arquivo))
        documentos_arquivo = loader.load()
        documentos.extend(documentos_arquivo)
    return documentos


def split_documents(documents):
    """
    Divide uma lista de documentos em partes menores usando um divisor de texto recursivo por caracteres.
    Args:
        documents (list): Uma lista de objetos de documentos a serem divididos. Cada objeto de documento deve ter um atributo 'metadata'.
    Retorna:
        list: Uma lista de partes menores de documentos com metadados atualizados. Cada parte terá os campos de metadados 'source' e 'doc_id'.
    """
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=250,
        separators=[".", "\n", "\n\n", "", " "]
    )
    documentos = recursive_splitter.split_documents(documents)

    for i, doc in enumerate(documents):
        doc.metadata["source"] = doc.metadata["source"].split("/")[-1]
        doc.metadata["doc_id"] = i
    return documentos


def create_vector_store(documents):
    """
    Cria um armazenamento vetorial a partir de uma lista de documentos usando embeddings do OpenAI e FAISS.

    Args:
        documents (list): Uma lista de documentos a serem incorporados e armazenados.

    Retorna:
        FAISS: Um armazenamento vetorial FAISS contendo os documentos incorporados.
    """
    embeddings_models = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings_models
    )
    return vector_store


def create_chain_conversation():
    """
    Cria uma cadeia de recuperação conversacional usando componentes do LangChain.
    Esta função executa as seguintes etapas:
    1. Carrega documentos usando a função `documents_loader`.
    2. Divide os documentos carregados usando a função `split_documents`.
    3. Cria um armazenamento vetorial a partir dos documentos divididos usando a função `create_vector_store`.
    4. Inicializa uma instância `ChatOpenAI` com o nome do modelo da configuração.
    5. Configura uma `ConversationBufferMemory` para armazenar o histórico de conversas e respostas.
    6. Configura um recuperador do armazenamento vetorial com o tipo de busca e parâmetros de busca da configuração.
    7. Cria um template de prompt a partir da configuração.
    8. Constrói uma `ConversationalRetrievalChain` usando o modelo de chat, memória, recuperador e template de prompt.
    9. Armazena a cadeia de chat criada no estado da sessão do Streamlit sob a chave "chain".
    Retorna:
        Nenhum
    """
    documents = documents_loader()
    documents = split_documents(documents)
    vector_store = create_vector_store(documents)

    chat = ChatOpenAI(
        model=get_config("model_name"),
        api_key=st.secrets["OPENAI_API_KEY"],
        temperature=1.0,
    )
    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )
    retriever = vector_store.as_retriever(
        search_type=get_config("retrieval_search_type"),
        search_kwargs=get_config("retrieval_kwargs")
    )
    prompt_template = PromptTemplate.from_template(get_config("prompt"))
    chat_chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        memory=memory,
        retriever=retriever,
        return_source_documents=True,
        verbose=True,
        combine_docs_chain_kwargs={"prompt": prompt_template}
    )

    st.session_state["chain"] = chat_chain
