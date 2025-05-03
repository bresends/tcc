import streamlit as st
from chat import get_gemini_response

def app():
    st.set_page_config(
        page_title="Normas Técnicas Q&A",
        page_icon="📚",
    )

    st.title("📚 Normas Técnicas CBMGO - Q&A")

    st.warning(body=
        "Este Assistente Virtual foi treinado para responder perguntas sobre normas técnicas do CBMGO. Ele pode cometer falhas. Consulte as informações fornecidas com um especialista ou fonte confiável.",
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

    # Accept user input
    if prompt := st.chat_input("Faça uma pergunta sobre normas técnicas: "):
        # Display user message in chat message container and add it to the chat history
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant message while waiting for response and add it to the chat history
        with st.spinner("💭Pensando..."):
            response = get_gemini_response(messages=st.session_state.messages, model="gemini-2.0-flash")
            with st.chat_message("assistant"):
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    app()