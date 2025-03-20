#!/usr/bin/env python
# File: backend/scripts/simple_websocket_server.py
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a simple FastAPI app
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Simple WebSocket Server"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected")
    
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received: {data}")
            await websocket.send_text(f"You sent: {data}")
    except WebSocketDisconnect:
        logger.info("Client disconnected")

if __name__ == "__main__":
    logger.info("Starting simple WebSocket server...")
    logger.info("WebSocket endpoint will be available at ws://localhost:8765/ws")
    uvicorn.run(app, host="0.0.0.0", port=8765) 