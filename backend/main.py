# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.upload import router as upload_router
from api.query import router as query_router

app = FastAPI(title="Smart Document Q&A")

# allow Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/upload", tags=["upload"])
app.include_router(query_router, prefix="/query", tags=["query"])

@app.get("/")
def root():
    return {"message": "Smart Document Q&A backend is running"}
