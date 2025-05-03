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
