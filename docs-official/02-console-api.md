# Rich Console API Documentation

## Overview

Rich provides a `Console` class for controlling terminal formatting with ANSI escape sequences. The typical pattern involves creating a module-level instance:

```python
from rich.console import Console
console = Console()
```

## Key Attributes

The Console auto-detects terminal properties:

- **size**: Current terminal dimensions
- **encoding**: Default text encoding (usually UTF-8)
- **is_terminal**: Boolean indicating terminal output
- **color_system**: The supported color standard

## Color Systems

Rich supports multiple color standards, configurable via the `color_system` parameter:

- `None`: Disables color
- `"auto"`: Auto-detects (default)
- `"standard"`: 16 colors
- `"256"`: 256-color palette
- `"truecolor"`: 16.7 million colors
- `"windows"`: Legacy Windows terminal

⚠️ Setting a higher color system than your terminal supports can render text unreadable.

## Core Methods

**print()**: Renders rich content with syntax highlighting and pretty-printing of containers. Supports Console Markup and objects implementing the Console Protocol.

**log()**: Similar to print but adds timestamps and file/line information for debugging. Includes optional `log_locals` parameter.

**print_json()**: Formats and styles JSON strings.

**rule()**: Draws horizontal divider lines with optional titles and styling.

**status()**: Displays animated status messages without interfering with regular output.

## Text Handling

**Justify/Alignment**: The `justify` parameter accepts "default", "left", "right", "center", or "full".

**Overflow**: Handles text exceeding available space via the `overflow` parameter:
- "fold": Wraps to next line
- "crop": Truncates text
- "ellipsis": Adds "…" after truncation
- "ignore": Allows overflow

**Soft Wrapping**: Set `soft_wrap=True` to disable word wrapping.

## Advanced Features

**input()**: Rich-enabled version of Python's built-in input function supporting formatted prompts.

**Exporting**: With `record=True`, export console output as text, HTML, or SVG via `export_text()`, `export_html()`, or `export_svg()`.

**Error Console**: Create separate error output with `Console(stderr=True)`.

**File Output**: Write to files using the `file` parameter.

**Capturing**: Use `capture()` context manager or `StringIO` to capture output.

**Paging**: Display long output using system pagers via `pager()`.

**Alternate Screen**: Full-screen mode with `screen()` context manager (experimental).

## Terminal Detection & Configuration

Rich auto-detects terminal capabilities and strips control codes for non-terminal output. Override with `force_terminal=True`.

**Environment Variables**:
- `TERM`: Set to "dumb" or "unknown" disables features
- `FORCE_COLOR`: Enables colors regardless of TERM
- `NO_COLOR`: Disables all color (takes precedence)
- `TTY_COMPATIBLE`: Override terminal detection ("0" or "1")
- `TTY_INTERACTIVE`: Override interactive mode
- `COLUMNS`/`LINES`: Set console dimensions
- `JUPYTER_COLUMNS`/`JUPYTER_LINES`: Jupyter-specific dimensions

For CI/GitHub Actions: Set `TTY_COMPATIBLE=1` and `TTY_INTERACTIVE=0` to enable escape sequences while disabling animations.
