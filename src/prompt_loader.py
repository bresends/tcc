import os
import glob

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