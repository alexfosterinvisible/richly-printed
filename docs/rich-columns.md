---
source: https://rich.readthedocs.io/en/latest/columns.html
scraped: 2025-11-19
cleaned: 2025-11-19
title: Rich Library - Columns
---

Columns
===========================================

Rich can render text or other Rich renderables in neat columns with the [`Columns`](https://rich.readthedocs.io/en/latest/reference/columns.html#rich.columns.Columns) class. To use, construct a Columns instance with an iterable of renderables and print it to the Console.

The following example is a very basic clone of the `ls` command in OSX / Linux to list directory contents:

```python
import os
import sys

from rich import print
from rich.columns import Columns

if len(sys.argv) < 2:
    print("Usage: python columns.py DIRECTORY")
else:
    directory = os.listdir(sys.argv[1])
    columns = Columns(directory, equal=True, expand=True)
    print(columns)
```

See [columns.py](https://github.com/willmcgugan/rich/blob/master/examples/columns.py) for an example which outputs columns containing more than just text.