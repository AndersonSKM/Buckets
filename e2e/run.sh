#!/bin/sh
set -e

if $CI; then
  cypress run --record
else
  cypress run
fi
