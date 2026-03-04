from fastapi import APIRouter
from schemas.request import AskRequest
from schemas.response import AskResponse
from services.rag_service import answer_question

router = APIRouter(prefix="/api", tags=["Ask"])


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):

    answer, sources = answer_question(request.question)

    return AskResponse(
        answer=answer,
        sources=sources
    )