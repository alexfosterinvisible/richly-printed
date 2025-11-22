# Rich Text Documentation

## Overview

Rich provides a `Text` class for marking up strings with colors and style attributes. Unlike standard Python strings, `Text` instances are mutable, with most methods modifying objects in-place rather than returning new instances.

## Styling Methods

**stylize() approach:**
Apply styles to specific character ranges using start and end offsets:

```python
from rich.console import Console
from rich.text import Text

console = Console()
text = Text("Hello, World!")
text.stylize("bold magenta", 0, 6)
console.print(text)
```

**append() approach:**
Build styled text incrementally by adding strings with associated styles:

```python
text = Text()
text.append("Hello", style="bold magenta")
text.append(" World!")
console.print(text)
```

**from_ansi() approach:**
Convert ANSI-formatted text to Text objects for further manipulation.

**assemble() approach:**
Combine multiple strings and style pairs into a single Text instance, useful for constructing complex formatted text from components.

## Advanced Styling

The library includes methods for pattern-based styling:
- `highlight_words()` — emphasizes specific words
- `highlight_regex()` — styles text matching regular expressions

## Text Attributes

Constructor parameters control display behavior:

- `justify` — "left", "center", "right", or "full" alignment
- `overflow` — "fold", "crop", or "ellipsis" handling
- `no_wrap` — prevents line wrapping
- `tab_size` — character width for tabs

Text instances integrate throughout the Rich API, enabling flexible presentation in panels, tables, and other renderables.
