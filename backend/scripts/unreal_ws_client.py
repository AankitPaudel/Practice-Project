#!/usr/bin/env python
# File: backend/scripts/unreal_ws_client.py
import websocket
import json
import os
import urllib.request
import time
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UnrealWebSocketClient:
    def __init__(self, server_url="ws://localhost:8000/ws"):
        """Initialize WebSocket client for Unreal Engine"""
        self.server_url = server_url
        self.ws = None
        self.unreal_audio_dir = Path("C:/UnrealAudio")
        
        # Create Unreal audio directory if it doesn't exist
        self.unreal_audio_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Unreal audio directory: {self.unreal_audio_dir}")

    def connect(self):
        """Connect to WebSocket server"""
        try:
            logger.info(f"Connecting to WebSocket server at {self.server_url}")
            self.ws = websocket.create_connection(self.server_url)
            logger.info("Connected to WebSocket server")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to WebSocket server: {e}")
            return False

    def disconnect(self):
        """Disconnect from WebSocket server"""
        if self.ws:
            self.ws.close()
            logger.info("Disconnected from WebSocket server")

    def send_audio(self, audio_path):
        """Send user speech to FastAPI backend & receive AI response"""
        if not self.ws:
            if not self.connect():
                logger.error("Cannot send audio: not connected to server")
                return None
        
        try:
            # Ensure audio path exists
            audio_file = Path(audio_path)
            if not audio_file.exists():
                logger.error(f"Audio file not found: {audio_path}")
                return None
            
            logger.info(f"Sending audio file: {audio_path}")
            self.ws.send(json.dumps({"audio_path": str(audio_path)}))
            
            # Receive AI response
            logger.info("Waiting for AI response...")
            response = json.loads(self.ws.recv())
            
            logger.info(f"Received AI response: {response['answer'][:50]}...")
            
            # Download AI Speech if available
            if response["audio_url"]:
                audio_url = f"http://localhost:8000{response['audio_url']}"
                output_audio = self.unreal_audio_dir / "output.mp3"
                
                logger.info(f"Downloading AI speech from {audio_url}")
                urllib.request.urlretrieve(audio_url, output_audio)
                
                logger.info(f"Downloaded AI speech to {output_audio}")
                response["local_audio_path"] = str(output_audio)
                
                # Play audio (Windows Media Player)
                self._play_audio(output_audio)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in send_audio: {e}")
            # Try to reconnect
            self.disconnect()
            self.connect()
            return None

    def _play_audio(self, audio_path):
        """Play audio file using Windows Media Player"""
        try:
            logger.info(f"Playing audio: {audio_path}")
            os.system(f'start wmplayer "{audio_path}"')
        except Exception as e:
            logger.error(f"Error playing audio: {e}")

# Example usage
if __name__ == "__main__":
    client = UnrealWebSocketClient()
    
    if client.connect():
        # Simulating a voice input from Unreal
        test_audio = Path("C:/UnrealAudio/input.wav")
        
        # Create a test audio file if it doesn't exist
        if not test_audio.exists():
            logger.warning(f"Test audio file not found: {test_audio}")
            logger.warning("Please create a test audio file before running this script")
        else:
            response = client.send_audio(str(test_audio))
            if response:
                logger.info(f"Full response: {response}")
        
        client.disconnect()
    else:
        logger.error("Failed to connect to WebSocket server. Make sure the server is running.") 