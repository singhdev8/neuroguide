from fastapi import APIRouter
from models import extract_emotions
from recommender import recommend
from explanation import generate_explanation

router = APIRouter()
from user_memory import save_feedback

@router.post("/feedback")
def feedback(data: dict):
    user_id = data.get("user_id", "user1")
    technique = data.get("technique")
    liked = data.get("liked", True)

    save_feedback(user_id, technique, liked)

    return {"message": "feedback saved"}
@router.post("/recommend")
def get_recommendation(data: dict):
    texts = data.get("texts", [])  # now list of inputs

    all_inputs = []

    for t in texts:
        detected = extract_emotions(t)
        all_inputs.extend(detected)

# remove duplicates
    inputs = list(set(all_inputs))

    recs = recommend(inputs, user_id="user1")

    results = []

    for r in recs:
        results.append({
            "technique": r["name"],
            "score": r["score"],
            "explanation": generate_explanation(inputs, r["name"])
        })

    return {"recommendations": results}
from collections import Counter
from user_memory import get_user_history

@router.get("/analytics")
def analytics(user_id: str = "user1"):
    history = get_user_history(user_id)

    liked = [h["technique"] for h in history if h["liked"]]
    disliked = [h["technique"] for h in history if not h["liked"]]

    liked_count = Counter(liked)
    disliked_count = Counter(disliked)

    return {
        "liked": [{"technique": k, "count": v} for k, v in liked_count.items()],
        "disliked": [{"technique": k, "count": v} for k, v in disliked_count.items()],
        "total_liked": len(liked),
        "total_disliked": len(disliked)
    }
@router.get("/insights")
def get_insights(user_id: str = "user1"):
    history = get_user_history(user_id)

    if not history:
        return {"insights": ["No user data available yet."]}

    liked = [h["technique"] for h in history if h["liked"]]
    disliked = [h["technique"] for h in history if not h["liked"]]

    insights = []

    # Pattern 1: Preference trend
    if len(liked) > len(disliked):
        insights.append("User shows a positive engagement trend with recommended techniques.")
    else:
        insights.append("User shows resistance or dissatisfaction with current recommendations.")

    # Pattern 2: Most liked technique
    if liked:
        most_liked = max(set(liked), key=liked.count)
        insights.append(f"Most preferred technique is '{most_liked}', indicating comfort with this approach.")

    # Pattern 3: Most disliked
    if disliked:
        most_disliked = max(set(disliked), key=disliked.count)
        insights.append(f"Technique '{most_disliked}' shows repeated negative feedback.")

    # Pattern 4: Behavior type
    if "Meditation" in liked or "Breathing Exercise" in liked:
        insights.append("User prefers calming and mindfulness-based interventions.")

    if "Pomodoro Technique" in liked:
        insights.append("User responds well to productivity-focused techniques.")

    if "Walking" in liked or "Exercise" in liked:
        insights.append("User benefits from physical activity-based recommendations.")

    return {"insights": insights}