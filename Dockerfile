# base image
FROM python:3.14.3-alpine AS base
WORKDIR /app

## set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

# dependencies
FROM node:22-alpine AS node
FROM base AS builder

## poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VERSION=2.1.1

RUN wget -qO- https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=${POETRY_CACHE_DIR} poetry install --only=main
ENV PATH="/app/.venv/bin:$PATH"

## tailwind needs node 💀
COPY --from=node /usr/lib /usr/lib
COPY --from=node /usr/local/share /usr/local/share
COPY --from=node /usr/local/lib /usr/local/lib
COPY --from=node /usr/local/include /usr/local/include
COPY --from=node /usr/local/bin /usr/local/bin

COPY ./src ./src
WORKDIR /app/src

RUN SECRET_KEY=dummy \
    python3 manage.py tailwind install && \
    python3 manage.py tailwind build && \
    python3 manage.py collectstatic --noinput


# runtime nginx image
FROM georgjung/nginx-brotli:alpine AS runtime-nginx

COPY --from=builder /app/src/static_built /var/www/html/static
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf


# runtime app image
FROM base AS runtime-app

ENV DB_ENGINE=postgresql

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY ./src ./ctm
COPY --from=builder /app/src/static_built/staticfiles*.json /app/ctm/static_built/

WORKDIR /app/ctm
EXPOSE 80
CMD ["gunicorn", "core.wsgi", "--bind 0.0.0.0:80", "--workers 3"]
