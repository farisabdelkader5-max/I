from app.models import RenderRequest


def build_shotstack_payload(req: RenderRequest) -> dict:
    """Return a Shotstack-style JSON timeline. Sending to Shotstack is intentionally separate."""
    clips = []
    assets = req.stock_assets
    for i, scene in enumerate(req.video_plan.scenes):
        asset = assets[i % len(assets)] if assets else None
        background_src = asset.download_url if asset and asset.download_url else "https://cdn.example.com/replace-with-licensed-stock.mp4"
        clips.append({
            "asset": {"type": "video", "src": background_src, "volume": 0},
            "start": scene.start,
            "length": max(1, scene.end - scene.start),
            "fit": "crop",
        })
        clips.append({
            "asset": {
                "type": "title",
                "text": scene.on_screen_text,
                "style": "minimal",
                "size": "medium",
                "position": "bottom",
            },
            "start": scene.start,
            "length": max(1, scene.end - scene.start),
        })

    return {
        "timeline": {
            "soundtrack": {"src": "https://cdn.example.com/replace-with-licensed-music.mp3", "effect": "fadeOut"},
            "tracks": [{"clips": clips}],
        },
        "output": {"format": "mp4", "resolution": "hd", "aspectRatio": "9:16"},
        "metadata": {
            "title": req.video_plan.title,
            "note": "Preview render payload. Replace placeholder URLs with licensed stock, voiceover, and music before production rendering.",
        },
    }
