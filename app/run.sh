#!/bin/bash
set -eo pipefail

python3 manage.py collectstatic --noinput

if [ "$DEBUG" == "true" ]; then
  /usr/local/bin/gunicorn api.wsgi -b 0.0.0.0:${PORT} --reload & yarn --cwd=/app/client/ serve --port ${NODE_PORT} && fg
else
  /usr/local/bin/gunicorn api.wsgi -b 0.0.0.0:${PORT}
fi
