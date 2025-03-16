FROM python:3.13-alpine AS builder
COPY --from=ghcr.io/astral-sh/uv:0.5.26 /uv /uvx /bin/

RUN apk add --no-cache postgresql-dev gcc musl-dev

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV VIRTUAL_ENV=/app/.venv

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

FROM python:3.13-alpine
RUN apk add --no-cache postgresql-dev gcc musl-dev

WORKDIR /app
COPY . /app
COPY --from=builder --chown=app:app /app/.venv /app/.venv

EXPOSE 8000
ENV PATH="/app/.venv/bin:$PATH"

CMD ["fastapi", "run", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]
