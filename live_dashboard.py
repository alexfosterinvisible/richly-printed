"""(Claude) Live Dashboard Demo: Multi-column job queue monitoring

Requirements:
☑️✅ Two-column dashboard layout (Jobs, Queue)
☑️✅ 10 concurrent tasks with random durations (1-6s)
☑️✅ Real-time completion counter in Jobs panel
☑️✅ Dynamic queue countdown in Queue panel
☑️✅ Live updates using asyncio.as_completed()
☑️✅ 8 fps refresh rate
⛔ Out of scope: Individual task details, progress bars, error handling

Features:
- Columns layout with two panels side-by-side
- Jobs panel: green border, shows completed count
- Queue panel: yellow border, shows remaining count (total - done)
- 10 tasks with random durations 1-6 seconds
- Updates trigger immediately on each task completion
- asyncio.as_completed() for event-driven updates
- Green-bordered introduction panel

Technical:
- Asyncio: asyncio.sleep() for task simulation
- Rich: Console, Columns, Live, Panel
- Pattern: Event-driven dashboard updates on task completion
- Update mechanism: Live.update() called per completion event
- Refresh rate: 8 fps
- Total runtime: max 6s (longest task duration)

Run: uv run live-dashboard
"""

import asyncio
import random

from rich.console import Console
from rich.columns import Columns
from rich.live import Live
from rich.panel import Panel


def _render(done: int, total: int) -> Columns:
    return Columns(
        [
            Panel(f"[bold]Jobs[/bold]\nDone: {done}", border_style="green"),
            Panel(f"[bold]Queue[/bold]\nLeft: {max(0, total - done)}", border_style="yellow"),
        ]
    )


async def _task(duration: float) -> None:
    await asyncio.sleep(duration)


async def main_async() -> None:
    console = Console()

    console.print(Panel.fit(
        "[bold green]Example 10: Live Dashboard[/bold green]\n\n"
        "This script demonstrates:\n"
        "• Multi-column dashboard layout\n"
        "• Live progress tracking\n"
        "• Dynamic queue updates",
        border_style="green"
    ))

    total = 10
    durations = [random.randint(1, 6) for _ in range(total)]
    tasks = [asyncio.create_task(_task(d)) for d in durations]
    done = 0
    with Live(_render(done, total), refresh_per_second=8) as live:
        for _ in asyncio.as_completed(tasks):
            await _
            done += 1
            live.update(_render(done, total))


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
