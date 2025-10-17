import streamlit as st

from auth import AuthManager
from chat import get_chat_response
from login_page import show_login_page


def app():
    st.set_page_config(
        page_title="Normas Técnicas CBMGO",
        page_icon="📚",
    )

    # Inicializa o gerenciador de autenticação
    auth_manager = AuthManager()

    # Verifica se o usuário está autenticado
    if not auth_manager.is_authenticated():
        show_login_page(auth_manager)
        return

    # Título com botão de sair na mesma linha
    col1, col2 = st.columns([6, 1])
    with col1:
        st.title("📚 Normas Técnicas CBMGO")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Espaço para alinhar com o título
        if st.button("Sair", type="primary", use_container_width=True):
            auth_manager.logout()
            st.rerun()

    # CSS para deixar o botão vermelho
    st.markdown(
        """
        <style>
        button[kind="primary"] {
            background-color: #dc3545 !important;
            border-color: #dc3545 !important;
        }
        button[kind="primary"]:hover {
            background-color: #c82333 !important;
            border-color: #bd2130 !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.warning(
        body="Este Assistente Virtual foi treinado para responder perguntas sobre normas técnicas do CBMGO. Ele pode cometer falhas. Consulte as informações fornecidas com um especialista ou fonte confiável.",
    )

    with st.chat_message("assistant"):
        st.write("👋 Olá! Como posso ajudar você com normas técnicas?")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Faça uma pergunta sobre normas técnicas: "):
        # Display user message in chat message container and add it to the chat history
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant message with spinner inside the chat message
        with st.chat_message("assistant"):
            with st.spinner("💭 Processando..."):
                stream = get_chat_response(
                    messages=st.session_state.messages, model="gemini-2.5-flash"
                )
                full_response = st.write_stream(stream)

        # Add the complete response to session state
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )


if __name__ == "__main__":
    app()
