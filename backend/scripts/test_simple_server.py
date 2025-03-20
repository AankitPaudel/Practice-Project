#!/usr/bin/env python
# File: backend/scripts/test_simple_server.py
import asyncio
import websockets
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_simple_server():
    """Test the simple WebSocket server"""
    uri = "ws://localhost:8765/ws"
    
    logger.info(f"Connecting to {uri}")
    try:
        async with websockets.connect(uri) as websocket:
            logger.info("Connected to simple WebSocket server")
            
            # Send a test message
            test_message = "Hello, Simple WebSocket Server!"
            logger.info(f"Sending message: {test_message}")
            await websocket.send(test_message)
            
            # Receive response
            logger.info("Waiting for response...")
            response = await websocket.recv()
            
            logger.info(f"Received response: {response}")
            
            return response
    except Exception as e:
        logger.error(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_simple_server()) 