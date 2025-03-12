lint:
	cd service && \
	uv run ruff format ./src && \
	uv run ruff check --fix ./src && \
	uv run mypy ./src

run:
	docker compose -f docker-compose.dev.yml up --build

db-up:
	docker compose -f docker-compose.dev.yml up db -d

db-down:
	docker compose -f docker-compose.dev.yml down db
