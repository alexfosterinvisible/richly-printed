"""(Claude) Agent Dashboard: Production-grade multi-panel monitoring with resource tracking

Requirements:
☑️✅ 6 concurrent agents with full lifecycle (starting→running→idle→completed)
☑️✅ Two-column layout with 4 panels (agents, progress, events, traces)
☑️✅ Real-time CPU and RAM monitoring with color-coded warnings
☑️✅ Live table sorting by CPU usage (descending)
☑️✅ Progress bars for all agents with percentage display
☑️✅ Event log with timestamps (HH:MM:SS format)
☑️✅ Debug trace log with millisecond precision (HH:MM:SS.mmm)
☑️✅ Resource-based styling (red: CPU>70% or RAM>800MB, yellow: CPU>40% or RAM>500MB, green: normal)
☑️✅ Staggered agent starts (0.3-0.8s delays)
☑️✅ CPU bursts (60-95%) and idle periods (1-5%)
⛔ Out of scope: Real system monitoring, process management, alerts, data persistence

Features:
- Four-panel layout in 2 columns: left (agents table, progress bars), right (events, traces)
- Agent table: sorted by CPU descending, columns: Agent, Status, CPU%, RAM, Progress
- Status color coding: yellow=starting, green=running, blue=idle, dim=completed
- Resource warnings: red for high usage, yellow for medium, green for normal
- Progress bars: custom bars with █/░ characters plus percentage
- Progress panel: standard Rich progress bars with percentage display
- Events panel: 5 most recent events with HH:MM:SS timestamps
- Traces panel: 12 most recent debug traces with millisecond timestamps
- Agent lifecycle: starting (0.3-0.8s) → running (3-7s with bursts) → completed
- CPU bursts: 30% chance per tick to spike to 60-95%, otherwise 10-45%
- Idle transitions: 15% chance per tick to pause for I/O (0.2-0.5s)
- Random debug messages: 40% per tick (processing, validating, fetching, etc.)
- System traces: 30% per tick (memory, queue depth, network, disk I/O)
- 6 agents: agent-alpha through agent-zeta
- 10 fps refresh rate for smooth updates
- ~10-15s total runtime depending on agent durations

Technical:
- Asyncio: staggered concurrent agent lifecycles
- Rich: Layout (2-column with nested splits), Live, Panel, Table, Progress, Text, Style
- Dataclass: Agent with status, cpu_percent, ram_mb, task_progress, started_at
- Pattern: Production monitoring dashboard with resource tracking
- Layout: split_row(left 3:2 right), left.split_column(agents 2:1 progress), right.split_column(events 1:2 traces)
- Globals: AGENTS list, EVENTS deque(maxlen=5), TRACES deque(maxlen=12), PROGRESS_TASKS dict
- Resource styling: _get_resource_style() returns Style based on thresholds
- Sorting: sorted(AGENTS, key=lambda a: a.cpu_percent, reverse=True)
- Event logging: _log_event() with time.strftime("%H:%M:%S")
- Trace logging: _log_trace() with time.strftime("%H:%M:%S.%f")[:-3]
- Update cycle: 0.1s polling with 10 fps refresh
- Panel padding: (0,1) for compact display

Run: uv run agent-dashboard
"""
from __future__ import annotations

import asyncio
import random
import time
from collections import deque
from dataclasses import dataclass
from typing import Deque, List

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TaskID, TextColumn
from rich.style import Style
from rich.table import Table
from rich.text import Text


@dataclass
class Agent:
    """Agent with resource tracking."""

    name: str
    status: str  # "starting", "running", "idle", "completed"
    cpu_percent: float
    ram_mb: int
    task_progress: float  # 0-100
    started_at: float


# Globals for tracking
AGENTS: List[Agent] = []
EVENTS: Deque[str] = deque(maxlen=5)
TRACES: Deque[str] = deque(maxlen=12)
PROGRESS_TASKS: dict[str, TaskID] = {}


def _get_resource_style(cpu: float, ram: int) -> Style:
    """Color code based on resource usage."""
    if cpu > 70 or ram > 800:
        return Style(color="red", bold=True)
    elif cpu > 40 or ram > 500:
        return Style(color="yellow")
    else:
        return Style(color="green")


