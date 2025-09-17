# Changelog

All notable changes made in this branch / session.

## Unreleased

### Added
- `pyproject.toml` updates
  - Added project metadata and dependencies (FastAPI, Uvicorn).
  - Added `[project.scripts]` entry: `uv = "pypelines.cli:main"` (console script).
  - Added `ai` optional dependencies (Streamlit, LangChain, Ollama client, sentence-transformers, chromadb, tiktoken).
  - Added `[tool.ruff]` and `[tool.pydocstyle]` config.
- `CONSTITUTION.md` updated to reflect the current project layout, CLI, AI features, and lint/typecheck config.
- `README.md` expanded with usage, AI features, chunking, endpoints, and test instructions.
- `Dockerfile` - multi-stage build for Python 3.13. Builds wheels in a builder stage and installs the wheel in the runtime image.
- `.dockerignore` to exclude caches, venvs, and build artifacts.
- Terraform configuration under `terraform/` to build the Docker image using the `kreuzwerker/docker` provider:
  - `terraform/main.tf`, `terraform/variables.tf`, `terraform/README.md`.
- GitHub Actions workflow: `.github/workflows/build-and-publish.yml` that builds Docker images on push and supports manual publish and tag-triggered publish to GHCR.
- Pre-commit config `.pre-commit-config.yaml` with hooks for ruff, mypy and pydocstyle.
- `mypy.ini` updated to strict mode; `mypy` hook configured to use the project's config.

### AI & App features
- `src/pypelines/ai.py` — Chroma-backed vector store and Ollama wrapper:
  - `ChromaVectorDB` with chunking via `CharacterTextSplitter`, metadata per chunk, `add_documents`, `similarity_search`, and `export`/`import_from` JSON snapshot methods.
  - `OllamaWrapper` for LangChain's Ollama LLM integration.
- `streamlit_app.py` — Streamlit chat UI:
  - Sidebar controls for chunk size and chunk overlap with sensible defaults (1000/200).
  - File upload for text ingestion.
  - Background indexing (threadpool) for non-blocking uploads.
  - Chat UI that includes top-k similar chunks as context for the LLM.
- `src/pypelines/main.py` — FastAPI app enhancements:
  - Endpoints: `/vector/add`, `/vector/import`, `/vector/export`, `/vector/clear`, `/chat`.
- `src/pypelines/cli.py` — CLI `uv` extended with `uv test` to run pytest.
- Tests: `tests/test_ai.py` added (skips when langchain/chromadb not installed).

### CI / Dev tooling
- `README.md` updated with instructions to install dev extras, run pre-commit, run Streamlit, run the API, and tests.
- `.pre-commit-config.yaml` includes pydocstyle to enforce Google docstring style.

### Build / CI adjustments
- GitHub Actions workflows updated to operate from the `test1` subfolder (this repository is nested). CI jobs now run install/lint/typecheck/tests from `test1` and the Docker build workflow uses `test1` as the build context. This ensures pipelines run correctly when the project is not at the repository root.

- CI updated to run from the repository root and `cd` into `test1` for project-level commands. Added a `terraform` job which runs `terraform init` and `terraform validate` inside `test1/terraform`.

### Notes
- Vector DB persistence uses Chroma and persists to `CHROMA_PERSIST_DIR` or `./chroma_store`.
- Export/import uses Chroma internals to extract documents and metadatas to a JSON file; consider a more robust format for long-term compatibility.

## How to use the new features
- Install environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev,ai]'
```
- Run Streamlit UI:
```bash
streamlit run streamlit_app.py
```
- Run FastAPI server:
```bash
uv run run --reload
# or
uvicorn pypelines.main:app --reload
```
- Run tests:
```bash
uv test
```

---

> This changelog was generated automatically summarizing modifications made in the current session. Review entries before releasing.
