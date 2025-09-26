#!/usr/bin/env bash

export HOST="localhost"
export PORT="9090"

export LLM_MODEL_CONV="gpt-oss:20b"
export LLM_MODEL_EMB="snowflake-arctic-embed2"

ollama pull ${LLM_MODEL_EMB}
ollama pull ${LLM_MODEL_CONV}

uv run python3 --version
uv run python3 -m streamlit run streamlit_app.py --server.port $PORT --server.address $HOST $@
