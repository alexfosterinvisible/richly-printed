"""(Claude) Live Coding Agents Dashboard: Pipeline simulation with loop-back workflow

Requirements:
☑️✅ 6-8 concurrent agents progressing through 7-stage pipeline
☑️✅ Visual pipeline representation (Plan → Build → Test → Fix → Review → Fix → PR)
☑️✅ Test stage loop-back to Fix (40% chance, max 2 loops per agent)
☑️✅ Multi-panel layout: pipeline visual, agent table, stats panel
☑️✅ Color-coded stages with progress bars per agent
☑️✅ Stage distribution tracking and elapsed time
☑️✅ Staggered agent starts (0-300ms delays)
☑️✅ 10 fps refresh rate for smooth updates
⛔ Out of scope: Real code execution, Git integration, actual testing, error handling

Features:
- Three-panel layout: pipeline visualization, agent status table, statistics
- 7-stage pipeline with color coding (cyan→blue→yellow→magenta→green→magenta→bright_green)
- Pipeline visual shows all stages with arrows (Stage1 → Stage2 → ...)
- Agent table columns: Agent, Stage, Progress (bar), Time, Loops
- Progress bars use block characters (█ filled, ░ empty) with percentage
- Loop-back mechanism: Test stage has 40% chance to return to Fix (up to 2 times)
- Stats panel: completed count, in-progress count, elapsed time, stage distribution
- Random stage durations: 0.5-2.0s per stage
- 6-8 agents (random count) starting from Plan stage
- Agents complete asynchronously and independently
- Loops counter tracks how many times agent returned to Fix

Technical:
- Asyncio: concurrent agent simulation with staggered starts
- Rich: Live, Panel, Table, Progress, Columns, Group, Text
- Dataclass: CodingAgent for state (stage, progress, time, loops, completed)
- Pattern: Multi-agent pipeline simulation with conditional branching
- Rendering: _render() returns Group of panels for clean updates
- Stage tracking: STAGES list with (name, color) tuples
- Loop logic: 40% probability at Test stage if loops < 2
- Total runtime: ~8-10s depending on random durations and loops

Run: uv run live_dashboard_coding_agents.py
"""

import asyncio
import random
from dataclasses import dataclass
from datetime import datetime
from typing import List

from rich.columns import Columns
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text


# Pipeline stages with colors
STAGES = [
    ("Plan", "cyan"),
    ("Build", "blue"),
    ("Test", "yellow"),
    ("Fix", "magenta"),
    ("Review", "green"),
    ("Fix", "magenta"),
    ("PR", "bright_green"),
]


@dataclass
class CodingAgent:
    """Represents a coding agent working through the pipeline."""

    name: str
    current_stage: int  # Index into STAGES
    progress: float  # 0-100
    time_in_stage: float  # seconds
    loops: int  # Number of times looped back from Test to Fix
    completed: bool = False


def _create_pipeline_visual() -> Table:
    """Create visual representation of the pipeline stages."""
    table = Table.grid(padding=(0, 1))
    table.add_column(justify="center")

    # Build pipeline visual
    pipeline_text = Text()
    for i, (stage, color) in enumerate(STAGES):
        pipeline_text.append(stage, style=f"bold {color}")
        if i < len(STAGES) - 1:
            pipeline_text.append(" → ", style="dim")

    table.add_row(pipeline_text)
    return table


def _create_agent_table(agents: List[CodingAgent], elapsed: float) -> Table:
    """Create table showing all agents and their current status."""
    table = Table(title="Coding Agents", show_header=True, header_style="bold magenta")
    table.add_column("Agent", style="cyan", width=12)
    table.add_column("Stage", justify="center", width=10)
    table.add_column("Progress", width=30)
    table.add_column("Time", justify="right", width=8)
    table.add_column("Loops", justify="center", width=6)

    # Create progress bars for agents
    progress_bars = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=20),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        expand=False,
    )

    for agent in agents:
        if agent.completed:
            stage_name = "✓ Done"
            stage_color = "bright_green"
        else:
            stage_name, stage_color = STAGES[agent.current_stage]

        # Add progress bar for this agent
        task_id = progress_bars.add_task("", total=100, completed=agent.progress)

        # Build progress bar display
        progress_display = Text()
        bar_chars = int(agent.progress / 5)  # 20 chars max
        filled = "█" * bar_chars
        empty = "░" * (20 - bar_chars)
        progress_display.append(filled, style=stage_color)
        progress_display.append(empty, style="dim")
        progress_display.append(f" {agent.progress:.0f}%", style="bold")

        table.add_row(
            agent.name,
            Text(stage_name, style=f"bold {stage_color}"),
            progress_display,
            f"{agent.time_in_stage:.1f}s",
            str(agent.loops) if agent.loops > 0 else "-",
        )

    return table


