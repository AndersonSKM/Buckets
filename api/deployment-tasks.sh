#!bin/bash
set -eo pipefail

echo "Running deployment tasks"

python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput
