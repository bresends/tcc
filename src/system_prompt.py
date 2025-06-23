"""
System prompt generator using Jinja templates for CBMGO norms assistant.
"""

from pathlib import Path
from jinja2 import Template
from prompt_loader import load_parsed_docs_prompt

def load_system_prompt_template():
    """Load the system prompt Jinja template."""
    template_file = Path(__file__).parent / "templates" / "system_prompt.j2"
    
    if not template_file.exists():
        raise FileNotFoundError(f"Template file not found: {template_file}")
    
    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    return Template(template_content)

def generate_system_prompt():
    """Generate the complete system prompt with all norms data."""
    template = load_system_prompt_template()
    all_norms = load_parsed_docs_prompt()
    
    return template.render(all_norms=all_norms)