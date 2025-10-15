import json
import os
from typing import Any, Dict, Iterator

import requests
try:
    from .auth_client import get_access_token
except ImportError:
    from auth_client import get_access_token


class OllamaClient:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key  # Fallback static token
        
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with current access token"""
        try:
            # Try to get OAuth2 token first
            token = get_access_token()
        except Exception:
            # Fallback to static API key if OAuth fails
            if not self.api_key:
                raise ValueError("No OAuth2 credentials configured and no fallback API key provided")
            token = self.api_key
        
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def chat_completions_create(
        self, model: str, messages: list, stream: bool = True, **kwargs
    ) -> Iterator[str]:
        """
        Create chat completion using Ollama format
        """
        url = f"{self.base_url}/chat"

        data = {
            "model": model,
            "messages": messages,
            "stream": stream,
            "format": "text",
            "keep_alive": "5m",
            "tools": [],
            "options": {
                "seed": 0,
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "num_predict": 1000,
                "repeat_penalty": 1.1,
                "num_ctx": 4096,
            },
        }

        headers = self._get_headers()
        response = requests.post(url, headers=headers, json=data, stream=stream)
        response.raise_for_status()

        if stream:
            for line in response.iter_lines():
                if line:
                    try:
                        json_line = json.loads(line.decode("utf-8"))
                        if "message" in json_line and "content" in json_line["message"]:
                            yield json_line["message"]["content"]
                    except json.JSONDecodeError:
                        # Se não for JSON, pode ser texto simples
                        yield line.decode("utf-8")
        else:
            # A API está retornando texto simples, não JSON
            if response.headers.get("content-type", "").startswith("text/plain"):
                yield response.text
            else:
                try:
                    result = response.json()
                    if "message" in result and "content" in result["message"]:
                        yield result["message"]["content"]
                except:
                    yield response.text

