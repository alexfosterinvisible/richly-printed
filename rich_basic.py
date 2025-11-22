"""(Claude) Basic Rich Console Demo: Introduction to Rich library fundamentals

Requirements:
☑️✅ Panel rendering with formatted text and styling
☑️✅ Console output with color markup
☑️✅ Loguru integration for structured logging
☑️✅ UV script execution via entry point
⛔ Out of scope: Complex layouts, live updates, tables

Features:
- Single fitted panel with green border displaying script purpose
- Rich markup syntax for bold text and bullet points
- Console.print() for styled terminal output
- Loguru logger.info() for demonstration of logging integration
- Success message with colored checkmark

Technical:
- Rich: Console, Panel (Panel.fit with border_style)
- Loguru: logger for structured logging
- Pattern: Simple console output with Rich markup syntax
- Entry point: Configured in pyproject.toml as 'basic'

Run: uv run basic
"""
from loguru import logger
from rich.console import Console
from rich.panel import Panel


def main() -> None:
    """Basic example showing UV script execution."""
    console = Console()
    
    console.print(Panel.fit(
        "[bold green]Example 1: Basic UV Script[/bold green]\n\n"
        "This script demonstrates:\n"
        "• Running scripts via entry points\n"
        "• Using project dependencies\n"
        "• Rich console output",
        border_style="green"
    ))
    
    logger.info("This is a log message using loguru")
    console.print("✅ Basic script execution works!", style="bold green")


if __name__ == "__main__":
    main()








