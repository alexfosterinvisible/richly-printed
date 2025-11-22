#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "rich",
# ]
# ///

"""
Clean Rich documentation files:
1. Add language identifiers to code blocks
2. Remove broken reference links
3. Remove "Link to this heading" anchors
4. Clean up excessive whitespace
5. Update front matter
"""

import re
from pathlib import Path
from datetime import datetime

DOCS_DIR = Path("/Users/alex/Code3b/UtilRepos/ScriptCentral/src/rich/docs")

def detect_code_language(code_block: str) -> str:
    """Detect programming language from code content."""
    code = code_block.strip()

    # Python indicators
    if any(x in code for x in ['from ', 'import ', 'def ', 'class ', 'console.', '>>>', 'print(']):
        return 'python'

    # JavaScript/TypeScript indicators
    if any(x in code for x in ['function ', 'const ', 'let ', 'var ', '=>', 'async ', 'await ']):
        return 'javascript'

    # JSON indicators
    if code.startswith('{') or code.startswith('['):
        try:
            # Try to parse as JSON
            import json
            json.loads(code)
            return 'json'
        except:
            pass

    # Shell/Bash indicators
    if any(x in code for x in ['$', '#!/', 'pip install', 'python ', 'npm ', 'git ']):
        return 'bash'

    # YAML indicators
    if ':' in code and '\n' in code:
        return 'yaml'

    # Default to python for Rich docs
    return 'python'

def clean_code_blocks(content: str) -> str:
    """Add language identifiers to code blocks without them."""
    # Pattern to match code blocks without language specifiers
    pattern = r'```\n((?:(?!```).)*?)\n```'

    def add_language(match):
        code_content = match.group(1)
        lang = detect_code_language(code_content)
        return f'```{lang}\n{code_content}\n```'

    return re.sub(pattern, add_language, content, flags=re.DOTALL)

def remove_link_anchors(content: str) -> str:
    """Remove 'Link to this heading' anchors."""
    # Remove patterns like: "[](#section-name "Link to this heading")"
    pattern = r'\s*\[.+?\]\(#[^)]+?\s+"Link to this heading"\)'
    return re.sub(pattern, '', content)

def clean_references(content: str) -> str:
    """Clean up broken reference links to keep them readable."""
    # Keep links but make them cleaner
    # Pattern: [text](reference/module.html#class.method "description")
    # Becomes: [text](reference/module.html#class.method)

    pattern = r'\]\(([^)]+?)\s+"[^"]+?"\)'
    return re.sub(pattern, r'](https://rich.readthedocs.io/en/latest/\1)', content)

def remove_excessive_whitespace(content: str) -> str:
    """Remove excessive blank lines while preserving formatting."""
    # Remove more than 2 consecutive blank lines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    return content

def update_front_matter(content: str) -> str:
    """Update cleaned status in front matter."""
    pattern = r'(---\nsource: .+?\nscrape: .+?\n)cleaned: pending'
    replacement = r'\1cleaned: ' + datetime.now().strftime('%Y-%m-%d')
    return re.sub(pattern, replacement, content, flags=re.DOTALL)

def clean_file(filepath: Path) -> tuple[int, int]:
    """Clean a single documentation file."""
    print(f"Cleaning {filepath.name:25} ... ", end='', flush=True)

    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    # Apply cleaning functions
    content = original
    content = clean_code_blocks(content)
    content = remove_link_anchors(content)
    content = clean_references(content)
    content = remove_excessive_whitespace(content)
    content = update_front_matter(content)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK]")
    return len(original), len(content)

def main():
    """Clean all documentation files."""
    print(f"Cleaning Rich documentation files...")
    print(f"Directory: {DOCS_DIR}\n")

    md_files = sorted(DOCS_DIR.glob("rich-*.md"))
    if not md_files:
        print("[ERROR] No markdown files found!")
        return

    print(f"Found {len(md_files)} files\n")

    total_before = 0
    total_after = 0

    for filepath in md_files:
        before, after = clean_file(filepath)
        total_before += before
        total_after += after

    print(f"\n[OK] Cleaning complete!")
    print(f"Total size before: {total_before:,} bytes")
    print(f"Total size after:  {total_after:,} bytes")
    print(f"Reduction: {total_before - total_after:,} bytes ({100 * (total_before - total_after) / total_before:.1f}%)")

if __name__ == "__main__":
    main()
