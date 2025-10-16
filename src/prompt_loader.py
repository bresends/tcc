import os
import glob
from typing import List

def load_parsed_docs_prompt(directory: str = "parsed_docs") -> str:
    """
    Loads all .md files in `directory`, merging their filenames and contents
    into a single string, with each file preceded by a header "### filename".
    """
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")
    parts = []
    pattern = os.path.join(directory, "*.md")
    for path in sorted(glob.glob(pattern)):
        name = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            content = f.read()
        parts.append(f"### {name}\n{content}")
    return "\n\n".join(parts)


def load_specific_norms(filenames: List[str], directory: str = "parsed_docs") -> str:
    """
    Loads specific .md files by filename from `directory`.

    Args:
        filenames: List of markdown filenames to load (e.g., ["NT_01_2025-...md"])
        directory: Directory containing the markdown files

    Returns:
        Concatenated content of specified files with headers
    """
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    parts = []
    for filename in filenames:
        path = os.path.join(directory, filename)
        if not os.path.exists(path):
            print(f"Warning: Norm file not found: {filename}")
            continue

        with open(path, encoding="utf-8") as f:
            content = f.read()
        parts.append(f"### {filename}\n{content}")

    if not parts:
        raise ValueError(f"None of the specified norms were found: {filenames}")

    return "\n\n".join(parts)