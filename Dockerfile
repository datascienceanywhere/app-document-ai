FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*


# Install Poetry
ENV POETRY_VERSION=2.2.0
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to Path
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY poetry.lock  ./
COPY pyproject.toml ./


RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

ENV PORT=10000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]