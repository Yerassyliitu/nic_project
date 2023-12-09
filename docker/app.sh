#!/bin/bash
echo "Waiting for 3 seconds..."
sleep 3

# Выполните миграции базы данных

alembic upgrade head

# Запустите приложение с Gunicorn и Uvicorn
gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT

