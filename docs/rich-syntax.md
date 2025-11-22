---
source: https://rich.readthedocs.io/en/latest/syntax.html
scraped: 2025-11-19
cleaned: 2025-11-19
title: Rich Library - Syntax
---

Syntax
=========================================

Rich can syntax highlight various programming languages with line numbers.

To syntax highlight code, construct a [`Syntax`](https://rich.readthedocs.io/en/latest/reference/syntax.html#rich.syntax.Syntax) object and print it to the console. Here’s an example:

```python
from rich.console import Console
from rich.syntax import Syntax

console = Console()
with open("syntax.py", "rt") as code_file:
    syntax = Syntax(code_file.read(), "python")
console.print(syntax)
```python

You may also use the [`from_path()`](https://rich.readthedocs.io/en/latest/reference/syntax.html#rich.syntax.Syntax.from_path) alternative constructor which will load the code from disk and auto-detect the file type. The example above could be re-written as follows:

```python
from rich.console import Console
from rich.syntax import Syntax

console = Console()
syntax = Syntax.from_path("syntax.py")
console.print(syntax)
```python

Line numbers
-----------------------------------------------------

If you set `line_numbers=True`, Rich will render a column for line numbers:

```python
syntax = Syntax.from_path("syntax.py", line_numbers=True)
```python

Theme
---------------------------------------

The Syntax constructor (and [`from_path()`](https://rich.readthedocs.io/en/latest/reference/syntax.html#rich.syntax.Syntax.from_path)) accept a `theme` attribute which should be the name of a [Pygments theme](https://pygments.org/demo/). It may also be one of the special case theme names “ansi\_dark” or “ansi\_light” which will use the color theme configured by the terminal.

Background color
-------------------------------------------------------------

You can override the background color from the theme by supplying a `background_color` argument to the constructor. This should be a string in the same format a style definition accepts, e.g. “red”, “#ff0000”, “rgb(255,0,0)” etc. You may also set the special value “default” which will use the default background color set in the terminal.

Syntax CLI
-------------------------------------------------

You can use this class from the command line. Here’s how you would syntax highlight a file called “syntax.py”:

```bash
python -m rich.syntax syntax.py
```text

For the full list of arguments, run the following:

```bash
python -m rich.syntax -h
```