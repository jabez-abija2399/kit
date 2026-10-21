#!/usr/bin/env bash
# The ONE command that starts this project locally (agents and the evaluator use it before testing in a browser).
# KICKOFF_FILLS_THIS: replace the lines below during the kickoff or FEAT-001, e.g.
#   docker compose up -d db && pnpm dev
#   uv run uvicorn app.main:app --reload
set -e
cd "$(dirname "$0")/.."
echo "scripts/dev.sh is not set up yet: the kickoff (or FEAT-001) writes the start command here." >&2
exit 1
