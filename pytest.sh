#!/bin/bash

uv pip install pytest
uv run pytest --junitxml=pytest.junit.xml
