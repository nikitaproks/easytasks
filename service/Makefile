lint:
	uv run ruff format ./src && \
	uv run ruff check --fix ./src && \
	uv run mypy ./src

test:
	uv run pytest tests
