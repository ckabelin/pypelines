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
- Requires-Python: `>=3.13` (declared in `pyproject.toml`)

Layout and important files

- `pyproject.toml` — project metadata, build-system and dependencies. Dev extras include `pytest`, `httpx`, `ruff`, and `mypy`.
- `src/pypelines/__init__.py` — package root.
- `src/pypelines/main.py` — application module exposing:
  - `create_app()` — factory returning a `FastAPI` app.
  - `app` — module-level app instance created by calling `create_app()` (this is the target used by the CLI and uvicorn).
- `src/pypelines/cli.py` — small CLI exposing a `uv` console script (configured in `pyproject.toml`) with a `run` subcommand that delegates to `uvicorn.run()`.
- `tests/test_smoke.py` — a smoke test that imports `pypelines.main.app` and performs a simple request with `httpx.AsyncClient`.
- `mypy.ini` — mypy configuration (minimal; currently ignores missing imports by default).

Entrypoints and running

- Console script: after installing the project (for example `pip install -e .`), the package exposes a `uv` command mapped to `pypelines.cli:main`.

- To run the app in development using the installed console script:

```bash
# start the server (development)
uv run run --host 0.0.0.0 --port 8000 --reload
```

- Alternatively you can run using uvicorn directly from the source layout (ensure `src` is on `PYTHONPATH` or install the package):

```bash
# when package is installed or PYTHONPATH includes src
uvicorn pypelines.main:app --host 0.0.0.0 --port 8000 --reload

# or when using the factory explicitly
uvicorn "pypelines.main:create_app()" --host 0.0.0.0 --port 8000 --reload
```

Notes about the CLI

- `uv run` is implemented in `src/pypelines/cli.py`. It supports the `run` subcommand and options `--host`, `--port`, and `--reload`.
- The CLI imports `uvicorn` lazily so `uv --help` stays fast and doesn't try to import the app.

Linting and type checking

- Ruff: configured in `pyproject.toml` under `[tool.ruff]` (line-length 88 and a minimal `select`). Run with:

```bash
ruff check src tests
```

- Mypy: configuration lives in `mypy.ini`. The project currently sets `ignore_missing_imports = True` to avoid third-party stubs noise. Run with:

```bash
mypy src tests
```

Tests

- Tests live in `tests/`. The smoke test `tests/test_smoke.py` uses `httpx.AsyncClient` to exercise `main.app`.
- Run tests with:

```bash
pytest
```

Acceptance criteria (current repo)

1. `pyproject.toml` exists and declares `pypelines`, dependencies and a `uv` console script. (satisfied)
2. `src/pypelines/main.py` exposes `create_app()` and `app` for uvicorn and programmatic use. (satisfied)
3. `src/pypelines/cli.py` implements `uv run` which starts the server via `uvicorn.run()`. (satisfied)
4. Linting and typing configured: `ruff` in `pyproject.toml`, `mypy.ini` present. (satisfied)

If you'd like I can now:

- run `ruff`, `mypy`, and `pytest` in this environment and fix any low-effort issues; or
- add a `README.md` documenting the commands (I can create it now). 

````

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
- Requires-Python: `>=3.13` (declared in `pyproject.toml`)

Layout and important files

- `pyproject.toml` — project metadata, build-system and dependencies. Dev extras include `pytest`, `httpx`, `ruff`, and `mypy`.
- `src/pypelines/__init__.py` — package root.
- `src/pypelines/main.py` — application module exposing:
  - `create_app()` — factory returning a `FastAPI` app.
  - `app` — module-level app instance created by calling `create_app()` (this is the target used by the CLI and uvicorn).
- `src/pypelines/cli.py` — small CLI exposing a `uv` console script (configured in `pyproject.toml`) with a `run` subcommand that delegates to `uvicorn.run()`.
- `tests/test_smoke.py` — a smoke test that imports `pypelines.main.app` and performs a simple request with `httpx.AsyncClient`.
- `mypy.ini` — mypy configuration (minimal; currently ignores missing imports by default).

Entrypoints and running

- Console script: after installing the project (for example `pip install -e .`), the package exposes a `uv` command mapped to `pypelines.cli:main`.

- To run the app in development using the installed console script:

```bash
# start the server (development)
uv run run --host 0.0.0.0 --port 8000 --reload
```

- Alternatively you can run using uvicorn directly from the source layout (ensure `src` is on `PYTHONPATH` or install the package):

```bash
# when package is installed or PYTHONPATH includes src
uvicorn pypelines.main:app --host 0.0.0.0 --port 8000 --reload

# or when using the factory explicitly
uvicorn "pypelines.main:create_app()" --host 0.0.0.0 --port 8000 --reload
```

Notes about the CLI

- `uv run` is implemented in `src/pypelines/cli.py`. It supports the `run` subcommand and options `--host`, `--port`, and `--reload`.
- The CLI imports `uvicorn` lazily so `uv --help` stays fast and doesn't try to import the app.

Linting and type checking

- Ruff: configured in `pyproject.toml` under `[tool.ruff]` (line-length 88 and a minimal `select`). Run with:

```bash
ruff check src tests
```

- Mypy: configuration lives in `mypy.ini`. The project currently sets `ignore_missing_imports = True` to avoid third-party stubs noise. Run with:

```bash
mypy src tests
```

Tests

- Tests live in `tests/`. The smoke test `tests/test_smoke.py` uses `httpx.AsyncClient` to exercise `main.app`.
- Run tests with:

```bash
pytest
```

Acceptance criteria (current repo)

1. `pyproject.toml` exists and declares `pypelines`, dependencies and a `uv` console script. (satisfied)
2. `src/pypelines/main.py` exposes `create_app()` and `app` for uvicorn and programmatic use. (satisfied)
3. `src/pypelines/cli.py` implements `uv run` which starts the server via `uvicorn.run()`. (satisfied)
4. Linting and typing configured: `ruff` in `pyproject.toml`, `mypy.ini` present. (satisfied)

If you'd like I can now:

- run `ruff`, `mypy`, and `pytest` in this environment and fix any low-effort issues; or
- add a `README.md` documenting the commands (I can create it now). 
