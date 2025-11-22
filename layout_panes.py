"""(Claude) Layout Panes Demo: Split-screen terminal regions with live updates

Requirements:
☑️✅ Terminal split into named regions (header, body, left, right)
☑️✅ Column-based vertical split (header/body)
☑️✅ Row-based horizontal split (left/right within body)
☑️✅ Live updates at 8 fps refresh rate
☑️✅ Independent pane updating every 0.2s
☑️✅ Fixed-size header (3 lines)
⛔ Out of scope: Dynamic resizing, nested splits beyond 2 levels, border customization

Features:
- Three-region layout: header (fixed 3 lines) and body (split left/right)
- Live.update() for real-time pane updates without flicker
- Header updates with counter (0-5)
- Left pane static content
- Right pane updates with iteration counter
- 6 iterations with 0.2s delay between updates
- 8 fps refresh rate for smooth updates
- Green-bordered introduction panel

Technical:
- Rich: Console, Layout, Live, Panel
- Layout: split_column() for vertical, split_row() for horizontal
- Live: refresh_per_second=8 for smooth updates
- Pattern: Multi-region dashboard with independent update zones
- Update cycle: 6 iterations × 0.2s = 1.2s total runtime

Run: uv run layout
"""

from time import sleep

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel


def _build_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
    )
    layout["body"].split_row(Layout(name="left"), Layout(name="right"))
    return layout


def main() -> None:
    console = Console()

    console.print(Panel.fit(
        "[bold green]Example 6: Layout Panes[/bold green]\n\n"
        "This script demonstrates:\n"
        "• Splitting terminal into regions\n"
        "• Live updating different panes\n"
        "• Column and row layouts",
        border_style="green"
    ))

    layout = _build_layout()
    with Live(layout, refresh_per_second=8):
        for i in range(6):
            layout["header"].update(Panel(f"Header {i}"))
            layout["left"].update(Panel("Left pane"))
            layout["right"].update(Panel(f"Right updates: {i}"))
            sleep(0.2)


if __name__ == "__main__":
    main()






