# backend/api/query.py
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from service.retriver import ask_question

router = APIRouter()

@router.post("/")
async def query_doc(payload: dict = Body(...)):
    q = payload.get("question")
    if not q:
        return JSONResponse({"error":"Missing 'question' field"}, status_code=400)
    try:
        answer = ask_question(q)
        return JSONResponse({"answer": answer})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
