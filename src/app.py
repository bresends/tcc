import streamlit as st
from chat import get_gemini_response

def app():
    st.set_page_config(
        page_title="Normas Técnicas Q&A",
        page_icon="📚",
    )

    st.title("📚 Normas Técnicas Q&A")

    user_message = st.chat_input("Faça uma pergunta sobre as normas técnicas: ")

    if user_message:
        if "messages" in st.session_state:
            messages = st.session_state["messages"]
        else:
            messages = []
            st.session_state["messages"] = messages

        messages.append({"user": "user", "text": user_message})

        # mensagem de resposta do assistant
        response = get_gemini_response(user_message)

        messages.append({"user": "assistant", "text": response})

        for message in messages:
            # colocar a mensagem do usuário na tela
            with st.chat_message(message["user"]):
                st.write(message["text"])

if __name__ == "__main__":
    app()