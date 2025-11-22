"""(Claude) Advanced Progress Bar Demo: Custom columns with ETA and transfer speed

Requirements:
☑️✅ Custom progress column composition
☑️✅ M-of-N completion display (e.g., "200/5000")
☑️✅ Transfer speed calculation and display
☑️✅ Time remaining (ETA) estimation
☑️✅ Standard progress bar with description
☑️✅ Simulated download progress (5000 total units)
⛔ Out of scope: Multiple progress bars, nested progress, actual file transfer

Features:
- Five custom progress columns in specific order
- Description column: task name/label
- BarColumn: visual progress bar
- MofNCompleteColumn: shows "completed/total" format
- TransferSpeedColumn: calculates and displays rate
- TimeRemainingColumn: ETA based on current rate
- Single task: "Downloading" with 5000 total units
- Advance by 200 units per iteration
- 0.05s delay between updates (simulates download chunks)
- Green-bordered introduction panel

Technical:
- Rich: Console, Panel, Progress and custom columns
- Columns: BarColumn, MofNCompleteColumn, TransferSpeedColumn, TimeRemainingColumn
- Pattern: File download simulation with rich progress info
- Update mechanism: progress.update(task, advance=200)
- Progress tracking: automatic ETA calculation by Rich
- Runtime: (5000/200) × 0.05s = 1.25s

Run: uv run progress-advanced
"""
from time import sleep
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TimeRemainingColumn,
    TransferSpeedColumn,
)


def main() -> None:
    console = Console()

    console.print(Panel.fit(
        "[bold green]Example 12: Advanced Progress Bar[/bold green]\n\n"
        "This script demonstrates:\n"
        "• Custom progress columns\n"
        "• ETA and transfer speed display\n"
        "• M-of-N completion tracking",
        border_style="green"
    ))

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        MofNCompleteColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("Downloading", total=5000)
        while not progress.finished:
            progress.update(task, advance=200)
            sleep(0.05)


if __name__ == "__main__":
    main()








