#!/bin/sh

until nc -z ${RABBITMQ_HOST} ${RABBITMQ_MANAGEMENT_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 1
done

cd /app
nameko run --config=config.yml mailer.services