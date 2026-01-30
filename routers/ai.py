
from fastapi import APIRouter, Depends
from schemas.ai import ChatRequest, ChatResponse
from services.openrouter_client import chat_completion

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/chat")
async def chat(
    body: ChatRequest,
):
    response = await chat_completion([
        {"role": "user", "content": body.message}
    ])
    return {"response": response}
