import os
import streamlit as st
from dotenv import load_dotenv
from prompt_loader import load_specific_norms
from system_prompt import generate_system_prompt_with_norms
from gemini_client import GeminiClient
from router import NormRouter

load_dotenv()

def check_env_vars():
    REQUIRED_ENV_VARS = [
        "GEMINI_API_KEY",
    ]

    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing:
        st.error(f"Missing required environment variables: {', '.join(missing)}")
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    return True

check_env_vars()

client = GeminiClient(
    api_key=os.getenv("GEMINI_API_KEY"),
)

router = NormRouter()

def get_chat_response(messages, model="gemini-2.5-flash"):
    """
    Two-stage RAG pipeline:
    1. Route query to relevant norms (using Gemini Flash-Lite)
    2. Generate response with only relevant norms (using Gemini 2.5 Flash)
    """
    # Get user's last message
    user_question = messages[-1]["content"] if messages else ""

    # Stage 1: Route to relevant norms (with Langfuse tracking via router)
    relevant_norms = router.route_query(user_question, max_norms=4)

    print(f"🧭 Routed to norms: {relevant_norms}")

    # Stage 2: Load only relevant norms and generate response
    relevant_docs = load_specific_norms(relevant_norms)
    system_prompt = generate_system_prompt_with_norms(relevant_docs)

    messages_with_context = [{"role": "system", "content": system_prompt}, *messages]

    # Create the streaming response using Gemini client with Langfuse metadata
    stream = client.chat_completions_create(
        model=model,
        messages=messages_with_context,
        stream=True,
        name="answer-generation",
        metadata={
            "stage": "generation",
            "query": user_question,
            "selected_norms": [n.split('_')[1] for n in relevant_norms],
            "num_norms": len(relevant_norms),
            "model": model
        }
    )

    return stream
