import streamlit as st

MODEL_NAME = "gpt-4o"
RETRIEVAL_SEARCH_TYPE = "mmr"
RETRIEVAL_KWARGS = {"k": 5, "fetch_k": 20}
PROMPT = """
Você é um chatbot que conversa sobre documentos PDF que lhe são fornecidos.
No contexto fornecido, você deve ser capaz de responder a perguntas sobre o conteúdo dos documentos.
Se você não souber a resposta, você pode dizer que não sabe e não tente inventar a resposta.

Contexto:
{context}

Conversa atual:
{chat_history}

Human: {question}
AI:"""

MODEL_OPTIONS = ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo", "o1-mini"]
SEARCH_TYPES = ["mmr", "similarity", "similarity_score_threshold", "hybrid"]

def get_config(config: str, st=st):
    """
    Recupera um valor de configuração do estado da sessão ou valores padrão.

    Args:
        config (str): O nome da configuração a ser recuperada.
        st: O módulo streamlit, que contém o estado da sessão.

    Retorna:
        O valor da configuração solicitada se existir no estado da sessão,
        caso contrário, retorna um valor padrão com base no nome da configuração.
        Retorna None se o nome da configuração não for reconhecido.
    """
    if config.lower() in st.session_state:
        return st.session_state[config.lower()]
    if config.lower() == "model_name":
        return MODEL_NAME
    elif config.lower() == "retrieval_search_type":
        return RETRIEVAL_SEARCH_TYPE
    elif config.lower() == "retrieval_kwargs":
        return RETRIEVAL_KWARGS
    elif config.lower() == "prompt":
        return PROMPT
    return None