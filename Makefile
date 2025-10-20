.PHONY: run

DB_NAME = facilibras

run:
	fastapi dev facilibras/main.py

initdb:
	python -m scripts.iniciar_db

resetdb:
	psql -c "DROP DATABASE $(DB_NAME);" || true
	psql -c "CREATE DATABASE $(DB_NAME);"
	python -m scripts.iniciar_db

cleanrun:
	psql -c "DROP DATABASE $(DB_NAME);" || true
	psql -c "CREATE DATABASE $(DB_NAME);"
	python -m scripts.iniciar_db
	fastapi dev facilibras/main.py

format:
	ruff format

lint:
	ruff format
	ruff check --fix

test:
	pytest -v

