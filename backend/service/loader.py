# backend/service/loader.py
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from pathlib import Path

def load_document(file_path: str):
    suffix = Path(file_path).suffix.lower()
    if suffix == ".pdf":
        loader = PyPDFLoader(file_path)
    elif suffix == ".docx":
        loader = Docx2txtLoader(file_path)
    elif suffix == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {suffix}")
    docs = loader.load()
    # ensure metadata has source/page
    for i, d in enumerate(docs):
        if "source" not in d.metadata:
            d.metadata["source"] = str(file_path)
        if "page_label" not in d.metadata:
            d.metadata["page_label"] = d.metadata.get("page", i)
    return docs
