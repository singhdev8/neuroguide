from sentence_transformers import SentenceTransformer, util
from database import get_session

model = SentenceTransformer('all-mpnet-base-v2')

def load_concepts_from_graph():
    session = get_session()
    # Load both concept names AND their aliases
    query = """
    MATCH (n)
    WHERE n:Emotion OR n:Symptom
    RETURN DISTINCT n.name AS name, coalesce(n.aliases, []) AS aliases
    """
    result = session.run(query)
    
    concepts = []
    alias_map = {}  # alias → concept name
    
    for record in result:
        name = record["name"]
        concepts.append(name)
        for alias in record["aliases"]:
            alias_map[alias.lower()] = name

    return concepts, alias_map


CONCEPTS, ALIAS_MAP = load_concepts_from_graph()
concept_embeddings = model.encode(CONCEPTS, convert_to_tensor=True)


def reload_concepts():
    global CONCEPTS, ALIAS_MAP, concept_embeddings
    CONCEPTS, ALIAS_MAP = load_concepts_from_graph()
    concept_embeddings = model.encode(CONCEPTS, convert_to_tensor=True)
    print(f"Reloaded {len(CONCEPTS)} concepts, {len(ALIAS_MAP)} aliases")


def extract_emotions(text):
    text_lower = text.lower().strip()

    # Check alias map first — direct match
    for alias, concept in ALIAS_MAP.items():
        if alias in text_lower:
            print(f"Alias match: '{alias}' → {concept}")
            return [concept]

    # Fall back to sentence transformer
    text_embedding = model.encode(text, convert_to_tensor=True)
    similarities = util.cos_sim(text_embedding, concept_embeddings)[0]

    detected = []
    high_confidence = []

    for i, score in enumerate(similarities):
        if score > 0.25:
            detected.append(CONCEPTS[i])
        if score > 0.33:
            high_confidence.append(CONCEPTS[i])

    if len(high_confidence) == 0:
        return []

    if not detected:
        detected.append("Stress")

    return list(set(detected))