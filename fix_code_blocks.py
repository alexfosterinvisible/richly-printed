#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "rich",
# ]
# ///

"""
Fix unmarked code blocks by adding language identifiers.
Scans all code blocks and adds appropriate language tags.
"""

import re
from pathlib import Path

DOCS_DIR = Path("/Users/alex/Code3b/UtilRepos/ScriptCentral/src/rich/docs")

def detect_language(code_block: str) -> str:
    """Detect programming language from code content."""
    code = code_block.strip()

    # Empty or very short blocks default to python
    if not code or len(code) < 3:
        return 'python'

    # Python indicators
    python_keywords = ['from ', 'import ', 'def ', 'class ', 'console.', '>>>', 'print(',
                       'for ', 'if ', 'try:', 'except', 'with ', '@', 'lambda', 'async ',
                       'await ', 'self.', 'return ', 'range(', '__', 'json.loads']
    if any(keyword in code for keyword in python_keywords):
        return 'python'

    # Shell/Bash indicators
    bash_indicators = ['$', '#!/bin/bash', 'pip install', 'python ', 'npm ', 'git ',
                       'python -m', 'sh', 'apt-', 'brew ', 'chmod ', 'cd ', 'ls ']
    if any(indicator in code for indicator in bash_indicators):
        return 'bash'

    # JSON indicators (starts with { or [)
    if (code.startswith('{') or code.startswith('[')) and ':' in code:
        return 'json'

    # YAML indicators
    if ': ' in code and '\n' in code and not code.startswith('{'):
        return 'yaml'

    # Shell/command output indicators
    if code.startswith('>>>') or code.startswith('...'):
        return 'python'

    # Text output (contains only printable text, no braces/brackets)
    if not any(c in code for c in ['[', '{', '(', '<<']):
        return 'text'

    return 'python'

def fix_file(filepath: Path) -> int:
    """Fix code blocks in a file. Returns number of blocks fixed."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    fixed = 0

    # Find all code blocks without language identifiers
    # Pattern: ``` followed by newline, then content, then ```
    pattern = r'```\n((?:(?!```).)+?)\n```'

    def replace_block(match):
        nonlocal fixed
        code = match.group(1)
        lang = detect_language(code)
        fixed += 1
        return f'```{lang}\n{code}\n```'

    content = re.sub(pattern, replace_block, content, flags=re.DOTALL)

    # Write back if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return fixed

def main():
    """Fix all documentation files."""
    print(f"Fixing code blocks in Rich documentation...")
    print(f"Directory: {DOCS_DIR}\n")

    md_files = sorted(DOCS_DIR.glob("rich-*.md"))
    total_fixed = 0

    for filepath in md_files:
        fixed = fix_file(filepath)
        if fixed > 0:
            print(f"{filepath.name:25} - Fixed {fixed:3} code blocks")
            total_fixed += fixed

    print(f"\n[OK] Total code blocks fixed: {total_fixed}")

if __name__ == "__main__":
    main()
