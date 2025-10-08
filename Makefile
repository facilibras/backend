.PHONY: run

run:
	fastapi dev facilibras/main.py

initdb:
	python -m scripts.iniciar_db

lint:
	ruff format
	ruff check --fix

test:
	pytest -v

format:
	ruff format

