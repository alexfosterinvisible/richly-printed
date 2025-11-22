# Traceback Documentation - Rich 14.1.0

## Overview

Rich enables Python developers to display tracebacks with syntax highlighting and enhanced formatting. The library provides multiple approaches to rendering exceptions, from manual printing to automatic handler installation.

## Printing Tracebacks

The `print_exception()` method handles current exception rendering. A basic implementation:

```python
from rich.console import Console
console = Console()

try:
    do_something()
except Exception:
    console.print_exception(show_locals=True)
```

The `show_locals=True` parameter displays local variable values within each traceback frame.

## Traceback Handler Installation

Rich can replace the default exception handler through:

```python
from rich.traceback import install
install(show_locals=True)
```

This processes all uncaught exceptions with Rich's formatting. Configuration options are available through the `install()` function.

### Automatic Handler Setup

To activate the handler automatically across a virtual environment, modify `sitecustomize.py` in your site-packages directory (typically `./.venv/lib/python3.9/site-packages/sitecustomize.py`):

```python
from rich.traceback import install
install(show_locals=True)
```

Create the file if it doesn't exist using `touch`.

## Frame Suppression

Framework developers can exclude specific modules from traceback output:

```python
import click
from rich.traceback import install
install(suppress=[click])
```

Suppressed frames display filename and line number only, omitting source code.

## Managing Large Tracebacks

Recursion errors generate extensive frames. Rich defaults to `max_frames=100`, showing only the first 50 and last 50 frames when exceeded. Setting `max_frames=0` disables this feature entirely.
