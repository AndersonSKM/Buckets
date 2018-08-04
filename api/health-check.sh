#!bin/sh
curl -sS --retry 10 --retry-max-time 30 --retry-connrefused http://0.0.0.0:${PORT}/api/health-check/