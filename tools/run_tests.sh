#!/bin/bash

source env/bin/activate
coverage run --source=feedloggr tests.py
exit $?
