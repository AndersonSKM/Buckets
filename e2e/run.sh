#!/bin/sh

if $CI; then
  cypress run --env api_url=$VUE_APP_API_URL --record
else
  cypress run --env api_url=$VUE_APP_API_URL
fi
