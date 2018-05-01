#!/bin/sh

rabbitmq_is_ready() {
    eval "curl -I http://${RABBITMQ_DEFAULT_USER}:${RABBITMQ_DEFAULT_PASS}@${RABBITMQ_HOST}:${RABBITMQ_MANAGEMENT_PORT}/api/vhosts"
}

i=0
while ! rabbitmq_is_ready; do
    i=`expr $i + 1`
    if [ $i -ge 10 ]; then
        echo "$(date) - rabbit still not ready, giving up"
        exit 1
    fi
    echo "$(date) - waiting for rabbit to be ready"
    sleep 3
done

echo "Starting Nameko Services..."

# Run Nameko
nameko run --config=settings.yaml mailer.services