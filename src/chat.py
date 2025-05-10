import os
import streamlit as st
from dotenv import load_dotenv
from prompt_loader import load_parsed_docs_prompt
from langfuse.openai import OpenAI

load_dotenv()

def check_env_vars():
    REQUIRED_ENV_VARS = [
    "LLM_API_KEY",
    "LLM_BASE_URL",
    "LANGFUSE_SECRET_KEY",
    "LANGFUSE_PUBLIC_KEY",
    "LANGFUSE_HOST",
    ]

    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing:
        st.error(f"Missing required environment variables: {', '.join(missing)}")
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    return True

check_env_vars()

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
)

def get_chat_response(messages, model="gemini-2.5-pro-exp-03-25"):
    all_norms = load_parsed_docs_prompt()

    system_prompt = (
        "Você é um assistente virtual especializado em normas técnicas do CBMGO (Corpo de Bombeiros Militar do Estado de Goiás). "
        "Seu objetivo é fornecer informações precisas e relevantes sobre normas técnicas, procedimentos e melhores práticas. "
        "Você não deve fornecer informações pessoais ou opiniões. "
        "Se não souber a resposta, informe que não tem certeza e sugira que o usuário consulte um especialista ou fonte confiável.\n"
        "Você deve responder em português, utilizando uma linguagem simples e acessível. "
        "Você deve ser capaz de explicar conceitos complexos de forma simples e acessível, ajudando os usuários a entenderem melhor as normas e suas aplicações práticas. "
        "A transcrição de todas as normas são fornecidas abaixo.\n"
        "---------------------\n"
        f"{all_norms}\n"
        "---------------------\n"
        "Com base nas informações de contexto e sem conhecimento prévio, "
        "responda à consulta sobre as normas técnicas do CBMGO (Corpo de Bombeiros Militar do Estado de Goiás). "
        "Forneça informações precisas e relevantes, incluindo detalhes sobre procedimentos, requisitos e melhores práticas. "
        "Explique conceitos complexos de forma simples e acessível. "
        "Responda de forma clara e objetiva, utilizando linguagem simples. "
        "Sempre que possível, forneça exemplos práticos. "
        "Caso não saiba a resposta, informe que não tem certeza e sugira que o usuário consulte um especialista ou fonte confiável.\n"
    )

    messages_with_context = [{"role": "system", "content": system_prompt}, *messages]

    # Create the streaming response
    stream = client.chat.completions.create(
        model=model,
        messages=messages_with_context,
        stream=True,
        name="tcc-assistant",
        stream_options={"include_usage": True},
    )

    return stream
