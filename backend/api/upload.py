import tempfile
from fastapi import FastAPI, File,UploadFile,APIRouter
from fastapi.responses import JSONResponse
import os
from service.loader import load_document
from service.embedding_store import chuck_documents,store_embedding

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False,suffix=os.path.splitext(file.filename)[1]) as tmp:
            contents = await file.read()
            tmp.write(contents)
            temp_path = tmp.name

        documents = load_document(temp_path)

        os.remove(temp_path)

        chunks = chuck_documents(documents)
        qdrant_store = store_embedding(collection_name="docs_store",documents=chunks)



        return JSONResponse(
            content = {
                "filename":file.filename,
                "num_chunks":len(chunks),
                "message":"Document embedding successfullly stored in Qdrant!"
            }
        )
    except Exception as e:
        return JSONResponse(content={
            "error": str(e)},
            status_code = 500
            )





