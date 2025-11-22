"""(Claude) Loader Tasks Demo: Package manager style multi-stage file processing

Requirements:
☑️✅ 6 concurrent file-processing tasks with random stage workflows
☑️✅ Spinner + label + bar + M-of-N + elapsed + status columns
☑️✅ Dynamic status text updates per stage (queued, resolving, fetching, etc.)
☑️✅ File-like labels padded for alignment
☑️✅ Three different stage workflow templates
☑️✅ One random task fails with red error marker
☑️✅ Stage durations randomized but capped at 5s per task
⛔ Out of scope: Actual file I/O, retry logic, cancellation, real package installation

Features:
- Six custom progress columns: Spinner, Label, Bar, M-of-N, Elapsed, Status
- Realistic file labels (dist/app.bundle.js, docker-compose.yml, etc.)
- Labels padded to same width for tidy alignment
- Spinners show activity while task progresses
- Status text updates with current stage name
- One randomly selected task shows "[red]× error[/red]" on completion
- Successful tasks show "[green]• done[/green]"
- Three stage templates: 6 stages each with different progression patterns
- Stage durations: 0.3-1.0s each, normalized to ≤5s total
- Yellow-bordered introduction panel

Technical:
- Asyncio: concurrent task execution with asyncio.gather()
- Rich: Progress with SpinnerColumn, BarColumn, MofNCompleteColumn, TextColumn, TimeElapsedColumn
- Pattern: Package manager style file processing (like npm, uv)
- Task fields: label and status for dynamic text display
- Error simulation: random.randrange() selects one task to fail
- Stage workflows: queued→resolving→fetching→installing→linking→finalizing (and variants)

Run: uv run loader-tasks
"""
from __future__ import annotations

import asyncio
import random
from typing import List, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)


def _build_stages() -> List[str]:
    sets = [
        ["queued", "resolving", "fetching", "installing", "linking", "finalizing"],
        ["ready", "configuring", "building", "starting", "seeding", "warming"],
        ["queued", "pulling", "extracting", "preparing", "starting", "warming"],
    ]
    return random.choice(sets)


def _durations_for(n: int) -> List[float]:
    # Random durations summing to <= 5 s
    weights = [random.uniform(0.3, 1.0) for _ in range(n)]
    total = sum(weights)
    scale = min(5.0 / total, 1.0)
    return [w * scale for w in weights]


async def _run_task(progress: Progress, task_id: int, stages: List[str]) -> None:
    durations = _durations_for(len(stages))
    for i, (stage, dur) in enumerate(zip(stages, durations, strict=True), start=1):
        progress.update(task_id, advance=1, status=f"{stage}")
        await asyncio.sleep(dur)
    # Complete
    progress.update(task_id, status="[green]• done[/green]")


async def main_async() -> None:
    console = Console()

    console.print(Panel.fit(
        "[bold yellow]Example 13: Loader Tasks[/bold yellow]\n\n"
        "This script demonstrates:\n"
        "• Multi-stage file processing\n"
        "• Spinners with status updates\n"
        "• Error handling (one random failure)",
        border_style="yellow"
    ))

    num = 6
    # Example labels (file-like), padded to same width for alignment
    base_labels = [
        "dist/app.bundle.js",
        "docker-compose.yml",
        "config/settings.json",
        "assets/images sprite.png",
        "README.md",
        "scripts/build.sh",
    ]
    labels = (base_labels * ((num + len(base_labels) - 1) // len(base_labels)))[:num]
    pad = max(len(s) for s in labels)
    padded: List[str] = [f"{s:<{pad}}" for s in labels]

    # Randomly choose one task to fail
    error_index = random.randrange(num)

    # Spinner + label + bar + N-of-M + elapsed + current status text
    with Progress(
        SpinnerColumn(),
        TextColumn("{task.fields[label]}", justify="left"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TextColumn(" • {task.fields[status]}", justify="left"),
    ) as progress:
        task_ids: List[Tuple[int, List[str]]] = []
        for i in range(num):
            stages = _build_stages()
            task_id = progress.add_task(
                description=stages[0],
                total=len(stages),
                status=stages[0],
                label=padded[i],
                visible=True,
            )
            task_ids.append((task_id, stages))

        # Run tasks concurrently; apply error styling to one at completion
        async def runner(idx: int, tid: int, stages: List[str]) -> None:
            await _run_task(progress, tid, stages)
            if idx == error_index:
                progress.update(tid, status="[red]× error[/red]")

        await asyncio.gather(*[runner(i, tid, stages) for i, (tid, stages) in enumerate(task_ids)])


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()


