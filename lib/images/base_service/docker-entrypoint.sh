#!/bin/sh

echo "Waiting RabbitMQ to be ready..."

rabbitmq_is_ready() {
    eval "curl -I ${RABBITMQ_CTL_URI}/api/vhosts"
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

cd /app
nameko run --config=config.yml mailer.services