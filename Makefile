PYTHON := python3
VENV := .venv

.PHONY: help bootstrap install lint typecheck test run

help:
	@echo "Available targets: bootstrap install lint typecheck test run"

bootstrap:
	$(PYTHON) -m venv $(VENV)
	@. $(VENV)/bin/activate && pip install --upgrade pip setuptools wheel && pip install -e '.[dev]'

install:
	@. $(VENV)/bin/activate && pip install -e .

lint:
	@. $(VENV)/bin/activate && uv lint

typecheck:
	@. $(VENV)/bin/activate && uv typecheck

test:
	@. $(VENV)/bin/activate && uv test

run:
	@. $(VENV)/bin/activate && uv run run --reload
