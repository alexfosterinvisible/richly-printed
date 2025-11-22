"""(Claude) Live Tasks Demo: Multi-stage task progression with spinners and elapsed time

Requirements:
☑️✅ 8 concurrent tasks with randomized multi-stage workflows
☑️✅ Spinners showing current stage for running tasks
☑️✅ Elapsed time displayed only on completion
☑️✅ 6-7 stage workflow variations (queued, resolving, fetching, installing, etc.)
☑️✅ Stage durations randomized but capped at 5s total per task
☑️✅ Live table updating at 10 fps
☑️✅ Tasks complete asynchronously in random order
⛔ Out of scope: Progress bars within stages, task cancellation, error states

Features:
- Table with columns: #, Task, Stage, Elapsed
- Three different stage workflow patterns randomly assigned
- Spinner with current stage text for running tasks
- "done" status on completion with elapsed seconds (X.XXs format)
- 8 tasks named "job-1" through "job-8"
- Stage durations: 0.3-1.0s each, normalized to max 5s total
- Live updates at 10 fps for smooth spinner animation
- Cyan-bordered introduction panel

Technical:
- Asyncio: concurrent task execution with create_task()
- Rich: Console, Panel, Table, Spinner (dots style)
- Dataclass: TaskInfo for state management
- Pattern: Multi-stage async workflows with visual progress
- Timing: time.perf_counter() for precise elapsed time
- Stage pools: 3 different workflow templates with 6-7 stages each

Run: uv run live-tasks
"""
from __future__ import annotations

import asyncio
import random
import time
from dataclasses import dataclass, field
from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live
from rich.table import Table


@dataclass
class TaskInfo:
    name: str
    stages: List[str]
    stage_durations: List[float]
    stage_index: int = 0
    started_at: Optional[float] = None
    elapsed_s: Optional[float] = None


def _render_table(tasks: List[TaskInfo]) -> Table:
    table = Table(title="Live Tasks")
    table.add_column("#", style="cyan")
    table.add_column("Task", style="magenta")
    table.add_column("Stage", style="yellow")
    table.add_column("Elapsed", style="green")
    for i, t in enumerate(tasks, start=1):
        if t.stage_index >= len(t.stages):
            # Done
            stage_cell = "done"
            elapsed_cell = f"{t.elapsed_s:.2f}s" if t.elapsed_s is not None else "-"
        else:
            # Running: show spinner + current stage; elapsed blank until done
            current_stage = t.stages[t.stage_index]
            stage_cell = Spinner("dots", text=f" {current_stage}")
            elapsed_cell = ""
        table.add_row(str(i), t.name, stage_cell, elapsed_cell)
    return table


def _now() -> float:
    return time.perf_counter()


def _plan_stages() -> tuple[list[str], list[float]]:
    # 6–7 stages with different starting labels; total <= 5s
    stage_pool = [
        ["queued", "pulling", "starting", "migrating", "warming", "ready", "done"],
        ["ready", "configuring", "building", "starting", "seeding", "warming", "done"],
        ["queued", "resolving", "fetching", "installing", "linking", "finalizing", "done"],
    ]
    stages = random.choice(stage_pool)
    # Number of actual running stages excludes final "done" which we set when finished
    run_count = len(stages) - 1
    # Random weights, normalize to at most 5s total
    weights = [random.uniform(0.3, 1.0) for _ in range(run_count)]
    total = sum(weights)
    scale = min(5.0 / total, 1.0)
    durations = [w * scale for w in weights]
    return stages, durations


async def _task_run(t: TaskInfo) -> None:
    t.started_at = _now()
    # Progress through all stages except the terminal "done"
    for _idx, delay in enumerate(t.stage_durations):
        await asyncio.sleep(delay)
        t.stage_index += 1
    # Mark as done
    t.stage_index = len(t.stages)  # past last index
    t.elapsed_s = _now() - (t.started_at or _now())


async def main_async() -> None:
    console = Console()

    console.print(Panel.fit(
        "[bold cyan]Example 8: Live Tasks[/bold cyan]\n\n"
        "This script demonstrates:\n"
        "• Multi-stage task progression\n"
        "• Spinners for running tasks\n"
        "• Elapsed time tracking on completion",
        border_style="cyan"
    ))

    num = 8
    jobs: List[TaskInfo] = []
    for i in range(num):
        stages, durations = _plan_stages()
        jobs.append(TaskInfo(name=f"job-{i+1}", stages=stages, stage_durations=durations))

    running = [asyncio.create_task(_task_run(t)) for t in jobs]
    with Live(_render_table(jobs), refresh_per_second=10) as live:
        # Periodically refresh until all tasks done
        while any(not c.done() for c in running):
            await asyncio.sleep(0.1)
            live.update(_render_table(jobs))
        # Final refresh to show completed elapsed
        live.update(_render_table(jobs))


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()


