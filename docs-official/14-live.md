# Live Display Documentation

The Live Display feature in Rich enables animated terminal displays for progress bars, status indicators, and custom applications. Here's the core documentation:

## Basic Usage

Create a `Live` object with a renderable and use it as a context manager. The display persists throughout the context duration and updates via the renderable:

```python
import time
from rich.live import Live
from rich.table import Table

table = Table()
table.add_column("Row ID")
table.add_column("Description")
table.add_column("Level")

with Live(table, refresh_per_second=4):
    for row in range(12):
        time.sleep(0.4)
        table.add_row(f"{row}", f"description {row}", "[red]ERROR")
```

## Updating Renderables

Call the `update()` method to change the renderable dynamically, useful for highly dynamic content that shouldn't update a single renderable internally.

## Key Configuration Options

**Alternate Screen**: Set `screen=True` to display full-screen with command prompt restoration on exit.

**Transient Display**: Set `transient=True` to make the display disappear upon exit instead of persisting.

**Auto Refresh**: Control refresh rate with `refresh_per_second` (default: 4). Disable auto-refresh with `auto_refresh=False` and manually call `refresh()` or `update(refresh=True)`.

**Vertical Overflow**: The `vertical_overflow` parameter handles content exceeding terminal height:
- "crop": Display up to terminal height
- "ellipsis": Similar to crop with "…" on last line (default)
- "visible": Show entire renderable without clearing

## Console Integration

Access the internal console via `live.console` to print output above the live display. Pass your own Console object to the constructor for custom console usage.

## Output Redirection

Rich automatically redirects `stdout` and `stderr` to prevent visual disruption. Disable this with `redirect_stdout=False` or `redirect_stderr=False`.

## Nesting

Live instances can nest within existing Live contexts (version 14.0.0+), with inner content displaying below the outer Live.
