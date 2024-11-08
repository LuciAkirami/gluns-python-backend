from fastapi import APIRouter

ai_router = APIRouter()

@ai_router.get("/models")
def get_models():
    return {"models": ["model1", "model2", "model3"]}

@ai_router.post("/inference")
def run_inference(data: dict):
    return {"results": [1, 2, 3]}