#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "firecrawl-py",
#     "python-dotenv",
#     "rich",
# ]
# ///

"""
Scrape Rich library documentation from readthedocs.
Handles complete documentation with all sections and examples.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from firecrawl import Firecrawl

load_dotenv()

# Documentation sections to scrape
SECTIONS = {
    "console-api": "https://rich.readthedocs.io/en/latest/console_api.html",
    "introduction": "https://rich.readthedocs.io/en/latest/introduction.html",
    "console-markup": "https://rich.readthedocs.io/en/latest/console_markup.html",
    "tables": "https://rich.readthedocs.io/en/latest/tables.html",
    "progress": "https://rich.readthedocs.io/en/latest/progress.html",
    "live": "https://rich.readthedocs.io/en/latest/live.html",
    "markdown": "https://rich.readthedocs.io/en/latest/markdown.html",
    "syntax": "https://rich.readthedocs.io/en/latest/syntax.html",
    "panels": "https://rich.readthedocs.io/en/latest/panels.html",
    "themes": "https://rich.readthedocs.io/en/latest/themes.html",
    "jupyter": "https://rich.readthedocs.io/en/latest/jupyter.html",
    "traceback": "https://rich.readthedocs.io/en/latest/traceback.html",
    "logging": "https://rich.readthedocs.io/en/latest/logging.html",
    "text": "https://rich.readthedocs.io/en/latest/text.html",
}

OUTPUT_DIR = Path("/Users/alex/Code3b/UtilRepos/ScriptCentral/src/rich/docs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def scrape_url(firecrawl, url: str, section: str) -> dict:
    """Scrape a single URL and return the document."""
    print(f"Scraping {section}...", end=" ")
    try:
        doc = firecrawl.scrape(
            url,
            formats=["markdown"],
            timeout=60,
        )
        print("[OK]")
        return {
            "success": True,
            "url": url,
            "section": section,
            "content": doc.markdown if hasattr(doc, 'markdown') else str(doc),
            "markdown": doc.markdown if hasattr(doc, 'markdown') else str(doc),
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
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        print("[ERROR] FIRECRAWL_API_KEY not set in .env")
        return

    firecrawl = Firecrawl(api_key=api_key)
    results = []

    print(f"Starting Rich documentation scrape...")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Total sections: {len(SECTIONS)}\n")

    for section, url in SECTIONS.items():
        result = scrape_url(firecrawl, url, section)
        results.append(result)

        if result["success"]:
            filename = save_to_file(section, result["markdown"], url)
            file_size = filename.stat().st_size
            print(f"  Saved to: {filename.name} ({file_size:,} bytes)")

    # Print summary
    successful = sum(1 for r in results if r["success"])
    print(f"\n[OK] Scraping complete: {successful}/{len(SECTIONS)} sections successful")

    # Save metadata
    metadata_file = OUTPUT_DIR / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump({
            "scraped": datetime.now().isoformat(),
            "total_sections": len(SECTIONS),
            "successful": successful,
            "sections": [r["section"] for r in results if r["success"]],
        }, f, indent=2)

    print(f"Metadata saved to: {metadata_file}")

if __name__ == "__main__":
    main()
