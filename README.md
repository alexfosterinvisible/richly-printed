# richly-printed

**20 demos of using the Rich library for basic, dynamic and live terminal prints.**

Intended for quick reference for coding agents when you want more flexibility from the terminal but don't want to turn on bloat from Streamlit/React/Vite etc. Includes basic clones of the Docker compose and Astral uv sync TUIs.

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
uv run basic
uv run live-dashboard
uv run agent-dashboard

# Or run all demos in sequence
./run_all_rich_demos.sh
```

## Demos

| # | Command | Description |
|---|---------|-------------|
| 1 | `basic` | Basic Rich Console - Panel rendering, color markup, loguru integration |
| 2 | `markdown` | Markdown & Syntax - Render markdown and syntax-highlighted code |
| 3 | `inline` | PEP 723 Inline Metadata - Self-contained scripts with embedded deps |
| 4 | `example-env` | Environment Variables - Config display with defaults |
| 5 | `async-http` | Async HTTP - Async requests with progress spinners |
| 6 | `layout` | Layout Panes - Split-screen terminal regions with live updates |
| 7 | `layout-judge` | LLM Judge Layout - Parallel evaluation with color-coded I/O |
| 8 | `live-tasks` | Live Tasks - Multi-stage progression with spinners |
| 9A | `live-logs` | Live Logs - Streaming log aggregation with rotation |
| 9B | `live-logs-ordered` | Live Logs Ordered - Out-of-order completion with sequential display |
| 10 | `live-dashboard` | Live Dashboard - Multi-column job queue monitoring |
| 11 | `live-metrics` | Live Metrics - Real-time RPS/errors/latency panels |
| 12 | `progress-advanced` | Advanced Progress - Custom columns with ETA and transfer speed |
| 13 | `loader-tasks` | Loader Tasks - Package manager style multi-stage processing |
| 14 | `loader-tasks-stream` | Streaming Loader - UV sync style irregular spawn with auto-cleanup |
| 15 | `tracebacks` | Rich Tracebacks - Enhanced error display with local variables |
| 16 | `deps` | HTTP Dependencies - External library integration with tables |
| 17 | `coding-agents` | Coding Agents Dashboard - Pipeline simulation with loop-back workflow |
| 18 | `agent-dashboard` | Agent Dashboard - Production-grade multi-panel monitoring |

## Highlights

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

