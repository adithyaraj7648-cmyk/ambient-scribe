import chromadb
from sentence_transformers import SentenceTransformer
from icd10_data import get_all_codes

print("Loading embedding model... (downloads ~80MB first time)")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded!")

# Create a persistent local database (saved to disk, survives restarts)
print("Setting up vector database...")
chroma_client = chromadb.PersistentClient(path="./icd10_vector_db")

# Delete old collection if it exists, so we start fresh each time this runs
try:
    chroma_client.delete_collection(name="icd10_codes")
except Exception:
    pass

collection = chroma_client.create_collection(name="icd10_codes")

# Load our curated codes
codes = get_all_codes()
descriptions = [desc for code, desc in codes]
code_ids = [code for code, desc in codes]

print(f"Generating embeddings for {len(codes)} codes...")
embeddings = embedder.encode(descriptions).tolist()

print("Storing in vector database...")
collection.add(
    ids=code_ids,
    embeddings=embeddings,
    documents=descriptions,
    metadatas=[{"code": code, "description": desc} for code, desc in codes]
)

print(f"\nDone! {collection.count()} ICD-10 codes stored in vector database.")
print("Database saved to ./icd10_vector_db/")