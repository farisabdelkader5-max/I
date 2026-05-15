import httpx
from app.config import settings
from app.models import StockAsset


MOCK_ASSETS = [
    StockAsset(
        provider="mock",
        title="Fast cinematic road motion",
        preview_url="https://images.pexels.com/videos/856973/free-video-856973.jpg",
        download_url=None,
        author="Mock provider",
        source_url=None,
        license_note="Mock asset for local testing. Replace with licensed provider result before production.",
    ),
    StockAsset(
        provider="mock",
        title="Abstract dark technology motion",
        preview_url="https://images.pexels.com/videos/3129671/free-video-3129671.jpg",
        download_url=None,
        author="Mock provider",
        source_url=None,
        license_note="Mock asset for local testing. Replace with licensed provider result before production.",
    ),
]


async def search_pexels(query: str, orientation: str, limit: int) -> list[StockAsset]:
    if not settings.pexels_api_key:
        return []
    headers = {"Authorization": settings.pexels_api_key}
    params = {"query": query, "orientation": orientation, "per_page": limit}
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get("https://api.pexels.com/videos/search", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

    assets: list[StockAsset] = []
    for item in data.get("videos", []):
        files = sorted(item.get("video_files", []), key=lambda f: f.get("width", 0), reverse=True)
        best = files[0] if files else {}
        assets.append(StockAsset(
            provider="pexels",
            title=item.get("url", "Pexels video"),
            preview_url=item.get("image", ""),
            download_url=best.get("link"),
            author=(item.get("user") or {}).get("name"),
            source_url=item.get("url"),
            license_note="Pexels result. Keep source metadata and follow Pexels API and license terms.",
        ))
    return assets


async def search_pixabay(query: str, orientation: str, limit: int) -> list[StockAsset]:
    if not settings.pixabay_api_key:
        return []
    params = {"key": settings.pixabay_api_key, "q": query, "per_page": limit, "video_type": "all"}
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get("https://pixabay.com/api/videos/", params=params)
        response.raise_for_status()
        data = response.json()

    assets: list[StockAsset] = []
    for item in data.get("hits", []):
        videos = item.get("videos", {})
        best = videos.get("large") or videos.get("medium") or videos.get("small") or {}
        assets.append(StockAsset(
            provider="pixabay",
            title=item.get("tags", "Pixabay video"),
            preview_url=item.get("picture_id", ""),
            download_url=best.get("url"),
            author=item.get("user"),
            source_url=item.get("pageURL"),
            license_note="Pixabay result. Display source where search results are shown and follow Pixabay Content License/API terms.",
        ))
    return assets


async def search_stock(query: str, orientation: str = "portrait", limit: int = 6) -> list[StockAsset]:
    results: list[StockAsset] = []
    errors: list[str] = []
    for provider in (search_pexels, search_pixabay):
        try:
            results.extend(await provider(query, orientation, limit))
        except Exception as exc:
            errors.append(str(exc))
    if results:
        return results[:limit]
    return MOCK_ASSETS[:limit]
