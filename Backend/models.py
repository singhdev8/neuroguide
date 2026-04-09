from sentence_transformers import SentenceTransformer, util
from database import get_session

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_concepts_from_graph():
    session = get_session()

    query = """
    MATCH (n)
    WHERE n:Emotion OR n:Symptom
    RETURN DISTINCT n.name AS name
    """

    result = session.run(query)

    return [record["name"] for record in result]


# Load dynamically
CONCEPTS = load_concepts_from_graph()
concept_embeddings = model.encode(CONCEPTS, convert_to_tensor=True)


def extract_emotions(text):
    text_embedding = model.encode(text, convert_to_tensor=True)

    similarities = util.cos_sim(text_embedding, concept_embeddings)[0]

    detected = []

    for i, score in enumerate(similarities):
        if score > 0.35:
            detected.append(CONCEPTS[i])

    if not detected:
        detected.append("Stress")  # fallback

    return list(set(detected))