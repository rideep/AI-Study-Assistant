import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import sys

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
from pdf_processor import PDFProcessor

load_dotenv()

st.set_page_config(page_title="AI Study Assistant", page_icon="🎓", layout="wide")

st.title("🎓 AI Study Assistant")
st.write("Upload your study materials and get personalized learning plans!")

# Initialize
if 'processor' not in st.session_state:
    st.session_state.processor = PDFProcessor()
    st.session_state.processed_docs = []

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Study Materials")
    
    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload lecture slides, textbooks, or study materials"
    )
    
    if uploaded_files:
        st.write(f"**{len(uploaded_files)} file(s) uploaded**")
        
        if st.button("Process PDFs", type="primary"):
            with st.spinner("Processing PDFs..."):
                results = []
                
                for uploaded_file in uploaded_files:
                    # Save uploaded file temporarily
                    temp_path = os.path.join("uploads", uploaded_file.name)
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Process
                    try:
                        result = st.session_state.processor.extract_text_from_pdf(temp_path)
                        results.append(result)
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                
                st.session_state.processed_docs = results
                st.success(f"✅ Processed {len(results)} documents!")
                st.rerun()

# Main content area
if st.session_state.processed_docs:
    st.header("📚 Processed Documents")
    
    # Show summary
    col1, col2, col3 = st.columns(3)
    
    total_pages = sum(doc['metadata']['num_pages'] for doc in st.session_state.processed_docs)
    total_chars = sum(doc['total_chars'] for doc in st.session_state.processed_docs)
    
    col1.metric("Documents", len(st.session_state.processed_docs))
    col2.metric("Total Pages", total_pages)
    col3.metric("Total Characters", f"{total_chars:,}")
    
    # Show document details
    st.subheader("Document Details")
    
    for i, doc in enumerate(st.session_state.processed_docs, 1):
        with st.expander(f"📄 {doc['metadata']['filename']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Metadata:**")
                st.write(f"- Pages: {doc['metadata']['num_pages']}")
                st.write(f"- Characters: {doc['total_chars']:,}")
                if doc['metadata']['title']:
                    st.write(f"- Title: {doc['metadata']['title']}")
            
            with col2:
                st.write("**Sample Text:**")
                sample = doc['pages'][0]['text'][:300] + "..."
                st.text(sample)
    
    # Next steps placeholder
    st.info("✅ PDF processing complete! Next: We'll add chunking and embedding generation.")
    
else:
    # Welcome screen
    st.info("👈 Upload PDF files in the sidebar to get started!")
    
    st.markdown("""
    ### How it works:
    
    1. **Upload** your study materials (PDFs)
    2. **Generate** personalized study plans
    3. **Create** flashcards for revision
    4. **Practice** with auto-generated quizzes
    
    ### Supported formats:
    - PDF lecture slides
    - PDF textbooks
    - PDF study guides
    
    *Ready to start? Upload your first document!*
    """)