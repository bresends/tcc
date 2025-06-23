#!/usr/bin/env python3
"""
Script to generate a system prompt with all CBMGO technical norms data using Jinja template.
Creates a comprehensive txt file with system prompt and all parsed documents.
"""

from pathlib import Path
from src.system_prompt import generate_system_prompt

def main():
    """Generate system prompt txt file."""
    
    output_file = Path("system_prompt_with_docs.txt")
    
    print("Generating system prompt with all CBMGO norms...")
    
    try:
        # Generate the complete system prompt
        system_prompt = generate_system_prompt()
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(system_prompt)
        
        print(f"\nSystem prompt successfully generated!")
        print(f"Output file: {output_file}")
        print(f"File size: {output_file.stat().st_size / (1024*1024):.2f} MB")
        
    except Exception as e:
        print(f"Error generating system prompt: {e}")

if __name__ == "__main__":
    main()