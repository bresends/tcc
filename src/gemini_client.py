"""
Gemini client using OpenAI-compatible API.
"""
import os
from typing import Iterator
from openai import OpenAI


class GeminiClient:
    """Client for Google Gemini using OpenAI-compatible interface."""

    def __init__(self, api_key: str = None):
        """
        Initialize Gemini client.

        Args:
            api_key: Gemini API key (optional, will use GEMINI_API_KEY env var if not provided)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not provided and not found in environment")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def chat_completions_create(
        self,
        model: str,
        messages: list,
        stream: bool = True,
        **kwargs
    ) -> Iterator[str]:
        """
        Create chat completion using Gemini API.

        Args:
            model: Model name (e.g., "gemini-2.0-flash-exp")
            messages: List of message dicts with 'role' and 'content'
            stream: Whether to stream the response
            **kwargs: Additional parameters (ignored for compatibility)

        Yields:
            Response content chunks if streaming, otherwise full response
        """
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=stream
        )

        if stream:
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        else:
            yield response.choices[0].message.content
