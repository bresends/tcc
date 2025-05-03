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

    user_message = st.chat_input("Faça uma pergunta sobre normas técnicas: ")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        messages = [{"role": "assistant", "content": "Olá! Como posso ajudar você com normas técnicas?"}]
        st.session_state["messages"] = messages

    if user_message:
        # Append user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_message})

        # Get response from Gemini API
        with st.spinner("Aguarde..."):
            gemini_response = get_gemini_response(question=user_message, model="gemini-2.0-flash")
            st.session_state.messages.append({"role": "assistant", "content": gemini_response})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


if __name__ == "__main__":
    app()