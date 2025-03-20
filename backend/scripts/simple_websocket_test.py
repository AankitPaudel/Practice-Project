#!/usr/bin/env python
# File: backend/scripts/simple_websocket_test.py
import asyncio
import websockets
import json
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_websocket():
    """Test WebSocket connection to the server"""
    uri = "ws://localhost:8000/ws"
    audio_path = "C:/UnrealAudio/input.wav"
    
    logger.info(f"Connecting to {uri}")
    try:
        async with websockets.connect(uri) as websocket:
            logger.info("Connected to WebSocket server")
            
            # Send audio path
            request = {"audio_path": audio_path}
            logger.info(f"Sending audio path: {audio_path}")
            await websocket.send(json.dumps(request))
            
            # Receive response
            logger.info("Waiting for response...")
            response = await websocket.recv()
            
            # Parse response
            data = json.loads(response)
            logger.info(f"Received response:")
            logger.info(f"Question: {data.get('question', 'N/A')}")
            logger.info(f"Answer: {data.get('answer', 'N/A')}")
            logger.info(f"Audio URL: {data.get('audio_url', 'N/A')}")
            
            return data
    except Exception as e:
        logger.error(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Check if audio file exists
    audio_path = Path("C:/UnrealAudio/input.wav")
    if not audio_path.exists():
        logger.warning(f"Warning: Audio file not found at {audio_path}")
        logger.warning("Please create a test audio file before running this script")
        logger.warning("You can use the create_test_audio.py script to create a test file")
    else:
        logger.info(f"Audio file found at {audio_path}")
        
    # Run the test
    asyncio.run(test_websocket()) 