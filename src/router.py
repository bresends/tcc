"""
Query router for selecting relevant norms using Gemini Flash.
"""
import json
import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

try:
    from .gemini_client import GeminiClient
except ImportError:
    from gemini_client import GeminiClient

# Load .env from project root
load_dotenv(Path(__file__).parent.parent / ".env")


class NormRouter:
    """Routes user queries to relevant CBMGO norms using LLM."""

    def __init__(self, index_path: str = "norm_metadata.json", api_key: str = None):
        """
        Initialize router with norm index and Gemini client.

        Args:
            index_path: Path to norm metadata JSON
            api_key: Gemini API key (optional, uses GEMINI_API_KEY env var)
        """
        with open(index_path, 'r', encoding='utf-8') as f:
            self.norms = json.load(f)

        self.client = GeminiClient(api_key=api_key or os.getenv("GEMINI_API_KEY"))

    def _build_routing_prompt(self, user_question: str) -> str:
        """Build prompt for routing decision with enhanced metadata."""
        # Create detailed norm descriptions using enhanced metadata
        norm_list = []
        for norm in self.norms:
            desc = f"- {norm['id']}: {norm['topic']}"

            # Add sections if available
            if norm.get('sections'):
                sections = ", ".join(norm['sections'][:3])
                desc += f"\n  Seções: {sections}"

            # Add table hints
            if norm.get('tables'):
                desc += f"\n  {norm['tables'][0]}"

            # Add requirements hints
            if norm.get('requirements'):
                req = ", ".join(str(r) for r in norm['requirements'][:2])
                desc += f"\n  Requisitos: {req}"

            # Add key keywords
            if norm.get('keywords'):
                keywords = ", ".join(norm['keywords'][:5])
                desc += f"\n  Palavras-chave: {keywords}"

            norm_list.append(desc)

        norms_text = "\n".join(norm_list)

        prompt = f"""Você é um assistente especializado em normas técnicas do CBMGO.

PERGUNTA DO USUÁRIO:
{user_question}

NORMAS DISPONÍVEIS:
{norms_text}

TAREFA:
Identifique quais normas são relevantes para responder a pergunta do usuário.
Retorne APENAS os IDs das normas (ex: NT_01, NT_15) separados por vírgula.

REGRAS:
- Para perguntas sobre licenciamento, CERCON, área construída, exigências: NT_01 Anexo A
- Para perguntas sobre extintores: NT_21
- Para perguntas sobre chuveiros automáticos/sprinklers: NT_23
- Para perguntas sobre hidrantes: NT_22
- Para perguntas sobre piscinas: NT_16
- Retorne até 3 normas mais relevantes

FORMATO DE RESPOSTA:
NT_XX, NT_YY, NT_ZZ

RESPOSTA:"""

        return prompt

    def route_query(self, user_question: str, max_norms: int = 3) -> List[str]:
        """
        Route user question to relevant norms.

        Args:
            user_question: User's question in Portuguese
            max_norms: Maximum number of norms to return

        Returns:
            List of norm filenames (e.g., ["NT_01_2025-Procedimentos...md"])
        """
        routing_prompt = self._build_routing_prompt(user_question)

        # Use Gemini 2.5 Flash-Lite for routing (faster, cheaper)
        messages = [{"role": "user", "content": routing_prompt}]

        response_chunks = []
        for chunk in self.client.chat_completions_create(
            model="gemini-2.5-flash-lite",
            messages=messages,
            stream=True
        ):
            response_chunks.append(chunk)

        response = "".join(response_chunks).strip()

        # Parse response to extract norm IDs
        norm_ids = self._parse_norm_ids(response)

        # Limit to max_norms
        norm_ids = norm_ids[:max_norms]

        # Map IDs to filenames
        id_to_filename = {n['id']: n['filename'] for n in self.norms}
        filenames = [id_to_filename[nid] for nid in norm_ids if nid in id_to_filename]

        # Fallback if no valid norms found
        if not filenames:
            # Default to NT_01 (Procedimentos Administrativos)
            filenames = [n['filename'] for n in self.norms if n['id'] == 'NT_01'][:1]

        return filenames

    def _parse_norm_ids(self, response: str) -> List[str]:
        """
        Parse norm IDs from router response.

        Args:
            response: Raw response from routing model

        Returns:
            List of norm IDs (e.g., ["NT_01", "NT_15"])
        """
        import re

        # Extract all NT_XX patterns
        matches = re.findall(r'NT_\d+', response.upper())

        # Remove duplicates while preserving order
        seen = set()
        unique_ids = []
        for match in matches:
            if match not in seen:
                seen.add(match)
                unique_ids.append(match)

        return unique_ids


if __name__ == "__main__":
    # Test the router
    router = NormRouter()

    test_questions = [
        "Como fazer o licenciamento de uma edificação?",
        "Quais são os requisitos para extintores de incêndio?",
        "Preciso instalar chuveiros automáticos na minha loja?",
        "Quais são as regras para piscinas em condomínios?",
    ]

    print("🧭 Testing Query Router\n")
    for question in test_questions:
        print(f"❓ {question}")
        norms = router.route_query(question)
        print(f"📚 Routed to: {', '.join(norms)}\n")
