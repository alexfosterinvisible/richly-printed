# Highlighting Documentation

Rich automatically highlights patterns in text including numbers, strings, collections, booleans, None, file paths, URLs, and UUIDs. You can disable this feature via the `highlight=False` parameter on `print()` or `log()` methods, or globally on the Console constructor.

## Custom Highlighters

### RegexHighlighter Approach

The simplest way to create custom highlighting involves extending `RegexHighlighter`, which applies styles to text matching regular expressions.

Example implementation for email addresses:

```python
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.theme import Theme

class EmailHighlighter(RegexHighlighter):
    """Apply style to anything that looks like an email."""
    base_style = "example."
    highlights = [r"(?P<email>[\w-]+@([\w-]+\.)+[\w-]+)"]

theme = Theme({"example.email": "bold magenta"})
console = Console(highlighter=EmailHighlighter(), theme=theme)
console.print("Send funds to money@example.org")
```

The `highlights` variable should contain regular expressions where group names are prefixed with `base_style` to create style identifiers.

### Direct Usage

Highlighters can also be used as callables without setting them on the Console:

```python
console = Console(theme=theme)
highlight_emails = EmailHighlighter()
console.print(highlight_emails("Send funds to money@example.org"))
```

### Custom Highlighter Base Class

For more complex highlighting schemes, extend the `Highlighter` base class and override the `highlight()` method, which receives a `Text` object to style.

## Built-in Highlighters

- `ISO8601Highlighter`: Highlights ISO8601 date-time strings
- `JSONHighlighter`: Highlights JSON-formatted strings
