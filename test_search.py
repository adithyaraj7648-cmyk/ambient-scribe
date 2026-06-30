import chromadb
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="./icd10_vector_db")
collection = chroma_client.get_collection(name="icd10_codes")

# Try searching with a diagnosis phrase, even if it doesn't exactly match any code description
query = "patient has a viral infection with high temperature"

query_embedding = embedder.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=5
)

print(f"Query: '{query}'\n")
print("Top 5 matching ICD-10 codes:")
for i in range(len(results["ids"][0])):
    code = results["ids"][0][i]
    desc = results["documents"][0][i]
    distance = results["distances"][0][i]
    print(f"  {code}: {desc}  (distance: {round(distance, 3)})")