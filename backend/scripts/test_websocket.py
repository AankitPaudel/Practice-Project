#!/usr/bin/env python
# File: backend/scripts/test_websocket.py
import sys
from pathlib import Path
import time
import argparse
import websocket
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

def test_websocket_connection(server_url, audio_path):
    """Test WebSocket connection directly"""
    try:
        logger.info(f"Testing direct WebSocket connection to {server_url}")
        # Connect with headers
        ws = websocket.create_connection(
            server_url,
            header=["Host: localhost:8000", "Origin: http://localhost:8000"]
        )
        logger.info("Connected to WebSocket server")
        
        # Send audio path
        request = {"audio_path": str(audio_path)}
        logger.info(f"Sending audio path: {audio_path}")
        ws.send(json.dumps(request))
        
        # Receive response
        logger.info("Waiting for response...")
        response = json.loads(ws.recv())
        
        logger.info(f"Received response: {response}")
        
        # Close connection
        ws.close()
        logger.info("Connection closed")
        
        return response
    except Exception as e:
        logger.error(f"Error testing WebSocket connection: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Test WebSocket connection with audio file")
    parser.add_argument("--audio", type=str, default="C:/UnrealAudio/input.wav", 
                        help="Path to audio file for testing")
    parser.add_argument("--server", type=str, default="ws://localhost:8000/ws",
                        help="WebSocket server URL")
    args = parser.parse_args()
    
    # Create test audio directory if it doesn't exist
    audio_dir = Path("C:/UnrealAudio")
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if test audio file exists
    audio_path = Path(args.audio)
    if not audio_path.exists():
        logger.warning(f"Warning: Test audio file not found at {audio_path}")
        logger.warning("Please create a test audio file before running this script")
        logger.warning("You can use any WAV file for testing")
        return
    
    print(f"Testing WebSocket connection to {args.server}")
    print(f"Using audio file: {audio_path}")
    
    # Test direct WebSocket connection
    response = test_websocket_connection(args.server, audio_path)
    
    if response:
        print("\n--- AI Response ---")
        print(f"Question: {response.get('question', 'N/A')}")
        print(f"Answer: {response.get('answer', 'N/A')}")
        print(f"Audio URL: {response.get('audio_url', 'N/A')}")
        print("-------------------\n")
    else:
        print("Failed to get response from WebSocket server")
        print("Make sure the server is running with: python scripts/run_websocket_server.py")

if __name__ == "__main__":
    main() 