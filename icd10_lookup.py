import chromadb
from sentence_transformers import SentenceTransformer

# Load these once when the module is imported, not every time we search
# (loading the model repeatedly would be slow)
print("Loading ICD-10 embedding model...")
_embedder = SentenceTransformer("all-MiniLM-L6-v2")

_chroma_client = chromadb.PersistentClient(path="./icd10_vector_db")
_collection = _chroma_client.get_collection(name="icd10_codes")
print("ICD-10 lookup ready!")


def get_icd10_suggestions(diagnosis_text: str, top_n: int = 5, min_confidence: float = 0.3) -> list[dict]:
    """
    Given a diagnosis or assessment string, returns the top N most likely
    ICD-10 codes as a list of dicts: [{"code": ..., "description": ..., "confidence": ...}]

    confidence is a 0-1 score where 1.0 = perfect match, 0.0 = no similarity.
    Results below min_confidence are excluded — they're likely irrelevant noise.
    """
    if not diagnosis_text or not diagnosis_text.strip():
        return []

    query_embedding = _embedder.encode([diagnosis_text]).tolist()

    # Fetch more than we need, since some will get filtered out
    results = _collection.query(
        query_embeddings=query_embedding,
        n_results=top_n * 2
    )

    suggestions = []
    for i in range(len(results["ids"][0])):
        code = results["ids"][0][i]
        description = results["documents"][0][i]
        distance = results["distances"][0][i]

        confidence = max(0.0, round(1 - (distance / 2), 3))

        if confidence >= min_confidence:
            suggestions.append({
                "code": code,
                "description": description,
                "confidence": confidence
            })

        if len(suggestions) >= top_n:
            break

    return suggestions

def get_suggestions_for_assessment_list(assessment_list: list[str], top_n: int = 3) -> dict:
    """
    Given a SOAP note's assessment list (multiple diagnoses), returns
    ICD-10 suggestions for EACH diagnosis separately.

    Returns: {"Viral infection": [...], "Tension headache": [...]}
    """
    results = {}
    for diagnosis in assessment_list:
        results[diagnosis] = get_icd10_suggestions(diagnosis, top_n=top_n)
    return results


if __name__ == "__main__":
    # Quick self-test
    test_diagnosis = "patient has hypertension and is overweight"
    print(f"\nTest query: '{test_diagnosis}'\n")

    suggestions = get_icd10_suggestions(test_diagnosis)
    for s in suggestions:
        print(f"  {s['code']}: {s['description']}  (confidence: {s['confidence']})")