#!/usr/bin/env bash
set -euo pipefail

# Run pytest for pre-commit. This runs the test suite quickly. If a .venv exists
# it will be used; otherwise pytest must be available on PATH (via system or user install).

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT_DIR/.venv"

cd "$ROOT_DIR"

if [ -f "$VENV/bin/activate" ]; then
  # shellcheck disable=SC1090
  . "$VENV/bin/activate"
fi

echo "Running pytest (pre-commit)..."
pytest -q
