POETRY=poetry
PYTEST=$(POETRY) run pytest
MYPY=$(POETRY) run mypy --ignore-missing-imports
BLACK=$(POETRY) run black
ISORT=$(POETRY) run isort
UVICORN=$(POETRY) run uvicorn
PACKAGE=dddpy

install:
	$(POETRY) install
	$(POETRY_EXPORT)

update:
	$(POETRY) update
	$(POETRY_EXPORT)

test: install  
	$(MYPY) main.py ./${PACKAGE}/
	$(PYTEST) -vv

fmt:
	$(ISORT) main.py ./${PACKAGE} ./tests
	$(BLACK) main.py ./${PACKAGE} ./tests

dev:
	${UVICORN} main:app --reload
