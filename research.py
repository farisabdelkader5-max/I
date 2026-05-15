import re
from app.models import CampaignRequest, CampaignResponse, ContentSystem, Idea, VideoPlanRequest, VideoPlanResponse, Scene
from app.services.scoring import score_idea
from app.services.storage import save_campaign, save_video_plan


def _clean_words(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z0-9]+", text.lower())
    return [w for w in words if len(w) > 2][:8]


def generate_campaign(req: CampaignRequest) -> CampaignResponse:
    base = req.niche.strip()
    base_words = _clean_words(base)
    kw = base_words or ["story", "science", "visual"]

    raw_ideas = [
        (f"Why {base} Is Stranger Than You Think", "A misconception-breaking short that starts familiar and reveals the hidden mechanism.", [*kw, "mystery", "visual", "shorts"]),
        (f"The Hidden Reason Behind {base}", "A premium documentary angle built around one surprising cause.", [*kw, "hidden", "documentary", "b-roll"]),
        (f"What If {base} Changed Overnight?", "A what-if scenario with escalating consequences and strong visual transitions.", [*kw, "what if", "future", "simulation"]),
        (f"The {base} Detail Everyone Misses", "A fast viral format focused on one overlooked visual detail.", [*kw, "detail", "close up", "viral"]),
        (f"How {base} Became So Powerful", "A chronological storytelling angle with before/after comparisons.", [*kw, "history", "scale", "before after"]),
        (f"This Is Why {base} Feels Impossible", "A high-retention hook that builds tension before explaining the truth.", [*kw, "impossible", "cinematic", "explain"]),
    ]

    def build_idea(title: str, angle: str, keywords: list[str]) -> Idea:
        score, reasons = score_idea(title, angle, keywords, base)
        hook = title.replace("Why ", "").replace("The ", "This ")
        return Idea(title=title, angle=angle, hook=f"You think you understand {base}... but one detail changes everything.", keywords=keywords, score=score, score_reasons=reasons)

    ideas = [build_idea(*idea) for idea in raw_ideas]
    ideas_sorted = sorted(ideas, key=lambda x: x.score, reverse=True)

    systems = [
        ContentSystem(
            system_name="viral_shorts",
            best_for="YouTube Shorts, TikTok, Instagram Reels",
            output_type="30-60 second vertical faceless video",
            ideas=ideas_sorted[:3],
        ),
        ContentSystem(
            system_name="documentary",
            best_for="8-12 minute YouTube documentary/explainer",
            output_type="Long-form script, storyboard, title, thumbnail, chapters",
            ideas=ideas_sorted[1:4],
        ),
        ContentSystem(
            system_name="repurpose_pack",
            best_for="Turning one theme into multiple content assets",
            output_type="1 long angle + 5 shorts + captions + community posts",
            ideas=ideas_sorted[:5],
        ),
        ContentSystem(
            system_name="trend_hunter",
            best_for="Finding weekly opportunities and evergreen questions",
            output_type="Trend questions, searchable angles, production recommendations",
            ideas=ideas_sorted[2:6],
        ),
    ]

    payload = {
        "request": req.model_dump(),
        "research_summary": f"The platform should position {base} through curiosity, visual explanation, and misconception-breaking hooks. Prioritize short, globally understandable questions, then expand winners into documentary packs.",
        "trend_questions": [
            f"Why is {base} becoming more popular now?",
            f"What do most people misunderstand about {base}?",
            f"What visual proof makes {base} instantly interesting?",
            f"Which {base} topic can become a repeatable series?",
        ],
        "systems": [s.model_dump() for s in systems],
        "recommended_first_build": "Start with Viral Shorts, then expand the winning ideas into Repurpose Packs.",
    }
    campaign_id = save_campaign(payload)
    return CampaignResponse(campaign_id=campaign_id, **{k: payload[k] for k in ["research_summary", "trend_questions", "systems", "recommended_first_build"]})


def generate_video_plan(req: VideoPlanRequest) -> VideoPlanResponse:
    title = req.selected_title.strip()
    duration = req.duration_seconds
    scene_count = 6 if duration <= 60 else 10
    step = duration / scene_count

    script_lines = [
        f"You think {title.lower()} is simple, but it is hiding something most people never notice.",
        "The first clue is visible in the way it moves, reacts, or changes under pressure.",
        "At normal speed, it looks ordinary. But when you slow it down, the pattern becomes obvious.",
        f"That is why this story matters: {req.selected_angle}",
        "The secret is not one magical detail. It is a system of small forces working together.",
        "And once you see it, you will never look at it the same way again.",
    ]

    scenes: list[Scene] = []
    for idx in range(scene_count):
        line = script_lines[idx % len(script_lines)]
        start = round(idx * step, 2)
        end = round((idx + 1) * step, 2)
        keywords = _clean_words(f"{title} {req.selected_angle}")[:5] + ["cinematic", "close up"]
        scenes.append(Scene(
            scene_number=idx + 1,
            start=start,
            end=end,
            voiceover=line,
            on_screen_text=line[:72] + ("..." if len(line) > 72 else ""),
            visual_keywords=keywords,
            visual_prompt=f"Cinematic vertical stock-style shot for: {line}. Style: {req.style}. No logos, no copyrighted characters, no identifiable private people.",
        ))

    captions = [scene.on_screen_text for scene in scenes]
    publishing_caption = f"{title} — explained in a way you cannot unsee. What should we explore next?"
    hashtags = ["#shorts", "#faceless", "#curiosity", "#documentary", "#ai"]
    payload = {
        "title": title,
        "script": "\n".join(script_lines),
        "scenes": [scene.model_dump() for scene in scenes],
        "captions": captions,
        "publishing_caption": publishing_caption,
        "hashtags": hashtags,
        "request": req.model_dump(),
    }
    video_id = save_video_plan(payload)
    return VideoPlanResponse(video_id=video_id, title=title, script=payload["script"], scenes=scenes, captions=captions, publishing_caption=publishing_caption, hashtags=hashtags)
