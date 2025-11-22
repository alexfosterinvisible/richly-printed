"""(Claude) LLM Judge Layout Demo: Parallel evaluation with color-coded input/output tracking

Requirements:
☑️✅ 5 concurrent LLM evaluations with different tones (technical, beginner, academic, casual, concise)
☑️✅ Four-panel layout: question, prompt template, rubric, inputs, outputs
☑️✅ ABC rubric (Accuracy, Brevity, Clarity) with color-coded headers
☑️✅ Color-linked inputs and outputs (same color for each evaluation pair)
☑️✅ Mock LLM responses with realistic delays (0.5-3.5s random)
☑️✅ Random completion order (tasks complete out-of-order)
☑️✅ Live updates as each evaluation completes
☑️✅ Template placeholder {Rubric} shown in orange for visual linking
⛔ Out of scope: Real LLM API calls, error handling, retry logic, streaming responses

Features:
- Five-panel layout split: top (question 3 lines), header row (prompt, rubric 9 lines), body row (inputs, outputs)
- Question panel: bright cyan with the evaluation question "What is machine learning?"
- Prompt template panel: cyan border, shows template with {Rubric} placeholder
- Rubric panel: dark orange border, ABC format (A: Accuracy, B: Brevity, C: Clarity)
- Inputs panel: yellow border, 5 formatted prompts with color-coded original answers
- Outputs panel: green border, 5 LLM responses with matching colors (dimmed)
- Five evaluation pairs with different tones: technical, beginner-friendly, academic, casual, concise
- Color palette for answers: cyan, green, magenta, yellow, blue (cycles)
- Template text: dimmed (bright_black) for readability
- Rubric text: orange (dark_orange) for visual distinction
- Original answers: highlighted in their identifying color
- Mock LLM responses include: Score (A/B/C ratings), Revised Answer, Justification (2 sentences)
- Random completion order: async tasks complete independently (0.5-3.5s delays)
- Live updates: outputs replace "..." with actual responses as they arrive
- 8 fps refresh rate for smooth updates
- Text truncation: max 1200 chars or 12 lines per output
- Blue-bordered introduction panel

Technical:
- Asyncio: concurrent evaluation with asyncio.gather()
- Rich: Console, Layout, Live, Panel, Text, Style
- Layout: split_column(question, header, body), header.split_row(prompt, rubric), body.split_row(inputs, outputs)
- Pattern: Parallel LLM evaluation with visual tracking
- Mock LLM: async function with random delay simulation
- Color scheme: ANSWER_COLORS (5 colors), RUBRIC_COLOR (dark_orange), TEMPLATE_COLOR (dim bright_black)
- Display prompts: keep {Rubric} placeholder for color linking
- LLM prompts: expand {Rubric} to full ABC description
- Update mechanism: callback function run_and_update() per task
- Rendering: render_lists() builds colored Text with line-by-line parsing
- Special handling: {Rubric} line shows "{{ A: Accuracy; B: Brevity; C: Clarity }}" in orange
- Refresh: screen=False for clean terminal output
- Total runtime: ~4-6s (max mock delay + overhead)

Run: uv run python src/rich/layout_judge.py
"""

from __future__ import annotations

import asyncio
import random
from typing import Dict, List, Tuple

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.style import Style
from rich.text import Text

# ----- Configuration ---------------------------------------------------------

# ABC Rubric details for expansion
ABC_RUBRIC_DETAILS = {
    "A": "Accuracy – factually correct and grounded",
    "B": "Brevity – succinct and to the point",
    "C": "Clarity – clear, organized, readable",
}
ABC_RUBRIC_EXPANDED = " ".join(
    f"{k}: {v.split('–')[0].strip()}" for k, v in ABC_RUBRIC_DETAILS.items()
)

PROMPT_TEMPLATE = (
    "You are an evaluator. Evaluate the following answer using ABC rubric {Rubric}. "
    "Refer to items as <A>, <B>, <C> with 1–3 word cues.\n"
    "Score the answer, then provide a revised version matching the requested tone: {tone}.\n"
    "After the revised answer, add a 2-sentence justification explaining your improvements.\n\n"
    "Question: {question}\n"
    "Original Answer: {original_answer}\n"
)

RUBRIC = (
    "ABC Rubric:\n"
    f"<A> {ABC_RUBRIC_DETAILS['A']}\n"
    f"<B> {ABC_RUBRIC_DETAILS['B']}\n"
    f"<C> {ABC_RUBRIC_DETAILS['C']}\n"
)

# Same question, different answers to evaluate
QUESTION = "What is machine learning?"

EXAMPLES: List[Dict[str, str]] = [
    {
        "tone": "technical",
        "question": QUESTION,
        "original_answer": "Machine learning is algorithms that learn patterns from data.",
    },
    {
        "tone": "beginner-friendly",
        "question": QUESTION,
        "original_answer": "ML is when computers get better at tasks by looking at examples instead of being explicitly programmed.",
    },
    {
        "tone": "academic",
        "question": QUESTION,
        "original_answer": "Machine learning is a subset of artificial intelligence focused on building systems that improve performance through experience.",
    },
    {
        "tone": "casual",
        "question": QUESTION,
        "original_answer": "It's basically teaching computers to recognize patterns and make predictions, like how Netflix recommends shows.",
    },
    {
        "tone": "concise",
        "question": QUESTION,
        "original_answer": "Algorithms that automatically improve through data exposure without explicit programming for each scenario.",
    },
]

# Mock LLM responses for demonstration purposes
MOCK_RESPONSES = [
    {
        "score": "A: 7/10 (good foundation), B: 9/10 (concise), C: 8/10 (clear)",
        "revised": "Machine learning enables algorithms to identify patterns in data and improve performance autonomously through statistical techniques and iterative refinement.",
        "justification": "Enhanced technical precision by adding 'statistical techniques' and 'iterative refinement' to better convey the computational nature. The revision maintains brevity while improving accuracy for a technical audience.",
    },
    {
        "score": "A: 8/10 (accurate analogy), B: 6/10 (could be shorter), C: 9/10 (very accessible)",
        "revised": "ML teaches computers to learn from examples, improving at tasks without explicit programming for every scenario.",
        "justification": "Simplified the explanation while preserving the core concept. The revised version reduces verbosity (addressing B) while maintaining the beginner-friendly tone and clear analogy.",
    },
    {
        "score": "A: 9/10 (academically sound), B: 8/10 (appropriate length), C: 7/10 (could be more structured)",
        "revised": "Machine learning constitutes a subdomain of artificial intelligence focused on developing computational systems that autonomously enhance performance metrics through empirical exposure to training data.",
        "justification": "Elevated the academic rigor by incorporating formal terminology ('subdomain', 'computational systems', 'empirical exposure'). The revision maintains appropriate length while improving structural clarity for an academic context.",
    },
    {
        "score": "A: 8/10 (good real-world example), B: 9/10 (nicely concise), C: 9/10 (highly relatable)",
        "revised": "Teaching computers to spot patterns and make predictions—like how Spotify knows what song you'll love next.",
        "justification": "Switched the example from Netflix to Spotify for variety while maintaining the casual, relatable tone. The dash punctuation creates a more conversational flow appropriate for casual communication.",
    },
    {
        "score": "A: 9/10 (precise definition), B: 7/10 (slightly verbose), C: 8/10 (well-organized)",
        "revised": "Algorithms that improve performance through data exposure without scenario-specific programming.",
        "justification": "Streamlined the definition by removing redundant qualifiers ('automatically', 'explicit') while preserving core accuracy. The revision achieves maximum conciseness requested while maintaining technical precision.",
    },
]

# ----- Utilities -------------------------------------------------------------


