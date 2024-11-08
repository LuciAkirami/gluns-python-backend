from fastapi import FastAPI
from routers import ai_api, bigdata_api
import uvicorn

app = FastAPI()
app.include_router(ai_api.router, prefix="/ai")
app.include_router(bigdata_api.router, prefix="/bigdata")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)