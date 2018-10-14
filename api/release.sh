#!/bin/sh
set -e

curl -sS --retry 10 --retry-max-time 30 --retry-connrefused http://0.0.0.0:${PORT}/api/health-check/
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
