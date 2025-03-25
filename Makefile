VENV=.venv
PYTEST=$(VENV)/bin/pytest
MYPY=$(VENV)/bin/mypy --ignore-missing-imports
UVICORN=$(VENV)/bin/uvicorn
RUFF=$(VENV)/bin/ruff
PACKAGE=dddpy

sync:
	uv sync

venv:
	uv venv .venv

install: venv
	uv pip install -e ".[dev]"

test: install  
	$(MYPY) main.py ./${PACKAGE}/
	$(PYTEST) -vv 

format: 
	$(RUFF) format

dev: install
	uv run fastapi dev
