#!/bin/sh
set -e

ps -ef | grep Xvfb | grep -v grep | awk '{print $2}' | xargs kill -9

cypress run
