# backend/api/upload.py
import os, tempfile, shutil
from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from service.loader import load_document
from service.embedding_store import async_store_embedding  # background wrapper
from uuid import uuid4

router = APIRouter()

@router.post("/")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # save upload to a temp file and schedule background indexing
    suffix = os.path.splitext(file.filename)[1]
    tmp_dir = tempfile.mkdtemp(prefix="upload_")
    tmp_path = os.path.join(tmp_dir, f"{uuid4().hex}{suffix}")
    try:
        contents = await file.read()
        with open(tmp_path, "wb") as f:
            f.write(contents)

        # schedule background indexing (non-blocking)
        background_tasks.add_task(async_store_embedding, collection_name="docs_store", file_path=tmp_path, original_filename=file.filename)

        return JSONResponse({"status":"accepted", "message":"File received. Indexing in background."})
    except Exception as e:
        # cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return JSONResponse({"error": str(e)}, status_code=500)
