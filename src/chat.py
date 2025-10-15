import os
import streamlit as st
from dotenv import load_dotenv
from prompt_loader import load_parsed_docs_prompt
from system_prompt import generate_system_prompt
from ollama_client import OllamaClient

load_dotenv()

def check_env_vars():
    REQUIRED_ENV_VARS = [
    "LLM_BASE_URL",
    "NORMA_OAUTH_CLIENT_ID",
    "NORMA_OAUTH_CLIENT_SECRET",
    ]

    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing:
        st.error(f"Missing required environment variables: {', '.join(missing)}")
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    return True

check_env_vars()

client = OllamaClient(
    base_url=os.getenv("LLM_BASE_URL"),
)

def get_chat_response(messages, model="llama3.3:70b"):
    system_prompt = generate_system_prompt()

    messages_with_context = [{"role": "system", "content": system_prompt}, *messages]

    # Create the streaming response using Ollama client
    stream = client.chat_completions_create(
        model=model,
        messages=messages_with_context,
        stream=True,
    )

    return stream
