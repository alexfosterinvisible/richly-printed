# Layout Documentation - Rich 14.1.0

## Overview
The Layout class enables division of screen space into independent sections, useful for creating full-screen terminal applications, particularly when paired with Live Display.

## Creating Layouts

Initialize a basic layout with:
```python
from rich.layout import Layout
layout = Layout()
print(layout)
```

### Splitting Layouts
Divide layouts vertically using `split_column()`:
```python
layout.split_column(
    Layout(name="upper"),
    Layout(name="lower")
)
```

Split horizontally with `split_row()`:
```python
layout["lower"].split_row(
    Layout(name="left"),
    Layout(name="right"),
)
```

## Setting Content

Add Rich renderables as layout content:
```python
from rich.panel import Panel
layout["right"].split(
    Layout(Panel("Hello")),
    Layout(Panel("World!"))
)
```

Update existing layout content via the `update()` method to set or replace renderables.

## Sizing Options

**Fixed Size:** Set exact dimensions regardless of terminal size:
```python
layout["upper"].size = 10
```

**Ratio:** Create flexible layouts using proportional spacing. Default ratio is 1; higher ratios occupy more space:
```python
layout["upper"].ratio = 2
```

Set minimum dimensions to prevent layouts from shrinking excessively:
```python
layout["lower"].minimum_size = 10
```

## Visibility Control

Toggle layout visibility:
```python
layout["upper"].visible = False
```

Invisible layouts don't render, allowing other sections to expand and fill available space.

## Debugging
Visualize layout structure using the tree attribute:
```python
print(layout.tree)
```
