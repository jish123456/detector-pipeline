#!/usr/bin/env bash
# Set up a virtualenv, install dependencies and run the tests (Linux / WSL).
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
echo "Tests passed. Start the API with: uvicorn app.main:app --reload"
