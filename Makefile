.SILENT:

run:
	uv run main.py

format:
	uv run black .
	uv run ruff format .

check:
	uv run black . --check
	uv run ruff check --fix .
	uv run flake8 .

test:
	uv run pytest src/tests.py
