RYE=rye
PYTEST=$(RYE) run pytest
MYPY=$(RYE) run mypy --ignore-missing-imports
BLACK=$(RYE) run black
ISORT=$(RYE) run isort
PYLINT=$(RYE) run pylint
UVICORN=$(RYE) run uvicorn
PACKAGE=dddpy

install:
	$(RYE) sync
	$(POETRY_EXPORT)

update:
	$(POETRY) sync

test: install  
	$(MYPY) main.py ./${PACKAGE}/
	$(PYTEST) -vv

fmt:
	$(ISORT) main.py ./${PACKAGE} ./tests
	$(BLACK) main.py ./${PACKAGE} ./tests

lint:
	$(PYLINT) main.py ./${PACKAGE} ./tests

dev:
	${UVICORN} main:app --reload
