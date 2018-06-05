#!/bin/sh

until nc -z ${POSTGRES_HOST} ${POSTGRES_PORT}; do
    echo "$(date) - waiting for postgresql..."
    sleep 1
done

until nc -z ${RABBITMQ_HOST} ${RABBITMQ_MANAGEMENT_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 1
done

until nc -z ${REDIS_HOST} ${REDIS_PORT}; do
    echo "$(date) - waiting for redis..."
    sleep 1
done

echo "Setup django application..."
cd /app

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

echo "Starting WSGI service application..."
if [ "$DEBUG" == "true" ]; then
  /usr/local/bin/gunicorn api.wsgi -b 0.0.0.0:8000 --reload
else
  /usr/local/bin/gunicorn api.wsgi -b 0.0.0.0:8000
fi
