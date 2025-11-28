# richly-printed

**19 Rich library demos: from basic copy-paste panels to dynamic dashboards with transient self-compacting output.**

Intended for quick reference for coding agents when you want more flexibility from the terminal but don't want to turn on bloat from Streamlit/React/Vite etc. Includes basic clones of the Docker compose and Astral uv sync TUIs.

## Complexity Levels

| Level | What | Examples |
|-------|------|----------|
| **Basic** | Static output, copy-paste | Panels, tables, syntax highlighting |
| **Dynamic** | Live updates, progress | Spinners, progress bars, layouts |
| **Advanced** | Production dashboards | Multi-panel monitoring, resource tracking |
| **Transient** | Self-compacting output | Live verbose → summary replacement |

## Installation

```bash
# Clone the repo
git clone https://github.com/alexfosterinvisible/richly-printed.git
cd richly-printed

# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

## Quick Start

```bash
# Run any demo via entry point
uv run basic              # Simple panel
uv run live-dashboard     # Dynamic job queue
uv run agent-dashboard    # Full monitoring
uv run transient-summary  # Self-compacting output

# Or run all demos in sequence
./run_all_rich_demos.sh
```

## Demos

### Basic (Static Output)

| # | Command | Description |
|---|---------|-------------|
| 1 | `basic` | Panel rendering, color markup, loguru integration |
| 2 | `markdown` | Render markdown and syntax-highlighted code |
| 3 | `inline` | PEP 723 self-contained scripts with embedded deps |
| 4 | `example-env` | Environment variables table with defaults |
| 16 | `deps` | HTTP request with response table |

### Dynamic (Live Updates)

| # | Command | Description |
|---|---------|-------------|
| 5 | `async-http` | Async requests with progress spinners |
| 6 | `layout` | Split-screen terminal regions |
| 7 | `layout-judge` | Multi-panel LLM evaluation workflow |
| 8 | `live-tasks` | Multi-stage task progression with spinners |
| 9A | `live-logs` | Streaming log aggregation with rotation |
| 9B | `live-logs-ordered` | Out-of-order completion → sequential display |
| 10 | `live-dashboard` | Two-column job queue monitoring |
| 11 | `live-metrics` | Real-time RPS/errors/latency panels |
| 12 | `progress-advanced` | Custom columns with ETA and transfer speed |

### Advanced (Production Dashboards)

| # | Command | Description |
|---|---------|-------------|
| 13 | `loader-tasks` | uv sync style multi-stage processing |
| 14 | `loader-tasks-stream` | Irregular spawn with auto-removal |
| 15 | `tracebacks` | Rich tracebacks with local variable inspection |
| 17 | `coding-agents` | Pipeline simulation with loop-back workflow |
| 18 | `agent-dashboard` | Full monitoring: CPU, RAM, events, traces |

### Transient (Self-Compacting)

| # | Command | Description |
|---|---------|-------------|
| 19 | `transient-summary` | Live verbose logs → summary replacement |

## Highlights

### Transient Self-Compacting Output (`transient-summary`)
Shows verbose progress during execution, then replaces with concise summary:
- Live panel with "Analyzing..." placeholders
- Async slot reservation maintains visual order
- Panel vanishes when done (`transient=True`)
- Final summary prints in its place
- Perfect for agent workflows, CI/CD output

### UV Sync Clone (`loader-tasks-stream`)
Mimics the Astral UV package manager TUI with:
- Irregular task spawning (30-180ms intervals)
- Auto-removal of successful tasks after brief green dot
- Persistent error display with red × marker
- Multi-stage workflow animations

### Docker Compose Clone (`agent-dashboard`)
Production-grade monitoring dashboard with:
- 6 concurrent agents with full lifecycle
- Real-time CPU/RAM monitoring with color-coded warnings
- Live table sorting by resource usage
- Event log with timestamps
- Debug trace log with millisecond precision

### LLM Judge Layout (`layout-judge`)
Parallel evaluation workflow with:
- 5 concurrent LLM evaluations
- Four-panel layout (question, prompt, rubric, I/O)
- Color-linked inputs and outputs
- Mock responses with realistic delays

## Dependencies

- `rich>=13.0.0` - Terminal formatting and TUI components
- `loguru>=0.7.0` - Structured logging
- `httpx>=0.27.0` - HTTP client for demos
- `aiohttp>=3.9.0` - Async HTTP for demos

## Documentation

The `docs/` folder contains curated Rich library documentation covering:
- Console API, Styles, Markup, Text
- Progress bars, Tables, Panels, Layouts
- Live displays, Trees, Tracebacks
- Syntax highlighting, Markdown rendering

## License

MIT
