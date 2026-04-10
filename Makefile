VENV=.venv
PYTEST=$(VENV)/bin/pytest
PYREFLY=$(VENV)/bin/pyrefly
UVICORN=$(VENV)/bin/uvicorn
RUFF=$(VENV)/bin/ruff
PACKAGE=dddpy
PYREFLY_FLAGS=--summarize-errors

sync:
	uv sync

venv:
	uv venv $(VENV) --allow-existing --seed

install: venv
	uv pip install -e ".[dev]" --python $(VENV)/bin/python

typecheck: install
	$(PYREFLY) check $(PYREFLY_FLAGS)

test: typecheck
	$(PYTEST) -vv 

format: 
	$(RUFF) format

dev: install
	uv run fastapi dev
