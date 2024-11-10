from enum import Enum
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List , Tuple
from services import ai_service
from services.SummaryService import SummaryService
from services.bd_tips.modelDTO.TransactionData import TransactionDataResponse

FILEPATH = "./services/bd_tips/datasets/summary_monthly_user.csv"
transaction_service = SummaryService(FILEPATH)

app = FastAPI()
#app.include_router(ai_api.router, prefix="/api/v1/chat", tags=["Chat"])

# Define response models

# Define an Enum for contexts
class ContextEnum(str, Enum):
    CAPITAL_MANAGEMENT = "CAPITAL_MANAGEMENT"
    INVESTMENT = "INVESTMENT"
    SAVE_MONEY = "SAVE_MONEY"
    BILLS_BALANCE = "BILLS_BALANCE"
    SUMMARY_INVOICES = "SUMMARY_INVOICES"

# Define the request model for user input and context
class UserInputRequest(BaseModel):
    context: ContextEnum
    input: str
    userId: str
    chatHistoryId: int
class ContextResponse(BaseModel):
    message: str
    body: List[str]

class ChatResponse(BaseModel):
    message: str
    body: dict
    
# Request model for input
class InputRequest(BaseModel):
    context: ContextEnum
    input: str
    userId: str
    chatHistoryId: int

# Response model for output
class OutputResponse(BaseModel):
    output: str
    
class ChatHistoryResponse(BaseModel):
    history: List[Tuple[str, str]]
    
# Mocked chat history data for users
user_chat_history = {
    1: [["Hello, how can I save?", "Try saving 20% of your income"], ["What’s the best investment?", "Consider low-risk options like bonds"]],
    2: [["How do I manage bills?", "Set a monthly budget and prioritize essentials."]],
}

@app.get("/")
async def root():
	return {"message": "FastAPI is running"}

# 1. GET /api/v1/chat/contexts - Retrieve list of contexts
@app.get("/api/v1/chat/contexts", response_model=ContextResponse)
async def get_contexts():
    return {
        "message": "Contexts retrieved successfully",
        "body": [
            ContextEnum.CAPITAL_MANAGEMENT,
            ContextEnum.INVESTMENT,
            ContextEnum.SAVE_MONEY,
            ContextEnum.BILLS_BALANCE,
            ContextEnum.SUMMARY_INVOICES
        ]
    }

#  POST /api/v1/chat - Handle user input with a context and text
@app.post("/api/v1/chat", response_model=ChatResponse)
async def post_chat(user_input: UserInputRequest):
    # Here we will simulate processing the input based on the context
    response_data = {
        "context": user_input.context,
        "input": user_input.input,
        "response": f"Processed input for {user_input.context}"
    }
    return {
        "message": "User input processed successfully",
        "body": response_data
    }

@app.get("/api/v1/{chatMessageID}", response_model=ChatHistoryResponse)
async def get_chat_history(request: InputRequest):
    history = user_chat_history.get(request.userId)
    if history is None:
        raise HTTPException(status_code=404, detail="Chat history not found for the specified user.")
    return ChatHistoryResponse(history=history)


@app.post("/api/v1/output", response_model=OutputResponse)
async def get_output(request: InputRequest):
    # Here you can implement your logic, for now we are returning dummy output
    try:
        chat_history = user_chat_history.get(request.chatHistoryId, {}).get(request.userId, [])
        # Call the function from ai_service to process with LLM
        output = ai_service.process_with_llm(request , chat_history)
        return OutputResponse(output=output)
    except Exception as e:
        print(f"Error during processing: {e}")
        return OutputResponse(output="Error in processing request.")
    
#  POST /api/v1/chat/{chatHistoryId}/{userId} - Handle user input with context and text based on chatHistoryId and userId
@app.post("/api/v1/chat/{chatHistoryId}/{userId}", response_model=ChatResponse)
async def post_chat(user_input: UserInputRequest, chatHistoryId=None):
    # Simulate processing the input based on the context and user-specific chat history
    history = user_chat_history.get(user_input.chatHistoryId, [])
    if not history:
        raise HTTPException(status_code=404, detail="Chat history not found for the specified chatHistoryId.")
    
    response_data = {
        "context": user_input.context,
        "input": user_input.input,
        "response": f"Processed input for {user_input.context} with userId {user_input.userId} and chatHistoryId {chatHistoryId}"
    }
    return {
        "message": "User input processed successfully",
        "body": response_data
    }

@app.get("/api/v1/chat/summary", response_model=List[TransactionDataResponse])
async def get_transactions(
    random: bool = Query(False, description="If true, selects transactions for a random user")
):
    """Fetch transactions data for a random user if random=True, otherwise for all users from the CSV file using TransactionService."""
    try:
        transactions = transaction_service.load_transaction_data(random_choice=random)
        return transactions
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving transaction data")