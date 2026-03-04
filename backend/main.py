from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routes.ask import router as ask_router
from routes.index import router as index_router

app = FastAPI(title="AI Codebase Assistant")

app.include_router(ask_router)
app.include_router(index_router)


@app.get("/")
def root():
    return {"message": "AI Codebase Assistant Backend Running"}