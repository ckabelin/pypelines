"""DDD."""

import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any, List

import streamlit as st

from pypelines.ai import ChromaVectorDB, OllamaWrapper

LOGGER: logging.Logger = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

LOGGER.info("Starting Streamlit app...")

STORAGE_DIR = "./chroma_store"

MAX_WORKERS: int = 4

st.set_page_config(page_title="Quazzel", layout="wide")
st.title("Quazzel")


def _init_db(persist_dir: str, chunk_size: int, chunk_overlap: int) -> ChromaVectorDB:
    """Initialize the ChromaVectorDB with given chunking params."""
    db: ChromaVectorDB = ChromaVectorDB(persist_directory=persist_dir)
    # override splitter if needed
    db.text_splitter = db.text_splitter.__class__(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return db


# Sidebar: settings
with st.sidebar:
    st.header("Context & Documents")
    chunk_size = st.number_input(
        "Chunk size", value=1000, min_value=128, max_value=5000, step=128
    )
    chunk_overlap = st.number_input(
        "Chunk overlap", value=200, min_value=0, max_value=1000, step=50
    )
    upload = st.file_uploader(
        "Upload text files to inject into the vector DB", accept_multiple_files=True
    )
    if st.button("Clear persisted context"):
        if os.path.exists(STORAGE_DIR):
            import shutil

            shutil.rmtree(STORAGE_DIR)
            st.experimental_rerun()


# Initialize DB and LLM resources (singleton)
if "db" not in st.session_state:
    try:
        st.session_state.db = _init_db(STORAGE_DIR, chunk_size, chunk_overlap)
    except Exception as e:
        st.error(f"Vector DB init failed: {e}")
        st.session_state.db = None

if "llm" not in st.session_state:
    try:
        st.session_state.llm = OllamaWrapper()
    except Exception as e:
        st.error(f"LLM init failed: {e}")
        st.session_state.llm = None

executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)


def _index_files(files: List[Any], db: ChromaVectorDB) -> int:
    texts: list[str] = []
    for f in files:
        t: str
        try:
            t = f.getvalue().decode("utf-8")
        except Exception:
            t = f.getvalue().decode("latin-1")
        texts.append(t)
    # add documents in background
    db.add_documents(texts)
    return len(texts)


with st.sidebar:
    if upload and st.session_state.db is not None:
        future = executor.submit(_index_files, upload, st.session_state.db)
        st.info("Indexing in background...")
        st.success("Upload accepted; indexing started")


# chat UI
if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Your message", key="input")
if st.button("Send") and query:
    db = st.session_state.db
    llm = st.session_state.llm
    context = db.similarity_search(query) if db is not None else []
    context_text = "\n\n".join([d.page_content for d in context])
    prompt: str
    if context_text:
        prompt = (
            "Use the following context to answer the question:\n"
            + f"{context_text}\n\n"
            + f"User: {query}\nAssistant:"
        )
    else:
        prompt = f"User: {query}\nAssistant:"

    if llm is not None:
        with st.spinner("Generating..."):
            resp = llm.complete(prompt)
    else:
        resp = "LLM not configured"

    st.session_state.history.append((query, resp))

for q, a in st.session_state.history[::-1]:
    st.markdown(f"**User:** {q}")
    st.markdown(f"**Assistant:** {a}")

LOGGER.info("Done ...")
