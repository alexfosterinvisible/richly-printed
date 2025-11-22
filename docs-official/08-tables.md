# Rich Tables Documentation

## Overview

Rich's `Table` class renders tabular data to the terminal. Create a table by constructing a `Table` object, adding columns with `add_column()`, and rows with `add_row()`, then print to console.

## Basic Example

```python
from rich.console import Console
from rich.table import Table

table = Table(title="Star Wars Movies")

table.add_column("Released", justify="right", style="cyan", no_wrap=True)
table.add_column("Title", style="magenta")
table.add_column("Box Office", justify="right", style="green")

table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

console = Console()
console.print(table)
```

Rich automatically calculates optimal column widths and wraps text to fit terminal width. You can add any Rich-renderable content to cells, including nested tables.

## Table Constructor Options

Key parameters include:
- `title` / `caption` - Text above/below table
- `width` / `min_width` - Control table dimensions
- `box` - Border style (or `None` for no borders)
- `safe_box` - Force ASCII characters
- `padding` - Cell padding configuration
- `pad_edge` - Toggle edge padding
- `expand` - Stretch to available width
- `show_header` / `show_footer` / `show_edge` - Toggle display elements
- `show_lines` - Display lines between all rows
- `row_styles` - Apply styles to alternating rows
- `header_style` / `footer_style` / `border_style` - Styling options
- `highlight` - Enable automatic cell content highlighting

## Border Styles

Import preset `Box` objects to customize borders:

```python
from rich import box
table = Table(title="Star Wars Movies", box=box.MINIMAL_DOUBLE_HEAD)
```

Set `box=None` to remove borders entirely.

## Lines Between Rows

By default, lines appear only under headers. Use `show_lines=True` for lines between all rows, or `end_section=True` on `add_row()` calls to force lines on specific rows. Alternatively, call `add_section()` to insert dividers.

## Handling Empty Tables

Check for columns before printing to avoid blank output:

```python
if table.columns:
    print(table)
else:
    print("[i]No data...[/i]")
```

## Column Declaration

Specify columns as positional arguments:

```python
table = Table("Released", "Title", "Box Office", title="Star Wars Movies")
```

For advanced configuration, use the `Column` class:

```python
from rich.table import Column, Table
table = Table(
    "Released",
    "Title",
    Column(header="Box Office", justify="right"),
    title="Star Wars Movies"
)
```

## Column Options

Configure individual columns with:
- `header_style` / `footer_style` - Text styling
- `style` - Column-wide styling
- `justify` - Horizontal alignment ("left", "center", "right", "full")
- `vertical` - Vertical alignment ("top", "middle", "bottom")
- `width` / `min_width` / `max_width` - Dimension controls
- `ratio` - Proportional sizing relative to other columns
- `no_wrap` - Prevent text wrapping
- `highlight` - Enable content highlighting

## Vertical Alignment

Set column-level vertical alignment via the `vertical` parameter, or wrap individual cells using the `Align` class:

```python
table.add_row(Align("Title", vertical="middle"))
```

## Grids

Use the alternative constructor `Table.grid()` to create layout tools without headers or borders:

```python
from rich import print
from rich.table import Table

grid = Table.grid(expand=True)
grid.add_column()
grid.add_column(justify="right")
grid.add_row("Raising shields", "[bold magenta]COMPLETED [green]:heavy_check_mark:")

print(grid)
```

This enables positioning content across terminal width without visible table structure.
