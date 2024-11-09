from fastapi import FastAPI
from routers import ai_router

app = FastAPI()
app.include_router(ai_router, prefix="/ai")
