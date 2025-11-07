import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
st.title("AI Study Assistant")
st.write("Upload your study materials and get personalized learning plans!")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
user_input = st.text_input("Test the AI (ask anything):")

if user_input:
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": user_input}],
            max_tokens=150
        )
        st.write(response.choices[0].message.content)

st.info("Setup complete! Ready to build the RAG system.")
