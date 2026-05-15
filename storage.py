import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import settings


def _connect() -> sqlite3.Connection:
    Path(settings.sqlite_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(settings.sqlite_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS campaigns (
                id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS video_plans (
                id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id TEXT PRIMARY KEY,
                item_type TEXT NOT NULL,
                item_id TEXT,
                rating INTEGER NOT NULL,
                reason TEXT,
                tags TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def save_campaign(payload: dict[str, Any]) -> str:
    campaign_id = f"camp_{uuid.uuid4().hex[:10]}"
    with _connect() as conn:
        conn.execute(
            "INSERT INTO campaigns (id, payload, created_at) VALUES (?, ?, ?)",
            (campaign_id, json.dumps(payload, ensure_ascii=False), now_iso()),
        )
        conn.commit()
    return campaign_id


def save_video_plan(payload: dict[str, Any]) -> str:
    video_id = f"vid_{uuid.uuid4().hex[:10]}"
    with _connect() as conn:
        conn.execute(
            "INSERT INTO video_plans (id, payload, created_at) VALUES (?, ?, ?)",
            (video_id, json.dumps(payload, ensure_ascii=False), now_iso()),
        )
        conn.commit()
    return video_id


def save_feedback(item_type: str, item_id: str | None, rating: int, reason: str | None, tags: list[str]) -> str:
    feedback_id = f"fb_{uuid.uuid4().hex[:10]}"
    created_at = now_iso()
    with _connect() as conn:
        conn.execute(
            "INSERT INTO feedback (id, item_type, item_id, rating, reason, tags, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (feedback_id, item_type, item_id, rating, reason, json.dumps(tags), created_at),
        )
        conn.commit()
    Path(settings.feedback_log_path).parent.mkdir(parents=True, exist_ok=True)
    with open(settings.feedback_log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "id": feedback_id,
            "item_type": item_type,
            "item_id": item_id,
            "rating": rating,
            "reason": reason,
            "tags": tags,
            "created_at": created_at,
        }, ensure_ascii=False) + "\n")
    return feedback_id


def get_feedback_stats() -> dict[str, Any]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT item_type, AVG(rating) as avg_rating, COUNT(*) as count FROM feedback GROUP BY item_type"
        ).fetchall()
    return {row["item_type"]: {"avg_rating": row["avg_rating"], "count": row["count"]} for row in rows}
