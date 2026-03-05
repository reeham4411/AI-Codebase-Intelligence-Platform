from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from services.code_intelligence_service import search_code, explain_code

router = APIRouter(prefix="/api", tags=["Code Intelligence"])


class SearchRequest(BaseModel):
    query: str
    k: Optional[int] = 5


class ExplainRequest(BaseModel):
    code: str
    language: Optional[str] = "auto"


@router.post("/search")
def code_search(request: SearchRequest):
    """
    Intelligent semantic code search across indexed repositories.
    Returns relevant code snippets ranked by similarity.
    """
    results = search_code(request.query, k=request.k)
    return {
        "query": request.query,
        "results": results,
        "total": len(results)
    }


@router.post("/explain")
def code_explain(request: ExplainRequest):
    """
    AI-powered code explanation - paste any code and get a clear explanation.
    """
    explanation = explain_code(request.code, request.language)
    return {
        "explanation": explanation,
        "language": request.language
    }
