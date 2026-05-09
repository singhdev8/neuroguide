from database import get_session

def get_techniques(inputs):
    session = get_session()

    query = """
    MATCH (start)
    WHERE start.name IN $inputs
    OR ANY(alias IN coalesce(start.aliases, []) WHERE alias IN $inputs)

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

    for t in result["direct"]:
        if t:
            scores[t] = scores.get(t, 0) + 3

    for t in result["symptom_path"]:
        if t:
            scores[t] = scores.get(t, 0) + 2

    for t in result["behavior_path"]:
        if t:
            scores[t] = scores.get(t, 0) + 1

    return [{"name": k, "score": v} for k, v in scores.items()]


def save_technique_to_graph(technique_name, symptom_name):
    session = get_session()

    technique_name = technique_name.strip().title()
    symptom_name = symptom_name.strip().title()

    if len(technique_name) < 4 or len(symptom_name) < 3:
        return

    if len(technique_name.split()) > 5:
        return

    query = """
    MERGE (s:Symptom {name: $symptom})
    MERGE (t:Technique {name: $technique})
    MERGE (s)-[:TREATED_BY]->(t)
    """
    session.run(query, symptom=symptom_name, technique=technique_name)
    print(f" Saved to graph: {symptom_name} → {technique_name}")


def add_aliases_to_node(node_name, aliases):
    session = get_session()

    # Store aliases in lowercase for easier matching
    aliases = [a.lower().strip() for a in aliases]

    query = """
    MATCH (n)
    WHERE n.name = $name
    SET n.aliases = $aliases
    """
    session.run(query, name=node_name, aliases=aliases)
    print(f" Aliases added to '{node_name}': {aliases}")