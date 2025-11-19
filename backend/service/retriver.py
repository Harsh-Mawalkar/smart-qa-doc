# backend/service/retriever.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_COMPAT_BASE = "https://generativelanguage.googleapis.com/v1beta/openai/"

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def get_vector_db(collection_name="docs_store"):
    embeddings = get_embeddings()
    # lazy create from existing collection - will raise if not exists; caller should catch
    return QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name=collection_name,
        embedding=embeddings,
    )

def ask_question(query: str) -> str:
    # lazy-load the vector DB each call (safer on startup)
    try:
        vector_db = get_vector_db()
    except Exception as e:
        return "No documents indexed yet. Please upload a document first."

    search_results = vector_db.similarity_search(query=query, k=5)

    context = "\n\n".join([
        f"Page: {res.metadata.get('page_label','N/A')}\nSource: {res.metadata.get('source','unknown')}\nContent:\n{res.page_content}"
        for res in search_results
    ])

    # Setup Gemini client with OpenAI-compatible interface
    client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"), base_url=OPENAI_COMPAT_BASE)

    SYSTEM_PROMPT = f"""
You are an assistant that answers only from the provided context.

Context:
{context}
Question:
{query}
Answer:
"""
    # call chat completion
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[{"role":"system","content":SYSTEM_PROMPT}, {"role":"user","content":query}],
    )
    return response.choices[0].message.content
