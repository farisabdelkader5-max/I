from __future__ import annotations

import uuid
from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="ContentForge AI Starter", version="0.2.0-phone-fixed")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Platform = Literal["youtube_shorts", "tiktok", "instagram_reels", "youtube_long"]


class CampaignRequest(BaseModel):
    niche: str = Field(..., min_length=2)
    goal: str = "Grow a faceless channel"
    platform: Platform = "youtube_shorts"
    language: str = "English"
    style: str = "Cinematic mysterious documentary"
    duration_seconds: int = Field(default=60, ge=15, le=720)
    audience: str = "Global English-speaking creators"


class VideoPlanRequest(BaseModel):
    title: str
    angle: str = "A curiosity-driven faceless video"
    style: str = "Cinematic mysterious documentary"
    duration_seconds: int = Field(default=60, ge=15, le=720)
    platform: Platform = "youtube_shorts"


class FeedbackRequest(BaseModel):
    item_type: str = "campaign"
    item_id: str | None = None
    rating: int = Field(..., ge=1, le=5)
    reason: str | None = None


HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ContentForge AI Starter</title>
  <style>
    body { font-family: Arial, sans-serif; background:#0f172a; color:#e5e7eb; margin:0; padding:24px; }
    .wrap { max-width: 920px; margin: auto; }
    .card { background:#111827; border:1px solid #334155; border-radius:18px; padding:20px; margin:16px 0; }
    input, select, textarea { width:100%; box-sizing:border-box; padding:12px; border-radius:12px; border:1px solid #475569; background:#020617; color:#e5e7eb; margin:8px 0 14px; }
    button { background:#22c55e; color:#04130a; font-weight:bold; border:0; border-radius:12px; padding:13px 18px; cursor:pointer; }
    pre { white-space:pre-wrap; overflow:auto; background:#020617; padding:16px; border-radius:12px; border:1px solid #1f2937; }
    h1 { margin-bottom:4px; }
    .muted { color:#94a3b8; }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>ContentForge AI Starter</h1>
    <p class="muted">Research → content systems → video plan → stock suggestions → render preview.</p>
    <div class="card">
      <h2>Create Content Campaign</h2>
      <label>Niche</label>
      <input id="niche" value="Formula 1" />
      <label>Goal</label>
      <input id="goal" value="Create viral faceless curiosity videos" />
      <label>Platform</label>
      <select id="platform">
        <option value="youtube_shorts">YouTube Shorts</option>
        <option value="tiktok">TikTok</option>
        <option value="instagram_reels">Instagram Reels</option>
        <option value="youtube_long">YouTube Long Form</option>
      </select>
      <label>Style</label>
      <input id="style" value="Cinematic mysterious documentary" />
      <label>Duration seconds</label>
      <input id="duration" type="number" value="60" />
      <button onclick="generateCampaign()">Research & Generate Systems</button>
    </div>
    <div class="card">
      <h2>Output</h2>
      <pre id="output">Ready.</pre>
    </div>
  </div>
<script>
async function postJSON(url, data) {
  const res = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)});
  return await res.json();
}
async function generateCampaign() {
  const data = {
    niche: document.getElementById('niche').value,
    goal: document.getElementById('goal').value,
    platform: document.getElementById('platform').value,
    style: document.getElementById('style').value,
    duration_seconds: Number(document.getElementById('duration').value || 60),
    language: 'English'
  };
  document.getElementById('output').textContent = 'Generating...';
  const campaign = await postJSON('/api/campaigns/generate', data);
  const firstIdea = campaign.systems[0].ideas[0];
  const plan = await postJSON('/api/videos/plan', {
    title: firstIdea.title,
    angle: firstIdea.angle,
    style: data.style,
    duration_seconds: data.duration_seconds,
    platform: data.platform
  });
  const stock = await postJSON('/api/stock/search', {query: plan.scenes[0].visual_keywords.join(' '), orientation:'portrait', limit:4});
  const render = await postJSON('/api/render/preview', {video_plan: plan, stock_assets: stock.assets});
  document.getElementById('output').textContent = JSON.stringify({campaign, plan, stock, render}, null, 2);
}
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return HTML


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "product": "ContentForge AI Starter"}


@app.post("/api/campaigns/generate")
def generate_campaign(req: CampaignRequest) -> dict:
    base = req.niche.strip()
    campaign_id = str(uuid.uuid4())
    ideas_raw = [
        (
            f"Why {base} Is Stranger Than You Think",
            "A misconception-breaking short that starts with something familiar, then reveals the hidden mechanism.",
            [base, "mystery", "visual", "shorts"],
            92,
        ),
        (
            f"The Hidden Reason Behind {base}",
            "A premium documentary angle built around one surprising cause.",
            [base, "hidden", "documentary", "b-roll"],
            88,
        ),
        (
            f"What If {base} Changed Overnight?",
            "A what-if scenario with escalating consequences and strong visual transitions.",
            [base, "what if", "future", "simulation"],
            85,
        ),
        (
            f"The {base} Detail Everyone Misses",
            "A fast viral format focused on one overlooked visual detail.",
            [base, "detail", "close up", "viral"],
            83,
        ),
    ]
    ideas = [
        {
            "title": title,
            "angle": angle,
            "hook": f"You think you understand {base}... but one detail changes everything.",
            "keywords": keywords,
            "score": score,
            "score_reasons": ["strong curiosity gap", "clear visual potential", "easy to turn into a short"],
        }
        for title, angle, keywords, score in ideas_raw
    ]
    systems = [
        {"system_name": "viral_shorts", "best_for": "YouTube Shorts, TikTok, Instagram Reels", "output_type": "30-60 second vertical faceless video", "ideas": ideas[:3]},
        {"system_name": "documentary", "best_for": "8-12 minute YouTube documentary/explainer", "output_type": "Long-form script, storyboard, thumbnail idea, description", "ideas": ideas[1:]},
        {"system_name": "repurpose_pack", "best_for": "Turning one theme into many content assets", "output_type": "1 long angle + 5 shorts + captions + community posts", "ideas": ideas},
        {"system_name": "trend_hunter", "best_for": "Finding weekly opportunities and evergreen questions", "output_type": "Trend questions, searchable angles, production recommendations", "ideas": ideas[2:]},
    ]
    return {
        "campaign_id": campaign_id,
        "research_summary": f"Position {base} through curiosity, visual explanation, and misconception-breaking hooks. Start with short, globally understandable questions, then expand winners into documentary packs.",
        "trend_questions": [
            f"Why is {base} interesting right now?",
            f"What do most people misunderstand about {base}?",
            f"What visual proof makes {base} instantly interesting?",
            f"Which {base} topic can become a repeatable series?",
        ],
        "systems": systems,
        "recommended_first_build": "Start with Viral Shorts, then expand winning ideas into Repurpose Packs.",
    }


@app.post("/api/videos/plan")
def generate_video_plan(req: VideoPlanRequest) -> dict:
    duration = req.duration_seconds
    scene_count = 6 if duration <= 60 else 10
    step = duration / scene_count
    script_lines = [
        f"You think {req.title.lower()} is simple, but it is hiding something most people never notice.",
        "The first clue is visible in the way it moves, reacts, or changes under pressure.",
        "At normal speed, it looks ordinary. But when you slow it down, the pattern becomes obvious.",
        f"That is why this story matters: {req.angle}",
        "The secret is not one magical detail. It is a system of small forces working together.",
        "And once you see it, you will never look at it the same way again.",
    ]
    scenes = []
    for idx in range(scene_count):
        line = script_lines[idx % len(script_lines)]
        start = round(idx * step, 2)
        end = round((idx + 1) * step, 2)
        scenes.append(
            {
                "scene_number": idx + 1,
                "start": start,
                "end": end,
                "voiceover": line,
                "on_screen_text": line[:72] + ("..." if len(line) > 72 else ""),
                "visual_keywords": [req.title, "cinematic", "close up", "vertical video", "no logos"],
                "visual_prompt": f"Cinematic vertical stock-style shot for: {line}. Style: {req.style}. No logos, no copyrighted characters.",
            }
        )
    return {
        "video_id": str(uuid.uuid4()),
        "title": req.title,
        "script": "\n".join(script_lines),
        "scenes": scenes,
        "captions": [scene["on_screen_text"] for scene in scenes],
        "publishing_caption": f"{req.title} — explained in a way you cannot unsee. What should we explore next?",
        "hashtags": ["#shorts", "#faceless", "#curiosity", "#documentary", "#ai"],
    }


@app.post("/api/stock/search")
def search_stock(payload: dict) -> dict:
    query = payload.get("query", "cinematic stock video")
    limit = int(payload.get("limit", 4))
    assets = [
        {
            "provider": "mock-stock",
            "title": f"Stock option {i + 1}: {query}",
            "preview_url": "https://example.com/preview.mp4",
            "download_url": None,
            "author": "Mock provider",
            "source_url": "https://example.com",
            "license_note": "Demo only. Connect Pexels/Pixabay/Storyblocks API for real licensed assets.",
        }
        for i in range(limit)
    ]
    return {"query": query, "assets": assets}


@app.post("/api/render/preview")
def render_preview(payload: dict) -> dict:
    scenes = payload.get("video_plan", {}).get("scenes", [])
    timeline = [
        {
            "scene": scene.get("scene_number"),
            "start": scene.get("start"),
            "end": scene.get("end"),
            "caption": scene.get("on_screen_text"),
            "visual_keywords": scene.get("visual_keywords"),
        }
        for scene in scenes
    ]
    return {
        "renderer": "mock-shotstack-json-preview",
        "status": "ready_for_real_renderer_integration",
        "timeline": timeline,
    }


@app.post("/api/feedback")
def save_feedback(req: FeedbackRequest) -> dict:
    return {
        "feedback_id": str(uuid.uuid4()),
        "message": "Feedback saved in demo mode. Production version should save this to Postgres/Supabase.",
        "feedback": req.model_dump(),
    }


@app.get("/api/learning/report")
def learning_report() -> dict:
    return {
        "mode": "demo",
        "how_it_learns": [
            "Track which ideas users choose",
            "Track feedback ratings",
            "Improve scoring weights",
            "Version prompts with human approval",
        ],
        "warning": "Self-changing production code without review is not enabled.",
    }
