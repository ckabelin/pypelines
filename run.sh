#!/usr/bin/env bash

HOST="localhost"
PORT="9090"

uv run python3 --version
uv run python3 -m streamlit run streamlit_app.py --server.port $PORT --server.address $HOST $@ 
