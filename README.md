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

## CI and workflows

This repository includes several GitHub Actions workflows under `.github/workflows/`.

- `ci.yml` — runs lint (ruff), mypy typechecks, and pytest across a Python matrix (3.11 and 3.12). It also validates Terraform in the `terraform/` folder.
- `build-and-publish.yml` and `docker-publish.yml` — build Docker images from the repository root and publish to GitHub Container Registry on tags or manual dispatch.
- `codeql.yml` — CodeQL security scans (weekly and on main/master). 
- `auto-code-review.yml` — runs on PRs and posts a summary comment with lint/typecheck/test results and artifacts.

Notes for maintainers:

- The workflows now call `ruff`, `mypy`, and `pytest` directly instead of relying on the project's `uv` entrypoint. This makes them more robust on GitHub-hosted runners.
- To reproduce CI locally, bootstrap the venv and install dev extras using `./scripts/bootstrap.sh` or `make bootstrap`, then run `ruff`, `mypy`, and `pytest`.

Pre-commit hooks (ruff, mypy, pytest)

This repository includes a `.pre-commit-config.yaml` that runs `ruff`, `mypy`, `pydocstyle` and a local `pytest` hook.

Install and enable pre-commit hooks locally:

```bash
# bootstrap the developer environment
./scripts/bootstrap.sh
source .venv/bin/activate

# install pre-commit if not already in your venv
pip install pre-commit

# install git hooks
pre-commit install

# run all hooks against the repo
pre-commit run --all-files
```

The `pytest` hook runs the entire test suite and is configured as a local script at `scripts/pre-commit-pytest.sh`. If your environment cannot create a `.venv` automatically, ensure `pytest` is available on your PATH.

Troubleshooting: system packages

If `./scripts/bootstrap.sh` fails to create a venv or bootstrap pip, you may need to install system packages.

Debian/Ubuntu:

```bash
sudo apt update
sudo apt install python3-venv python3-pip
```

macOS (Homebrew):

```bash
brew install python
```

After installing system packages, re-run the bootstrap script:

```bash
./scripts/bootstrap.sh
# or skip tests
./scripts/bootstrap.sh --skip-tests
# install AI extras too
./scripts/bootstrap.sh --ai
# only install pre-commit hooks (fast)
./scripts/bootstrap.sh --precommit-only
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
