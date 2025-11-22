# Pretty Printing Documentation

## Overview
Rich formats containers like lists, dicts, and sets with syntax highlighting and intelligent layout adjustments based on terminal width.

## pprint Method
The `pprint()` function provides customization options:

```python
from rich.pretty import pprint
pprint(locals())
```

**Indent Guides**: Enabled by default to show nesting levels. Disable with `indent_guides=False`.

**Expand All**: By default, Rich conserves space. Set `expand_all=True` to fully expand all data structures.

**Truncation Options**:
- `max_length`: Truncates containers exceeding a specified element count, displaying "..." and the omitted count
- `max_string`: Limits string length and appends the character count not displayed

## Pretty Renderable Class
The `Pretty` class embeds formatted data within other renderables:

```python
from rich.pretty import Pretty
from rich.panel import Panel

pretty = Pretty(locals())
panel = Panel(pretty)
print(panel)
```

## Rich Repr Protocol
Custom objects can implement `__rich_repr__()` for Rich-compatible formatting. This method yields tuples representing output elements:

- `yield value` creates a positional argument
- `yield name, value` creates a keyword argument
- `yield name, value, default` includes the argument only if the value differs from the default

### Angular Bracket Style
Set `__rich_repr__.angular = True` to use angle bracket formatting (`<ClassName ...>`), typically for objects without simple constructors.

### Automatic Rich Repr
Use the `@rich.repr.auto` decorator for classes where parameter names match attribute names:

```python
import rich.repr

@rich.repr.auto
class Bird:
    def __init__(self, name, eats=None, fly=True, extinct=False):
        self.name = name
        self.eats = list(eats) if eats else []
        self.fly = fly
        self.extinct = extinct
```

The decorator auto-generates both `__repr__()` and `__rich_repr__()` methods. Use `@rich.repr.auto(angular=True)` for angular-style output.
