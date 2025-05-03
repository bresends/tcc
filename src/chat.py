import streamlit as st
import google.genai as genai
from dotenv import load_dotenv
import os
from google.genai import types

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

def get_gemini_response(messages, model="gemini-2.5-pro-preview-03-25"):
    client = initialize_google_genai()

    if client is None:
        return "Error initializing Google GenAI client."

    # Transform message roles based on model version (2.5 has a different api)
    formatted_messages = []
    for m in messages:
        role = m["role"]
        # For Gemini 2.5 models, convert "assistant" role to "model"
        if "2.5" in model and role == "assistant":
            role = "model"
        formatted_messages.append({"role": role, "content": m["content"]})

    # Convert messages to the required format using types.Content and types.Part
    formatted_contents = [
        types.Content(
            role=m["role"],
            parts=[types.Part.from_text(text=m["content"])]
        ) for m in formatted_messages
    ]

    system_instruction = types.Part.from_text(text="""
Você é um ótimo assistente que ajuda a responder perguntas sobre normas técnicas do CBMGO (Corpo de Bombeiros Militar do Estado de Goiás).
Você deve fornecer informações precisas e relevantes sobre as normas técnicas, incluindo detalhes sobre procedimentos, requisitos e melhores práticas.
Além disso, você deve ser capaz de explicar conceitos complexos de forma simples e acessível, ajudando os usuários a entenderem melhor as normas e suas aplicações práticas.
Você deve responder de forma clara e objetiva, utilizando uma linguagem simples e acessível.
Sempre que possível, forneça exemplos práticos para ilustrar suas respostas.
Caso não saiba a resposta, informe que não tem certeza e sugira que o usuário consulte um especialista ou fonte confiável.
""")

    stream = client.models.generate_content_stream(
        model=model,
        contents=formatted_contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
        ),
    )
    return stream
