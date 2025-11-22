#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

"""Update front matter cleaned dates in all documentation files."""

from pathlib import Path
import re
from datetime import datetime

DOCS_DIR = Path("/Users/alex/Code3b/UtilRepos/ScriptCentral/src/rich/docs")
TODAY = datetime.now().strftime('%Y-%m-%d')

def update_file(filepath: Path) -> bool:
    """Update front matter in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace cleaned date
    updated = re.sub(
        r'cleaned: pending',
        f'cleaned: {TODAY}',
        content
    )

    if updated != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)
        return True
    return False

md_files = sorted(DOCS_DIR.glob("rich-*.md"))
count = sum(1 for f in md_files if update_file(f))
print(f"[OK] Updated {count} files with cleaned date: {TODAY}")
