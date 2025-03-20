# #!/usr/bin/env python
# # File: backend/scripts/unreal_engine_ws.py
# # This script is designed to be run from within Unreal Engine's Python API

# import websocket
# import json
# import os
# import urllib.request
# import unreal
# import time
# from pathlib import Path

# # Unreal Engine logging
# def log(message, level="info"):
#     """Log message to Unreal Engine's output log"""
#     if level == "info":
#         unreal.log(message)
#     elif level == "warning":
#         unreal.log_warning(message)
#     elif level == "error":
#         unreal.log_error(message)

# class UnrealWebSocketClient:
#     def __init__(self, server_url="ws://localhost:8000/ws"):
#         """Initialize WebSocket client for Unreal Engine"""
#         self.server_url = server_url
#         self.ws = None
#         self.unreal_audio_dir = Path("C:/UnrealAudio")
        
#         # Create Unreal audio directory if it doesn't exist
#         self.unreal_audio_dir.mkdir(parents=True, exist_ok=True)
#         log(f"Unreal audio directory: {self.unreal_audio_dir}")

#     def connect(self):
#         """Connect to WebSocket server"""
#         try:
#             log(f"Connecting to WebSocket server at {self.server_url}")
#             self.ws = websocket.create_connection(self.server_url)
#             log("Connected to WebSocket server")
#             return True
#         except Exception as e:
#             log(f"Failed to connect to WebSocket server: {e}", "error")
#             return False

#     def disconnect(self):
#         """Disconnect from WebSocket server"""
#         if self.ws:
#             self.ws.close()
#             log("Disconnected from WebSocket server")

#     def send_audio(self, audio_path):
#         """Send user speech to FastAPI backend & receive AI response"""
#         if not self.ws:
#             if not self.connect():
#                 log("Cannot send audio: not connected to server", "error")
#                 return None
        
#         try:
#             # Ensure audio path exists
#             audio_file = Path(audio_path)
#             if not audio_file.exists():
#                 log(f"Audio file not found: {audio_path}", "error")
#                 return None
            
#             log(f"Sending audio file: {audio_path}")
#             self.ws.send(json.dumps({"audio_path": str(audio_path)}))
            
#             # Receive AI response
#             log("Waiting for AI response...")
#             response = json.loads(self.ws.recv())
            
#             log(f"Received AI response: {response['answer'][:50]}...")
            
#             # Download AI Speech if available
#             if response["audio_url"]:
#                 audio_url = f"http://localhost:8000{response['audio_url']}"
#                 output_audio = self.unreal_audio_dir / "output.mp3"
                
#                 log(f"Downloading AI speech from {audio_url}")
#                 urllib.request.urlretrieve(audio_url, output_audio)
                
#                 log(f"Downloaded AI speech to {output_audio}")
#                 response["local_audio_path"] = str(output_audio)
                
#                 # Play audio in Unreal Engine
#                 self._play_audio_in_unreal(str(output_audio))
            
#             return response
            
#         except Exception as e:
#             log(f"Error in send_audio: {e}", "error")
#             # Try to reconnect
#             self.disconnect()
#             self.connect()
#             return None

#     def _play_audio_in_unreal(self, audio_path):
#         """Play audio file in Unreal Engine"""
#         try:
#             log(f"Playing audio in Unreal Engine: {audio_path}")
            
#             # Option 1: Use Unreal Engine's Sound Wave asset
#             # This requires importing the audio file as a Sound Wave asset first
#             # sound_wave = unreal.load_asset('/Game/Sounds/AIResponse')
#             # unreal.play_sound_at_location(sound_wave, unreal.Vector(0, 0, 0))
            
#             # Option 2: Use Windows Media Player (fallback)
#             os.system(f'start wmplayer "{audio_path}"')
            
#         except Exception as e:
#             log(f"Error playing audio: {e}", "error")

# # Function to be called from Unreal Engine Blueprint
# def process_voice_input(audio_path):
#     """Process voice input from Unreal Engine and return AI response"""
#     client = UnrealWebSocketClient()
    
#     if client.connect():
#         response = client.send_audio(audio_path)
#         client.disconnect()
#         return response
#     else:
#         log("Failed to connect to WebSocket server", "error")
#         return None

# # Example usage (for testing outside Unreal Engine)
# if __name__ == "__main__":
#     # This part won't run in Unreal Engine
#     print("This script is designed to be imported in Unreal Engine")
#     print("Example usage in Unreal Engine Python:")
#     print("import unreal_engine_ws")
#     print("response = unreal_engine_ws.process_voice_input('C:/UnrealAudio/input.wav')")

# # Process voice input and get AI response
# response = process_voice_input('C:/UnrealAudio/input.wav')

# # Access the response
# if response:
#     answer_text = response['answer']
#     audio_path = response['local_audio_path']
    
#     # Do something with the response in Unreal Engine
#     print(f"AI Answer: {answer_text}") 