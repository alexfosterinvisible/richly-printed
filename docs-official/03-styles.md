# Rich Styles Documentation

## Overview

Rich provides styling capabilities for text in various parts of its API. Styles can be specified as strings containing style definitions or as `Style` class instances.

## Defining Styles

### Colors

Foreground colors can be specified using standard color names:

```python
console.print("Hello", style="magenta")
```

Colors can also be referenced by number (0-255):

```python
console.print("Hello", style="color(5)")
```

Truecolor support is available through hex or RGB syntax:

```python
console.print("Hello", style="#af00ff")
console.print("Hello", style="rgb(175,0,255)")
```

### Background Colors

Prefix a color with "on" to set the background:

```python
console.print("DANGER!", style="red on white")
```

Use "default" to reset colors to terminal defaults.

### Text Attributes

Available attributes include:
- **bold** (`b`) and **italic** (`i`)
- **underline** (`u`), **underline2** (`uu`)
- **strike** (`s`), **reverse** (`r`)
- **blink** and **blink2** (rapid blinking)
- **frame**, **encircle**, **overline** (`o`)

Combine multiple attributes:

```python
console.print("Danger!", style="blink bold red underline on white")
```

Negate attributes with "not":

```python
console.print("foo [not bold]bar[/not bold] baz", style="bold")
```

### Hyperlinks

Add link functionality to styled text:

```python
console.print("Google", style="link https://google.com")
```

## Style Class

The `Style` class provides programmatic style construction:

```python
from rich.style import Style
danger_style = Style(color="red", blink=True, bold=True)
console.print("Danger!", style=danger_style)
```

Combine styles through addition:

```python
base_style = Style.parse("cyan")
console.print("Hello", style=base_style + Style(underline=True))
```

## Style Themes

The `Theme` class enables reusable, named styles:

```python
from rich.theme import Theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red"
})
console = Console(theme=custom_theme)
console.print("This is information", style="info")
```

Style names must be lowercase, start with a letter, and contain only letters, dots, hyphens, or underscores.

### Customizing Defaults

Override built-in styles:

```python
console = Console(theme=Theme({"repr.number": "bold green blink"}))
```

Disable default theme inheritance with `inherit=False`.

### External Theme Files

Load styles from configuration files:

```
[styles]
info = dim cyan
warning = magenta
danger = bold red
```

Use the `Theme.read()` method to load external theme files.
