from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.ai_service import process_with_llm
from ..db.database import store_user_context

router = APIRouter()

class TextRequest(BaseModel):
    user_id: str
    text: str

@router.post("/process_text")
async def process_text(request: TextRequest):
    # Process text with LLM
    try:
        response = process_with_llm(request.text)
        # Store the response in the database
        store_user_context({"user_id": request.user_id, "response": response})
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
