from app.services.storage import get_feedback_stats


def score_idea(title: str, angle: str, keywords: list[str], niche: str) -> tuple[int, list[str]]:
    """Simple transparent score. Replace with ML ranking later."""
    score = 50
    reasons: list[str] = []
    title_lower = title.lower()
    angle_lower = angle.lower()

    curiosity_terms = ["why", "what if", "secret", "hidden", "strange", "mystery", "faster", "future"]
    if any(term in title_lower for term in curiosity_terms):
        score += 15
        reasons.append("Strong curiosity framing")

    if len(title.split()) <= 9:
        score += 8
        reasons.append("Short title suitable for Shorts")

    if any(term in angle_lower for term in ["misconception", "hidden", "surprising", "visual"]):
        score += 10
        reasons.append("Angle breaks a wrong/incomplete assumption")

    if 3 <= len(keywords) <= 7:
        score += 5
        reasons.append("Clear visual search keywords")

    if niche.lower() in title_lower or niche.lower().split()[0] in title_lower:
        score += 5
        reasons.append("Niche is explicit")

    # Feedback-aware lightweight improvement.
    stats = get_feedback_stats()
    idea_stats = stats.get("idea")
    if idea_stats and idea_stats["count"] >= 5:
        if idea_stats["avg_rating"] >= 4:
            score += 3
            reasons.append("Idea format has performed well in feedback")
        elif idea_stats["avg_rating"] <= 2.5:
            score -= 3
            reasons.append("Idea format needs improvement based on feedback")

    return max(1, min(100, score)), reasons or ["Baseline score"]
