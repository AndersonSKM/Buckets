#!/bin/bash

if [ "$CI" == "true" ]; then
  cypress run --record
else
  cypress run
fi
