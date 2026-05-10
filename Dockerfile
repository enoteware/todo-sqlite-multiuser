FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     TODO_DB_PATH=/data/todo.sqlite3

WORKDIR /app

COPY pyproject.toml README.md ./
COPY app ./app
COPY templates ./templates
COPY static ./static
COPY DESIGN.md ./DESIGN.md

RUN pip install --no-cache-dir -e .

RUN mkdir -p /data
VOLUME ["/data"]

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
