from fastapi import FastAPI
from myapp.routers import ai_router, bigdata_router

app = FastAPI()
app.include_router(ai_router, prefix="/ai")
app.include_router(bigdata_router, prefix="/bigdata")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)