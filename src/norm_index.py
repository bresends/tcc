"""
Extract metadata from parsed CBMGO norms for query routing.
"""
import json
import re
from pathlib import Path
from typing import List, Dict


def extract_norm_metadata(md_path: Path) -> Dict:
    """
    Extract comprehensive metadata from a norm markdown file.

    Args:
        md_path: Path to markdown file

    Returns:
        Dict with norm metadata (id, title, summary, keywords, content_hints)
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract norm ID from filename (e.g., NT_01_2025-...)
    filename = md_path.stem
    norm_id_match = re.match(r'(NT_\d+)', filename)
    norm_id = norm_id_match.group(1) if norm_id_match else filename

    # Extract title (first ##  heading)
    title_match = re.search(r'##\s*NORMA\s+TÉCNICA\s+(.+?)(?:\n|$)', content, re.IGNORECASE)
    if not title_match:
        title_match = re.search(r'##\s+(.+?)(?:\n|$)', content)
    title = title_match.group(1).strip() if title_match else ""

    # Extract main topic (second ## heading or from filename)
    topic_match = re.search(r'##\s+(?!NORMA|SUMÁRIO)(.+?)(?:\n|$)', content, re.IGNORECASE)
    topic = topic_match.group(1).strip() if topic_match else ""

    # Extract ALL section headers (## and ###)
    all_sections = []
    section_matches = re.finditer(r'^#{2,3}\s+(.+?)$', content, re.MULTILINE)
    for match in section_matches:
        section_title = match.group(1).strip()
        # Skip generic headers
        if section_title.upper() not in ['NORMA TÉCNICA', 'SUMÁRIO', 'ANEXOS', 'ANEXO']:
            all_sections.append(section_title)

    # Extract summary items (bullet points after SUMÁRIO)
    summary_section = re.search(r'##\s*SUMÁRIO.*?\n((?:[-*]\s+.+?\n)+)', content, re.DOTALL | re.IGNORECASE)
    summary_items = []
    if summary_section:
        summary_text = summary_section.group(1)
        summary_items = [
            re.sub(r'^\s*[-*]\s+', '', line).strip()
            for line in summary_text.split('\n')
            if line.strip() and line.strip().startswith(('-', '*'))
        ]

    # Extract numbered list items (indicativo de conteúdo detalhado)
    numbered_items = re.findall(r'^\d+(?:\.\d+)*\s+([A-ZÁÀÂÃÉÊÍÓÔÕÚÇ].{10,80})(?:\n|$)', content, re.MULTILINE)

    # Extract table hints (look for common table patterns)
    table_hints = []
    if re.search(r'\|.*\|.*\|', content):  # Markdown tables
        table_hints.append("Contém tabelas")
    if re.search(r'(?i)tabela\s+\d+', content):
        table_matches = re.findall(r'(?i)tabela\s+\d+\s*[-–—:]\s*(.{0,60})', content)
        table_hints.extend(table_matches[:5])

    # Extract key terms related to requirements
    requirement_terms = []
    patterns = [
        r'(?i)(área\s+(?:construída|total|mínima|máxima))\s*[:\-]?\s*(\d+[.,]?\d*\s*m[²2])',
        r'(?i)(altura)\s*[:\-]?\s*(\d+[.,]?\d*\s*m)',
        r'(?i)(ocupação|divisão|grupo|subgrupo)\s*[:\-]?\s*([A-Z]\-?\d*)',
        r'(?i)(CERCON|CVCB|CLCB|licenciamento|certificado)',
        r'(?i)(obrigatório|exigível|deve|necessário)\s+(?:para|em|quando)',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, content)
        requirement_terms.extend([' '.join(m) if isinstance(m, tuple) else m for m in matches[:3]])

    # Extract first 500 chars after "Objetivo" section for context
    objective_match = re.search(r'##?\s*\d+\s+Objetivo\s*\n(.{0,500})', content, re.IGNORECASE | re.DOTALL)
    objective_text = objective_match.group(1).strip() if objective_match else ""

    # Generate keywords from all extracted content
    keywords = set()
    text_sources = [title, topic, objective_text] + summary_items[:10] + all_sections[:15] + numbered_items[:10]
    for text in text_sources:
        if text:
            # Extract meaningful words (3+ chars)
            words = re.findall(r'\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇa-záàâãéêíóôõúç]{3,}\b', str(text))
            keywords.update(w.lower() for w in words)

    # Remove very common words
    common_words = {'objetivo', 'aplicação', 'referências', 'definições', 'procedimentos',
                    'normativas', 'bibliográficas', 'norma', 'técnica', 'contra', 'incêndio',
                    'segurança', 'pânico', 'deve', 'quando', 'para', 'esta', 'conforme'}
    keywords = keywords - common_words

    return {
        "id": norm_id,
        "filename": md_path.name,
        "title": title,
        "topic": topic,
        "summary": summary_items[:15],  # More summary items
        "sections": all_sections[:20],  # Top 20 section headers
        "tables": table_hints[:5],  # Table descriptions
        "requirements": requirement_terms[:10],  # Key requirements
        "objective": objective_text[:300],  # First 300 chars of objective
        "keywords": sorted(list(keywords))[:30]  # Top 30 keywords
    }


def build_norm_index(docs_dir: str = "parsed_docs") -> List[Dict]:
    """
    Build index of all norms in the parsed_docs directory.

    Args:
        docs_dir: Directory containing parsed markdown files

    Returns:
        List of norm metadata dicts
    """
    docs_path = Path(docs_dir)

    if not docs_path.exists():
        raise FileNotFoundError(f"Directory not found: {docs_dir}")

    norms = []
    for md_file in sorted(docs_path.glob("*.md")):
        try:
            metadata = extract_norm_metadata(md_file)
            norms.append(metadata)
            print(f"✓ Indexed {metadata['id']}: {metadata['topic']}")
        except Exception as e:
            print(f"✗ Failed to index {md_file.name}: {e}")

    return norms


def save_index(norms: List[Dict], output_path: str = "norm_metadata.json"):
    """Save norm index to JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(norms, f, ensure_ascii=False, indent=2)
    print(f"\n📁 Saved index with {len(norms)} norms to {output_path}")


def load_index(index_path: str = "norm_metadata.json") -> List[Dict]:
    """Load norm index from JSON file."""
    with open(index_path, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == "__main__":
    print("🔍 Building norm index...\n")
    norms = build_norm_index()
    save_index(norms)

    print("\n📊 Index statistics:")
    print(f"   Total norms: {len(norms)}")
    print(f"   Avg keywords per norm: {sum(len(n['keywords']) for n in norms) / len(norms):.1f}")
    print(f"   Avg summary items: {sum(len(n['summary']) for n in norms) / len(norms):.1f}")
