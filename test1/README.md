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

## Install and run (`uv` and `uvx`)

After installing the package, you get a small CLI wrapper `uv` that exposes convenient subcommands. `uvx` below refers to running uvicorn directly.

Install (editable) and run the CLI:

```bash
pip install -e .
# start the server using the uv CLI (wrapper around uvicorn)
uv run run --host 0.0.0.0 --port 8000 --reload
```

Run the app directly with uvicorn (referred here as `uvx`):

```bash
uvx() { uvicorn "$@"; }
# example usage:
uvx pypelines.main:app --host 0.0.0.0 --port 8000 --reload
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

## AI features (Chroma + LangChain + Ollama)

This project includes an AI chat UI and programmatic vector DB based on LangChain + Chroma.

Key components

- `src/pypelines/ai.py` — contains `ChromaVectorDB` and `OllamaWrapper`.
	- `ChromaVectorDB.add_documents(texts, metadatas=None)` — adds documents, chunks them (1000 chars, 200 overlap), and stores metadata. Each chunk receives a `chunk_index` in metadata.
	- `ChromaVectorDB.similarity_search(query, k=4)` — returns top-k matching chunks as LangChain `Document` objects.
	- `ChromaVectorDB.export(path)` / `import_from(path)` — export/import collection documents + metadatas as JSON.

- `streamlit_app.py` — Streamlit chat UI that uploads text files to the vector DB and uses `OllamaWrapper` to answer queries using the retrieved context.

- `src/pypelines/main.py` — FastAPI app with endpoints:
	- `POST /vector/add` — add a list of texts to the vector DB (JSON body: ["text1", "text2"])
	- `POST /vector/import` — upload a JSON export to import
	- `GET /vector/export` — export stored vectors/metadatas to a JSON file (path returned)
	- `POST /vector/clear` — clears persisted Chroma directory
	- `POST /chat` — post a `query` string and receive an LLM answer using retrieved context

Persistence and configuration

- Chroma persistence directory is configurable via the `CHROMA_PERSIST_DIR` env var (defaults to `./chroma_store`).
- The vector DB chunk size and overlap are in `src/pypelines/ai.py` (CharacterTextSplitter chunk_size=1000, chunk_overlap=200). Adjust as needed.

Testing the AI pieces

- Tests live in `tests/test_ai.py`. They are skipped if LangChain/Chroma are not installed.
- Run tests with:

```bash
pytest -q
```

### Run tests via CLI

You can run the test suite using the installed `uv` console script:

```bash
uv test
# or quietly
uv test --quiet
```

### Chunking parameters and background indexing

- Streamlit sidebar exposes `Chunk size` and `Chunk overlap` with healthy defaults (1000/200). Users can adjust before uploading.
- Uploaded documents are indexed in a background thread so the UI stays responsive. Background indexing uses a small threadpool and persists to Chroma.


Notes

- Chroma and HuggingFace embeddings can be resource-intensive. Consider smaller embedding models or hosted embeddings for production.
- Ollama client must be reachable; set `OLLAMA_HOST` or run a local Ollama daemon if you use a local model.

