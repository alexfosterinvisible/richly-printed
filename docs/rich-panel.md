---
source: https://rich.readthedocs.io/en/latest/panel.html
scraped: 2025-11-19
cleaned: 2025-11-19
title: Rich Library - Panel
---

Panel
=======================================

To draw a border around text or other renderable, construct a [`Panel`](https://rich.readthedocs.io/en/latest/reference/panel.html#rich.panel.Panel) with the renderable as the first positional argument. Here’s an example:

```python
from rich import print
from rich.panel import Panel
print(Panel("Hello, [red]World!"))
```python

You can change the style of the panel by setting the `box` argument to the Panel constructor. See [Box](appendix/box.html#appendix-box) for a list of available box styles.

Panels will extend to the full width of the terminal. You can make panel *fit* the content by setting `expand=False` on the constructor, or by creating the Panel with [`fit()`](https://rich.readthedocs.io/en/latest/reference/panel.html#rich.panel.Panel.fit). For example:

```python
from rich import print
from rich.panel import Panel
print(Panel.fit("Hello, [red]World!"))
```text

The Panel constructor accepts a `title` argument which will draw a title on the top of the panel, as well as a `subtitle` argument which will draw a subtitle on the bottom of the panel:

```python
from rich import print
from rich.panel import Panel
print(Panel("Hello, [red]World!", title="Welcome", subtitle="Thank you"))
```

See [`Panel`](https://rich.readthedocs.io/en/latest/reference/panel.html#rich.panel.Panel) for details how to customize Panels.