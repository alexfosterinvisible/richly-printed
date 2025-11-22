---
source: https://rich.readthedocs.io/en/latest/tables.html
scraped: 2025-11-19
cleaned: 2025-11-19
title: Rich Library - Tables
---

Tables
=========================================

Rich’s [`Table`](https://rich.readthedocs.io/en/latest/reference/table.html#rich.table.Table) class offers a variety of ways to render tabular data to the terminal.

To render a table, construct a [`Table`](https://rich.readthedocs.io/en/latest/reference/table.html#rich.table.Table) object, add columns with [`add_column()`](https://rich.readthedocs.io/en/latest/reference/table.html#rich.table.Table.add_column), and rows with [`add_row()`](https://rich.readthedocs.io/en/latest/reference/table.html#rich.table.Table.add_row) – then print it to the console.

Here’s an example:

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
```text

This produces the following output:

```bash
                           Star Wars Movies                           
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃     Released ┃ Title                             ┃     Box Office ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ Dec 20, 2019 │ Star Wars: The Rise of Skywalker  │   $952,110,690 │
│ May 25, 2018 │ Solo: A Star Wars Story           │   $393,151,347 │
│ Dec 15, 2017 │ Star Wars Ep. V111: The Last Jedi │ $1,332,539,889 │
│ Dec 16, 2016 │ Rogue One: A Star Wars Story      │ $1,332,439,889 │
└──────────────┴───────────────────────────────────┴────────────────┘
```python

Rich will calculate the optimal column sizes to fit your content, and will wrap text to fit if the terminal is not wide enough to fit the contents.

Note

You are not limited to adding text in the `add_row` method. You can add anything that Rich knows how to render (including another table).

Table Options
-------------------------------------------------------

There are a number of keyword arguments on the Table constructor you can use to define how a table should look.

* `title` Sets the title of the table (text shown above the table).
* `caption` Sets the table caption (text shown below the table).
* `width` Sets the desired width of the table (disables automatic width calculation).
* `min_width` Sets a minimum width for the table.
* `box` Sets one of the [Box](appendix/box.html#appendix-box) styles for the table grid, or `None` for no grid.
* `safe_box` Set to `True` to force the table to generate ASCII characters rather than unicode.
* `padding` An integer, or tuple of 1, 2, or 4 values to set the padding on cells (see [Padding](padding.html#padding)).
* `collapse_padding` If True the padding of neighboring cells will be merged.
* `pad_edge` Set to False to remove padding around the edge of the table.
* `expand` Set to True to expand the table to the full available size.
* `show_header` Set to True to show a header, False to disable it.
* `show_footer` Set to True to show a footer, False to disable it.
* `show_edge` Set to False to disable the edge line around the table.
* `show_lines` Set to True to show lines between rows as well as header / footer.
* `leading` Additional space between rows.
* `style` A Style to apply to the entire table, e.g. “on blue”
* `row_styles` Set to a list of styles to style alternating rows. e.g. `["dim", ""]` to create *zebra stripes*
* `header_style` Set the default style for the header.
* `footer_style` Set the default style for the footer.
* `border_style` Set a style for border characters.
* `title_style` Set a style for the title.
* `caption_style` Set a style for the caption.
* `title_justify` Set the title justify method (“left”, “right”, “center”, or “full”)
* `caption_justify` Set the caption justify method (“left”, “right”, “center”, or “full”)
* `highlight` Set to True to enable automatic highlighting of cell contents.

Border Styles
-------------------------------------------------------

You can set the border style by importing one of the preset `Box` objects and setting the `box` argument in the table constructor. Here’s an example that modifies the look of the Star Wars table:

```python
from rich import box
table = Table(title="Star Wars Movies", box=box.MINIMAL_DOUBLE_HEAD)
```python

See [Box](appendix/box.html#appendix-box) for other box styles.

You can also set `box=None` to remove borders entirely.

The [`Table`](https://rich.readthedocs.io/en/latest/reference/table.html#rich.table.Table) class offers a number of configuration options to set the look and feel of the table, including how borders are rendered and the style and alignment of the columns.

Lines
---------------------------------------

By default, Tables will show a line under the header only. If you want to show lines between all rows add `show_lines=True` to the constructor.

You can also force a line on the next row by setting `end_section=True` on the call to [`add_row()`](https://rich.readthedocs.io/en/latest/reference/table.html#rich.table.Table.add_row), or by calling the [`add_section()`](https://rich.readthedocs.io/en/latest/reference/table.html#rich.table.Table.add_section) to add a line between the current and subsequent rows.

Empty Tables
-----------------------------------------------------

Printing a table with no columns results in a blank line. If you are building a table dynamically and the data source has no columns, you might want to print something different. Here’s how you might do that:

```python
if table.columns:
    print(table)
else:
    print("[i]No data...[/i]")
```python

Adding Columns
---------------------------------------------------------

You may also add columns by specifying them in the positional arguments of the [`Table`](https://rich.readthedocs.io/en/latest/reference/table.html#rich.table.Table) constructor. For example, we could construct a table with three columns like this:

```python
table = Table("Released", "Title", "Box Office", title="Star Wars Movies")
```python

This allows you to specify the text of the column only. If you want to set other attributes, such as width and style, you can add a [`Column`](https://rich.readthedocs.io/en/latest/reference/table.html#rich.table.Column) class. Here’s an example:

```python
from rich.table import Column, Table
table = Table(
    "Released",
    "Title",
    Column(header="Box Office", justify="right"),
    title="Star Wars Movies"
)
```python

Column Options
---------------------------------------------------------

There are a number of options you can set on a column to modify how it will look.

* `header_style` Sets the style of the header, e.g. “bold magenta”.
* `footer_style` Sets the style of the footer.
* `style` Sets a style that applies to the column. You could use this to highlight a column by setting the background with “on green” for example.
* `justify` Sets the text justify to one of “left”, “center”, “right”, or “full”.
* `vertical` Sets the vertical alignment of the cells in a column, to one of “top”, “middle”, or “bottom”.
* `width` Explicitly set the width of a row to a given number of characters (disables automatic calculation).
* `min_width` When set to an integer will prevent the column from shrinking below this amount.
* `max_width` When set to an integer will prevent the column from growing beyond this amount.
* `ratio` Defines a ratio to set the column width. For instance, if there are 3 columns with a total of 6 ratio, and `ratio=2` then the column will be a third of the available size.
* `no_wrap` Set to True to prevent this column from wrapping.
* `highlight` Set to True to enable automatic highlighting of cell contents.

Vertical Alignment
-----------------------------------------------------------------

You can define the vertical alignment of a column by setting the `vertical` parameter of the column. You can also do this per-cell by wrapping your text or renderable with a [`Align`](https://rich.readthedocs.io/en/latest/reference/align.html#rich.align.Align) class:

```python
table.add_row(Align("Title", vertical="middle"))
```python

Grids
---------------------------------------

The Table class can also make a great layout tool. If you disable headers and borders you can use it to position content within the terminal. The alternative constructor [`grid()`](https://rich.readthedocs.io/en/latest/reference/table.html#rich.table.Table.grid) can create such a table for you.

For instance, the following code displays two pieces of text aligned to both the left and right edges of the terminal on a single line:

```python
from rich import print
from rich.table import Table

grid = Table.grid(expand=True)
grid.add_column()
grid.add_column(justify="right")
grid.add_row("Raising shields", "[bold magenta]COMPLETED [green]:heavy_check_mark:")

print(grid)
```