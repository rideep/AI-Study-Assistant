import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "llama-3.1-70b-versatile"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 5

UPLOAD_DIR = "uploads"
CHROMA_DIR = "chroma_db"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)
