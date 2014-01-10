#!/bin/bash
# This script will run pylint for you and analyze the source code
# and see if there's any errors, warnings etc.

cd feedloggr/
pylint *.py blueprint/*.py | less