def _render_agents_table() -> Panel:
    """Render agent status table, sorted by resource usage."""
    table = Table(show_header=True, header_style="bold cyan", expand=True, padding=(0,1), box=None)
    table.add_column("Agent", style="cyan", no_wrap=True, min_width=13, max_width=15)
    table.add_column("Status", no_wrap=True, min_width=9, max_width=11)
    table.add_column("CPU%", justify="right", no_wrap=True, min_width=5, max_width=6)
    table.add_column("RAM", justify="right", no_wrap=True, min_width=4, max_width=6)
    table.add_column("Progress", no_wrap=True, min_width=12)

    # Sort by CPU usage descending
    sorted_agents = sorted(AGENTS, key=lambda a: a.cpu_percent, reverse=True)

    for agent in sorted_agents:
        style = _get_resource_style(agent.cpu_percent, agent.ram_mb)

        # Status with color
        status_colors = {
            "starting": "yellow",
            "running": "green",
            "idle": "blue",
            "completed": "dim",
        }
        status_text = Text(agent.status, style=status_colors.get(agent.status, "white"))

        # CPU and RAM with color coding
        cpu_text = Text(f"{agent.cpu_percent:.1f}", style=style)
        ram_text = Text(f"{agent.ram_mb}", style=style)

        # Progress bar
        if agent.status == "completed":
            progress_text = "✓ done"
        elif agent.status == "starting":
            progress_text = "..."
        else:
            bar_width = 8
            filled = int((agent.task_progress / 100) * bar_width)
            bar = "█" * filled + "░" * (bar_width - filled)
            progress_text = f"{bar} {agent.task_progress:.0f}%"

        table.add_row(agent.name, status_text, cpu_text, ram_text, progress_text)

    return Panel(table, title="[bold cyan]Agent Monitor[/bold cyan]", border_style="cyan", padding=(0,1))


def _render_events() -> Panel:
    """Render recent events."""
    content = "\n".join(EVENTS) if EVENTS else "[dim]No events yet[/dim]"
    return Panel(content, title="[bold yellow]Events[/bold yellow]", border_style="yellow", padding=(0,1))


def _render_traces() -> Panel:
    """Render debug trace log."""
    content = "\n".join(TRACES) if TRACES else "[dim]No traces yet[/dim]"
    return Panel(content, title="[bold magenta]Debug Traces[/bold magenta]", border_style="magenta", padding=(0,1))


def _render_progress_bars(progress: Progress) -> Panel:
    """Render progress bars for active tasks."""
    return Panel(progress, title="[bold green]Active Tasks[/bold green]", border_style="green", padding=(0,1))


def _build_layout(progress: Progress) -> Layout:
    """Build two-column dashboard layout."""
    layout = Layout(name="root")

    # Split into left and right columns with better ratios
    layout.split_row(
        Layout(name="left", ratio=3),
        Layout(name="right", ratio=2),
    )

    # Left column: agents table + progress bars
    layout["left"].split_column(
        Layout(name="agents", ratio=2),
        Layout(name="progress", ratio=1),
    )

    # Right column: events + traces (more compact)
    layout["right"].split_column(
        Layout(name="events", ratio=1),
        Layout(name="traces", ratio=2),
    )

    # Initial render
    layout["agents"].update(_render_agents_table())
    layout["progress"].update(_render_progress_bars(progress))
    layout["events"].update(_render_events())
    layout["traces"].update(_render_traces())

    return layout


def _log_event(msg: str) -> None:
    """Add event to log."""
    timestamp = time.strftime("%H:%M:%S")
    EVENTS.append(f"[dim]{timestamp}[/dim] {msg}")


def _log_trace(msg: str) -> None:
    """Add trace to debug log."""
    timestamp = time.strftime("%H:%M:%S.%f")[:-3]
    TRACES.append(f"[dim]{timestamp}[/dim] {msg}")


