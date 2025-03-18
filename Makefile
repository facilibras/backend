.PHONY: run

run:
	fastapi dev facilibras/main.py

lint:
	ruff format
	ruff check --fix

test:
	pytest -v

format:
	ruff format

