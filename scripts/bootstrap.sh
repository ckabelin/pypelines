#!/usr/bin/env bash
set -euo pipefail

# Bootstrap development environment:
# - create a venv in .venv
# - activate and install editable package with dev extras
# - optionally install AI extras with --ai
# - install pre-commit and set up hooks
# - run quick smoke checks (ruff, mypy, pytest)

AI_EXTRAS=false
SKIP_TESTS=false
PRECOMMIT_ONLY=false
while [ "$#" -gt 0 ]; do
  case "$1" in
    --ai)
      AI_EXTRAS=true
      shift
      ;;
    --skip-tests)
      SKIP_TESTS=true
      shift
      ;;
    --precommit-only)
      PRECOMMIT_ONLY=true
      shift
      ;;
    --help|-h)
      echo "Usage: $0 [--ai] [--skip-tests] [--precommit-only]"
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

PY=$(command -v python3 || command -v python)
if [ -z "$PY" ]; then
  echo "python3 not found" >&2
  exit 1
fi

if [ ! -d .venv ]; then
  echo "Creating virtualenv .venv"
  if ! "$PY" -m venv .venv 2>/dev/null; then
    echo "Warning: failed to create .venv via '$PY -m venv'. Falling back to system/user installs." >&2
  else
    echo ".venv created"
  fi
fi

# Decide how to install: prefer venv pip if available, else fallback to system pip --user
USE_VENV=false
if [ -f .venv/bin/activate ]; then
  # shellcheck source=/dev/null
  . .venv/bin/activate
  PIP_CMD=".venv/bin/pip"
  PY_CMD=".venv/bin/python"
  USE_VENV=true
else
  echo "No .venv available; falling back to system Python environment (will use --user installs)." >&2
  PIP_CMD="$PY -m pip"
  PY_CMD="$PY"
fi

echo "Upgrading pip/setuptools/wheel"

# Ensure pip is available for the chosen Python
ensure_pip() {
  if "$PY_CMD" -m pip --version >/dev/null 2>&1; then
    return 0
  fi
  echo "pip not found for $PY_CMD, trying ensurepip..."
  if "$PY_CMD" -m ensurepip --upgrade >/dev/null 2>&1; then
    echo "ensurepip succeeded"
    return 0
  fi
    echo -e "Could not bootstrap pip for $PY_CMD. On Debian/Ubuntu install 'python3-venv' and 'python3-pip', e.g.:\n  sudo apt update && sudo apt install python3-venv python3-pip" >&2
    return 1
}

if ! ensure_pip; then
  exit 1
fi

"$PY_CMD" -m pip install --upgrade pip setuptools wheel

if [ "$AI_EXTRAS" = true ]; then
  echo "Installing dev and AI extras (.[dev,ai])"
  if [ "$USE_VENV" = true ]; then
    "$PIP_CMD" install -e '.[dev,ai]'
  else
    "$PIP_CMD" install --user -e '.[dev,ai]'
  fi
else
  echo "Installing dev extras (.[dev])"
  if [ "$USE_VENV" = true ]; then
    "$PIP_CMD" install -e '.[dev]'
  else
    "$PIP_CMD" install --user -e '.[dev]'
  fi
fi

echo "Installing pre-commit and setting up git hooks"
"$PY_CMD" -m pip install --upgrade pre-commit
"$PY_CMD" -m pre_commit install || true

if [ "$PRECOMMIT_ONLY" = true ]; then
  echo "Pre-commit tooling installed and hooks set up. Exiting due to --precommit-only." 
  echo "Activate the venv (if created) with: source .venv/bin/activate"
  exit 0
fi

echo "Running quick smoke checks: ruff, mypy, pytest (fast mode)"
if [ "$SKIP_TESTS" = true ]; then
  echo "Skipping smoke checks due to --skip-tests"
  MYPY_EXIT=0
  PYTEST_EXIT=0
else
  set +e
  ruff check .
  MYPY_EXIT=0
  mypy src tests || MYPY_EXIT=$?
  PYTEST_EXIT=0
  pytest -q --maxfail=1 || PYTEST_EXIT=$?
  set -e
fi

echo "Bootstrap complete. Activate with: source .venv/bin/activate"

if [ $MYPY_EXIT -ne 0 ] || [ $PYTEST_EXIT -ne 0 ]; then
  echo "One or more smoke checks failed (mypy=$MYPY_EXIT pytest=$PYTEST_EXIT)." >&2
  echo "Fix issues or re-run tests after activating the venv." >&2
  exit 2
fi

echo "All smoke checks passed. You're ready to develop."
