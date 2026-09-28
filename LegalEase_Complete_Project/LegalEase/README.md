# LegalEase — AI-Powered Legal Document Generator

LegalEase is a complete local web application based on the supplied project documentation. It uses **Streamlit** for the UI, **FastAPI** for the backend API, **Google Gemini** for document generation, and Python document utilities for TXT/DOCX/PDF export.

> **Important:** LegalEase is a drafting/education tool, not a law firm or a substitute for a qualified lawyer. AI output can contain errors. Review documents for the applicable jurisdiction before signing or relying on them.

## Architecture

```text
Streamlit Frontend
       |
       | POST /generate
       v
FastAPI Backend
       |
       v
GeminiDocumentGenerator
       |
       v
Google Gemini API
       |
       v
Generated legal text
       |
       +--> TXT
       +--> DOCX
       +--> PDF
```

## Project structure

```text
LegalEase/
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
├── assets/
│   └── logo.png
├── frontend/
│   └── app.py
├── legalese_api/
│   ├── __init__.py
│   ├── main.py
│   └── routes.py
├── tests/
│   ├── test_api.py
│   └── test_formats.py
├── utils/
│   ├── __init__.py
│   ├── document_formatters.py
│   └── text_utils.py
├── .env.example
├── .gitignore
├── config.py
├── requirements.txt
└── README.md
```

## Windows + VS Code setup

### 1. Open the folder

Open `LegalEase` in VS Code.

### 2. Create a virtual environment

PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create `.env`

Copy `.env.example` to `.env` and put your Gemini API key in:

```text
GEMINI_API_KEY=your_real_key
```

For real AI generation, use `DEMO_MODE=false` after adding the key. If you leave `DEMO_MODE=true`, the app still runs without an API key using a local deterministic draft generator, which is useful for UI/export testing.

### 5. Start the FastAPI backend

Terminal 1:

```powershell
python -m uvicorn legalese_api.main:app --host 127.0.0.1 --port 8000 --reload
```

Open:

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

### 6. Start Streamlit

Terminal 2:

```powershell
streamlit run frontend/app.py
```

Open the URL Streamlit prints, normally `http://localhost:8501`.

## Quick test without Gemini

Keep `DEMO_MODE=true`. Start both servers, enter a document type such as `Freelance Work Contract`, parties, terms separated by semicolons, and an effective date. Click **Generate Document**. You can edit the result and download TXT, DOCX and PDF.

## Test suite

With the virtual environment active:

```powershell
pytest -q
```

The tests cover API validation/health and document export functions without requiring a Gemini key.

## Real Gemini mode

Set:

```text
DEMO_MODE=false
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-3.8-flash
```

Then restart FastAPI. The backend creates a Google GenAI client and calls Gemini's `generate_content` interface.

If your Google account does not have access to the configured model, change `GEMINI_MODEL` to a model available to your account.

## API example

```http
POST http://127.0.0.1:8000/generate
Content-Type: application/json
```

```json
{
  "document_type": "Non-Disclosure Agreement",
  "parties": "Jane Doe (Disclosing Party), TechNova Inc. (Receiving Party)",
  "terms": "Confidential information must be protected; Disclosure is limited to authorized personnel; Agreement may be terminated with 30 days notice",
  "dates": "September 27, 2026",
  "jurisdiction": "India",
  "language": "English"
}
```

## Features implemented

- Streamlit responsive UI
- FastAPI REST backend
- Pydantic request validation
- Google Gemini integration using the current `google-genai` SDK
- Demo/offline mode for development
- Structured prompt with user-controlled document fields
- Editable preview
- TXT export
- DOCX export with Times New Roman styling, title, parties/terms table and footer
- PDF export with branded header/footer
- Input length validation
- Error handling and health endpoint
- API documentation through FastAPI Swagger/OpenAPI
- Automated tests

## Notes about the supplied specification

The supplied documentation names `gemini-1.5-pro` and the older `google-generativeai` SDK. Those choices are retained conceptually but updated in this implementation because the current Google Gemini documentation uses the `google-genai` Python SDK and current model IDs. The application keeps the original architecture: Streamlit → FastAPI → Gemini → TXT/DOCX/PDF.
