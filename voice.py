import httpx
from app.config import settings


async def text_to_speech(text: str) -> dict:
    """Optional ElevenLabs adapter. Returns mock metadata if keys are missing."""
    if not settings.elevenlabs_api_key or not settings.elevenlabs_voice_id:
        return {
            "mode": "mock",
            "audio_url": None,
            "message": "Add ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID to generate audio.",
        }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{settings.elevenlabs_voice_id}"
    headers = {"xi-api-key": settings.elevenlabs_api_key, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        # Production: store bytes in S3/R2 and return signed URL.
        return {"mode": "generated", "bytes": len(response.content), "message": "Audio generated. Store it in object storage in production."}
