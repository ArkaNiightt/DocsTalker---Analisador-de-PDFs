from utils.avatar_image import load_avatar
import streamlit
from time import sleep


def get_chat_mensage(st: streamlit, mensagem, container, input_mensagem=None, chain=None, is_input=False):
    """
    Lida com a exibição de mensagens de chat em uma aplicação Streamlit.

    Parâmetros:
    st (streamlit): A instância do Streamlit.
    mensagem: O objeto de mensagem contendo o tipo e o conteúdo da mensagem.
    container: O container no qual as mensagens de chat serão exibidas.
    input_mensagem (str, opcional): A mensagem de entrada do usuário. Padrão é None.
    chain (opcional): O objeto chain usado para gerar respostas. Padrão é None.
    is_input (bool, opcional): Flag indicando se a mensagem é uma mensagem de entrada. Padrão é False.

    Retorna:
    Nenhum
    """
    if is_input:
        chat = container.chat_message(
            "human", avatar=load_avatar("images/avatar_user.png"))
        chat.markdown(mensagem)
        chat = container.chat_message(
            "ai", avatar=load_avatar("images/avatar_assistant.png"))
        chat.markdown("Gerando Resposta...")
        with st.spinner(""):
            sleep(1)
            resposta = chain.invoke({"question": input_mensagem})
            st.session_state["ultima_resposta"] = resposta
            st.rerun()
    else:
        if mensagem.type == "human":
            chat = container.chat_message(
                "human", avatar=load_avatar("images/avatar_user.png"))
            chat.markdown(mensagem.content)
        elif mensagem.type == "ai":
            chat = container.chat_message(
                "ai", avatar=load_avatar("images/avatar_assistant.png"))
            chat.markdown(mensagem.content)