def truncate_text(text: str, max_lines: int = 12, max_chars: int = 1200) -> str:
    """Truncate text to fit within display constraints."""
    text = text.strip()
    if len(text) > max_chars:
        text = text[: max_chars - 1] + "…"
    lines = text.splitlines()
    if len(lines) > max_lines:
        lines = lines[:max_lines] + ["…"]
    return "\n".join(lines)


async def mock_llm_call(prompt: str, delay_ms: int = 800) -> str:
    """Simulate an LLM API call with realistic delay."""
    # Simulate random network latency and processing time - outputs appear in random order
    await asyncio.sleep(random.uniform(0.5, 3.5))

    # Extract the index from the prompt to return the corresponding mock response
    # For simplicity, we'll cycle through responses based on the tone
    for i, example in enumerate(EXAMPLES):
        if f"tone: {example['tone']}" in prompt or example['original_answer'] in prompt:
            response = MOCK_RESPONSES[i]
            return (
                f"Score: {response['score']}\n\n"
                f"Revised Answer: {response['revised']}\n\n"
                f"Justification: {response['justification']}"
            )

    # Fallback response
    return "Score: A: 8/10, B: 8/10, C: 8/10\n\nRevised Answer: [Mock response]\n\nJustification: This is a simulated response for demonstration purposes."


# Colors for highlighting the original answers being evaluated (avoid white)
ANSWER_COLORS: List[Style] = [
    Style(color="cyan", bold=False),
    Style(color="green", bold=False),
    Style(color="magenta", bold=False),
    Style(color="yellow", bold=False),
    Style(color="blue", bold=False),
]

# Reserved colors
RUBRIC_COLOR = Style(color="dark_orange", bold=False)  # Orange reserved for rubric only
TEMPLATE_COLOR = Style(color="bright_black", dim=True)  # Dimmed for template text


# ----- Layout building -------------------------------------------------------


def build_layout() -> Layout:
    layout = Layout(name="root")
    layout.split_column(
        Layout(name="question", size=3),  # Show the question at the top
        Layout(name="header", size=9),
        Layout(name="body"),
    )
    # Header split in two panes: prompt template and rubric
    layout["header"].split_row(
        Layout(name="prompt", ratio=1),
        Layout(name="rubric", ratio=1),
    )
    # Body split left/right: inputs and outputs
    layout["body"].split_row(
        Layout(name="inputs", ratio=1),
        Layout(name="outputs", ratio=1),
    )
    return layout


def render_header(
    prompt_template: str, rubric_template: str, example: Dict[str, str]
) -> Tuple[Panel, Panel]:
    # Show template with sample values
    sample = dict(example)
    sample["Rubric"] = "{Rubric}"  # Keep placeholder
    prompt_sample = prompt_template.format(**sample)
    prompt_block = Text(prompt_sample, style=TEMPLATE_COLOR)
    rubric_block = Text(rubric_template, style=RUBRIC_COLOR)
    return (
        Panel(prompt_block, title="Prompt Template", border_style="cyan"),
        Panel(rubric_block, title="Rubric (ABC)", border_style="dark_orange"),
    )


