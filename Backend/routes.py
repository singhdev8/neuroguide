from fastapi import APIRouter
from models import extract_emotions, reload_concepts
from recommender import recommend
from explanation import generate_explanation
from kg_engine import save_technique_to_graph, add_aliases_to_node
import httpx
import os
import re
from dotenv import load_dotenv
from collections import Counter
from user_memory import save_feedback, get_user_history
from database import get_session

load_dotenv()
router = APIRouter()


def get_existing_aliases(node_name):
    session = get_session()
    result = session.run(
        "MATCH (n {name: $name}) RETURN coalesce(n.aliases, []) AS aliases",
        name=node_name
    ).single()
    return list(result["aliases"]) if result else []


@router.post("/feedback")
def feedback(data: dict):
    user_id = data.get("user_id", "user1")
    technique = data.get("technique")
    liked = data.get("liked", True)
    save_feedback(user_id, technique, liked)
    return {"message": "feedback saved"}


@router.post("/recommend")
def get_recommendation(data: dict):
    texts = data.get("texts", [])
    all_inputs = []

    for t in texts:
        detected = extract_emotions(t)
        all_inputs.extend(detected)

    inputs = list(set(all_inputs))
    recs = recommend(inputs, user_id="user1")

    results = []
    for r in recs:
        results.append({
            "technique": r["name"],
            "score": round(r["score"], 1),
            "explanation": generate_explanation(inputs, r["name"])
        })

    if not results:
        return {"recommendations": [], "fallback": True, "query": texts[0] if texts else ""}
    return {"recommendations": results, "fallback": False}


@router.post("/ai-fallback")
async def ai_fallback(data: dict):
    query = data.get("query", "")
    api_key = os.getenv("GROQ_API_KEY")

    # Block non-wellness queries before calling Groq
    unrelated_keywords = [
        "movie", "movies", "film", "netflix", "series", "show", "anime",
        "recipe", "food", "cook", "coding", "code", "programming",
        "song", "music", "game", "games", "sport", "cricket", "football",
        "suggest", "recommend me", "tell me about", "who is", "what is"
    ]
    query_lower = query.lower()
    if any(word in query_lower for word in unrelated_keywords):
        return {
            "answer": "I can only help with mental health and wellness topics. Please describe how you are feeling emotionally or physically 💙",
            "source": "ai"
        }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system",
                        "content": """You are a mental wellness assistant for an app called NeuroGuide.
First check if the user's message is related to mental health, emotions, physical symptoms, or wellbeing.

If NOT related to mental health (e.g. movie suggestions, coding, recipes etc):
Respond with exactly:
SYMPTOM: Unrelated
Sorry, I can only help with mental health and wellness related topics. Please describe how you are feeling emotionally or physically.

If YES related to mental health:
First line MUST be: SYMPTOM: <one short keyword only e.g. Dizziness, Loneliness, Grief>
The keyword must be a single word or two words max.
Then suggest 2-3 practical evidence-based wellness techniques in this format:
1. Technique Name: description
2. Technique Name: description
3. Technique Name: description
IMPORTANT: Technique names must have spaces between words. Never use CamelCase.
Be concise and compassionate."""
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                "max_tokens": 500
            },
            timeout=30.0
        )

    result = response.json()
    full_text = result["choices"][0]["message"]["content"]

    lines = full_text.split("\n")
    print("FIRST LINE FROM GROQ:", lines[0])

    symptom_keyword = "General"
    clean_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("SYMPTOM:"):
            symptom_keyword = stripped.replace("SYMPTOM:", "").strip().title()
        else:
            if stripped:
                clean_lines.append(stripped)

    text = "\n".join(clean_lines).strip()

    # Don't save to graph if unrelated query
    if symptom_keyword == "Unrelated":
        return {"answer": text, "source": "ai"}

    # Save techniques to Neo4j
    saved = set()
    for line in clean_lines:
        line = line.strip()
        if line and any(char.isalpha() for char in line):
            raw = line.lstrip("0123456789.-* ").split(":")[0].strip("* ")
            raw = re.sub(r'([A-Z][a-z])', r' \1', raw).strip()
            technique = " ".join(raw.split()).title()
            if 4 < len(technique) < 40 and technique not in saved:
                save_technique_to_graph(technique, symptom_keyword)
                saved.add(technique)

    #  Save original query as alias so next time KG finds it directly
    existing = get_existing_aliases(symptom_keyword)
    new_alias = query.lower().strip()
    if new_alias not in existing:
        existing.append(new_alias)
        add_aliases_to_node(symptom_keyword, existing)
        print(f" Alias saved: '{new_alias}' → {symptom_keyword}")

    print(f" Symptom keyword saved: {symptom_keyword}")
    reload_concepts()

    return {"answer": text, "source": "ai"}


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

    if len(liked) > len(disliked):
        insights.append("User shows a positive engagement trend with recommended techniques.")
    else:
        insights.append("User shows resistance or dissatisfaction with current recommendations.")

    if liked:
        most_liked = max(set(liked), key=liked.count)
        insights.append(f"Most preferred technique is '{most_liked}', indicating comfort with this approach.")

    if disliked:
        most_disliked = max(set(disliked), key=disliked.count)
        insights.append(f"Technique '{most_disliked}' shows repeated negative feedback.")

    if "Meditation" in liked or "Breathing Exercise" in liked:
        insights.append("User prefers calming and mindfulness-based interventions.")

    if "Pomodoro Technique" in liked:
        insights.append("User responds well to productivity-focused techniques.")

    if "Walking" in liked or "Exercise" in liked:
        insights.append("User benefits from physical activity-based recommendations.")

    return {"insights": insights}


@router.get("/graph-stats")
def graph_stats():
    session = get_session()
    nodes = session.run("MATCH (n) RETURN count(n) AS count").single()["count"]
    rels = session.run("MATCH ()-[r]->() RETURN count(r) AS count").single()["count"]
    return {"nodes": nodes, "relationships": rels, "hop_depth": 3}