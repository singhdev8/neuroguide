from database import get_session

def get_techniques(inputs):
    session = get_session()

    query = """
    MATCH (start)
    WHERE start.name IN $inputs

    // Direct techniques
    OPTIONAL MATCH (start)-[:IMPROVES|TREATED_BY]->(t1:Technique)

    // 2-hop (Emotion → Symptom → Technique)
    OPTIONAL MATCH (start)-[:CAUSES]->(s:Symptom)
                   -[:TREATED_BY]->(t2:Technique)

    // 3-hop (Emotion → Symptom → Behavior → Technique)
    OPTIONAL MATCH (start)-[:CAUSES]->(s2:Symptom)
                   -[:LEADS_TO]->(b:Behavior)
                   -[:MANAGED_BY]->(t3:Technique)

    WITH 
        collect(DISTINCT t1.name) AS direct,
        collect(DISTINCT t2.name) AS symptom_path,
        collect(DISTINCT t3.name) AS behavior_path

    RETURN direct, symptom_path, behavior_path
    """

    result = session.run(query, inputs=inputs).single()

    scores = {}

    # Direct = highest weight
    for t in result["direct"]:
        if t:
            scores[t] = scores.get(t, 0) + 3

    # Symptom path = medium
    for t in result["symptom_path"]:
        if t:
            scores[t] = scores.get(t, 0) + 2

    # Behavior path = lower
    for t in result["behavior_path"]:
        if t:
            scores[t] = scores.get(t, 0) + 1

    return [{"name": k, "score": v} for k, v in scores.items()]