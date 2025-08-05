#!/usr/bin/env python3
"""
Script to remove directories and specific text from files as specified in scratchpad.txt
"""

import os
import shutil
import sys
from pathlib import Path


def remove_directories():
    """Remove the first two directories specified in scratchpad.txt"""
    directories_to_remove = [
        "web/src/app/ee",
        "backend/ee"
    ]
    
    for dir_path in directories_to_remove:
        abs_path = Path(dir_path).resolve()
        if abs_path.exists():
            print(f"Removing directory: {abs_path}")
            try:
                shutil.rmtree(abs_path)
                print(f"✓ Successfully removed {abs_path}")
            except Exception as e:
                print(f"✗ Error removing {abs_path}: {e}")
        else:
            print(f"Directory not found: {abs_path}")


def remove_text_from_files():
    """Remove specific text from files as specified in scratchpad.txt"""
    
    # Define file modifications
    file_modifications = {
        ".github/workflows/pr-integration-tests.yml": [
            "pip install --retries 5 --timeout 30 -r backend/requirements/ee.txt",
            "backend/requirements/ee.txt",
        ],
        "backend/tests/integration/Dockerfile": [
            "COPY ./requirements/ee.txt /tmp/ee-requirements.txt",
            "-r /tmp/ee-requirements.txt && \\",
            "COPY ./ee /app/ee"
        ],
        "CONTRIBUTING.md": [
            "pip install -r onyx/backend/requirements/ee.txt"
        ],
        "backend/Dockerfile": [
            "COPY ./requirements/ee.txt /tmp/ee-requirements.txt",
            "-r /tmp/ee-requirements.txt && \\",
            "COPY ./ee /app/ee"
        ]
    }
    
    for file_path, texts_to_remove in file_modifications.items():
        abs_file_path = Path(file_path).resolve()
        
        if not abs_file_path.exists():
            print(f"File not found: {abs_file_path}")
            continue
            
        print(f"Processing file: {abs_file_path}")
        
        try:
            # Read the file content
            with open(abs_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Remove each specified text
            for text_to_remove in texts_to_remove:
                if text_to_remove in content:
                    content = content.replace(text_to_remove, "")
                    print(f"  ✓ Removed: {text_to_remove}")
                else:
                    print(f"  - Text not found: {text_to_remove}")
            
            # Clean up extra whitespace and empty lines
            lines = content.split('\n')
            cleaned_lines = []
            
            for line in lines:
                # Skip completely empty lines that resulted from removals
                if line.strip() or (cleaned_lines and cleaned_lines[-1].strip()):
                    cleaned_lines.append(line)
            
            # Remove trailing empty lines
            while cleaned_lines and not cleaned_lines[-1].strip():
                cleaned_lines.pop()
            
            content = '\n'.join(cleaned_lines)
            
            # Write back only if content changed
            if content != original_content:
                with open(abs_file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ Successfully updated {abs_file_path}")
            else:
                print(f"- No changes made to {abs_file_path}")
                
        except Exception as e:
            print(f"✗ Error processing {abs_file_path}: {e}")


def main():
    """Main function to execute the cleanup script"""
    print("Starting cleanup script...")
    print("=" * 50)
    
    # Change to the script's directory (should be project root)
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    print(f"Working directory: {Path.cwd()}")
    print()
    
    # Remove directories
    print("1. Removing directories...")
    remove_directories()
    print()
    
    # Remove text from files
    print("2. Removing text from files...")
    remove_text_from_files()
    print()
    
    print("Cleanup script completed!")


if __name__ == "__main__":
    main()