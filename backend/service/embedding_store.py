from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
import os

def get_embedding_model():
    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
    return embeddings

def get_qdrant_client():
    client = QdrantClient(
        host="localhost",
        port=6333
    )
    return client


def chuck_documents(documents,chunk_size=500,overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=overlap)
    chunks = splitter.split_documents(documents)
    return chunks

def store_embedding(collection_name:str,documents):
    embeddings = get_embedding_model()
    client = get_qdrant_client()

    
    vector_store = QdrantVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        url="http://localhost:6333",
        collection_name=collection_name
)

    print("indexing with hugging face embedding")
    return vector_store