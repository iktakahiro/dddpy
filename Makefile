VENV=.venv
PYTHON=$(VENV)/bin/python
PYTEST=$(PYTHON) -m pytest
PYREFLY=$(VENV)/bin/pyrefly
UVICORN=$(VENV)/bin/uvicorn
RUFF=$(VENV)/bin/ruff
PACKAGE=dddpy
PYREFLY_FLAGS=--summarize-errors
RUFF_FLAGS=

.PHONY: sync venv install lint typecheck test format dev

sync:
	uv sync --frozen --extra dev

venv:
	uv venv $(VENV) --allow-existing --seed

install: sync

lint: install
	$(RUFF) check . $(RUFF_FLAGS)

typecheck: install
	$(PYREFLY) check $(PYREFLY_FLAGS)

test: typecheck
	$(PYTEST) -vv 

format: install
	$(RUFF) format

dev: install
	uv run fastapi dev
