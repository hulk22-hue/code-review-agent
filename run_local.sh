#!/bin/bash

# Simple runner for MacOS/Linux/WSL2.
# Starts Redis, Ollama, Celery, and FastAPI in separate terminal windows.

# Start Redis
osascript -e 'tell app "Terminal" to do script "redis-server"'
sleep 1

# Start Ollama
osascript -e 'tell app "Terminal" to do script "ollama serve"'
sleep 1

# Start Celery Worker
osascript -e 'tell app "Terminal" to do script "cd '"$PWD"' && celery -A app.celery_worker.celery worker --loglevel=INFO"'
sleep 1

# Start FastAPI
osascript -e 'tell app "Terminal" to do script "cd '"$PWD"' && uvicorn app.main:app --reload"'