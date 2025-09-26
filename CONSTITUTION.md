# Project Constitution — minimal requirements

This repository follows a minimal layout and contract for a small Python service runnable with an ASGI server (uv/uvicorn) and managed with a `pyproject.toml`.

Key points (authoritative contract)

- The project is rooted at the repository root.
- Developer entrypoint is the `uv` console script (installed via `pip install -e '.[dev]'`). Linting, typechecking and tests are invoked via `uv` (for example `uv lint`, `uv typecheck`, `uv test`).
- A helper bootstrap script is provided: `./scripts/bootstrap.sh` (creates `.venv` and installs `.[dev]`). A `Makefile` exposes common targets (`bootstrap`, `lint`, `typecheck`, `test`, `run`).
- Heavy AI/ML dependencies are in an optional `ai` extra. Install them only when you need Streamlit/LLM features: `pip install -e '.[dev,ai]'`.

Minimal layout

- `pyproject.toml` — project metadata, dependencies and console scripts.
- `src/pypelines/` — package sources.
- `tests/` — test suite.
- `terraform/` — terraform examples and optional GitHub provider hooks.
- `scripts/bootstrap.sh` and `Makefile` — standardized developer setup and tasks.

Entrypoints and running

- Install (development):

```bash
./scripts/bootstrap.sh
source .venv/bin/activate
```

- Common commands (via `uv`):

```bash
uv lint           # run ruff
uv typecheck      # run mypy
uv test           # run pytest
uv run run        # run ASGI app via uvicorn
```

CI and workflows

- NOTE: As of this change, GitHub Actions workflow files have been removed from the repository. Continuous Integration is therefore not present in this repository by default.
- If CI is required, workflows should be added back under `.github/workflows/` or CI configured centrally via organization tooling.

Governance

1. Keep `CONSTITUTION.md` and `pyproject.toml` in sync for declared dependencies and runtime contracts.
2. When reintroducing CI, prefer direct CLI tools (ruff, mypy, pytest) in workflows rather than project-only entrypoints to improve portability.
````markdown

Project Constitution — minimal requirements

This repository follows a minimal layout and contract for a small Python service runnable with an ASGI server (uv/uvicorn) and managed with a `pyproject.toml`.

Files and layout (minimum)

- `pyproject.toml` — mandatory. Defines build-system and project metadata and sets `uvicorn` (or `uv`) as an optional/run dependency.
- `src/<package_name>/__init__.py` — package root.
- `src/<package_name>/main.py` — ASGI application entrypoint exposing `app` (an ASGI callable) or a factory `create_app()` returning the app.
- `tests/` — optional but recommended. At least one smoke test that imports the app.

Project Constitution — synced with current code

This file documents the minimal, authoritative contract for this repository as implemented in the codebase on branch `feature/initialize`.

Project identity

- Name: `pypelines` (see `pyproject.toml`)
- Version: `0.1.0` (placeholder in `pyproject.toml`)
# Project Constitution — minimal requirements

This repository follows a minimal layout and contract for a small Python service runnable with an ASGI server (uv/uvicorn) and managed with a `pyproject.toml`.

The contents below describe the authoritative, current contract for this repository (branch `feature/initialize`). Keep this file small and stable — it is intended for humans and CI documentation.

## Identity

- Name: `pypelines`
- Version: `0.1.0` (placeholder in `pyproject.toml`)
- Requires-Python: `>=3.11` (declared in `pyproject.toml`)

## Minimal layout

- `pyproject.toml` — mandatory. Declares project metadata, dependencies and optional extras (`dev`, `ai`).
- `src/pypelines/` — package sources.
  - `main.py` — provides `app` (FastAPI instance) and `create_app()` factory.
  - `cli.py` — exposes `uv` console script wrapper.
- `tests/` — unit/integration tests; include at least a smoke test.
- `.github/workflows/` — GitHub Actions workflows live at the repository root (CI, CodeQL, build-and-publish, auto code review, etc.).

## Dependencies contract

- Runtime dependencies are minimal: the framework (`fastapi`), the ASGI server (`uvicorn`), and UI runtime (`streamlit`).
- Heavy AI/ML dependencies (LangChain, Chroma, sentence-transformers, tiktoken, Ollama client) are in the optional `ai` extras. Install them only when you need AI features.
- Dev tooling is in the `dev` extras (testing, linting, type checking).

## CI and workflows

- CI workflows are stored in `.github/workflows/` at the repository root. Key workflows:
  - `ci.yml` — runs ruff, mypy, pytest; includes an optional `ai-tests` job that installs `.[dev,ai]` for heavy AI tests.
  - `auto-code-review.yml` — annotates pull requests with ruff/mypy/pytest using reviewdog (Actions).
  - `codeql.yml` — CodeQL scanning and SARIF export.
  - `build-and-publish.yml` — builds Docker image and optionally publishes to GHCR.

## Running

- Install (development):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

- To run the API in development:

```bash
uv run run --host 0.0.0.0 --port 8000 --reload
# or directly with uvicorn
uvicorn pypelines.main:app --reload
```

- To enable AI features (optional):

```bash
pip install -e '.[dev,ai]'
# then run heavy AI tests or start the Streamlit UI with embeddings/LLM enabled
```

## Governance and acceptance

1. Repositories must keep `pyproject.toml` and `CONSTITUTION.md` in sync for declared dependencies and runtime contracts.
2. CI must run ruff, mypy and pytest on PRs; heavy AI tests run in the `ai-tests` job when requested.

If you want, I can run the linters/tests and fix low-effort failures as a follow-up.
