# pypelines

Minimal ASGI service (FastAPI) with a small CLI wrapper (`uv`) and basic lint/typecheck/test tooling.

This repository was refactored to run from the repository root and exposes a single developer entrypoint `uv` (console script) that centralizes common tasks.

Quick start (development)

1. Bootstrap the developer environment (creates `.venv` and installs dev extras):

```bash
./scripts/bootstrap.sh
# or via Makefile
make bootstrap
```

2. Activate the venv:

```bash
source .venv/bin/activate
```

3. Use the `uv` CLI for common tasks:

```bash
uv lint           # run ruff (linter)
uv typecheck      # run mypy
uv test           # run pytest
uv run run        # start the ASGI app via uvicorn
```

Alternatively use the Makefile targets which rely on `.venv`:

```bash
make lint
make typecheck
make test
make run
```

Notes
- The `uv` CLI is implemented in `src/pypelines/cli.py` and is the recommended entrypoint for local dev and CI.
- Heavy AI dependencies are intentionally in the optional `ai` extra. Install them only if you need the AI features:

```bash
pip install -e '.[dev,ai]'
```
# pypelines
DevOps Pipeline with Python

This repo relies on Spec-Driven Development and Spec Kit: https://github.com/github/spec-kit

# clone
git clone http://<youruser>:<yourtoken>@github.com/ckabelin/pypelines.git
cd pypelines

- make a new branch 'feature/<whatever>'!

git checkout feature/<whatever>

create a new app under apps

# installation
sudo snap install astral-uv
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>

open VSCode under newly created subdirectory <PROJECT_NAME>.

do your credential/ssh, git config stuff
git remote set-url origin git@github.com:ckabelin/pypelines.git

# get informed & watch cools stuff
https://www.youtube.com/watch?v=a9eR1xsfvHg
https://www.youtube.com/watch?v=o6SYjY1Bkzo
