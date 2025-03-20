import unreal
import time
import sys
import os
import requests
import urllib.request
import urllib.error

# Make sure our scripts are in the Python path
project_dir = unreal.Paths.project_dir()
scripts_dir = os.path.join(project_dir, "Scripts")
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

# Import our modules
import audio_capture
import websocket_client
import audio_player

# Import chat handler with fallback
try:
    import chat_handler
except ImportError:
    unreal.log_warning("Chat handler not found, UI updates disabled")
    chat_handler = None

class ConversationManager:
    def __init__(self):
        """Initialize the conversation system by connecting all components"""
        # Initialize all subsystems
        self.audio_recorder = audio_capture.audio_recorder
        self.websocket_client = websocket_client.websocket_client
        self.audio_player = audio_player.audio_player
        
        # Status tracking
        self.is_conversation_active = False
        self.backend_connected = False
        
        # Connect to WebSocket server
        unreal.log("Connecting to AI backend...")
        self.backend_connected = self.websocket_client.connect()
        
        if self.backend_connected:
            unreal.log("Connected to AI backend successfully.")
            # Send a message to the chat UI
            if chat_handler:
                chat_handler.add_message("System", "Connected to AI backend successfully.")
        else:
            unreal.log_error("Failed to connect to AI backend. Check if server is running.")
            if chat_handler:
                chat_handler.add_message("System", "Failed to connect to AI backend. Check if server is running.")
    
    def update_status(self, status_text):
        """Update status in game"""
        unreal.log(status_text)
        # Send status updates to chat
        if chat_handler:
            chat_handler.update_status(status_text)
            chat_handler.add_message("System", f"Status: {status_text}")
    
    def start_voice_conversation(self, recording_duration=30):
        """Start a voice conversation by recording user speech and sending to AI"""
        if self.is_conversation_active:
            self.update_status("Conversation already in progress.")
            return False
        
        if not self.backend_connected:
            self.update_status("Cannot start conversation - not connected to AI backend.")
            return False
        
        try:
            self.is_conversation_active = True
            
            # Step 1: Record audio
            self.update_status("Starting audio recording...")
            self.audio_recorder.start_recording()
            
            # Wait for recording duration
            self.update_status(f"Recording for {recording_duration} seconds...")
            time.sleep(recording_duration)
            
            # Stop recording
            audio_file = self.audio_recorder.stop_recording()
            
            if not audio_file:
                self.update_status("Failed to record audio.")
                self.is_conversation_active = False
                return False
            
            self.update_status(f"Audio recorded: {audio_file}")
            
            # Step 2: Send to AI backend via WebSocket
            self.update_status("Sending to AI backend...")
            self.websocket_client.send_audio(audio_file, callback=self._handle_ai_response)
            
            # Add message to chat indicating voice input
            if chat_handler:
                chat_handler.add_message("You", "[Voice Message]")
            
            return True
            
        except Exception as e:
            self.update_status(f"Error in conversation: {str(e)}")
            self.is_conversation_active = False
            return False
    
    def send_text_message(self, text_message):
        """Send a text message to the AI backend"""
        if self.is_conversation_active:
            self.update_status("Conversation already in progress.")
            return False
        
        if not self.backend_connected:
            self.update_status("Cannot send message - not connected to AI backend.")
            return False
        
        if not text_message or text_message.strip() == "":
            self.update_status("Cannot send empty message.")
            return False
        
        try:
            self.is_conversation_active = True
            
            # Add message to chat history
            if chat_handler:
                chat_handler.add_message("You", text_message)
            
            # Send to AI backend
            self.update_status("Sending message to AI...")
            self.websocket_client.send_text(text_message, callback=self._handle_ai_response)
            
            return True
            
        except Exception as e:
            self.update_status(f"Error sending message: {str(e)}")
            self.is_conversation_active = False
            return False
    
    def _download_audio_file(self, audio_url):
        """Download audio file from URL and save locally"""
        try:
            timestamp = int(time.time())
            local_filename = os.path.join(self.audio_recorder.audio_dir, f"response_{timestamp}.mp3")
            
            self.update_status(f"Downloading audio from: {audio_url}")
            
            # Download the file
            try:
                # Try with requests first (handles more HTTP scenarios)
                response = requests.get(audio_url, stream=True)
                response.raise_for_status()  # Raise exception for HTTP errors
                
                with open(local_filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            except (ImportError, Exception) as req_error:
                # Fallback to urllib if requests fails or is not available
                unreal.log_warning(f"Requests download failed, trying urllib: {str(req_error)}")
                
                # Using urllib as fallback
                try:
                    urllib.request.urlretrieve(audio_url, local_filename)
                except urllib.error.URLError as url_error:
                    raise Exception(f"Failed to download using urllib: {str(url_error)}")
            
            self.update_status(f"Audio downloaded to: {local_filename}")
            return local_filename
            
        except Exception as e:
            self.update_status(f"Error downloading audio: {str(e)}")
            return None
    
    def _handle_ai_response(self, response_data):
        """Handle the AI response (called by WebSocket client)"""
        try:
            # Check response type
            if isinstance(response_data, dict):
                # Format from backend: {'type': 'text', 'question': '...', 'answer': '...', 'audio_url': '...'}
                response_type = response_data.get("type", "")
                
                # Handle text response
                if "answer" in response_data:
                    message = response_data["answer"]
                    
                    # Add message to chat history
                    if chat_handler:
                        chat_handler.add_message("AI", message)
                    
                    self.update_status("Received AI text response.")
                
                # Handle audio response
                if "audio_url" in response_data and response_data["audio_url"]:
                    audio_url = response_data["audio_url"]
                    
                    # Check if this is a local file path or a URL
                    if os.path.exists(audio_url):
                        # It's a local file path
                        self.update_status("Playing AI audio response...")
                        self.audio_player.play_audio_file(audio_url)
                    elif audio_url.startswith("/api/"):
                        # It's a URL relative to the backend
                        # We need to construct the full URL and download it
                        base_url = "http://localhost:8000"  # Adjust if your server is on a different port
                        full_audio_url = f"{base_url}{audio_url}"
                        
                        # Download the file
                        local_audio_file = self._download_audio_file(full_audio_url)
                        
                        # Play the audio if download was successful
                        if local_audio_file and os.path.exists(local_audio_file):
                            self.update_status("Playing AI audio response...")
                            self.audio_player.play_audio_file(local_audio_file)
                
                # For direct audio file responses (legacy format)
                elif response_type == "audio" and "file" in response_data:
                    audio_file = response_data["file"]
                    if os.path.exists(audio_file):
                        self.update_status("Playing AI response...")
                        self.audio_player.play_audio_file(audio_file)
            
            # Legacy format (string path to audio file)
            elif isinstance(response_data, str):
                if os.path.exists(response_data):
                    # It's an audio file path
                    self.update_status("Playing AI response...")
                    self.audio_player.play_audio_file(response_data)
                else:
                    # It's a text message
                    if chat_handler:
                        chat_handler.add_message("AI", response_data)
                    self.update_status("Received AI text response.")
            
            # Reset conversation state
            self.is_conversation_active = False
                
        except Exception as e:
            self.update_status(f"Error handling AI response: {str(e)}")
            self.is_conversation_active = False

# Create a global instance
conversation_manager = ConversationManager()

# Test functions to run in Unreal's Python console
def start_voice_conversation(duration=30):
    """Start a voice conversation with the AI"""
    return conversation_manager.start_voice_conversation(duration)

def send_text_message(message):
    """Send a text message to the AI"""
    return conversation_manager.send_text_message(message) 