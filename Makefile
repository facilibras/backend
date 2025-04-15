.PHONY: run

run:
	fastapi dev facilibras/main.py

migrate:
	alembic upgrade head

makemigrations:
	alembic revision --autogenerate -m "$(m)"

lint:
	ruff format
	ruff check --fix

test:
	pytest -v

format:
	ruff format

