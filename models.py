from typing import Literal
from pydantic import BaseModel, Field


Platform = Literal["youtube_shorts", "tiktok", "instagram_reels", "youtube_long"]
ContentSystemName = Literal["viral_shorts", "documentary", "repurpose_pack", "trend_hunter"]


class CampaignRequest(BaseModel):
    niche: str = Field(..., min_length=2, examples=["Formula 1"])
    goal: str = Field(default="Grow a faceless channel")
    platforms: list[Platform] = Field(default_factory=lambda: ["youtube_shorts"])
    language: str = Field(default="English")
    style: str = Field(default="Cinematic mysterious documentary")
    duration_seconds: int = Field(default=60, ge=15, le=720)
    audience: str = Field(default="Global English-speaking creators")


class Idea(BaseModel):
    title: str
    angle: str
    hook: str
    keywords: list[str]
    score: int
    score_reasons: list[str]


class ContentSystem(BaseModel):
    system_name: ContentSystemName
    best_for: str
    output_type: str
    ideas: list[Idea]


class CampaignResponse(BaseModel):
    campaign_id: str
    research_summary: str
    trend_questions: list[str]
    systems: list[ContentSystem]
    recommended_first_build: str


class VideoPlanRequest(BaseModel):
    campaign_id: str | None = None
    selected_title: str
    selected_angle: str
    style: str = "Cinematic mysterious documentary"
    duration_seconds: int = Field(default=60, ge=15, le=720)
    platform: Platform = "youtube_shorts"


class Scene(BaseModel):
    scene_number: int
    start: float
    end: float
    voiceover: str
    on_screen_text: str
    visual_keywords: list[str]
    visual_prompt: str


class VideoPlanResponse(BaseModel):
    video_id: str
    title: str
    script: str
    scenes: list[Scene]
    captions: list[str]
    publishing_caption: str
    hashtags: list[str]


class StockSearchRequest(BaseModel):
    query: str
    orientation: Literal["portrait", "landscape", "square"] = "portrait"
    limit: int = Field(default=6, ge=1, le=20)


class StockAsset(BaseModel):
    provider: str
    title: str
    preview_url: str
    download_url: str | None = None
    author: str | None = None
    source_url: str | None = None
    license_note: str


class RenderRequest(BaseModel):
    video_plan: VideoPlanResponse
    stock_assets: list[StockAsset] = Field(default_factory=list)


class FeedbackRequest(BaseModel):
    item_type: Literal["idea", "script", "stock_asset", "render", "campaign"]
    item_id: str | None = None
    rating: int = Field(..., ge=1, le=5)
    reason: str | None = None
    tags: list[str] = Field(default_factory=list)
