# Console Protocol Documentation

## Overview

Rich provides a protocol enabling custom objects to render with rich formatting capabilities. This allows printing objects with colors, styles, and formatting beyond standard `__repr__` output.

## Console Customization

The simplest approach involves implementing a `__rich__` method that returns a renderable object. According to the documentation, "This method accepts no arguments, and should return an object that Rich knows how to render, such as a Text or Table."

**Example:**
```python
class MyObject:
    def __rich__(self) -> str:
        return "[bold cyan]MyObject()"
```

When printed, this renders with the specified styling.

## Console Render

For more sophisticated rendering, implement `__rich_console__`. The documentation states: "The `__rich_console__` method should accept a Console and ConsoleOptions instance. It should return an iterable of other renderable objects."

**Example:**
```python
from dataclasses import dataclass
from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table

@dataclass
class Student:
    id: int
    name: str
    age: int
    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield f"[b]Student:[/b] #{self.id}"
        my_table = Table("Attribute", "Value")
        my_table.add_row("name", self.name)
        my_table.add_row("age", str(self.age))
        yield my_table
```

## Low-Level Rendering

For granular control, yield `Segment` objects containing text and optional styling:

```python
class MyObject:
    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield Segment("My", Style(color="magenta"))
        yield Segment("Object", Style(color="green"))
        yield Segment("()", Style(color="cyan"))
```

## Measuring Renderables

Implement `__rich_measure__` to specify rendering dimensions. This method returns a `Measurement` object with minimum and maximum character requirements:

```python
class ChessBoard:
    def __rich_measure__(self, console: Console, options: ConsoleOptions) -> Measurement:
        return Measurement(8, options.max_width)
```
