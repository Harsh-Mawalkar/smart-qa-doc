# backend/service/embedding_store.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from service.loader import load_document
import os, shutil

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
QDRANT_URL = "http://localhost:6333"

def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def get_qdrant_client():
    return QdrantClient(host="localhost", port=6333)

def chunk_documents(documents, chunk_size=500, overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_documents(documents)

def recreate_collection_if_needed(client, collection_name: str, dim: int = 384):
    # create or recreate to ensure correct dims
    existing = client.get_collections().collections
    names = [c.name for c in existing]
    if collection_name in names:
        client.delete_collection(collection_name=collection_name)
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
    )

def store_documents_to_qdrant(collection_name: str, chunks):
    embeddings = get_embedding_model()
    vector_store = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=QDRANT_URL,
        collection_name=collection_name,
    )
    return vector_store

def async_store_embedding(collection_name: str, file_path: str, original_filename: str):
    """
    Background worker: loads file, chunks, ensures collection config, and indexes.
    Called by FastAPI BackgroundTasks.
    """
    client = get_qdrant_client()
    try:
        docs = load_document(file_path)  # returns list[Document]
        chunks = chunk_documents(docs)
        # ensure collection set up with correct vector dims
        recreate_collection_if_needed(client, collection_name, dim=384)
        store_documents_to_qdrant(collection_name, chunks)
        # you can also store metadata mapping file->collection etc.
    except Exception as e:
        # log error (print for now)
        print("Background indexing error:", e)
    finally:
        # cleanup uploaded file and temp dir
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            parent = os.path.dirname(file_path)
            if os.path.isdir(parent):
                shutil.rmtree(parent, ignore_errors=True)
        except Exception:
            pass
