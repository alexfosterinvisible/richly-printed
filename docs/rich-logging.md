---
source: https://rich.readthedocs.io/en/latest/logging.html
scraped: 2025-11-19
cleaned: 2025-11-19
title: Rich Library - Logging
---

Logging Handler
===========================================================

Rich supplies a [logging handler](https://rich.readthedocs.io/en/latest/reference/logging.html#logging) which will format and colorize text written by Python's logging module.

Here’s an example of how to set up a rich logger:

```python
import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")
log.info("Hello, World!")
```

Rich logs won't render [Console Markup](https://rich.readthedocs.io/en/latest/console_markup.html#console-markup) in logging by default as most libraries won't be aware of the need to escape literal square brackets, but you can enable it by setting `markup=True` on the handler. Alternatively you can enable it per log message by supplying the `extra` argument as follows:

```python
log.error("[bold red blink]Server is shutting down![/]", extra={"markup": True})
```

Similarly, the highlighter may be overridden per log message:

```python
log.error("123 will not be highlighted", extra={"highlighter": None})
```

Handle exceptions
---------------------------------------------------------------

The [`RichHandler`](https://rich.readthedocs.io/en/latest/reference/logging.html#rich.logging.RichHandler) class may be configured to use Rich’s [`Traceback`](https://rich.readthedocs.io/en/latest/reference/traceback.html#rich.traceback.Traceback) class to format exceptions, which provides more context than a built-in exception. To get beautiful exceptions in your logs set `rich_tracebacks=True` on the handler constructor:

```python
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log = logging.getLogger("rich")
try:
    print(1 / 0)
except Exception:
    log.exception("unable print!")
```

There are a number of other options you can use to configure logging output, see the [`RichHandler`](https://rich.readthedocs.io/en/latest/reference/logging.html#rich.logging.RichHandler) reference for details.

Suppressing Frames
-----------------------------------------------------------------

If you are working with a framework (click, django etc), you may only be interested in seeing the code from your own application within the traceback. You can exclude framework code by setting the suppress argument on Traceback, install, and Console.print\_exception, which should be a list of modules or str paths.

Here’s how you would exclude [click](https://click.palletsprojects.com/en/8.0.x/) from Rich exceptions:

```python
import click
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[click])]
)
```

Suppressed frames will show the line and file only, without any code.