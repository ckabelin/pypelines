# pypelines

Minimal ASGI service (FastAPI) with a small CLI wrapper (`uv run`) and basic lint/typecheck/test tooling.

## Quick start (development)

1. Create and activate a virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install the package in editable mode with dev extras:

```bash
pip install -e '.[dev]'
```

3. Run the app with the provided console script (after install):

```bash
uv run run --host 0.0.0.0 --port 8000 --reload
```

Or use uvicorn directly when `src` is on `PYTHONPATH` or the package is installed:

```bash
uvicorn pypelines.main:app --host 0.0.0.0 --port 8000 --reload
```

## Tests

Run tests with pytest:

```bash
pytest
```

## Linting and Type Checking

Run ruff (linter/formatter):

```bash
ruff check src tests
```

Run mypy (type checker):

```bash
mypy src tests
```

## Pre-commit

To enable pre-commit hooks that run ruff and mypy on commits:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

The configured hooks will run `ruff` (auto-fix) and `mypy` on staged files.
