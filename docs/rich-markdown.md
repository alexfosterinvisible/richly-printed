---
source: https://rich.readthedocs.io/en/latest/markdown.html
scraped: 2025-11-19
cleaned: 2025-11-19
title: Rich Library - Markdown
---

Markdown
=============================================

Rich can render Markdown to the console. To render markdown, construct a [`Markdown`](https://rich.readthedocs.io/en/latest/reference/markdown.html#rich.markdown.Markdown) object then print it to the console. Markdown is a great way of adding rich content to your command line applications. Here’s an example of use:

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
```python

Note that code blocks are rendered with full syntax highlighting!

You can also use the Markdown class from the command line. The following example displays a readme in the terminal:

```bash
python -m rich.markdown README.md
```python

Run the following to see the full list of arguments for the markdown command:

```bash
python -m rich.markdown -h
```