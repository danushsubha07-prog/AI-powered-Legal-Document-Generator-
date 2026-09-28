@echo off
call .venv\Scripts\activate
python -m uvicorn legalese_api.main:app --host 127.0.0.1 --port 8000 --reload