def _create_stats_panel(agents: List[CodingAgent], elapsed: float) -> Panel:
    """Create statistics panel."""
    completed = sum(1 for a in agents if a.completed)
    total = len(agents)
    in_progress = total - completed

    # Stage distribution
    stage_counts = {}
    for agent in agents:
        if not agent.completed:
            stage_name = STAGES[agent.current_stage][0]
            stage_counts[stage_name] = stage_counts.get(stage_name, 0) + 1

    stage_dist = " | ".join(
        f"{stage}: {count}" for stage, count in sorted(stage_counts.items())
    )

    stats = f"""[bold]Status[/bold]
Completed: [green]{completed}[/green] / {total}
In Progress: [yellow]{in_progress}[/yellow]
Elapsed: [cyan]{elapsed:.1f}s[/cyan]

[bold]Stage Distribution[/bold]
{stage_dist if stage_dist else "All agents completed"}"""

    return Panel(stats, border_style="blue", title="Stats")


def _render(agents: List[CodingAgent], elapsed: float) -> Group:
    """Render the entire dashboard."""
    pipeline = _create_pipeline_visual()
    agent_table = _create_agent_table(agents, elapsed)
    stats = _create_stats_panel(agents, elapsed)

    return Group(
        Panel(pipeline, border_style="bright_blue", title="Pipeline"),
        agent_table,
        stats,
    )


async def _simulate_agent(agent: CodingAgent) -> None:
    """Simulate an agent progressing through the pipeline."""
    while agent.current_stage < len(STAGES):
        # Random duration for this stage (0.5 to 2 seconds)
        stage_duration = random.uniform(0.5, 2.0)
        steps = 20
        step_duration = stage_duration / steps

        # Progress through current stage
        for i in range(steps):
            await asyncio.sleep(step_duration)
            agent.progress = (i + 1) * (100 / steps)
            agent.time_in_stage += step_duration

        # Special logic: Test stage has 40% chance to loop back to Fix
        current_stage_name = STAGES[agent.current_stage][0]
        if current_stage_name == "Test" and random.random() < 0.4 and agent.loops < 2:
            # Loop back to Fix stage (index 3)
            agent.current_stage = 3
            agent.loops += 1
            agent.progress = 0
            agent.time_in_stage = 0
        else:
            # Move to next stage
            agent.current_stage += 1
            agent.progress = 0
            agent.time_in_stage = 0

    # Mark as completed
    agent.completed = True
    agent.progress = 100


async def main_async() -> None:
    """Run the coding agent pipeline simulation."""
    # Create 6-8 agents with different starting points
    num_agents = random.randint(6, 8)
    agents = [
        CodingAgent(
            name=f"Agent-{i+1:02d}",
            current_stage=0,  # All start at Plan
            progress=0,
            time_in_stage=0,
            loops=0,
        )
        for i in range(num_agents)
    ]

    # Stagger agent starts slightly for visual variety
    tasks = []
    for i, agent in enumerate(agents):
        # Add small random delay before starting each agent
        delay = random.uniform(0, 0.3)
        task = asyncio.create_task(_simulate_agent_with_delay(agent, delay))
        tasks.append(task)

    # Run live dashboard
    start_time = asyncio.get_event_loop().time()
    with Live(_render(agents, 0), refresh_per_second=10) as live:
        while not all(a.completed for a in agents):
            await asyncio.sleep(0.1)
            elapsed = asyncio.get_event_loop().time() - start_time
            live.update(_render(agents, elapsed))

        # Final update
        elapsed = asyncio.get_event_loop().time() - start_time
        live.update(_render(agents, elapsed))

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)


async def _simulate_agent_with_delay(agent: CodingAgent, delay: float) -> None:
    """Simulate agent with initial delay."""
    await asyncio.sleep(delay)
    await _simulate_agent(agent)


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
