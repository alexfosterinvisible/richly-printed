"""(Claude) Transient Summary Demo: Self-compacting live output that replaces with summary

Requirements:
☑️✅ Live panel showing streaming log entries
☑️✅ Panel disappears when complete (transient=True)
☑️✅ Final summary replaces verbose logs
☑️✅ Async slot reservation for ordered updates
☑️✅ Simulated processing with "Analyzing..." placeholders
⛔ Out of scope: Real LLM calls, actual agent integration

Features:
- Live panel with blue border titled "Processing Logs"
- Each log entry starts as "• Analyzing..." placeholder
- Slots fill in asynchronously but maintain visual order
- Panel uses transient=True so it vanishes when done
- Final green summary prints after panel disappears
- Simulates agent/LLM workflow with mock processing
- 10 fps refresh rate for smooth updates

Use Case:
- Show verbose progress during execution
- Replace with concise summary when complete
- Keeps terminal clean while still showing live feedback
- Perfect for agent workflows, batch processing, CI/CD output

Technical:
- Asyncio: slot reservation pattern with asyncio.create_task()
- Rich: Live (transient=True), Panel, Group, Text, Markdown
- Pattern: Self-compacting stdout / transient verbose logs
- Slot mechanism: Reserve index immediately, fill asynchronously
- Summary: Generated after Live context exits

Run: uv run transient-summary
"""
from __future__ import annotations

import asyncio
import random
from typing import List

from rich.console import Group
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint


# Mock messages simulating agent/LLM responses
MOCK_MESSAGES = [
    "Initializing workspace and loading configuration files...",
    "Reading project structure from ./src directory...",
    "Analyzing dependencies in pyproject.toml...",
    "Executing validation script: python -m pytest tests/",
    "Processing test results: 12 passed, 0 failed",
    "Generating coverage report...",
    "Writing summary to ./reports/coverage.md",
    "Cleanup: removing temporary files",
]


async def mock_summarize(text: str) -> str:
    """Simulate LLM summarization with random delay."""
    await asyncio.sleep(random.uniform(0.2, 0.8))
    
    # Simple mock summaries based on content
    if "Initializing" in text:
        return "SystemMessage(init): tools: Read, Write, Bash"
    elif "Reading" in text:
        return "AssistantMessage: Scanning project structure..."
    elif "dependencies" in text:
        return "AssistantMessage: Found 4 dependencies in pyproject.toml"
    elif "pytest" in text:
        return "AssistantMessage: Running test suite..."
    elif "passed" in text:
        return "Result: ✓ All tests passed (12/12)"
    elif "coverage" in text:
        return "AssistantMessage: Generating coverage metrics..."
    elif "Writing" in text:
        return "AssistantMessage: Saved report to ./reports/"
    elif "Cleanup" in text:
        return "Result: ----cleanup complete----"
    else:
        return f"AssistantMessage: \"{text[:50]}...\""


async def mock_final_summary(logs: str) -> str:
    """Simulate final summary generation."""
    await asyncio.sleep(0.3)
    return (
        "All tests passed (12/12). Coverage report saved to ./reports/coverage.md.\n"
        "- Scanned project structure\n"
        "- Validated dependencies\n"
        "- Ran pytest suite\n"
        "- Generated coverage report\n"
        "- Cleaned up temp files"
    )


async def transient_agent_stream(messages: List[str]) -> None:
    """Process messages in a transient Live panel that disappears when done.
    
    Pattern:
    1. Reserve a slot immediately (maintains visual order)
    2. Spawn background task to fill that slot
    3. Wait for all tasks before closing
    4. Panel vanishes, summary prints
    """
    log_items: list = []
    tasks: list = []
    summary_texts: list[str] = []

    def get_panel():
        return Panel(
            Group(*log_items), 
            title="Processing Logs", 
            border_style="blue", 
            padding=(1, 2)
        )

    with Live(get_panel(), refresh_per_second=10, transient=True) as live:
        
        async def update_slot(index: int, msg: str):
            """Update a specific slot with summarized content."""
            summary = await mock_summarize(msg)
            log_items[index] = Markdown(summary)
            # Store for final summary
            while len(summary_texts) <= index:
                summary_texts.append("")
            summary_texts[index] = summary
            live.update(get_panel())

        # Simulate receiving messages with delays
        for msg in messages:
            await asyncio.sleep(random.uniform(0.1, 0.3))
            
            # 1. Reserve slot immediately with placeholder
            log_items.append(Text("• Analyzing...", style="dim italic"))
            summary_texts.append("")
            live.update(get_panel())

            # 2. Spawn background task for this slot
            task = asyncio.create_task(update_slot(len(log_items) - 1, msg))
            tasks.append(task)

        # 3. Wait for all summaries before panel closes
        if tasks:
            await asyncio.gather(*tasks)

    # 4. Panel gone - print final summary
    if summary_texts:
        full_log = "\n".join(summary_texts)
        final_summary = await mock_final_summary(full_log)
        rprint(f"\n[green]{final_summary}[/green]\n")


async def main_async() -> None:
    """Run the transient summary demo."""
    rprint(Panel.fit(
        "[bold blue]Example 19: Transient Summary[/bold blue]\n\n"
        "This script demonstrates:\n"
        "• Live panel with transient=True\n"
        "• Self-compacting verbose output\n"
        "• Final summary replaces logs",
        border_style="blue"
    ))
    
    rprint("\n[yellow]Starting batch processing...[/yellow]\n")
    
    await transient_agent_stream(MOCK_MESSAGES)
    
    rprint("[dim]Panel disappeared, only summary remains above.[/dim]")


def main() -> None:
    """Entry point."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()

