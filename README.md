<div align="center">

# ✈️ Flight Delay Prediction

**Full-stack ML-powered service for predicting flight delays**

[![Python](https://img.shields.io/badge/Python-3.12+-3776ab?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15-000?logo=next.js&logoColor=white)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-compose-2496ed?logo=docker&logoColor=white)](https://docs.docker.com/compose/)

</div>

---

## 📖 Overview

REST API + web UI for predicting whether a flight will be delayed, powered by **CatBoost** and **LightGBM** models trained on US domestic flight data.

| Stack | Technology |
|-------|-----------|
| **Backend** | FastAPI · SQLAlchemy 2 · Alembic · Pydantic v2 |
| **Frontend** | Next.js 15 · React 19 · TypeScript |
| **Database** | PostgreSQL 16 (async via asyncpg) |
| **ML** | CatBoost · LightGBM · scikit-learn |
| **Infra** | Docker Compose · multi-stage builds |

---

## 🤖 ML Models

Four binary classifiers predict **delayed / on time**:

| Model | Params | Highlights |
|-------|--------|-----------|
| **CatBoost Default** | iter=1000, depth=6, lr=0.065 | Baseline CatBoost |
| **CatBoost Optimized** | iter=786, depth=6, lr=0.109 | Tuned hyperparams |
| **LightGBM Default** | n_est=100, lr=0.1, leaves=31 | Baseline LightGBM |
| **LightGBM Optimized** | n_est=93, depth=9, lr=0.071, leaves=25 | Tuned hyperparams |

### Input Features

| Feature | Type | Example |
|---------|------|---------|
| `month` | int 1–12 | `7` |
| `day_of_month` | int 1–31 | `15` |
| `day_of_week` | int 1–7 | `3` |
| `dep_time` | int HHMM | `1430` |
| `carrier` | string | `"AA"` |
| `origin` | string | `"LAX"` |
| `dest` | string | `"JFK"` |
| `distance` | int (miles) | `2475` |

---

## 🚀 Quick Start

```bash
git clone https://github.com/<your-username>/api-ml.git
cd api-ml
docker compose up -d
```

| Service | URL |
|---------|-----|
| API docs | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Frontend | [http://localhost:3000](http://localhost:3000) |
| Health | [http://localhost:8000/health](http://localhost:8000/health) |

### Run Migrations

```bash
cd backend
alembic upgrade head
```

---

## 📁 Project Structure

```
flight-delay-prediction/
├── docker-compose.yml          # Orchestrates all services
├── docker/
│   └── scripts/
│       └── run.sh              # Entrypoint: migrations + uvicorn
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── alembic/                # Database migrations
│   │   ├── env.py
│   │   └── versions/
│   ├── ml/                     # Trained model files (.pkl)
│   └── src/
│       ├── main.py             # FastAPI app + lifespan
│       ├── agents/             # ML model wrappers
│       ├── api/
│       │   ├── dependencies.py # DI with Annotated
│       │   ├── router.py
│       │   └── v1/predictions.py
│       ├── core/
│       │   ├── config/         # Pydantic Settings
│       │   ├── db_helper.py    # Async DB engine & session
│       │   ├── enums/
│       │   ├── models/         # SQLAlchemy models + Base
│       │   └── schemas/        # Pydantic request/response
│       ├── dao/                # Data Access Objects
│       ├── services/           # Business logic
│       └── utils/              # Helpers (agents setup, etc.)
├── frontend/
│   ├── Dockerfile
│   ├── next.config.js
│   └── src/
│       ├── app/                # Next.js App Router
│       ├── components/         # React components
│       └── lib/api.ts          # API client
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/api/v1/models` | List loaded models |
| `POST` | `/api/v1/predictions/` | Create prediction |
| `GET` | `/api/v1/predictions/` | Prediction history |
| `GET` | `/api/v1/predictions/{id}` | Get single prediction |

### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/predictions/?model_name=catboost_default" \
  -H "Content-Type: application/json" \
  -d '{
    "month": 7,
    "day_of_month": 15,
    "day_of_week": 3,
    "dep_time": 1430,
    "carrier": "AA",
    "origin": "LAX",
    "dest": "JFK",
    "distance": 2475
  }'
```

### Example Response

```json
{
  "prediction_id": "a1b2c3d4-...",
  "delayed": false,
  "delay_probability": 0.32,
  "no_delay_probability": 0.68,
  "model_used": "catboost_default",
  "created_at": "2026-02-15T12:00:00Z"
}
```

---

## ⚙️ Environment Variables

Create `backend/.env`:

```env
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=api_ml
```

---

## 🛠 Development

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .
uvicorn src.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

## 📝 License

MIT
