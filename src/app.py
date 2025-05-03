import streamlit as st
import google.genai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Please set the GOOGLE_API_KEY environment variable to the path of your service account key file.")
    st.stop()

client = genai.Client(api_key=api_key)

def get_gemini_response(question):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=question,
    )
    return response.text

st.set_page_config(
    page_title="Normas Técnicas Q&A",
    page_icon="📚"
)

st.title="Normas Técnicas Q&A"
st.header("Gemini Pro Chatbot")

input = st.text_input("Ask me anything")
submit = st.button("Generate Response")

if submit:
    response = get_gemini_response(input)
    st.write(response)