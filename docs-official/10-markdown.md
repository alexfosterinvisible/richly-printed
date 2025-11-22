# Markdown Documentation Content

Rich provides functionality to render Markdown directly to the console. To use this feature, you instantiate a `Markdown` object and pass it to the console's print method.

## Basic Usage

Here's a practical example demonstrating Markdown rendering:

```python
MARKDOWN = """
# This is an h1

Rich can do a pretty *decent* job of rendering markdown.

1. This is a list item
2. This is another list item
"""
from rich.console import Console
from rich.markdown import Markdown

console = Console()
md = Markdown(MARKDOWN)
console.print(md)
```

A key feature is that "code blocks are rendered with full syntax highlighting."

## Command Line Usage

You can also leverage Markdown rendering from the terminal directly:

```bash
python -m rich.markdown README.md
```

To view all available command-line options, run:

```bash
python -m rich.markdown -h
```

This capability makes it straightforward to incorporate formatted documentation and styled content into command-line applications without additional formatting tools.