async def _simulate_agent(agent: Agent, progress: Progress, task_id: TaskID) -> None:
    """Simulate agent lifecycle with resource usage."""
    # Starting phase
    agent.status = "starting"
    _log_event(f"[yellow]Agent {agent.name} starting...[/yellow]")
    _log_trace(f"DEBUG: {agent.name} initializing workspace")
    await asyncio.sleep(random.uniform(0.3, 0.8))

    # Running phase
    agent.status = "running"
    _log_event(f"[green]Agent {agent.name} running[/green]")
    _log_trace(f"DEBUG: {agent.name} connected to task queue")

    # Simulate work with varying resource usage
    duration = random.uniform(3, 7)
    steps = 20
    for i in range(steps):
        # Update progress
        agent.task_progress = (i / steps) * 100
        progress.update(task_id, completed=agent.task_progress)

        # Vary resource usage (simulate bursts)
        if random.random() < 0.3:  # Burst
            agent.cpu_percent = random.uniform(60, 95)
            agent.ram_mb = random.randint(600, 1000)
            _log_trace(f"DEBUG: {agent.name} high CPU burst processing data")
        else:  # Normal
            agent.cpu_percent = random.uniform(10, 45)
            agent.ram_mb = random.randint(200, 600)

        # Occasional idle
        if random.random() < 0.15:
            agent.status = "idle"
            agent.cpu_percent = random.uniform(1, 5)
            _log_trace(f"DEBUG: {agent.name} waiting for I/O")
            await asyncio.sleep(random.uniform(0.2, 0.5))
            agent.status = "running"
        else:
            await asyncio.sleep(duration / steps)

        # Random debug traces
        if random.random() < 0.4:
            actions = [
                "processing batch",
                "validating output",
                "fetching context",
                "compiling results",
                "checkpoint saved",
            ]
            _log_trace(f"DEBUG: {agent.name} {random.choice(actions)}")

    # Completion
    agent.status = "completed"
    agent.cpu_percent = 0
    agent.ram_mb = 50
    agent.task_progress = 100
    progress.update(task_id, completed=100)
    _log_event(f"[green]✓ Agent {agent.name} completed[/green]")
    _log_trace(f"DEBUG: {agent.name} cleanup finished")


async def main_async() -> None:
    """Main dashboard loop."""
    console = Console()

    console.print(Panel.fit(
        "[bold bright_cyan]Example 18: Agent Dashboard[/bold bright_cyan]\n\n"
        "This script demonstrates:\n"
        "• Complex multi-panel monitoring\n"
        "• Resource tracking with color coding\n"
        "• Live sorting and event logs",
        border_style="bright_cyan"
    ))

    # Initialize agents
    agent_names = [
        "agent-alpha",
        "agent-beta",
        "agent-gamma",
        "agent-delta",
        "agent-epsilon",
        "agent-zeta",
    ]

    for name in agent_names:
        agent = Agent(
            name=name,
            status="starting",
            cpu_percent=0.0,
            ram_mb=100,
            task_progress=0.0,
            started_at=time.time(),
        )
        AGENTS.append(agent)

    # Create progress bars
    progress = Progress(
        TextColumn("[bold]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )

    for agent in AGENTS:
        task_id = progress.add_task(agent.name, total=100)
        PROGRESS_TASKS[agent.name] = task_id

    # Build layout
    layout = _build_layout(progress)

    # Start live dashboard
    with Live(layout, refresh_per_second=10, screen=False) as live:
        # Stagger agent starts
        tasks = []
        for agent in AGENTS:
            task_id = PROGRESS_TASKS[agent.name]
            task = asyncio.create_task(_simulate_agent(agent, progress, task_id))
            tasks.append(task)
            await asyncio.sleep(random.uniform(0.3, 0.8))  # Stagger starts

            # Update dashboard
            layout["agents"].update(_render_agents_table())
            layout["progress"].update(_render_progress_bars(progress))
            layout["events"].update(_render_events())
            layout["traces"].update(_render_traces())

        # Continuous updates while agents run
        while any(not t.done() for t in tasks):
            await asyncio.sleep(0.1)

            # Update all panels
            layout["agents"].update(_render_agents_table())
            layout["progress"].update(_render_progress_bars(progress))
            layout["events"].update(_render_events())
            layout["traces"].update(_render_traces())

            # Add random system traces
            if random.random() < 0.3:
                system_traces = [
                    "SYSTEM: memory pressure normal",
                    "SYSTEM: task queue depth: 3",
                    "SYSTEM: network latency 45ms",
                    "SYSTEM: disk I/O within limits",
                ]
                _log_trace(random.choice(system_traces))

        # Final update
        layout["agents"].update(_render_agents_table())
        layout["progress"].update(_render_progress_bars(progress))
        layout["events"].update(_render_events())
        layout["traces"].update(_render_traces())

        # Brief pause to show final state
        await asyncio.sleep(1)

    _log_event("[bold green]All agents completed successfully[/bold green]")


def main() -> None:
    """Entry point."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
