# ContentForge AI Starter

A runnable starter blueprint for an AI content research + stock-video studio.

## What this starter does

- Accepts a niche, platform, goal, language and style.
- Generates multiple content systems: Viral Shorts, Documentary Angle, Repurpose Pack.
- Scores ideas using a simple learning-aware scoring engine.
- Builds a scene-by-scene video plan.
- Searches stock video providers if API keys are provided; otherwise uses mock examples.
- Produces a Shotstack-compatible render payload preview.
- Saves user feedback locally so the scoring engine can improve over time.

## What this starter does NOT do yet

- It does not ship a production-grade paid SaaS by itself.
- It does not train a new video model.
- It does not bypass paid platforms, scrape YouTube videos, or reuse copyrighted clips.
- It does not let the system change its own code automatically. Learning is implemented through feedback, prompt versions, scoring weights, and analytics.

## Quick start

### Option A: Docker

```bash
docker compose up --build
```

Then open:

```text
http://localhost:8000
```

### Option B: Python

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open:

```text
http://localhost:8000
```

## Environment variables

Copy `.env.example` to `.env` and fill what you have:

```bash
cp .env.example .env
```

The app runs in mock mode without keys.

## Recommended next production steps

1. Replace the local SQLite database with Postgres/Supabase.
2. Add real auth: Clerk, Supabase Auth, or Auth.js.
3. Add payments and credit accounting.
4. Add queue workers for video rendering jobs.
5. Add object storage: Cloudflare R2/S3.
6. Add human review before publishing.
7. Add provider cost tracking.
8. Add proper legal terms for stock/video use.

## Folder structure

```text
backend/app/main.py                 FastAPI app and routes
backend/app/services/research.py    Research and content system generation
backend/app/services/stock.py       Pexels/Pixabay stock adapters
backend/app/services/scoring.py     Idea scoring + feedback-weighted learning
backend/app/services/renderer.py    Shotstack JSON render payload generator
backend/app/services/voice.py       Voiceover adapter placeholder
backend/app/services/storage.py     Local SQLite + JSONL persistence
frontend/index.html                 Simple working UI served by FastAPI

docs/competitor_analysis.md         Competitor analysis and product strategy
docs/product_blueprint.md           Platform blueprint and roadmap
```
