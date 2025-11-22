# Columns Documentation

## Overview

Rich provides a `Columns` class for rendering text and other Rich renderables in organized columns. You instantiate a Columns object with an iterable of renderables and pass it to the Console for display.

## Basic Example

The documentation includes a practical example demonstrating a simple directory listing tool inspired by the `ls` command:

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

This example accepts a directory path as a command-line argument, retrieves its contents, and displays them using the Columns class with `equal=True` and `expand=True` parameters to ensure uniform column sizing.

## Additional Resources

The documentation references a more comprehensive example file (`columns.py`) in the Rich repository that demonstrates rendering columns with richer content beyond simple text elements.
