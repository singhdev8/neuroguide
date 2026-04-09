from collections import defaultdict
from kg_engine import get_techniques
from user_memory import get_user_history

def recommend(inputs, user_id="user1"):
    techniques = get_techniques(inputs)
    history = get_user_history(user_id)

    preference = defaultdict(int)
    count = defaultdict(int)

    for h in history:
        technique = h["technique"]
        count[technique] += 1

        if h["liked"]:
            preference[technique] += 1
        else:
            preference[technique] -= 1

    # Normalize score
    for t in techniques:
        tech = t["name"]

        if count[tech] > 0:
            # average preference
            t["score"] += preference[tech] / count[tech]

    ranked = sorted(techniques, key=lambda x: x["score"], reverse=True)

    return ranked