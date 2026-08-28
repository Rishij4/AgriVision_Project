# AgriVision — AI-Powered Crop Disease Detection

Hackathon MVP: React + Tailwind frontend, FastAPI backend, Gemini Vision API, MongoDB + GridFS, JWT authentication, and PDF reports.

## Structure
frontend/   React + Vite UI
backend/    FastAPI API
backend/app/routes/     auth, analysis, reports
backend/app/services/   Gemini and PDF services
backend/app/db/         MongoDB + GridFS
backend/app/utils/      JWT/password helpers

## Setup
1. Install Node.js 18+, Python 3.10+, and MongoDB (local or Atlas).
2. Backend:
   cd backend
   python -m venv .venv
   .venv\Scripts\activate   (Windows)
   pip install -r requirements.txt
   copy .env.example .env
   uvicorn app.main:app --reload
3. Put your MongoDB URI, Gemini API key, and JWT secret in backend/.env.
4. Frontend:
   cd frontend
   npm install
   npm run dev

Backend: http://localhost:8000
Swagger: http://localhost:8000/docs
Frontend: http://localhost:5173

The system is an AI-assisted screening tool, not a definitive agricultural diagnosis.
