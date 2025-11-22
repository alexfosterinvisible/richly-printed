"""(Claude) Live Logs Demo: Streaming log aggregation with automatic rotation

Requirements:
☑️✅ 3 concurrent worker tasks producing log events
☑️✅ Automatic log rotation (max 12 lines displayed)
☑️✅ Shared deque for thread-safe log aggregation
☑️✅ Random event timing (0.3-1.2s intervals)
☑️✅ 5 events per worker (15 total events)
☑️✅ Live panel updates at 10 fps
☑️✅ Fitted panel auto-sizing to content
⛔ Out of scope: Log levels, filtering, persistence, timestamps

Features:
- Panel.fit automatically sizes to log content
- Cyan-bordered panel titled "Live Logs"
- 3 workers named "worker-1", "worker-2", "worker-3"
- Each worker produces 5 events with format "worker-N: event M"
- Random delays 0.3-1.2s between events
- Deque with maxlen=12 for automatic old log removal
- Live updates every 0.1s at 10 fps
- Cyan-bordered introduction panel

Technical:
- Asyncio: concurrent producer tasks with random delays
- Collections: deque(maxlen=12) for automatic rotation
- Rich: Console, Live, Panel, Text
- Pattern: Multi-producer log aggregation
- Update cycle: 0.1s polling with 10 fps refresh
- Total runtime: ~3-6s depending on random delays

Run: uv run live-logs
"""
from __future__ import annotations

import asyncio
import random
from collections import deque
from typing import Deque

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text


def _render_logs(lines: Deque[str]) -> Panel:
    content = "\n".join(lines)
    return Panel.fit(Text(content), title="Live Logs", border_style="cyan")


async def _producer(name: str, lines: Deque[str]) -> None:
    for i in range(1, 6):
        await asyncio.sleep(random.uniform(0.3, 1.2))
        lines.append(f"{name}: event {i}")
        if len(lines) > 12:
            lines.popleft()


async def main_async() -> None:
    console = Console()

    console.print(Panel.fit(
        "[bold cyan]Example 9A: Live Logs[/bold cyan]\n\n"
        "This script demonstrates:\n"
        "• Streaming log lines from workers\n"
        "• Automatic log rotation (max lines)\n"
        "• Real-time panel updates",
        border_style="cyan"
    ))

    lines: Deque[str] = deque()
    prods = [asyncio.create_task(_producer(f"worker-{i+1}", lines)) for i in range(3)]
    with Live(_render_logs(lines), refresh_per_second=10) as live:
        while any(not p.done() for p in prods):
            await asyncio.sleep(0.1)
            live.update(_render_logs(lines))


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()


