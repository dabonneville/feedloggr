#!/bin/bash

# The config file will be loaded relative from the instance folder
export FEEDLOGGR_CONFIG=testing.py
python feedloggr/main.py test
unset FEEDLOGGR_CONFIG
