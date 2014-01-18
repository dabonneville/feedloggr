#!/bin/bash

# The config file will be loaded relative from the instance folder
export FEEDLOGGR_CONFIG=testing.py
coverage run --source=feedloggr tests.py
STATUS=$?
unset FEEDLOGGR_CONFIG
exit $STATUS
