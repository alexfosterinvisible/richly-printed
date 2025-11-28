#!/usr/bin/env bash

#   To run all Rich demos:
#   cd src/rich/ && ./run_all_rich_demos.sh

set -euo pipefail
cd "$(dirname "$0")"
scripts=(
    rich_basic.py
    deps_httpx.py
    inline_pep723.py
    env.py
    async_http.py
    markdown_syntax.py
    prog_bar_advanced.py
    layout_panes.py
    live_logs.py
    live_logs_ordered.py
    live_metrics.py
    live_dashboard.py
    live_dashboard_coding_agents.py
    live_tasks.py
    loader_tasks.py
    loader_tasks_stream.py
    layout_judge.py
    agent_dashboard.py
    trace_rich.py
    transient_summary.py
)
echo "[OK] Will run ${#scripts[@]} demos in numbered order:"
for i in "${!scripts[@]}"; do
    echo "  Example $((i+1)): ${scripts[$i]}"
done
echo ""
for script in "${scripts[@]}"; do
    echo "[OK] Running $script"
    uv run "$script" || echo "[WARN] $script failed (continuing...)"
done
echo "[OK] All demos completed"
