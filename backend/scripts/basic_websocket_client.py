#!/usr/bin/env python
# File: backend/scripts/basic_websocket_client.py
import asyncio
import websockets
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def hello():
    """Connect to WebSocket server and send/receive messages"""
    uri = "ws://localhost:8765"
    
    logger.info(f"Connecting to {uri}")
    try:
        async with websockets.connect(uri) as websocket:
            logger.info("Connected to WebSocket server")
            
            # Send a message
            message = "Hello, WebSocket Server!"
            logger.info(f"Sending message: {message}")
            await websocket.send(message)
            
            # Receive response
            response = await websocket.recv()
            logger.info(f"Received response: {response}")
            
            return response
    except Exception as e:
        logger.error(f"Error: {e}")
        return None

if __name__ == "__main__":
    logger.info("Starting basic WebSocket client...")
    asyncio.run(hello()) 