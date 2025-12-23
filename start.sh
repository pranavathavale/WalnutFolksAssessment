#!/bin/bash
set -e

echo "Starting Celery worker..."
celery -A worker worker --loglevel=info &

echo "Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 10000
