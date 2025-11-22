"""(Claude) HTTP Dependencies Demo: External library integration with error handling

Requirements:
☑️✅ HTTPX library for synchronous HTTP requests
☑️✅ GET request to httpbin.org/json endpoint
☑️✅ 5-second timeout for request
☑️✅ Response JSON parsing and table display
☑️✅ Network error handling with sys.exit(1)
☑️✅ Rich table with key-value pairs from response
⛔ Out of scope: Async requests, retry logic, authentication, POST requests

Features:
- Magenta-bordered panel introduction
- Synchronous HTTP GET request using httpx.get()
- 5-second timeout to prevent hanging
- Response status validation with raise_for_status()
- JSON response parsing into dict
- Rich table with two columns: Key (cyan), Value (green)
- Dynamic rows from response JSON keys
- HTTPError and general Exception handling
- Exit code 1 on errors for shell integration
- Success message on successful request

Technical:
- HTTPX: httpx.get() for synchronous requests
- Rich: Console, Panel, Table
- Error handling: httpx.HTTPError for network errors
- Pattern: External API integration with graceful degradation
- Timeout: timeout=5.0 parameter
- Exit: sys.exit(1) for error cases
- Table: titled "Response Data" with styled columns

Run: uv run deps
"""
import sys

import httpx
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


def main() -> None:
    """Example showing scripts with external dependencies."""
    console = Console()

    console.print(
        Panel.fit(
            "[bold magenta]Example 16: HTTP with Dependencies[/bold magenta]\n\n"
            "This script demonstrates:\n"
            "• Using httpx for HTTP requests\n"
            "• Rich table formatting\n"
            "• Network error handling",
            border_style="magenta",
        )
    )

    # Make a simple remote HTTP request (may timeout/fail)
    try:
        console.print("\n[cyan]Making HTTP request to httpbin.org...[/cyan]")
        response = httpx.get("https://httpbin.org/json", timeout=5.0)
        response.raise_for_status()
        data = response.json()

        table = Table(title="Response Data")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="green")

        for key, value in data.items():
            table.add_row(str(key), str(value))

        console.print(table)
        console.print("✅ HTTP request successful!", style="bold green")
    except httpx.HTTPError as e:
        console.print(f"[red]HTTP Error:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()








