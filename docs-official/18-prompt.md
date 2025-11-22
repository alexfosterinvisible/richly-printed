# Rich Prompt Documentation

## Overview

Rich provides multiple `Prompt` classes that request user input and validate responses before returning. These classes utilize the Console API internally.

## Basic Usage

The simplest implementation uses `Prompt.ask()`:

```python
from rich.prompt import Prompt
name = Prompt.ask("Enter your name")
```

Prompts accept strings with Console Markup and emoji code, or `Text` instances.

## Default Values

Specify a fallback value returned when users press enter without typing:

```python
name = Prompt.ask("Enter your name", default="Paul Atreides")
```

## Choice Validation

Restrict input to predefined options:

```python
name = Prompt.ask("Enter your name",
                  choices=["Paul", "Jessica", "Duncan"],
                  default="Paul")
```

By default, matching is case-sensitive. Use `case_sensitive=False` to accept variations like "paul" or "Paul".

## Specialized Prompt Types

- **IntPrompt**: Requests integer input
- **FloatPrompt**: Requests floating-point input
- **Confirm**: Yes/no question prompt

Example:

```python
from rich.prompt import Confirm
is_rich_great = Confirm.ask("Do you like rich?")
```

## Customization

The `Prompt` class supports customization through inheritance. Reference the project's prompt.py file for implementation examples.

You can test prompts via: `python -m rich.prompt`
