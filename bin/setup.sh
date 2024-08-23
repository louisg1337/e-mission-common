#!/bin/bash

echo "Creating virtual environment..."
python3 -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing pip dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Installing npm dependencies from package.json..."
npm i
