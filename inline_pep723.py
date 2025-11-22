#!/usr/bin/env -S uv run --script
"""(Claude) PEP 723 Inline Metadata Demo: Self-contained scripts with embedded dependencies

Requirements:
☑️✅ PEP 723 inline metadata format (/// script /// block)
☑️✅ Self-documenting dependency specification
☑️✅ Executable via UV without pyproject.toml
☑️✅ Syntax-highlighted example code display
☑️✅ Demonstrating both inline execution methods
⛔ Out of scope: Complex dependency resolution, virtual environment management

Features:
- Inline script metadata block with dependencies array
- Rich >= 13.0.0 dependency specification
- Yellow-bordered panel introduction
- Syntax-highlighted example showing PEP 723 format
- Monokai theme with line numbers for code display
- Demonstrates self-contained script pattern

Technical:
- PEP 723: /// script /// toml-formatted metadata block
- Rich: Console, Panel, Syntax
- Syntax: Python highlighting with monokai theme
- UV: Executes inline metadata scripts without pyproject.toml
- Pattern: Portable single-file scripts with dependencies

Run: uv run inline
Or:  uv run examples/inline_pep723.py
"""
# /// script
# dependencies = [
#     "rich>=13.0.0",
# ]
# ///

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax


def main() -> None:
    """Example showing inline script metadata."""
    console = Console()

    console.print("[dim]# inline_pep723.py[/dim]")
    console.print(Panel.fit(
        "[bold yellow]Example 3: Inline Script Metadata[/bold yellow]\n\n"
        "This script demonstrates:\n"
        "• PEP 723 inline script metadata\n"
        "• Self-contained scripts\n"
        "• Can specify dependencies inline",
        border_style="yellow"
    ))
    
    # Show the inline metadata format
    example_code = '''#!/usr/bin/env python3
# /// script
# dependencies = [
#     "rich>=13.0.0",
# ]
# ///

from rich import print as rprint

rprint("[bold green]Hello from inline script![/bold green]")
'''
    
    syntax = Syntax(example_code, "python", theme="monokai", line_numbers=True)
    console.print("\n[cyan]Example inline metadata format:[/cyan]")
    console.print(syntax)
    console.print("✅ Inline metadata example!", style="bold green")


if __name__ == "__main__":
    main()








