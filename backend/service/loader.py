from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from typing import List

def load_document(file_path:str):

    loader = PyPDFLoader(file_path)

    docs  = loader.load()
    # print(docs)
    return docs

# pdf_path = Path(__file__).parent / "mml-book.pdf"
# load_document(pdf_path)

    

    