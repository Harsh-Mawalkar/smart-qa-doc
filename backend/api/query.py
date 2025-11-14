from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Body
from service.retriver import ask_question

router = APIRouter()

@router.post("/")
async def query_doc(payload: dict = Body(...)):
    query = payload.get("question")
    
    if not query:
        return JSONResponse({"error": "Missing 'question' field"}, status_code=400)

    try:
        answer = ask_question(query)
        return JSONResponse({"answer": answer})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
