# Progress Display Documentation Summary

## Overview
Rich provides utilities for displaying continuously updated progress information for long-running tasks. The library supports multiple concurrent tasks with customizable progress bars and information displays.

## Basic Usage
The simplest approach uses the `track()` function:

```python
from rich.progress import track
import time

for i in track(range(20), description="Processing..."):
    time.sleep(1)
```

This automatically yields values while updating progress visuals.

## Advanced Features

**Context Manager Pattern** (Recommended):
```python
with Progress() as progress:
    task1 = progress.add_task("[red]Downloading...", total=1000)
    while not progress.finished:
        progress.update(task1, advance=0.5)
```

**Key Methods:**
- `add_task()` - Create a tracked task, returns task ID
- `update()` - Modify task progress using `completed` or `advance` parameters
- `start()` / `stop()` - Manual lifecycle control

## Customization Options

**Column Types Available:**
- BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
- FileSizeColumn, DownloadColumn, TransferSpeedColumn
- SpinnerColumn, RenderableColumn

**Configuration Parameters:**
- `transient=True` - Remove progress display after completion
- `expand=True` - Stretch to terminal width
- `refresh_per_second` - Adjust refresh rate (default: 10)
- `auto_refresh=False` - Disable automatic updates

## Special Features

**Indeterminate Progress**: Display pulsing animation when total steps are unknown by setting `total=None` or `start=False`.

**File Reading**: Track progress while reading files using `open()` or `wrap_file()` context managers.

**Nesting**: Create progress bars within existing progress contexts for hierarchical task tracking.

**Console Integration**: Access `progress.console` to print messages above the progress display without breaking visuals.
