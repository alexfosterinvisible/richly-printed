"""(Claude) Environment Variables Demo: Configuration management with env vars and defaults

Requirements:
☑️✅ Environment variable reading with os.getenv()
☑️✅ Default value fallback mechanism
☑️✅ Rich table display of environment configuration
☑️✅ Source tracking (Environment vs Default)
☑️✅ Multiple environment variable examples
⛔ Out of scope: .env file parsing (python-dotenv), validation, type conversion

Features:
- Magenta-bordered panel introduction
- Table with three columns: Variable, Value, Source
- Four example environment variables checked (LOG_LEVEL, PYTHONPATH, HOME, USER)
- Default value provision with " (default)" suffix for clarity
- Source column distinguishes environment vs default values
- Helpful tip about creating .env files
- Success confirmation message

Technical:
- Rich: Console, Panel, Table
- Environment: os.getenv(key, default) for safe access
- Table styling: cyan variable names, green values, yellow sources
- Pattern: Configuration introspection and display
- No external dependencies for env parsing

Run: uv run example-env
"""

import os

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


def main() -> None:
    """Example showing environment variable handling."""
    console = Console()

    console.print("[dim]# env.py[/dim]")
    console.print(
        Panel.fit(
            "[bold magenta]Example 4: Environment Variables[/bold magenta]\n\n"
            "This script demonstrates:\n"
            "• Reading environment variables\n"
            "• Configuration from .env files\n"
            "• Default values",
            border_style="magenta",
        )
    )

    # Show environment variables
    table = Table(title="Environment Configuration")
    table.add_column("Variable", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Source", style="yellow")

    # Check various env vars
    env_vars = {
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO (default)"),
        "PYTHONPATH": os.getenv("PYTHONPATH", "Not set"),
        "HOME": os.getenv("HOME", "Not set"),
        "USER": os.getenv("USER", "Not set"),
    }

    for var, value in env_vars.items():
        source = "Environment" if os.getenv(var) else "Default"
        table.add_row(var, str(value), source)

    console.print(table)
    console.print("\n[dim]Tip: Create a .env file to set LOG_LEVEL and other variables[/dim]")
    console.print("✅ Environment example!", style="bold green")


if __name__ == "__main__":
    main()






