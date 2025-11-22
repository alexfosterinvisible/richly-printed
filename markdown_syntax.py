"""(Claude) Markdown & Syntax Highlighting Demo: Document rendering and code display

Requirements:
☑️✅ Markdown rendering with headers, lists, and inline formatting
☑️✅ Python syntax highlighting with line numbers
☑️✅ Custom color theme (monokai) for code display
☑️✅ Fitted panel introduction with styling
⛔ Out of scope: Live markdown editing, multiple languages, custom themes

Features:
- Panel.fit introduction with blue border and Rich markup
- Markdown rendering of headers, bullet lists, bold text, and inline code
- Syntax highlighting for Python code snippets
- Monokai theme with line numbers for code display
- Demonstrates both documentation and code presentation

Technical:
- Rich: Console, Markdown, Syntax, Panel
- Syntax: line_numbers=True, theme="monokai"
- Markdown: Headers (#), lists (-), bold (**), inline code (`)
- Pattern: Document-first presentation with code examples

Run: uv run markdown
"""
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax


def main() -> None:
    console = Console()

    console.print(Panel.fit(
        "[bold blue]Example 2: Markdown & Syntax Highlighting[/bold blue]\n\n"
        "This script demonstrates:\n"
        "• Rendering Markdown with Rich\n"
        "• Syntax highlighting for code blocks\n"
        "• Custom themes (monokai) with line numbers",
        border_style="blue"
    ))

    console.print(Markdown("# Hello\n\n- Bullet 1\n- Bullet 2\n\n**Bold** and `code`."))
    code = "for i in range(3):\n    print(i)"
    console.print(Syntax(code, "python", line_numbers=True, theme="monokai"))


if __name__ == "__main__":
    main()








