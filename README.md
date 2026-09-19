# AI-Powered Smart Email Assistant

A full-stack, AI-powered email workspace automation web application that secure connects to Google Gmail using OAuth 2.0 and processes inbox management using NLP and the Gemini Generative AI API.

This application classifies incoming messages, determines action items, extracts meetings or calendar deadlines, performs OCR text extraction from PDF attachments, schedules queue replies, and renders visual analytics.

---

## Technical Stack

- **Backend:** Python 3.11/3.13, FastAPI, Gmail API, Google Generative AI (Gemini 1.5 Flash), PyPDF (text extractor), Motor (Async MongoDB Driver).
- **Frontend:** React (Vite SPA template), Tailwind CSS, Framer Motion (micro-animations), Recharts (data visualization), Axios (REST API mappings).
- **Database:** MongoDB (Local container or MongoDB Atlas Cloud).

---

## Highlight Features

1. **Zero-Config Demo Mode (Fallback sandbox):** Runs out-of-the-box. If Gmail/Google credentials are not set, it simulates a highly realistic email account, sync activities, ML classifications, OCR text extracts, and interactive chats.
2. **AI Email Summarizer:** Extracts key points, deadlines, meeting slots, and urgency.
3. **Smart Priority badge routing:** High (Red), Medium (Orange), Low (Green) urgency indicators.
4. **Interactive OCR Scanner:** Scans PDF file attachments and outputs summaries.
5. **Smart Auto-Repliers:** Draft responses matching tones (Friendly, Professional, Formal) and queue scheduled replies.
6. **Smart Natural Search:** Type plain English searches like "Emails from HR" or "amazon orders".
7. **Analytics widgets:** Pie charts for category shares, bar/line charts for weekly sync load, top senders.

---

## Directory Architecture

```
smart-email-assistant/
  ├── backend/
  │   ├── app/
  │   │   ├── auth/          # JWT and User profile middleware resolvers
  │   │   ├── database/      # Motor database client and mock cache fallbacks
  │   │   ├── models/        # Pydantic schemas (Emails, Notifications, Logs)
  │   │   ├── routes/        # Router controllers (Auth, Emails, Analytics, Admin)
  │   │   ├── services/      # Gmail API, Gemini AI connection, OCR extraction
  │   │   ├── config.py      # Env validations and Demo toggles
  │   │   └── main.py        # FastAPI orchestrator
  │   ├── requirements.txt   # Python deps
  │   └── Dockerfile         # Backend compilation recipe
  ├── frontend/
  │   ├── src/
  │   │   ├── components/    # Layout sidebars and navigation panels
  │   │   ├── pages/         # Landing, Inbox, Details, Spam, Analytics, Admin
  │   │   ├── services/      # Axios API endpoint client
  │   │   ├── App.jsx        # Routing shell and toast notifications toaster
  │   │   ├── main.jsx       # DOM mounter
  │   │   └── index.css      # Core Design system class and glass styles
  │   ├── package.json       # React SPA deps
  │   ├── tailwind.config.js # Dark mode and colors preferences
  │   └── Dockerfile         # Frontend deployment build recipe
  ├── docker-compose.yml     # local Mongo container configurations
  └── README.md              # Documentation guide
```

---

## Quick Start Setup (Without Docker)

### 1. Configure backend environment

In `backend/.env`, set `DEMO_MODE=True` for sandbox evaluation:

```env
MONGO_URI=mongodb://localhost:27017/smart_email_db
JWT_SECRET=super_secret_jwt_key_123_change_me
ACCESS_TOKEN_EXPIRE_MINUTES=1440
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/callback
GEMINI_API_KEY=your-gemini-api-key
DEMO_MODE=True
```

### 2. Run backend FastAPI server

Ensure you have Python 3.11+ installed. Run from `/backend`:

```bash
cd backend
python -m venv venv
# Windows powershell:
.\venv\Scripts\Activate.ps1
# Mac/Linux terminal:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
- API Docs URL: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger OpenAPI specifications).

### 3. Run frontend Vite server

From `/frontend`, download dependencies and start Vite dev server:

```bash
cd frontend
npm install
npm run dev
```
- Dashboard URL: [http://localhost:5173](http://localhost:5173)

---

## Quick Start Setup (With Docker)

To spin up Frontend, Backend, and a local MongoDB instance in unified network bridge mode, run in workspace root directory:

```bash
docker-compose up --build
```
This serves the application globally:
- Frontend Client: [http://localhost:5173](http://localhost:5173)
- Backend REST API: [http://localhost:8000](http://localhost:8000)
- API OpenAPI Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Local MongoDB Instance: `mongodb://localhost:27017/`
