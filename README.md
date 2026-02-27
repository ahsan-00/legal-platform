# Legal Document Search System — QA Test Suite

> **This repository is a fork of [AcmeAI-Git/SQA-assignment](https://github.com/AcmeAI-Git/SQA-assignment)**  
> I cloned this project, ran it locally, explored it manually, and built a complete QA test suite on top of it as part of a technical assessment for Acme AI Ltd.

---

## What I Added

- ✅ **15 automated tests** — all passing
- ✅ **8 backend tests** using Pytest + httpx
- ✅ **7 frontend tests** using Playwright (real Chromium browser)
- ✅ **7 bugs found** through manual exploration and code reading
- ✅ **HTML test report** generated via pytest-html

```
tests/
├── conftest.py        # shared fixtures and URL configuration
├── test_backend.py    # API integration + security tests
└── test_frontend.py   # end-to-end browser tests
```

---

## Bugs Found

| ID | Severity | Location | Bug |
|----|----------|----------|-----|
| CR-01 | HIGH | SearchBar.tsx | Enter key bypasses empty input validation — fires API with no user feedback |
| CR-02 | HIGH | response.py | Error responses return HTTP 200 instead of proper 4xx status codes |
| CR-03 | MEDIUM | generate_route.py | Duplicate function name — GET handler silently overwrites POST handler |
| CR-04 | MEDIUM | generate_route.py | GET /generate returns raw string `"hello"` instead of proper JSON or 405 |
| CR-05 | MEDIUM | schema.py | No max length on query field — allows unlimited input size |
| CR-06 | LOW | generate_route.py | No logging or request tracing anywhere in the backend |

---

## About the Application

The **Legal Document Search System** is a full-stack app for searching and exploring legal documents.

- **Backend:** FastAPI serving a `POST /generate` endpoint that performs keyword search over mock legal documents
- **Frontend:** React (Vite) single-page app with a search bar and results panel
- **Data:** 10 mock legal documents in `backend/app/data/mock_docs.json`

---

## Project Structure

```
SQA-assignment/
├── backend/
│   └── app/
│       ├── main.py                   # FastAPI app entry point
│       ├── routes/generate_route.py  # POST /generate endpoint
│       ├── services/generate_service.py
│       ├── models/schema.py          # Pydantic request model
│       ├── utils/response.py         # response helpers
│       └── data/mock_docs.json       # 10 mock legal documents
├── frontend/
│   └── src/
│       ├── page/HomePage.tsx
│       ├── components/home/SearchBar.tsx
│       └── hooks/useSearchPortal.ts
└── tests/
    ├── conftest.py
    ├── test_backend.py
    └── test_frontend.py
```

---

## Running the Application

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1        # Windows
pip install fastapi uvicorn
uvicorn app.main:app --reload --port 8000
# Runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
# Runs at http://localhost:3001
```

### Test the API manually

```bash
curl --location 'http://localhost:8000/generate' \
--header 'Content-Type: application/json' \
--data '{"query": "Data Protection and Privacy Act"}'
```

Example response:

```json
{
    "data": {
        "summary": "Found 1 relevant legal document(s): Data Protection and Privacy Act.",
        "matched_docs": [
            {
                "id": 1,
                "title": "Data Protection and Privacy Act",
                "content": "This act establishes the rules for collecting, storing, and processing personal data."
            }
        ]
    },
    "message": "Search completed successfully",
    "success": true,
    "status": 200
}
```

---

## Running the Tests

### Install test dependencies

```bash
pip install pytest playwright pytest-playwright httpx pytest-html
python -m playwright install
```

### Run all tests

```bash
python -m pytest tests/ -v
```

Expected output:

```
tests/test_backend.py::test_valid_query_returns_200              PASSED
tests/test_backend.py::test_valid_query_returns_matched_docs     PASSED
tests/test_backend.py::test_empty_query_returns_error            PASSED
tests/test_backend.py::test_unknown_query_returns_empty_results  PASSED
tests/test_backend.py::test_response_structure_is_correct        PASSED
tests/test_backend.py::test_sql_injection_does_not_crash_server  PASSED
tests/test_backend.py::test_xss_payload_not_reflected            PASSED
tests/test_backend.py::test_missing_query_field_returns_422      PASSED
tests/test_frontend.py::test_page_loads_and_shows_title          PASSED
tests/test_frontend.py::test_search_returns_results              PASSED
tests/test_frontend.py::test_search_with_unknown_query           PASSED
tests/test_frontend.py::test_empty_query_enter_key_no_feedback   PASSED
tests/test_frontend.py::test_search_button_disabled_when_empty   PASSED
tests/test_frontend.py::test_search_button_enabled_when_typed    PASSED
tests/test_frontend.py::test_multiple_results_returned           PASSED

15 passed in 28.85s
```

### Run with HTML report

```bash
mkdir reports
python -m pytest tests/ -v --html=reports/test_report.html --self-contained-html
# Open reports/test_report.html in your browser
```

---

## Test Coverage Summary

| File | Tests | Areas Covered |
|------|-------|---------------|
| test_backend.py | 8 | Happy path, empty query, unknown query, response structure, SQL injection, XSS, missing fields |
| test_frontend.py | 7 | Page load, search flow, no results state, empty Enter bug, button states, multiple results |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, Uvicorn |
| Frontend | React, TypeScript, Vite, Tailwind CSS |
| Backend Tests | Pytest, httpx |
| Frontend Tests | Playwright, pytest-playwright |
| Test Report | pytest-html |

---

## About

**Md. Ahsan Habib**
**QA Engineer**  

> AI assistance (Claude, Anthropic) was used during this assessment and is fully disclosed per the assignment policy. All tests were written, run, and verified by the candidate against the live application.
