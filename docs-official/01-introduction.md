# Rich 14.1.0 Documentation - Introduction

## Overview

Rich is a Python library for outputting styled text and advanced content to the terminal. It enables developers to create visually appealing command-line applications and display data in more readable formats. The library also serves as a debugging tool through pretty-printing and syntax highlighting capabilities.

## System Requirements

- **Operating Systems**: macOS, Linux, and Windows
- **Python Version**: 3.8.0 or higher
- **Windows Support**: Both legacy cmd.exe and the modern Windows Terminal are supported, though the latter offers superior color and styling capabilities
- **PyCharm Note**: Users must enable "emulate terminal" in output console settings to view styled output properly

## Installation

Install via pip:
```
pip install rich
```

For Jupyter support, add optional dependencies:
```
pip install "rich[jupyter]"
```

Verify installation by running:
```
python -m rich
```

## Quick Start

Import Rich's print function as a drop-in replacement for Python's built-in print:

```python
from rich import print
```

This enables automatic syntax highlighting and formatted output of data structures. Use Console Markup to add colors and styles:

```python
print("[italic red]Hello[/italic red] World!", locals())
```

Alternatively, import as `rprint` to avoid shadowing the built-in:
```python
from rich import print as rprint
```

## REPL Integration

Enable automatic pretty-printing in the Python REPL:

```python
from rich import pretty
pretty.install()
```

### IPython Extension

For IPython users, load the Rich extension:
```
%load_ext rich
```

This provides pretty-printing and enhanced tracebacks automatically.

## Rich Inspect Function

The `inspect()` function generates detailed reports on Python objects, useful for debugging:

```python
from rich import inspect
inspect(some_object, methods=True)
```