def render_lists(inputs: List[str], outputs: List[str]) -> Tuple[Panel, Panel]:
    left_text = Text()
    for i, s in enumerate(inputs):
        if i:
            left_text.append("\n\n")
        answer_color = ANSWER_COLORS[i % len(ANSWER_COLORS)]

        # Split prompt into parts to color differently
        left_text.append(f"[{i + 1}] ", style=Style(color="bright_black"))

        # Parse the formatted prompt to identify the original answer
        lines = s.split("\n")
        for line_idx, line in enumerate(lines):
            if line_idx > 0:
                left_text.append("\n")

            if "{Rubric}" in line:
                # Handle rubric line specially
                before, sep, after = line.partition("{Rubric}")
                left_text.append(before, style=TEMPLATE_COLOR)
                left_text.append("{{ ", style=RUBRIC_COLOR)
                left_text.append("A: Accuracy; B: Brevity; C: Clarity", style=RUBRIC_COLOR)
                left_text.append(" }}", style=RUBRIC_COLOR)
                if after:
                    left_text.append(after, style=TEMPLATE_COLOR)
            elif line.startswith("Original Answer:"):
                # Color the label dimmed, the answer in its identifying color
                left_text.append("Original Answer: ", style=TEMPLATE_COLOR)
                answer_text = line[len("Original Answer: ") :]
                left_text.append(truncate_text(answer_text, max_lines=3), style=answer_color)
            else:
                # Everything else is template text
                left_text.append(line, style=TEMPLATE_COLOR)

    right_text = Text()
    for i, s in enumerate(outputs):
        if i:
            right_text.append("\n\n")
        # Use same color for output as the corresponding input's answer
        output_color = ANSWER_COLORS[i % len(ANSWER_COLORS)]
        right_text.append(f"[{i + 1}] ", style=Style(color="bright_black"))
        right_text.append(truncate_text(s), style=Style(color=output_color.color, dim=True))
    return (
        Panel(left_text, title="Inputs (compiled prompts)", border_style="yellow"),
        Panel(right_text, title="Outputs (LLM responses)", border_style="green"),
    )


# ----- Async execution -------------------------------------------------------


async def main_async() -> int:
    """Main async function that orchestrates the judge layout demo."""
    console = Console()

    console.print(Panel.fit(
        "[bold blue]Example 7: LLM Judge Layout[/bold blue]\n\n"
        "This script demonstrates:\n"
        "• Complex multi-panel layouts\n"
        "• Parallel LLM evaluation workflow\n"
        "• Color-coded inputs and outputs",
        border_style="blue"
    ))

    layout = build_layout()

    # Display the question being evaluated
    question_text = Text(f"Question: {QUESTION}", style=Style(color="bright_cyan", bold=True))
    layout["question"].update(Panel(question_text, border_style="bright_cyan", title="Evaluating"))

    header_left, header_right = render_header(PROMPT_TEMPLATE, RUBRIC, example=EXAMPLES[0])
    layout["prompt"].update(header_left)
    layout["rubric"].update(header_right)

    formatted_inputs: List[str] = []  # For display (with {Rubric} placeholder)
    llm_prompts: List[str] = []  # For actual LLM calls (with expanded rubric)
    outputs: List[str] = ["…"] * len(EXAMPLES)

    with Live(layout, refresh_per_second=8, console=console, screen=False):
        for ex in EXAMPLES:
            # Display version: keep {Rubric} placeholder for color-linking
            ex_display = dict(ex)
            ex_display["Rubric"] = "{Rubric}"
            formatted_inputs.append(PROMPT_TEMPLATE.format(**ex_display))

            # LLM version: expand rubric fully
            ex_llm = dict(ex)
            ex_llm["Rubric"] = ABC_RUBRIC_EXPANDED
            llm_prompts.append(PROMPT_TEMPLATE.format(**ex_llm))

        left_panel, right_panel = render_lists(formatted_inputs, outputs)
        layout["inputs"].update(left_panel)
        layout["outputs"].update(right_panel)

        # Create tasks and track them properly with a callback
        async def run_and_update(index: int, prompt: str) -> None:
            # No sequential delay - let them complete in random order
            result = await mock_llm_call(prompt)
            outputs[index] = result
            left_panel, right_panel = render_lists(formatted_inputs, outputs)
            layout["inputs"].update(left_panel)
            layout["outputs"].update(right_panel)

        # Create all tasks (they run concurrently and complete in random order)
        tasks = [
            asyncio.create_task(run_and_update(i, llm_prompts[i])) for i in range(len(EXAMPLES))
        ]

        # Wait for all to complete
        await asyncio.gather(*tasks)

        # Small delay to ensure final state is visible
        await asyncio.sleep(0.5)

    console.print("\n[green][OK][/green] All evaluations complete!")
    return 0


def main() -> None:
    raise SystemExit(asyncio.run(main_async()))


if __name__ == "__main__":
    main()
