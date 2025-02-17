#!/bin/bash
set -e

echo "Waiting for the database to be ready..."

while ! nc -z db 5432; do
    sleep 1
done

echo "Database is ready. Running Alembic migrations..."
cd core/db/migrations
alembic --config alembic.ini upgrade head 
cd ../../..

echo "Starting uvicorn server..."
exec uvicorn apps.app1.src.main:app --host 0.0.0.0 --port 8000 --reload