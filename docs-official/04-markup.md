# Console Markup Documentation

## Overview

Rich supports a straightforward markup system for adding color and styling to text in applications using `print()` and `log()` methods.

## Syntax Basics

The markup language uses square bracket tags inspired by BBCode. A style like `[bold red]` remains active until closed with `[/bold red]`.

**Example:**
```python
print("[bold red]alert![/bold red] Something happened")
```

Styles automatically close at the end of a string, and you can use shorthand by writing `[/]` to close the most recent tag without specifying which one.

Tags can overlap without strict nesting requirements:
```python
print("[bold]Bold[italic] bold and italic [/bold]italic[/italic]")
```

## Key Features

**Hyperlinks:** Use `[link=URL]text[/link]` syntax to create clickable links in supported terminals.

**Emoji:** Embed emoji codes with colons (e.g., `:warning:`) which convert to Unicode characters. Variants exist for color (`:red_heart-emoji:`) or monochrome (`:red_heart-text:`) display.

**Escaping:** Precede markup with a backslash to treat it as literal text. The `escape()` function automatically handles escaping for dynamic content, which is important when constructing markup from user input to prevent injection attacks.

## Error Handling

Rich raises `MarkupError` for mismatched tags or unmatched closing tags.

## Controlling Markup Rendering

Set `markup=False` on `print()` or the `Console` constructor to disable markup interpretation when the syntax conflicts with your content.

## Markup API

Convert markup strings to styled text objects using `Text.from_markup()`, which returns a `Text` instance for further customization.
