#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "rich",
# ]
# ///

"""
Verify Rich documentation quality:
- Check front matter format
- Verify code block consistency
- Check for broken references
- Summarize documentation stats
"""

from pathlib import Path
import re
from datetime import datetime

DOCS_DIR = Path("/Users/alex/Code3b/UtilRepos/ScriptCentral/src/rich/docs")

def check_file(filepath: Path) -> dict:
    """Check a single documentation file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    stats = {
        'file': filepath.name,
        'size': len(content),
        'has_front_matter': False,
        'front_matter_valid': False,
        'code_blocks': 0,
        'code_blocks_with_lang': 0,
        'images': 0,
        'links': len(re.findall(r'\[.+?\]\(', content)),
        'issues': [],
    }

    # Check front matter
    if content.startswith('---'):
        stats['has_front_matter'] = True
        match = re.match(r'^---\n(.+?)\n---', content, re.DOTALL)
        if match:
            fm = match.group(1)
            stats['front_matter_valid'] = all(
                key in fm for key in ['source:', 'scraped:', 'cleaned:', 'title:']
            )
            if not stats['front_matter_valid']:
                stats['issues'].append('Invalid front matter fields')

    # Count code blocks
    code_blocks = re.findall(r'```(\w*)\n', content)
    stats['code_blocks'] = len(code_blocks)
    stats['code_blocks_with_lang'] = sum(1 for b in code_blocks if b)

    # Check for common issues
    if '](reference/' in content:
        stats['issues'].append('Contains unresolved reference links')

    if '[](#' in content and 'Link to this heading' in content:
        stats['issues'].append('Contains unreplaced anchor links')

    return stats

def main():
    """Main verification function."""
    print(f"Verifying Rich documentation...")
    print(f"Directory: {DOCS_DIR}\n")

    md_files = sorted(DOCS_DIR.glob("rich-*.md"))
    results = [check_file(f) for f in md_files]

    # Print table
    print(f"{'File':<25} {'Size':>10} {'Blocks':>8} {'With Lang':>12} {'Status':<30}")
    print("-" * 85)

    total_size = 0
    total_blocks = 0
    total_with_lang = 0

    for r in results:
        status = "OK" if not r['issues'] else f"ISSUES: {', '.join(r['issues'])}"
        print(f"{r['file']:<25} {r['size']:>10,} {r['code_blocks']:>8} {r['code_blocks_with_lang']:>12} {status:<30}")
        total_size += r['size']
        total_blocks += r['code_blocks']
        total_with_lang += r['code_blocks_with_lang']

    print("-" * 85)
    print(f"{'TOTAL':<25} {total_size:>10,} {total_blocks:>8} {total_with_lang:>12}")

    # Summary statistics
    print(f"\n[OK] Summary:")
    print(f"  Total files: {len(results)}")
    print(f"  Total size: {total_size:,} bytes")
    print(f"  Total code blocks: {total_blocks}")
    print(f"  Code blocks with language: {total_with_lang} ({100*total_with_lang/total_blocks:.1f}%)" if total_blocks > 0 else "")
    print(f"  Files with front matter: {sum(1 for r in results if r['has_front_matter'])}")
    print(f"  Files with valid front matter: {sum(1 for r in results if r['front_matter_valid'])}")

    # Check for issues
    all_issues = [issue for r in results for issue in r['issues']]
    if all_issues:
        print(f"\n[WARN] Issues found:")
        for issue in set(all_issues):
            count = all_issues.count(issue)
            print(f"  - {issue} ({count} files)")
    else:
        print(f"\n[OK] No issues found!")

if __name__ == "__main__":
    main()
