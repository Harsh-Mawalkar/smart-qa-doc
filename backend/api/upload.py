import tempfile
from fastapi import FastAPI, File,UploadFile,APIRouter
from fastapi.responses import JSONResponse
import os
from service.loader import load_document

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

        combined_text = "\n".join([doc.page_content for doc in documents])


        return JSONResponse(
            content = {
                "filename":file.filename,
                "num_chunks":len(documents),
                "sample_text": combined_text[:800]
            }
        )
    except Exception as e:
        return JSONResponse(content={
            "error": str(e)},
            status_code = 500
            )





