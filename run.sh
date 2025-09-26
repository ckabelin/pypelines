#!/usr/bin/env bash

HOST="0.0.0.0"
PORT="8080"

uv run streamlit_app.py $@ --server.port $PORT --server.address $HOST