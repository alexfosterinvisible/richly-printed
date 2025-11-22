"""(Claude) Streaming Loader Tasks Demo: UV sync style irregular spawn with auto-cleanup

Requirements:
☑️✅ 18 tasks spawning irregularly (30-180ms intervals)
☑️✅ Successful tasks auto-remove after 200ms green dot display
☑️✅ Failed tasks persist with red × marker
☑️✅ Random 1-in-8 failure rate
☑️✅ Multi-stage workflow (6 stages per task, randomized templates)
☑️✅ Stage durations: 0.2-0.9s each, capped at 3.5s total per task
☑️✅ Two-line summary at completion: successes and failures
⛔ Out of scope: Real package installation, dependency resolution, network I/O

Features:
- UV sync style irregular task spawning (like uv add/sync behavior)
- Six progress columns: Spinner, Label, Bar, M-of-N, Elapsed, Status
- File-like labels padded for alignment (8 unique labels cycled)
- Successful tasks: show "[green]• done[/green]" for 200ms, then removed
- Failed tasks: show "[red]× error[/red]" and remain visible
- Random error selection: 1-in-8 tasks fail (max 1, ~12% failure rate)
- Three stage templates with 6 stages each
- Spawn interval: 30-180ms between task starts (fast like uv)
- Summary: "X succeeded, Y failed" with error warning if any failed
- Yellow-bordered introduction panel

Technical:
- Asyncio: staggered task spawning with random delays
- Rich: Progress with transient=False (required for task removal)
- Pattern: Streaming package manager (uv sync, npm install style)
- Progress API: progress.remove_task() for auto-cleanup
- Error tracking: success_count and error_count arrays (mutable refs)
- Spawn pattern: 18 tasks × 30-180ms = ~1-3s spawn window
- Total runtime: ~4-7s (spawn window + longest task duration)

Run: uv run loader-tasks-stream
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
    # Random durations summing to <= 3.5 s to keep it snappy
    weights = [random.uniform(0.2, 0.9) for _ in range(n)]
    total = sum(weights)
    scale = min(3.5 / total, 1.0)
    return [w * scale for w in weights]


async def _run_one(progress: Progress, task_id: int, stages: List[str], is_error: bool, counters) -> None:
    nonlocal_success, nonlocal_error = counters
    durations = _durations_for(len(stages))
    for stage, dur in zip(stages, durations, strict=True):
        progress.update(task_id, advance=1, status=stage)
        await asyncio.sleep(dur)
    if is_error:
        progress.update(task_id, status="[red]× error[/red]")
        nonlocal_error[0] += 1
        # Keep error visible
    else:
        progress.update(task_id, status="[green]• done[/green]")
        nonlocal_success[0] += 1
        # Briefly show success, then remove
        await asyncio.sleep(0.2)
        try:
            progress.remove_task(task_id)
        except Exception:
            pass


async def main_async() -> None:
    console = Console()

    console.print(Panel.fit(
        "[bold yellow]Example 14: Streaming Loader Tasks[/bold yellow]\n\n"
        "This script demonstrates:\n"
        "• Irregular task spawning (like uv sync)\n"
        "• Auto-removal of successful tasks\n"
        "• Persistent error display",
        border_style="yellow"
    ))

    num = 18

    # File-like labels, padded to same width for tidy left column
    base_labels = [
        "dist/app.bundle.js",
        "docker-compose.yml",
        "config/settings.json",
        "assets/images sprite.png",
        "README.md",
        "scripts/build.sh",
        "src/index.ts",
        "pyproject.toml",
    ]
    labels = (base_labels * ((num + len(base_labels) - 1) // len(base_labels)))[:num]
    pad = max(len(s) for s in labels)
    padded: List[str] = [f"{s:<{pad}}" for s in labels]

    # Random set of error indices (small fraction)
    error_indices = set(random.sample(range(num), k=max(1, num // 8)))
    success_count = [0]
    error_count = [0]

    with Progress(
        SpinnerColumn(),
        TextColumn("{task.fields[label]}", justify="left"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TextColumn(" • {task.fields[status]}", justify="left"),
        transient=False,
    ) as progress:
        runners: List[asyncio.Task[None]] = []
        for i in range(num):
            stages = _build_stages()
            tid = progress.add_task(
                description=stages[0],
                total=len(stages),
                status=stages[0],
                label=padded[i],
                visible=True,
            )
            runner = asyncio.create_task(
                _run_one(progress, tid, stages, is_error=(i in error_indices), counters=(success_count, error_count))
            )
            runners.append(runner)
            # Irregular spawn cadence, quick like uv: 30–180 ms between spawns
            await asyncio.sleep(random.uniform(0.03, 0.18))

        # Wait for all to finish
        await asyncio.gather(*runners, return_exceptions=False)

    # Minimal 2-line summary
    console.print(f"[bold]Summary[/bold]: {success_count[0]} succeeded, {error_count[0]} failed")
    if error_count[0]:
        console.print("[red]One or more tasks ended with errors[/red]")


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()








