# Panel Documentation

## Overview

The Panel component draws a border around text or other renderable content. Create one by instantiating a `Panel` object with your content as the first argument.

## Basic Usage

```python
from rich import print
from rich.panel import Panel
print(Panel("Hello, [red]World!"))
```

## Customization Options

**Box Styles:** Modify the panel's appearance using the `box` parameter. The documentation references an appendix listing available box styles.

**Sizing:** By default, panels expand to fill terminal width. To constrain a panel to its content size, either set `expand=False` or use the `fit()` method:

```python
print(Panel.fit("Hello, [red]World!"))
```

**Headers and Footers:** Add a top title and bottom subtitle using the `title` and `subtitle` parameters:

```python
print(Panel("Hello, [red]World!", title="Welcome", subtitle="Thank you"))
```

For complete customization details, consult the full `Panel` reference documentation.
