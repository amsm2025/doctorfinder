# HMO Doctor Finder

A full-stack healthcare portfolio demo for discovering doctors by HMO network, specialty, location, patient type, rating, experience, and teleconsult availability.

## Stack
- Frontend: HTML, CSS, JavaScript
- Backend: FastAPI / Python
- API docs: Swagger / OpenAPI
- Deployment: Render

## Features
- Search doctors by HMO provider
- Specialty and location filters
- Adult / child / senior patient filters
- Teleconsult filtering
- HMO verification indicator
- Ratings and experience filters
- Appointment request workflow

## Local run

Backend:
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Frontend:
```bash
cd frontend
python -m http.server 5500
```

## Disclaimer
All doctors, clinics, HMO relationships, ratings, schedules, and availability are fictional sample data for demonstration only.
