---
source: https://rich.readthedocs.io/en/latest/live.html
scraped: 2025-11-19
cleaned: 2025-11-19
title: Rich Library - Live
---

Live Display
=====================================================

Progress bars and status indicators use a *live* display to animate parts of the terminal. You can build custom live displays with the [`Live`](https://rich.readthedocs.io/en/latest/reference/live.html#rich.live.Live) class.

For a demonstration of a live display, run the following command:

```bash
python -m rich.live
```python

Note

If you see ellipsis “…”, this indicates that the terminal is not tall enough to show the full table.

Basic usage
---------------------------------------------------

To create a live display, construct a [`Live`](https://rich.readthedocs.io/en/latest/reference/live.html#rich.live.Live) object with a renderable and use it as a context manager. The live display will persist for the duration of the context. You can update the renderable to update the display:

```python
import time

from rich.live import Live
from rich.table import Table

table = Table()
table.add_column("Row ID")
table.add_column("Description")
table.add_column("Level")

with Live(table, refresh_per_second=4):  # update 4 times a second to feel fluid
    for row in range(12):
        time.sleep(0.4)  # arbitrary delay
        # update the renderable internally
        table.add_row(f"{row}", f"description {row}", "[red]ERROR")
```python

Updating the renderable
---------------------------------------------------------------------------

You can also change the renderable on-the-fly by calling the [`update()`](https://rich.readthedocs.io/en/latest/reference/live.html#rich.live.Live.update) method. This may be useful if the information you wish to display is too dynamic to generate by updating a single renderable. Here is an example:

```python
import random
import time

from rich.live import Live
from rich.table import Table

def generate_table() -> Table:
    """Make a new table."""
    table = Table()
    table.add_column("ID")
    table.add_column("Value")
    table.add_column("Status")

    for row in range(random.randint(2, 6)):
        value = random.random() * 100
        table.add_row(
            f"{row}", f"{value:3.2f}", "[red]ERROR" if value < 50 else "[green]SUCCESS"
        )
    return table

with Live(generate_table(), refresh_per_second=4) as live:
    for _ in range(40):
        time.sleep(0.4)
        live.update(generate_table())
```python

Alternate screen
-------------------------------------------------------------

You can opt to show a Live display in the “alternate screen” by setting `screen=True` on the constructor. This will allow your live display to go full screen and restore the command prompt on exit.

You can use this feature in combination with [Layout](layout.html#layout) to display sophisticated terminal “applications”.

Transient display
---------------------------------------------------------------

Normally when you exit live context manager (or call [`stop()`](https://rich.readthedocs.io/en/latest/reference/live.html#rich.live.Live.stop)) the last refreshed item remains in the terminal with the cursor on the following line.
You can also make the live display disappear on exit by setting `transient=True` on the Live constructor.

Auto refresh
-----------------------------------------------------

By default, the live display will refresh 4 times a second. You can set the refresh rate with the `refresh_per_second` argument on the [`Live`](https://rich.readthedocs.io/en/latest/reference/live.html#rich.live.Live) constructor.
You should set this to something lower than 4 if you know your updates will not be that frequent or higher for a smoother feeling.

You might want to disable auto-refresh entirely if your updates are not very frequent, which you can do by setting `auto_refresh=False` on the constructor.
If you disable auto-refresh you will need to call [`refresh()`](https://rich.readthedocs.io/en/latest/reference/live.html#rich.live.Live.refresh) manually or [`update()`](https://rich.readthedocs.io/en/latest/reference/live.html#rich.live.Live.update) with `refresh=True`.

Vertical overflow
---------------------------------------------------------------

By default, the live display will display ellipsis if the renderable is too large for the terminal. You can adjust this by setting the
`vertical_overflow` argument on the [`Live`](https://rich.readthedocs.io/en/latest/reference/live.html#rich.live.Live) constructor.

* “crop” Show renderable up to the terminal height. The rest is hidden.
* “ellipsis” Similar to crop except last line of the terminal is replaced with “…”. This is the default behavior.
* “visible” Will allow the whole renderable to be shown. Note that the display cannot be properly cleared in this mode.

Note

Once the live display stops on a non-transient renderable, the last frame will render as **visible** since it doesn’t have to be cleared.

Print / log
-------------------------------------------------

The Live class will create an internal Console object which you can access via `live.console`. If you print or log to this console, the output will be displayed *above* the live display. Here’s an example:

```python
import time

from rich.live import Live
from rich.table import Table

table = Table()
table.add_column("Row ID")
table.add_column("Description")
table.add_column("Level")

with Live(table, refresh_per_second=4) as live:  # update 4 times a second to feel fluid
    for row in range(12):
        live.console.print(f"Working on row #{row}")
        time.sleep(0.4)
        table.add_row(f"{row}", f"description {row}", "[red]ERROR")
```python

If you have another Console object you want to use, pass it in to the [`Live`](https://rich.readthedocs.io/en/latest/reference/live.html#rich.live.Live) constructor. Here’s an example:

```python
from my_project import my_console

with Live(console=my_console) as live:
    my_console.print("[bold blue]Starting work!")
    ...
```

Note

If you are passing in a file console, the live display only show the last item once the live context is left.

Redirecting stdout / stderr
---------------------------------------------------------------------------------

To avoid breaking the live display visuals, Rich will redirect `stdout` and `stderr` so that you can use the builtin `print` statement.
This feature is enabled by default, but you can disable by setting `redirect_stdout` or `redirect_stderr` to `False`.

### Nesting Lives

If you create a Live instance within the context of an existing Live instance, then the content of the inner Live will be displayed below the outer Live.

Prior to version 14.0.0 this would have resulted in a `LiveError` exception.

### Examples

See [table\_movie.py](https://github.com/willmcgugan/rich/blob/master/examples/table_movie.py) and
[top\_lite\_simulator.py](https://github.com/willmcgugan/rich/blob/master/examples/top_lite_simulator.py)
for deeper examples of live displaying.