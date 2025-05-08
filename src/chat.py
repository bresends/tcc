import streamlit as st
import google.genai as genai
from dotenv import load_dotenv
import os
from google.genai import types
from prompt_loader import load_parsed_docs_prompt

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

def get_gemini_response(messages, model="gemini-2.5-pro-exp-03-25"):
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

    normas = load_parsed_docs_prompt()

    cbmgo_qa_prompt_tmpl_str = (
        "Você é um assistente virtual especializado em normas técnicas do CBMGO (Corpo de Bombeiros Militar do Estado de Goiás). "
        "Seu objetivo é fornecer informações precisas e relevantes sobre normas técnicas, procedimentos e melhores práticas. "
        "Você não deve fornecer informações pessoais ou opiniões. "
        "Se não souber a resposta, informe que não tem certeza e sugira que o usuário consulte um especialista ou fonte confiável.\n"
        "Você deve responder em português, utilizando uma linguagem simples e acessível. "
        "Você deve ser capaz de explicar conceitos complexos de forma simples e acessível, ajudando os usuários a entenderem melhor as normas e suas aplicações práticas. "
        "A transcrição de todas as normas são fornecidas abaixo.\n"
        "---------------------\n"
        f"{normas}\n"
        "---------------------\n"
        "Com base nas informações de contexto e sem conhecimento prévio, "
        "responda à consulta sobre as normas técnicas do CBMGO (Corpo de Bombeiros Militar do Estado de Goiás). "
        "Forneça informações precisas e relevantes, incluindo detalhes sobre procedimentos, requisitos e melhores práticas. "
        "Explique conceitos complexos de forma simples e acessível. "
        "Responda de forma clara e objetiva, utilizando linguagem simples. "
        "Sempre que possível, forneça exemplos práticos. "
        "Caso não saiba a resposta, informe que não tem certeza e sugira que o usuário consulte um especialista ou fonte confiável.\n"
    )

    system_instruction = types.Part.from_text(text=cbmgo_qa_prompt_tmpl_str)

    stream = client.models.generate_content_stream(
        model=model,
        contents=formatted_contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
        ),
    )
    return stream
