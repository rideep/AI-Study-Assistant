import streamlit as st
from groq import Groq
from sentence_transformers import SentenceTransformer
import chromadb
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

print("Testing setup...")

# Test 1: Groq API
print("\n1. Testing Groq API...")
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Say 'Setup successful!' "}],
        max_tokens=10
    )
    print(f" Groq API works: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Groq API failed: {e}")

# Test 2: Sentence Transformers
print("\n2. Testing Sentence Transformers...")
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode("test sentence")
    print(f" Embeddings work: Generated {len(embedding)}-dimensional vector")
except Exception as e:
    print(f"❌ Embeddings failed: {e}")

# Test 3: ChromaDB
print("\n3. Testing ChromaDB...")
try:
    client = chromadb.Client()
    collection = client.create_collection("test")
    print(f" ChromaDB works: Created test collection")
except Exception as e:
    print(f"❌ ChromaDB failed: {e}")

# Test 4: Streamlit
print("\n4. Testing Streamlit...")
print("Streamlit is installed (run 'streamlit hello' to test UI)")

print("\n All core components are ready!")