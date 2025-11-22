#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx",
#     "beautifulsoup4",
#     "html2text",
#     "markdownify",
#     "rich",
# ]
# ///

"""
Fetch Rich library documentation from readthedocs using direct HTTP.
Converts HTML to clean markdown with proper formatting.
"""

import httpx
import re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# Documentation sections to scrape
SECTIONS = {
    "console": "https://rich.readthedocs.io/en/latest/console.html",
    "introduction": "https://rich.readthedocs.io/en/latest/introduction.html",
    "text": "https://rich.readthedocs.io/en/latest/text.html",
    "tables": "https://rich.readthedocs.io/en/latest/tables.html",
    "progress": "https://rich.readthedocs.io/en/latest/progress.html",
    "live": "https://rich.readthedocs.io/en/latest/live.html",
    "markdown": "https://rich.readthedocs.io/en/latest/markdown.html",
    "syntax": "https://rich.readthedocs.io/en/latest/syntax.html",
    "panel": "https://rich.readthedocs.io/en/latest/panel.html",
    "layout": "https://rich.readthedocs.io/en/latest/layout.html",
    "tree": "https://rich.readthedocs.io/en/latest/tree.html",
    "columns": "https://rich.readthedocs.io/en/latest/columns.html",
    "logging": "https://rich.readthedocs.io/en/latest/logging.html",
    "traceback": "https://rich.readthedocs.io/en/latest/traceback.html",
}

OUTPUT_DIR = Path("/Users/alex/Code3b/UtilRepos/ScriptCentral/src/rich/docs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_main_content(html: str) -> str:
    """Extract main documentation content from HTML."""
    soup = BeautifulSoup(html, 'html.parser')

    # Remove script and style tags
    for tag in soup(['script', 'style', 'nav', 'footer']):
        tag.decompose()

    # Find main content area
    main_content = soup.find('main')
    if not main_content:
        main_content = soup.find('div', class_='document')
    if not main_content:
        main_content = soup.find('article')
    if not main_content:
        main_content = soup.find('div', role='main')

    if main_content:
        return str(main_content)
    return str(soup)

def html_to_markdown(html: str) -> str:
    """Convert HTML to markdown, cleaning up unnecessary elements."""
    content = extract_main_content(html)
    markdown = md(content)

    # Clean up markdown
    lines = markdown.split('\n')
    cleaned = []
    for line in lines:
        # Skip empty lines and navigation elements
        if not line.strip():
            cleaned.append('')
        elif 'edit on github' in line.lower():
            continue
        elif 'view page source' in line.lower():
            continue
        elif line.strip().startswith('['):
            # Keep internal markdown links but check context
            cleaned.append(line)
        else:
            cleaned.append(line)

    # Remove multiple consecutive blank lines
    result = []
    prev_blank = False
    for line in cleaned:
        if not line.strip():
            if not prev_blank:
                result.append('')
                prev_blank = True
        else:
            result.append(line)
            prev_blank = False

    return '\n'.join(result).strip()

def fetch_url(url: str, section: str) -> dict:
    """Fetch a single URL and convert to markdown."""
    print(f"Fetching {section:15} ... ", end='', flush=True)
    try:
        response = httpx.get(url, timeout=30, follow_redirects=True)
        response.raise_for_status()
        print("[OK]")
        markdown = html_to_markdown(response.text)
        return {
            "success": True,
            "url": url,
            "section": section,
            "content": markdown,
        }
    except Exception as e:
        print(f"[ERROR] {e}")
        return {
            "success": False,
            "url": url,
            "section": section,
            "error": str(e),
        }

def save_to_file(section: str, content: str, url: str):
    """Save content to markdown file with front matter."""
    filename = OUTPUT_DIR / f"rich-{section}.md"

    front_matter = f"""---
source: {url}
scraped: {datetime.now().strftime('%Y-%m-%d')}
cleaned: pending
title: Rich Library - {section.replace('-', ' ').title()}
---

"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write(content)

    return filename

def main():
    """Main scraping function."""
    print(f"Starting Rich documentation fetch...")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Total sections: {len(SECTIONS)}\n")

    results = []
    for section, url in SECTIONS.items():
        result = fetch_url(url, section)
        results.append(result)

        if result["success"]:
            filename = save_to_file(section, result["content"], url)
            file_size = filename.stat().st_size
            print(f"  Saved: {filename.name} ({file_size:,} bytes)")

    # Print summary
    successful = sum(1 for r in results if r["success"])
    print(f"\n[OK] Fetch complete: {successful}/{len(SECTIONS)} sections successful")

    # Show failed sections
    failed = [r["section"] for r in results if not r["success"]]
    if failed:
        print(f"Failed sections: {', '.join(failed)}")

if __name__ == "__main__":
    main()
