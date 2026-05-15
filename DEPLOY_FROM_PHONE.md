# Deploy ContentForge AI Starter from your phone

Recommended cloud host: Render. The app is a FastAPI service.

## Render settings
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Environment variables
You can deploy without API keys first. It will run in mock/demo mode. Later add:
- `PEXELS_API_KEY`
- `PIXABAY_API_KEY`
- `ELEVENLABS_API_KEY`
- `SHOTSTACK_API_KEY`
- `OPENAI_API_KEY`

## Local test
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open `http://localhost:8000`.
