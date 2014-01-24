#!/bin/bash
# This script will run pylint for you and analyze the source code
# and see if there's any errors, warnings etc.

source env/bin/activate
pylint tests.py example/*.py feedloggr/*.py | less
