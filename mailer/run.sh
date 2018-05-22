#!/bin/sh

rabbitmq_is_ready() {
    eval "curl -I http://${RABBITMQ_DEFAULT_USER}:${RABBITMQ_DEFAULT_PASS}@${RABBITMQ_HOST}:${RABBITMQ_MANAGEMENT_PORT}/api/vhosts"
}

count=0
until ( rabbitmq_is_ready )
do
    count=$((count+1))
    if [ ${count} -gt 62 ]
    then
        echo "$(date) - RabbitMQ didn't up in a time"
        exit 1
    fi
    sleep 1
done

echo "Starting Nameko Services..."
nameko run --config=settings.yaml mailer.services