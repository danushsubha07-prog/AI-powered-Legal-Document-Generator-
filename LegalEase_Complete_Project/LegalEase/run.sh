#!/usr/bin/env bash
set -e
source .venv/bin/activate
python -m uvicorn legalese_api.main:app --host 127.0.0.1 --port 8000 --reload
