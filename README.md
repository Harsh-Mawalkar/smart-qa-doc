📄 Smart Document Q&A

An AI-powered application that lets users upload documents (PDF/DOCX/TXT) and ask natural language questions about the content. Built using Streamlit, FastAPI, Python, LLM embeddings, and vector search.

🚀 Features

✅ Upload documents (PDF / DOCX / TXT)
✅ Extract and index text using embeddings
✅ Vector search for relevant chunks
✅ Ask natural language questions
✅ Fast, accurate, context-based answers
✅ Streamlit frontend + FastAPI backend
✅ CORS-enabled communication
✅ Modular, production-like architecture

🛠️ Tech Stack
Frontend

Streamlit

Python

File Upload Component

Axios-like API calls (via requests)

Backend

FastAPI

Python

CORS Middleware

LangChain / Qdrant / SentenceTransformers

Text extraction (pypdf, python-docx)

LLM / Embeddings

OpenAI / HuggingFace models

SentenceTransformer embeddings

Qdrant vector-db

📁 Project Structure
smart-doc-qa/
│
├── backend/
│   ├── main.py
│   ├── api/
│   ├── vector_store/
│   ├── service/
│   ├── requirements.txt
│
├── frontend/
│   ├── app.py
│   ├── components/
│   ├── utils/
│
└── README.md

⚙️ How It Works
1️⃣ Upload Document

User uploads PDF/DOCX/TXT → sent to FastAPI backend.

2️⃣ Text Extraction

Backend extracts text using:

pypdf for PDF

python-docx for DOCX

direct read for TXT

3️⃣ Chunking & Embeddings

Content is chunked (500–1000 characters).
Each chunk is converted into a vector embedding.

4️⃣ Store Vectors

Stored using Qdant db

5️⃣ Ask Questions

Question → embedding → similarity search → relevant chunks → LLM generates answer.

▶️ Running the Project
1. Start Backend
cd backend
uvicorn main:app --reload

2. Start Frontend
cd frontend
streamlit run app.py

🔧 Troubleshooting
❗ "Request timed out"

Embeddings for large PDFs take time — increase timeout in frontend.

Use multiprocessing or async embeddings in backend.

Use chunk size = 500.

Ensure backend CORS allowed:

allow_origins=["*"]

❗ CORS Error

Add middleware in FastAPI:

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



Harsh Mawalkar
AI/ML & Full-Stack Developer
Passionate about building real-world AI applications.
