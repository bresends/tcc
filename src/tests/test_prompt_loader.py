import pytest
import os
import tempfile
import shutil
from src.prompt_loader import load_parsed_docs_prompt

# Fixture to create a temporary directory for testing
@pytest.fixture
def temp_test_dir():
    """Creates a temporary directory and cleans it up after the test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

# Test case 1: Directory exists and contains multiple .md files
def test_load_parsed_docs_prompt_multiple_files(temp_test_dir):
    # Create dummy .md files in the temporary directory
    file1_path = os.path.join(temp_test_dir, "file1.md")
    file2_path = os.path.join(temp_test_dir, "file2.md")
    file3_path = os.path.join(temp_test_dir, "file3.md")

    with open(file1_path, "w", encoding="utf-8") as f:
        f.write("Content of file 1")
    with open(file2_path, "w", encoding="utf-8") as f:
        f.write("Content of file 2\nwith a second line")
    with open(file3_path, "w", encoding="utf-8") as f:
        f.write("Content of file 3")

    # Expected output (sorted by filename)
    expected_output = "### file1.md\nContent of file 1\n\n### file2.md\nContent of file 2\nwith a second line\n\n### file3.md\nContent of file 3"

    # Call the function and assert the output
    result = load_parsed_docs_prompt(temp_test_dir)
    assert result == expected_output

# Test case 2: Directory exists but is empty (no .md files)
def test_load_parsed_docs_prompt_empty_directory(temp_test_dir):
    # The temporary directory is already empty
    result = load_parsed_docs_prompt(temp_test_dir)
    assert result == ""

# Test case 3: Directory does not exist
def test_load_parsed_docs_prompt_directory_not_found():
    non_existent_dir = "non_existent_directory_12345"
    with pytest.raises(FileNotFoundError) as excinfo:
        load_parsed_docs_prompt(non_existent_dir)
    assert f"Directory not found: {non_existent_dir}" in str(excinfo.value)

# Test case 4: Directory contains non-.md files (should be ignored)
def test_load_parsed_docs_prompt_ignore_non_md_files(temp_test_dir):
    # Create a .md file and a .txt file
    md_file_path = os.path.join(temp_test_dir, "important.md")
    txt_file_path = os.path.join(temp_test_dir, "ignore.txt")

    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write("This content should be included")
    with open(txt_file_path, "w", encoding="utf-8") as f:
        f.write("This content should be ignored")

    expected_output = "### important.md\nThis content should be included"

    result = load_parsed_docs_prompt(temp_test_dir)
    assert result == expected_output

# Test case 5: Files contain special characters and empty lines
def test_load_parsed_docs_prompt_special_characters_and_empty_lines(temp_test_dir):
    file_path = os.path.join(temp_test_dir, "special_content.md")

    content = "Line 1\n\nLine 3 with symbols !@#$%^&*()\nLine 4"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    expected_output = f"### special_content.md\n{content}"

    result = load_parsed_docs_prompt(temp_test_dir)
    assert result == expected_output