from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
# from ..services.ai_service import process_with_llm
# from ..db.database import store_user_context
from ..utils.http_utils import fetch_contexts, fetch_chat_data

router = APIRouter()
# TODO: Fetch value for different  context
@router.get("/contexts")
async def get_contexts():
    """Fetch available contexts from the Spring API."""
    try:
        data = fetch_contexts()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving contexts")
# TODO: test data is fetching
@router.get("/chat")
async def get_chat_data():
    """Fetch chat data from the Spring API."""
    try:
        data = fetch_chat_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving chat data")