from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Gemini via OpenAI compat mode
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Vectorstore


def ask_question(query: str) -> str:
    """RAG pipeline: retrieve → build context → LLM."""
    vector_db = QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name="docs_store",
        embedding=embeddings,
    )
    # 1. Retrieve chunks
    search_results = vector_db.similarity_search(query=query, k=5)

    # 2. Build context
    context = "\n\n".join([
        f"Page: {res.metadata.get('page_label', 'N/A')}\n"
        f"Source: {res.metadata.get('source', 'unknown')}\n"
        f"Content:\n{res.page_content}"
        for res in search_results
    ])

    # 3. System prompt
    SYSTEM_PROMPT = f"""
    You are a helpful AI assistant. 
    Answer the user's question ONLY using the context retrieved from the document.

    If the answer is not found in the context,
    say: "I don't know based on the document."

    --- BEGIN CONTEXT ---
    {context}
    --- END CONTEXT ---
    """

    # 4. Gemini Chat Completion
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )

    return response.choices[0].message.content
