from fastapi import FastAPI
from api.upload import router as upload_router
from api.query import router as query_router
app = FastAPI(title = "Smart Document Q&A system")

app.include_router(upload_router, prefix="/upload", tags=["upload"])
app.include_router(query_router,prefix="/query",tags=["query"])

@app.get("/")
def root():
    return {"message":"Smart Document Q&A backend is running"}

