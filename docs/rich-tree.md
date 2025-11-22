---
source: https://rich.readthedocs.io/en/latest/tree.html
scraped: 2025-11-19
cleaned: 2025-11-19
title: Rich Library - Tree
---

Tree
=====================================

Rich has a [`Tree`](https://rich.readthedocs.io/en/latest/reference/tree.html#rich.tree.Tree) class which can generate a tree view in the terminal. A tree view is a great way of presenting the contents of a filesystem or any other hierarchical data. Each branch of the tree can have a label which may be text or any other Rich renderable.

Run the following command to see a demonstration of a Rich tree:

```bash
python -m rich.tree
```python

The following code creates and prints a tree with a simple text label:

```python
from rich.tree import Tree
from rich import print

tree = Tree("Rich Tree")
print(tree)
```python

With only a single `Tree` instance this will output nothing more than the text “Rich Tree”. Things get more interesting when we call [`add()`](https://rich.readthedocs.io/en/latest/reference/tree.html#rich.tree.Tree.add) to add more branches to the Tree. The following code adds two more branches:

```python
tree.add("foo")
tree.add("bar")
print(tree)
```python

The tree will now have two branches connected to the original tree with guide lines.

When you call [`add()`](https://rich.readthedocs.io/en/latest/reference/tree.html#rich.tree.Tree.add) a new Tree instance is returned. You can use this instance to add more branches to, and build up a more complex tree. Let’s add a few more levels to the tree:

```python
baz_tree = tree.add("baz")
baz_tree.add("[red]Red").add("[green]Green").add("[blue]Blue")
print(tree)
```

Tree Styles
---------------------------------------------------

The Tree constructor and [`add()`](https://rich.readthedocs.io/en/latest/reference/tree.html#rich.tree.Tree.add) method allows you to specify a `style` argument which sets a style for the entire branch, and `guide_style` which sets the style for the guide lines. These styles are inherited by the branches and will apply to any sub-trees as well.

If you set `guide_style` to bold, Rich will select the thicker variations of unicode line characters. Similarly, if you select the “underline2” style you will get double line style of unicode characters.

Examples
---------------------------------------------

For a more practical demonstration, see [tree.py](https://github.com/willmcgugan/rich/blob/master/examples/tree.py) which can generate a tree view of a directory in your hard drive.