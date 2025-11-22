"""(Claude) Live Logs Ordered Demo: Out-of-order completion with sequential display buffering

Requirements:
☑️✅ 12 concurrent tasks completing in random order
☑️✅ Sequential display buffer preserving original order (1→2→3...→12)
☑️✅ Tasks have random delays (0.1-4.0s, fully random)
☑️✅ Live status showing completed/total and buffered count
☑️✅ Immediate display updates using live.refresh()
☑️✅ asyncio.wait() with FIRST_COMPLETED for event-driven updates
☑️✅ Max 12 lines displayed with automatic rotation
☑️✅ 20 fps refresh rate for smooth progressive display
☑️✅ Green highlighting for most recently added entry
⛔ Out of scope: Timestamps, log levels, filtering, persistence, real async work

Features:
- Panel.fit with title "Live Logs (Ordered)" and cyan border
- Status line: "(X/12 tasks completed, Y buffered)" updated live
- Tasks numbered worker-1 through worker-12
- Log format: "worker-N > event N (X.Xs)" showing delay duration
- Random task completion order but sequential display order
- Most recently added line highlighted in green
- When new line arrives, previous green line returns to white
- Buffer mechanism: arrived dict stores out-of-order results
- Flush mechanism: displays tasks 1, 2, 3... as soon as they're ready
- Display only shows logs that maintain sequential order
- Deque with maxlen=12 for automatic old log rotation
- Update every 0.1s polling cycle at 20 fps
- Random delays: 0.1-4.0s (no bias, purely random for clear out-of-order demo)
- Cyan-bordered introduction panel explaining purpose

Technical:
- Asyncio: asyncio.wait() with FIRST_COMPLETED for event-driven processing
- Rich: Console, Live, Panel, Text
- Collections: deque(maxlen=12) for log rotation, dict for buffering
- Pattern: Order-preserving async result collection
- Buffer: arrived dict maps index→log_line
- Pointer: next_index tracks next sequential line to display
- Newest tracking: newest_line_index tracks last line added for green highlight
- Flush logic: while next_index in arrived, pop and display
- Update mechanism: live.update() + live.refresh() for instant visual update
- Refresh rate: 20 fps for smooth progressive display
- Timeout: 0.1s on asyncio.wait() allows periodic refreshes
- Done tracking: done_set to count completed tasks
- Total runtime: ~5s (depends on random delays, max 4.0s)

Run: uv run live-logs-ordered
"""
from __future__ import annotations

import asyncio
import random
from collections import deque
from typing import Deque, Dict, List, Tuple

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text


def _render_lines(lines: Deque[str], completed: int = 0, total: int = 0, buffered: int = 0, newest_index: int = -1):
    # Show status if tasks are buffered (completed but can't display yet)
    status = ""
    if total > 0 and completed < total:
        status = f"[dim]({completed}/{total} tasks completed, {buffered} buffered)[/dim]\n\n"

    # Build Text object with conditional green highlighting for newest entry
    text = Text(status)
    for i, line in enumerate(lines):
        if i > 0:
            text.append("\n")
        # Highlight newest line in green
        if i == newest_index:
            text.append(line, style="green")
        else:
            text.append(line)

    # Left-aligned panel that auto-sizes to content
    return Panel.fit(text, title="Live Logs (Ordered)", border_style="cyan")


def _planned_delay(index: int, total: int) -> float:
    """Plan delays with random variation - fully random order, ~5s total runtime."""
    # Wide random spread (0.1-4.0s) for clearly visible out-of-order completion
    # No bias - purely random to demonstrate buffering behavior
    return random.uniform(0.1, 4.0)


async def _produce(index: int, total: int) -> Tuple[int, str]:
    delay = _planned_delay(index, total)
    await asyncio.sleep(delay)
    # Format: worker-i > event i (x.xs)
    return index, f"worker-{index} > event {index} ({delay:.1f}s)"


async def main_async() -> None:
    console = Console()

    console.print(Panel.fit(
        "[bold cyan]Example 9B: Live Logs (Ordered)[/bold cyan]\n\n"
        "This script demonstrates:\n"
        "• Out-of-order task completion\n"
        "• Buffering and sequential display\n"
        "• Preserving original order despite async chaos",
        border_style="cyan"
    ))

    total = 12
    max_lines = 12
    lines: Deque[str] = deque()

    # Launch tasks
    tasks = [asyncio.create_task(_produce(i, total)) for i in range(1, total + 1)]

    # Buffer for arrived results and pointer for next expected index
    arrived: Dict[int, str] = {}
    next_index = 1
    newest_line_index = -1  # Track newest line for green highlighting

    with Live(_render_lines(lines, 0, total, 0, newest_line_index), refresh_per_second=20) as live:
        # Process tasks as they complete
        pending_tasks = set(tasks)
        done_set: set = set()

        while len(done_set) < total:
            # Wait for next task with a short timeout to allow periodic refreshes
            done, pending_tasks = await asyncio.wait(
                pending_tasks,
                timeout=0.1,
                return_when=asyncio.FIRST_COMPLETED
            )

            # Collect newly completed results
            for finished in done:
                idx, text = finished.result()
                arrived[idx] = text
                done_set.add(idx)

            # Flush any contiguous results starting from next_index
            lines_added = False
            while next_index in arrived:
                lines.append(arrived.pop(next_index))
                if len(lines) > max_lines:
                    lines.popleft()
                # Mark newest as last line in deque
                newest_line_index = len(lines) - 1
                lines_added = True
                next_index += 1

            # Update display on every loop iteration showing progress
            buffered_count = len(arrived)
            completed_count = len(done_set)
            live.update(_render_lines(lines, completed_count, total, buffered_count, newest_line_index))
            live.refresh()


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()


