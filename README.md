# Spending Tracker

A personal finance app to track transactions, visualize spending patterns, and get AI-powered insights.

## Stack

| Layer | Tech |
|---|---|
| Frontend | React 19, Vite, Recharts, react-markdown |
| Backend | FastAPI, SQLAlchemy, psycopg3 |
| Database | PostgreSQL 16 |
| AI | OpenAI GPT-4o-mini |
| Deployment | Docker Compose |

## Features

- Add, edit, and delete transactions (income and expenses)
- Mark transactions as subscriptions
- Filter by date range, category, and subscription status
- Stats page with spending charts
- AI insights: summarizes spending patterns and suggests savings

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL running locally

### Setup

1. Clone the repo and create a `.env` file (see [Environment Variables](#environment-variables)).

2. Set up the backend:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Start everything with the dev script from the project root:

```bash
./start-dev.sh
```

This starts PostgreSQL, the FastAPI backend on `http://localhost:8000`, and the Vite dev server on `http://localhost:5173`.

## Docker Deployment

```bash
docker compose up --build -d
```

| Service | Port |
|---|---|
| Frontend | 8082 |
| Backend | 8001 |
| Database | (internal only) |

## Environment Variables

Create a `.env` file in the project root. **Never commit this file.**

```env
POSTGRES_PASSWORD=your_postgres_password
OPENAI_API_KEY=your_openai_api_key
```

The `VITE_API_URL` for the frontend Docker build is set in `docker-compose.yml` under `args`.

## Project Structure

```
spending-tracker/
├── backend/
│   └── app/
│       ├── main.py          # FastAPI app, CORS config
│       ├── models.py        # Transaction model
│       ├── schemas.py       # Pydantic schemas
│       ├── crud.py          # Database operations
│       ├── database.py      # SQLAlchemy engine/session
│       ├── routers/
│       │   ├── transactions.py
│       │   └── ai.py
│       └── services/
│           └── ai_service.py  # OpenAI integration
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── StatsPage.jsx
│       │   └── AIInsights.jsx
│       └── components/
│           ├── TransactionForm.jsx
│           └── TransactionList.jsx
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── start-dev.sh
```
