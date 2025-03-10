lint:
	cd service && \
	uv run ruff format && \
	uv run ruff check --fix && \
	uv run mypy .

run:
	docker compose -f docker-compose.dev.yml up --build
