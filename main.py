from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Reads your .env file and loads the API key into Python
load_dotenv()

# Creates your web app
app = FastAPI()

# A test endpoint — like knocking on a door to check if anyone's home
@app.get("/health")
def health_check():
    api_key = os.getenv("OPENAI_API_KEY")
    return {
        "status": "ok",
        "api_key_loaded": api_key is not None
    }