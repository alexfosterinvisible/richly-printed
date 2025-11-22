# Logging Handler Documentation

## Overview

Rich provides a logging handler that formats and colorizes output from Python's logging module. Basic setup involves importing `RichHandler` and configuring it through Python's standard logging:

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

## Markup and Highlighting

By default, Rich logs don't process console markup to avoid issues with unescaped brackets in third-party libraries. You can enable markup either globally on the handler or per-message:

**Per-message approach:**
```python
log.error("[bold red blink]Server is shutting down![/]", extra={"markup": True})
```

Similarly, override the highlighter per-message using the `extra` parameter with `"highlighter": None`.

## Exception Handling

Enable Rich's enhanced traceback formatting by setting `rich_tracebacks=True` on the handler:

```python
handlers=[RichHandler(rich_tracebacks=True)]
```

This provides superior context compared to standard Python exceptions.

## Suppressing Framework Frames

When working with frameworks like Click or Django, you can exclude framework code from tracebacks using the `tracebacks_suppress` parameter:

```python
handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[click])]
```

"Suppressed frames will show the line and file only, without any code," helping focus on application-specific issues rather than framework internals.
