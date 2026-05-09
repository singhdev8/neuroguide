from sentence_transformers import SentenceTransformer, util
from database import get_session

# Lazy load — model loaded only on first request, not at startup
_model = None
_concepts = None
_alias_map = None
_concept_embeddings = None


def get_model():
    global _model
    if _model is None:
        print("Loading sentence transformer model...")
        _model = SentenceTransformer('all-mpnet-base-v2')
        print("Model loaded!")
    return _model


def load_concepts_from_graph():
    try:
        session = get_session()
        query = """
        MATCH (n)
        WHERE n:Emotion OR n:Symptom
        RETURN DISTINCT n.name AS name, coalesce(n.aliases, []) AS aliases
        """
        result = session.run(query)

        concepts = []
        alias_map = {}

        for record in result:
            name = record["name"]
            concepts.append(name)
            for alias in record["aliases"]:
                alias_map[alias.lower()] = name

        print(f"Loaded {len(concepts)} concepts, {len(alias_map)} aliases")
        return concepts, alias_map

    except Exception as e:
        print(f"Warning: Could not load concepts from graph: {e}")
        return [], {}


def get_concepts():
    global _concepts, _alias_map, _concept_embeddings
    if _concepts is None:
        _concepts, _alias_map = load_concepts_from_graph()
        if _concepts:
            model = get_model()
            _concept_embeddings = model.encode(_concepts, convert_to_tensor=True)
    return _concepts, _alias_map, _concept_embeddings


def reload_concepts():
    global _concepts, _alias_map, _concept_embeddings
    _concepts, _alias_map = load_concepts_from_graph()
    if _concepts:
        model = get_model()
        _concept_embeddings = model.encode(_concepts, convert_to_tensor=True)
    print(f"Reloaded {len(_concepts)} concepts, {len(_alias_map)} aliases")


def extract_emotions(text):
    concepts, alias_map, concept_embeddings = get_concepts()

    if not concepts or concept_embeddings is None:
        return []

    text_lower = text.lower().strip()

    for alias, concept in alias_map.items():
        if alias in text_lower:
            print(f"Alias match: '{alias}' → {concept}")
            return [concept]

    model = get_model()
    text_embedding = model.encode(text, convert_to_tensor=True)
    similarities = util.cos_sim(text_embedding, concept_embeddings)[0]

    detected = []
    high_confidence = []

    for i, score in enumerate(similarities):
        if score > 0.25:
            detected.append(concepts[i])
        if score > 0.33:
            high_confidence.append(concepts[i])

    if len(high_confidence) == 0:
        return []

    if not detected:
        detected.append("Stress")

    return list(set(detected))