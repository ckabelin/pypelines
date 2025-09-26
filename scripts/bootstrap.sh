#!/usr/bin/env bash
set -euo pipefail

# Bootstrap development environment:
# - create a venv in .venv
# - activate and install editable package with dev extras

PY=$(command -v python3 || command -v python)
if [ -z "$PY" ]; then
  echo "python3 not found" >&2
  exit 1
fi

if [ ! -d .venv ]; then
  echo "Creating virtualenv .venv"
  "$PY" -m venv .venv
fi

echo "Activating .venv and installing dev dependencies"
# shellcheck source=/dev/null
. .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -e '.[dev]'

echo "Bootstrap complete. Activate with: source .venv/bin/activate"
