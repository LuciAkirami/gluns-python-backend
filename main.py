from fastapi import FastAPI
from .routers import ai_api , auth_api

app = FastAPI()
app.include_router(ai_api.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(auth_api.router, prefix="/api/v1/iam", tags=["Auth"])

@app.get("/")
async def root():
	return {"message": "FastAPI is running"}
