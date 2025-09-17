
Project Constitution — minimal requirements

This repository follows a minimal layout and contract for a small Python service runnable with an ASGI server (uv/uvicorn) and managed with a `pyproject.toml`.

Files and layout (minimum)

- `pyproject.toml` — mandatory. Defines build-system and project metadata and sets `uvicorn` (or `uv`) as an optional/run dependency.
- `src/<package_name>/__init__.py` — package root.
- `src/<package_name>/main.py` — ASGI application entrypoint exposing `app` (an ASGI callable) or a factory `create_app()` returning the app.
- `tests/` — optional but recommended. At least one smoke test that imports the app.

Minimal `pyproject.toml` example

Replace `<package_name>` and versions as appropriate.

```toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "<package_name>"
version = "0.1.0"
description = "Minimal ASGI service"
authors = [ { name = "Your Name" } ]
dependencies = [
	"uvicorn>=0.20.0", # ASGI server
]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

Entrypoint contract

- `src/<package_name>/main.py` must expose one of the following:
	- `app` — an ASGI application instance (e.g., a FastAPI or Starlette app)
	- `create_app()` — a zero-arg function that returns `app`.

Examples

- Simple FastAPI-style `src/<package_name>/main.py`:

```py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
		return {"ok": True}
```

- Run with uvicorn (recommended)

Use the package path to the module exposing `app`. From the project root:

```bash
# run module path: src/<package_name>/main.py => <package_name>.main:app
uvicorn <package_name>.main:app --host 0.0.0.0 --port 8000 --reload
```

Notes and minimal checks

- Ensure `PYTHONPATH` or installation includes `src` (common patterns: use `pip install -e .` or set `PYTHONPATH=src`).
- Quick smoke test: `python -c "import <package_name>.main; print(getattr(<package_name>.main, 'app', 'no-app'))"` should not error and should show `app`.
- If using `create_app()`, run `uvicorn "<package_name>.main:create_app()"` (note quoting). Some shells require different quoting.

Recommended tiny additions (optional)

- `README.md` with the two run commands (development and production).
- `requirements.txt` or `constraints.txt` if pinning is required by deploys.
- `tests/test_smoke.py` with a simple import and client request.

Acceptance criteria (bare minimum)

1. `pyproject.toml` exists at repo root and defines the project name and the build-system.
2. `src/<package_name>/main.py` exposes `app` or `create_app()`.
3. `uvicorn <package_name>.main:app` starts the server without import errors when `src` is on `PYTHONPATH` or the package is installed.

That's it — the smallest practical constitution to get a Python ASGI service running with uv/uvicorn and a `pyproject.toml`.
