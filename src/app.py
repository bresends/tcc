import streamlit as st
import google.genai as genai
from dotenv import load_dotenv
import os

def initialize_google_genai():
    try:
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("API key not found in environment variables.")
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing Google GenAI: {e}")
        return None

def get_gemini_response(question):
    client = initialize_google_genai()
    if client is None:
        return "Error initializing Google GenAI client."

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=question,
    )
    return response.text

def app():
    # Initialize Streamlit app
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