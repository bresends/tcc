import json
import os
from typing import Any, Dict, Iterator

import requests


class OllamaClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
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

        response = requests.post(url, headers=self.headers, json=data, stream=stream)
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

