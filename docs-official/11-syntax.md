# Syntax Documentation - Rich 14.1.0

## Overview

Rich provides syntax highlighting capabilities for multiple programming languages with optional line numbering.

## Basic Usage

To highlight code, instantiate a `Syntax` object and print it:

```python
from rich.console import Console
from rich.syntax import Syntax

console = Console()
with open("syntax.py", "rt") as code_file:
    syntax = Syntax(code_file.read(), "python")
console.print(syntax)
```

Alternatively, use the `from_path()` constructor to load code from disk with automatic file type detection:

```python
from rich.console import Console
from rich.syntax import Syntax

console = Console()
syntax = Syntax.from_path("syntax.py")
console.print(syntax)
```

## Line Numbers

Enable line number rendering by setting `line_numbers=True`:

```python
syntax = Syntax.from_path("syntax.py", line_numbers=True)
```

## Theme Configuration

Both constructors accept a `theme` parameter specifying a Pygments theme name. Special theme options include "ansi_dark" and "ansi_light," which use terminal-configured colors.

## Background Color

Override theme background colors using the `background_color` argument, accepting values like "red", "#ff0000", "rgb(255,0,0)", or "default" for terminal defaults.

## Command-Line Interface

Highlight files from the terminal:

```
python -m rich.syntax syntax.py
```

For complete options:

```
python -m rich.syntax -h
```
