import asyncio
import websocket

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

ws_router = APIRouter()

@ws_router.websocket("/models")
async def model_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        async for message in websocket.iter_text():
            # Process the WebSocket message here
            response = {"models": ["model1", "model2", "model3"]}
            await websocket.send_json(response)
    except WebSocketDisconnect:
        print("WebSocket connection closed")