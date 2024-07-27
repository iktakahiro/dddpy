RYE=rye
PYTEST=$(RYE) run pytest
MYPY=$(RYE) run mypy --ignore-missing-imports
UVICORN=$(RYE) run uvicorn
PACKAGE=dddpy

sync:
	$(RYE) sync

test: install  
	$(MYPY) main.py ./${PACKAGE}/
	$(PYTEST) -vv 

format:
	$(RYE) run ruff format

dev:
	${UVICORN} main:app --reload
