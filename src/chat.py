import os
import streamlit as st
from dotenv import load_dotenv
from prompt_loader import load_parsed_docs_prompt
from system_prompt import generate_system_prompt
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
    system_prompt = generate_system_prompt()

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
