#!/bin/sh

echo "Waiting PostgreSQL to be ready..."

test_postgresql() {
    pg_isready -h "$POSTGRES_HOST" -U "$POSTGRES_USER"
}

count=0
until ( test_postgresql )
do
    count=$((count+1))
    if [ ${count} -gt 62 ]
    then
        echo "$(date) - PostgreSQL didn't up in a time"
        exit 1
    fi
    sleep 1
done

echo "Creating the api database..."
psql postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT <<-EOSQL
    CREATE DATABASE $POSTGRES_DB ENCODING 'UTF-8' OWNER $POSTGRES_USER;
EOSQL

echo "Setup django application..."
cd /app

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

echo "Starting WSGI service application..."
if [ "$DEBUG" == "true" ]; then
  /usr/local/bin/gunicorn auth.wsgi -b 0.0.0.0:8000 --reload
else
  /usr/local/bin/gunicorn auth.wsgi -b 0.0.0.0:8000
fi
