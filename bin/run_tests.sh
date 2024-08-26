#!/bin/bash

. setup/activate_conda.sh && conda activate emcommon

echo "Running tests..."
PYTHONPATH=./src python -m unittest discover -s test -p 'test_*.py'
