# Sales Insight Automator

> Upload sales data (.csv / .xlsx) → AI generates an executive summary → Delivered to your inbox.

Built for **Rabbitt AI** as a quick-response tool for the sales team.

---

## Architecture

```
┌──────────────┐       POST /api/analyze       ┌──────────────┐
│   Next.js    │  ────────────────────────────▶ │   FastAPI     │
│   Frontend   │  ◀────────────────────────────  │   Backend     │
│  (React SPA) │       JSON response            │               │
└──────────────┘                                 │  ┌──────────┐ │
                                                 │  │ Groq     │ │
                                                 │  │ LLM      │ │
                                                 │  └──────────┘ │
                                                 │  ┌──────────┐ │
                                                 │  │ Resend   │ │
                                                 │  │ Email    │ │
                                                 │  └──────────┘ │
                                                 └──────────────┘
```

## Live URLs

| Service | URL |
|---------|-----|
| Frontend | https://frontend-seven-rose-42.vercel.app |
| Backend API | https://sales-insight-api-production.up.railway.app |
| Swagger Docs | https://sales-insight-api-production.up.railway.app/docs |
| ReDoc | https://sales-insight-api-production.up.railway.app/redoc |

---

## Running Locally with Docker Compose

### Prerequisites
- Docker & Docker Compose installed
- API keys for **Groq** and **Resend**

### Steps

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/rabbiittai.git
   cd rabbiittai
   ```

2. **Configure environment**
   ```bash
   cp .env.example backend/.env
   # Edit backend/.env and fill in your real API keys
   ```

3. **Spin up the stack**
   ```bash
   docker-compose up --build
   ```

4. **Access the app**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Running Without Docker

### Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in keys
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
# Create .env.local with NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

---

## API Documentation

Interactive Swagger UI is available at **`/docs`** and ReDoc at **`/redoc`** on the backend.

### `POST /api/analyze`
Upload a `.csv` or `.xlsx` file and a recipient email to generate and send an AI summary.

**Form Data:**
| Field | Type | Description |
|-------|------|-------------|
| `file` | file | `.csv` or `.xlsx` sales data |
| `email` | string | Recipient email address |

### `GET /api/health`
Health check endpoint.

---

## Security Measures

| Layer | Implementation |
|-------|---------------|
| **CORS** | Strict origin whitelisting via `ALLOWED_ORIGINS` env var. Only configured domains can call the API. |
| **Rate Limiting** | `slowapi` enforces 10 requests/minute per IP on the `/api/analyze` endpoint to prevent abuse. |
| **File Validation** | Only `.csv` and `.xlsx` extensions accepted. File content is parsed with pandas — rejects malformed data. |
| **File Size Cap** | Configurable max upload size (default 10 MB) enforced before processing. |
| **Input Sanitization** | Email validated via regex; file extensions checked server-side. |
| **No Secrets in Code** | All credentials loaded from environment variables. `.env` files are gitignored. |
| **Minimal Docker Image** | `python:3.12-slim` base, multi-stage Node build to reduce attack surface.  |

---

## CI/CD Pipeline

A GitHub Actions workflow (`.github/workflows/ci.yml`) triggers on every **Pull Request to `main`**:

1. **Backend** — Installs deps, lints with Ruff, validates imports.
2. **Frontend** — Installs deps, lints with ESLint, builds the production bundle.
3. **Docker** — Validates that both Docker images build successfully.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Next.js 15 · React 19 · Tailwind CSS 4 |
| Backend | FastAPI · Python 3.12 |
| AI Engine | Groq · Llama 3.3 70B Versatile |
| Email | Resend |
| Containerization | Docker · Docker Compose |
| CI/CD | GitHub Actions |
| Hosting | Vercel (frontend) · Render (backend) |

---

## `.env.example`

```env
GROQ_API_KEY=your_groq_api_key_here
RESEND_API_KEY=your_resend_api_key_here
FROM_EMAIL=onboarding@resend.dev
ALLOWED_ORIGINS=http://localhost:3000
MAX_UPLOAD_SIZE_MB=10
RATE_LIMIT=10/minute
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Test Data

A sample CSV file is provided at `data/sales_q1_2026.csv` for quick testing.
