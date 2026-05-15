from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.models import CampaignRequest, VideoPlanRequest, StockSearchRequest, RenderRequest, FeedbackRequest
from app.services.research import generate_campaign, generate_video_plan
from app.services.stock import search_stock
from app.services.renderer import build_shotstack_payload
from app.services.storage import init_db, save_feedback
from app.services.learning import learning_report
from app.services.voice import text_to_speech

app = FastAPI(title="ContentForge AI Starter", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def home() -> FileResponse:
    # Works both locally and on cloud hosts where the working directory can differ.
    candidates = [
        Path(__file__).resolve().parents[1] / "frontend" / "index.html",  # backend/frontend
        Path(__file__).resolve().parents[2] / "frontend" / "index.html",  # project-root/frontend
        Path("./frontend/index.html"),
    ]
    for frontend_file in candidates:
        if frontend_file.exists():
            return FileResponse(frontend_file)
    raise RuntimeError("frontend/index.html not found")


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "product": "ContentForge AI Starter"}


@app.post("/api/campaigns/generate")
def api_generate_campaign(req: CampaignRequest):
    return generate_campaign(req)


@app.post("/api/videos/plan")
def api_video_plan(req: VideoPlanRequest):
    return generate_video_plan(req)


@app.post("/api/stock/search")
async def api_stock_search(req: StockSearchRequest):
    return {"query": req.query, "assets": await search_stock(req.query, req.orientation, req.limit)}


@app.post("/api/voiceover")
async def api_voiceover(payload: dict):
    text = payload.get("text", "")
    return await text_to_speech(text)


@app.post("/api/render/shotstack-preview")
def api_render_preview(req: RenderRequest):
    return build_shotstack_payload(req)


@app.post("/api/feedback")
def api_feedback(req: FeedbackRequest):
    feedback_id = save_feedback(req.item_type, req.item_id, req.rating, req.reason, req.tags)
    return {"feedback_id": feedback_id, "message": "Feedback saved. Learning report updated."}


@app.get("/api/learning/report")
def api_learning_report():
    return learning_report()
