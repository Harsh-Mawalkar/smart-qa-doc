# frontend/app.py
import streamlit as st
import requests
import io

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="SmartDoc QA")
st.title("📄 Smart Document Q&A")

st.header("📤 Upload Document")
uploaded_file = st.file_uploader("Upload a document (pdf/docx/txt)", type=["pdf","docx","txt"])
if uploaded_file is not None:
    file_like = io.BytesIO(uploaded_file.read())
    file_like.name = uploaded_file.name
    with st.spinner("Uploading..."):
        try:
            files = {"file": (file_like.name, file_like, "application/octet-stream")}
            resp = requests.post(f"{BACKEND_URL}/upload/", files=files, timeout=10)
        except Exception as e:
            st.error(f"Upload error: {e}")
        else:
            st.write("HTTP status:", resp.status_code)
            st.json(resp.json())

st.header("❓ Ask a question")
query = st.text_input("Enter your question:")
if st.button("Ask"):
    if not query.strip():
        st.warning("Enter a question")
    else:
        with st.spinner("Getting answer..."):
            try:
                resp = requests.post(f"{BACKEND_URL}/query/", json={"question": query}, timeout=30)
                st.write("HTTP status:", resp.status_code)
                st.json(resp.json())
            except Exception as e:
                st.error(f"Error: {e}")
