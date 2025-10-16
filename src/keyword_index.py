"""
BM25-based keyword search for CBMGO norms using full document content.
"""
import json
import re
from pathlib import Path
from typing import List, Tuple
from rank_bm25 import BM25Okapi


class KeywordIndex:
    """BM25 keyword search index for technical norms."""

    def __init__(self, docs_dir: str = "parsed_docs", metadata_path: str = "norm_metadata.json"):
        """
        Initialize keyword index with full norm documents.

        Args:
            docs_dir: Directory containing parsed markdown files
            metadata_path: Path to norm metadata JSON (for ID to filename mapping)
        """
        self.docs_dir = Path(docs_dir)

        # Load metadata for ID to filename mapping
        with open(metadata_path, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)

        # Build index
        self.documents = []  # List of (norm_id, filename, content)
        self.tokenized_docs = []  # List of tokenized documents for BM25

        self._build_index()

        # Initialize BM25
        self.bm25 = BM25Okapi(self.tokenized_docs)

    def _build_index(self):
        """Build searchable index from all markdown files."""
        for norm in self.metadata:
            norm_id = norm['id']
            filename = norm['filename']
            filepath = self.docs_dir / filename

            if not filepath.exists():
                print(f"⚠️  Warning: {filename} not found, skipping")
                continue

            # Read full markdown content
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Tokenize content
            tokens = self._tokenize(content)

            self.documents.append((norm_id, filename, content))
            self.tokenized_docs.append(tokens)

        print(f"📚 Indexed {len(self.documents)} norms for keyword search")

    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize text for BM25 indexing.

        Args:
            text: Raw text to tokenize

        Returns:
            List of tokens (lowercased words)
        """
        # Remove markdown syntax
        text = re.sub(r'#+\s+', '', text)  # Remove headers
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Remove bold
        text = re.sub(r'\*(.+?)\*', r'\1', text)  # Remove italic
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)  # Remove links
        text = re.sub(r'`(.+?)`', r'\1', text)  # Remove code
        text = re.sub(r'\|', ' ', text)  # Remove table separators

        # Lowercase and extract words (3+ chars for meaningful terms)
        # Keep Portuguese characters
        words = re.findall(r'\b[a-záàâãéêíóôõúçA-ZÁÀÂÃÉÊÍÓÔÕÚÇ]{3,}\b', text.lower())

        return words

    def search(self, query: str, top_k: int = 2) -> List[str]:
        """
        Search for most relevant norms using BM25.

        Args:
            query: User query in Portuguese
            top_k: Number of top results to return

        Returns:
            List of norm filenames (e.g., ["NT_10_2022-...md", "NT_01_2025-...md"])
        """
        # Tokenize query
        query_tokens = self._tokenize(query)

        if not query_tokens:
            return []

        # Get BM25 scores
        scores = self.bm25.get_scores(query_tokens)

        # Get top-k results
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        # Map to filenames
        results = []
        for idx in top_indices:
            norm_id, filename, _ = self.documents[idx]
            score = scores[idx]
            results.append((filename, score))
            print(f"🔍 Keyword match: {norm_id} (score: {score:.2f})")

        return [filename for filename, _ in results]


if __name__ == "__main__":
    # Test the keyword index
    index = KeywordIndex()

    test_queries = [
        "telha translúcida combustível na cobertura",
        "extintores de incêndio para loja",
        "CERCON para supermercado",
        "piscina em condomínio",
    ]

    print("\n🔍 Testing Keyword Search\n")
    for query in test_queries:
        print(f"❓ Query: {query}")
        results = index.search(query, top_k=2)
        print(f"📚 Results: {', '.join(results)}\n")
