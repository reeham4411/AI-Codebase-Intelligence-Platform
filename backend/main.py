from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.ask import router as ask_router
from routes.index import router as index_router
from routes.github import router as github_router
from routes.code_intelligence import router as code_intelligence_router
from routes.slack import router as slack_router

app = FastAPI(
    title="AI Codebase Intelligence Platform",
    description="Intelligent code search, AI explanations, GitHub integration, and Slack assistant",
    version="1.0.0"
)

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ask_router)
app.include_router(index_router)
app.include_router(github_router)
app.include_router(code_intelligence_router)
app.include_router(slack_router)


@app.get("/")
def root():
    return {"message": "AI Codebase Intelligence Platform Running"}