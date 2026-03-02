FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*


# Install Poetry
ENV POETRY_VERSION=2.2.0
RUN curl -sSL https://install.python-poetry.org | python3 -


WORKDIR /app

COPY poetry.lock  ./
COPY pyproject.toml ./


RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

ENV PORT=10000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]