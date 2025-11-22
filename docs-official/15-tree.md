# Tree Documentation Content

## Overview

Rich provides a `Tree` class for generating hierarchical tree views in the terminal. This feature is ideal for displaying filesystem contents or other nested data structures, where each branch can contain text or any Rich renderable object.

## Basic Usage

To demonstrate the Tree functionality, run:
```
python -m rich.tree
```

Create a simple tree with this code:
```python
from rich.tree import Tree
from rich import print

tree = Tree("Rich Tree")
print(tree)
```

A single Tree instance displays only its root label. Use the `add()` method to expand the tree with branches:

```python
tree.add("foo")
tree.add("bar")
print(tree)
```

The `add()` method returns a new Tree instance, enabling nested branch construction:

```python
baz_tree = tree.add("baz")
baz_tree.add("[red]Red").add("[green]Green").add("[blue]Blue")
print(tree)
```

## Styling Options

Both the Tree constructor and `add()` method support styling parameters:

- **`style`**: Applies formatting to an entire branch and inherited sub-trees
- **`guide_style`**: Controls the appearance of connector lines

When `guide_style` is set to bold, thicker Unicode line characters are used. Setting it to "underline2" produces double-line styling.

## Practical Example

For a real-world implementation, see the provided `tree.py` example file, which demonstrates generating a directory tree view from your filesystem.
