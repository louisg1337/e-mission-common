#!/bin/bash
echo "Running tests..."
PYTHONPATH=./src python -m unittest discover -s src/emcommon/tests -p 'test_*.py'
