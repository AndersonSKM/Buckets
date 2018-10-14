#!/bin/sh
set -e

python3 manage.py collectstatic --noinput

if [ "$DEBUG" == "True" ]; then
  /usr/local/bin/gunicorn api.wsgi -b 0.0.0.0:${PORT} --reload
else
  /usr/local/bin/gunicorn api.wsgi -b 0.0.0.0:${PORT}
fi
