---
source: https://rich.readthedocs.io/en/latest/text.html
scraped: 2025-11-19
cleaned: 2025-11-19
title: Rich Library - Text
---

Rich Text
===============================================

Rich has a [`Text`](https://rich.readthedocs.io/en/latest/reference/text.html#rich.text.Text) class you can use to mark up strings with color and style attributes. You can use a Text instance anywhere a string is accepted, which gives you a lot of control over presentation.

You can consider this class to be like a string with marked up regions of text. Unlike a built-in `str`, a Text instance is mutable, and most methods operate in-place rather than returning a new instance.

One way to add a style to Text is the [`stylize()`](https://rich.readthedocs.io/en/latest/reference/text.html#rich.text.Text.stylize) method which applies a style to a start and end offset. Here is an example:

```python
from rich.console import Console
from rich.text import Text

console = Console()
text = Text("Hello, World!")
text.stylize("bold magenta", 0, 6)
console.print(text)
```python

This will print “Hello, World!” to the terminal, with the first word in bold magenta.

Alternatively, you can construct styled text by calling [`append()`](https://rich.readthedocs.io/en/latest/reference/text.html#rich.text.Text.append) to add a string and style to the end of the Text. Here’s an example:

```python
text = Text()
text.append("Hello", style="bold magenta")
text.append(" World!")
console.print(text)
```python

If you would like to use text that is already formatted with ANSI codes, call [`from_ansi()`](https://rich.readthedocs.io/en/latest/reference/text.html#rich.text.Text.from_ansi) to convert it to a `Text` object:

```python
text = Text.from_ansi("\033[1;35mHello\033[0m, World!")
console.print(text.spans)
```python

Since building Text instances from parts is a common requirement, Rich offers [`assemble()`](https://rich.readthedocs.io/en/latest/reference/text.html#rich.text.Text.assemble) which will combine strings or pairs of string and Style, and return a Text instance. The following example is equivalent to the ANSI example above:

```python
text = Text.assemble(("Hello", "bold magenta"), ", World!")
console.print(text)
```python

You can apply a style to given words in the text with [`highlight_words()`](https://rich.readthedocs.io/en/latest/reference/text.html#rich.text.Text.highlight_words) or for ultimate control call [`highlight_regex()`](https://rich.readthedocs.io/en/latest/reference/text.html#rich.text.Text.highlight_regex) to highlight text matching a *regular expression*.

Text attributes
-----------------------------------------------------------

The Text class has a number of parameters you can set on the constructor to modify how the text is displayed.

* `justify` should be “left”, “center”, “right”, or “full”, and will override default justify behavior.
* `overflow` should be “fold”, “crop”, or “ellipsis”, and will override default overflow.
* `no_wrap` prevents wrapping if the text is longer then the available width.
* `tab_size` Sets the number of characters in a tab.

A Text instance may be used in place of a plain string virtually everywhere in the Rich API, which gives you a lot of control in how text renders within other Rich renderables. For instance, the following example right aligns text within a [`Panel`](https://rich.readthedocs.io/en/latest/reference/panel.html#rich.panel.Panel):

```python
from rich import print
from rich.panel import Panel
from rich.text import Text
panel = Panel(Text("Hello", justify="right"))
print(panel)
```