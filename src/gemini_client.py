"""
Gemini client using OpenAI-compatible API with Langfuse observability.
"""
import os
from typing import Iterator
from langfuse.openai import OpenAI


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
        name: str = None,
        metadata: dict = None,
        **kwargs
    ) -> Iterator[str]:
        """
        Create chat completion using Gemini API with Langfuse tracing.

        Args:
            model: Model name (e.g., "gemini-2.0-flash-exp")
            messages: List of message dicts with 'role' and 'content'
            stream: Whether to stream the response
            name: Optional name for the Langfuse trace (for grouping)
            metadata: Optional metadata dict for Langfuse tracking
            **kwargs: Additional parameters (ignored for compatibility)

        Yields:
            Response content chunks if streaming, otherwise full response
        """
        # Build request params with optional Langfuse metadata
        params = {
            "model": model,
            "messages": messages,
            "stream": stream
        }

        if name:
            params["name"] = name
        if metadata:
            params["metadata"] = metadata

        response = self.client.chat.completions.create(**params)

        if stream:
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        else:
            yield response.choices[0].message.content
