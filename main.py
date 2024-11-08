from fastapi import FastAPI
from myapp.routers import ai_api, bigdata_api

app = FastAPI()
app.include_router(ai_api.router, prefix="/ai")
app.include_router(bigdata_api.router, prefix="/bigdata")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)