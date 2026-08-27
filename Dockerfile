FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends sqlite3 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt pyproject.toml README.md ./
COPY nexus ./nexus
COPY db ./db
COPY config ./config

RUN pip install --no-cache-dir -e .

RUN sqlite3 /app/nexus.db < /app/db/schema.sql || true

EXPOSE 8000
CMD ["nexus", "serve", "--host", "0.0.0.0", "--port", "8000"]
