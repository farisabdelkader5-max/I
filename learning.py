from app.services.storage import get_feedback_stats


def learning_report() -> dict:
    stats = get_feedback_stats()
    recommendations = []
    idea_stats = stats.get("idea")
    if not idea_stats:
        recommendations.append("Collect at least 20 idea ratings before changing ranking weights.")
    elif idea_stats["avg_rating"] < 3:
        recommendations.append("Idea scores are weak. Increase weight for curiosity framing and reduce generic titles.")
    else:
        recommendations.append("Idea feedback is positive. Start A/B testing hook templates.")

    script_stats = stats.get("script")
    if script_stats and script_stats["avg_rating"] < 3:
        recommendations.append("Scripts need stronger first 3 seconds and more visual proof.")

    return {
        "feedback_stats": stats,
        "self_improvement_mode": "human-approved learning loop",
        "what_improves_automatically": [
            "idea ranking weights",
            "preferred hooks",
            "stock keyword choices",
            "style presets",
            "cost/performance routing",
        ],
        "what_needs_approval": [
            "code changes",
            "new providers",
            "policy changes",
            "publishing without review",
        ],
        "recommendations": recommendations,
    }
