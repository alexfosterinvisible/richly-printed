"""(Claude) Rich Tracebacks Demo: Enhanced error display with local variable inspection

Requirements:
☑️✅ Rich traceback formatting with syntax highlighting
☑️✅ Local variable inspection in error context
☑️✅ Color-coded error messages and stack frames
☑️✅ Deliberate exception to demonstrate formatting
☑️✅ Traceback installation with show_locals=True
⛔ Out of scope: Exception handling, logging integration, custom formatters

Features:
- Rich traceback installation replaces default Python traceback
- show_locals=True displays variable values at exception point
- Syntax-highlighted code context in stack frames
- Color-coded file paths and line numbers
- Deliberate ZeroDivisionError to demonstrate formatting
- Shows numerator=1 and denominator=0 in locals
- Red-bordered introduction panel explaining purpose
- Enhanced readability compared to default Python tracebacks

Technical:
- Rich: Console, Panel, traceback.install()
- Install: show_locals=True for variable inspection
- Pattern: Developer-friendly error debugging
- Exception: Deliberate division by zero (numerator / denominator)
- Enhancement: Replaces sys.excepthook globally
- Color scheme: Syntax highlighting for Python code in trace

Run: uv run tracebacks
"""
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install


def main() -> None:
    console = Console()

    console.print(Panel.fit(
        "[bold red]Example 15: Rich Tracebacks[/bold red]\n\n"
        "This script demonstrates:\n"
        "• Pretty formatted tracebacks\n"
        "• Local variable inspection\n"
        "• Syntax highlighted error messages",
        border_style="red"
    ))

    install(show_locals=True)
    # Deliberately trigger an exception to show a rich traceback
    numerator = 1
    denominator = 0
    _ = numerator / denominator  # noqa: B018


if __name__ == "__main__":
    main()








