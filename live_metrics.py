"""(Claude) Live Metrics Demo: Real-time monitoring dashboard with color-coded panels

Requirements:
☑️✅ Three-column metrics layout (RPS, Errors, Latency)
☑️✅ Simulated metrics with random fluctuations
☑️✅ Color-coded panels by metric type
☑️✅ 60 iterations at 0.2s intervals (~12s runtime)
☑️✅ 8 fps refresh rate for smooth updates
☑️✅ Realistic metric patterns (RPS drift, occasional errors, latency variance)
⛔ Out of scope: Real data sources, alerting, history graphs, percentile tracking

Features:
- Three side-by-side panels in Columns layout
- RPS panel: green border, tracks requests per second (-5 to +10 drift)
- Errors panel: red border, occasional increments (10% chance per tick)
- Latency panel: yellow border, p95 latency in ms (±10ms variance)
- Starting values: RPS=0, Errors=0, Latency=120ms
- Minimum bounds: RPS≥0, Latency≥60ms
- 60 update cycles × 0.2s = 12s total runtime
- Yellow-bordered introduction panel

Technical:
- Asyncio: async/await for update loop timing
- Rich: Console, Columns, Live, Panel
- Random: random.randint() for realistic metric fluctuations
- Pattern: Multi-metric monitoring dashboard
- Update rate: 0.2s per cycle with 8 fps refresh
- Bounds checking: max(0, value) for RPS, max(60, value) for latency

Run: uv run live-metrics
"""
from __future__ import annotations

import asyncio
import random
from rich.console import Console
from rich.columns import Columns
from rich.live import Live
from rich.panel import Panel


def _render(rps: int, errors: int, latency_ms: int) -> Columns:
    return Columns(
        [
            Panel(f"[bold]RPS[/bold]\n{rps}", border_style="green"),
            Panel(f"[bold]Errors[/bold]\n{errors}", border_style="red"),
            Panel(f"[bold]p95 latency[/bold]\n{latency_ms} ms", border_style="yellow"),
        ]
    )


async def main_async() -> None:
    console = Console()

    console.print(Panel.fit(
        "[bold yellow]Example 11: Live Metrics[/bold yellow]\n\n"
        "This script demonstrates:\n"
        "• Real-time metrics monitoring\n"
        "• Simulated RPS, errors, latency\n"
        "• Color-coded metric panels",
        border_style="yellow"
    ))

    rps, errors, latency = 0, 0, 120
    with Live(_render(rps, errors, latency), refresh_per_second=8) as live:
        for _ in range(60):
            await asyncio.sleep(0.2)
            rps = max(0, rps + random.randint(-5, 10))
            if random.random() < 0.1:
                errors += random.randint(0, 2)
            latency = max(60, latency + random.randint(-10, 10))
            live.update(_render(rps, errors, latency))


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()


