#!/usr/bin/env python
# File: backend/scripts/basic_websocket_server.py
import asyncio
import websockets
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def echo(websocket, path):
    """Echo server handler"""
    logger.info(f"Client connected from {websocket.remote_address}")
    
    try:
        async for message in websocket:
            logger.info(f"Received message: {message}")
            await websocket.send(f"Echo: {message}")
            logger.info(f"Sent echo response")
    except websockets.exceptions.ConnectionClosed:
        logger.info("Client disconnected")

async def main():
    """Start the WebSocket server"""
    # Use port 8080 which is commonly open in firewalls
    server = await websockets.serve(echo, "localhost", 8080)
    logger.info("WebSocket server started at ws://localhost:8080")
    await server.wait_closed()

if __name__ == "__main__":
    logger.info("Starting basic WebSocket server...")
    asyncio.run(main()) 