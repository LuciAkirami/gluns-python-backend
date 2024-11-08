from fastapi import APIRouter

bigdata_router = APIRouter()

@bigdata_router.get("/data")
def get_data():
    return {"data": [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]}

@bigdata_router.post("/upload")
def upload_data(data: dict):
    return {"status": "success"}