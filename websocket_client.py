import unreal
import websocket
import threading
import time
import os
import json

class WebSocketClient:
    def __init__(self, server_url="ws://localhost:8000/ws"):
        """Initialize WebSocket client with server URL"""
        self.server_url = server_url
        self.ws = None
        self.connected = False
        self.response_callback = None
        
        # Set up audio directory
        project_dir = unreal.Paths.project_dir()
        self.audio_dir = os.path.join(project_dir, "Audio")
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir)
            unreal.log(f"Created audio directory: {self.audio_dir}")
    
    def connect(self):
        """Connect to the WebSocket server"""
        try:
            websocket.enableTrace(False)  # Disable detailed logging for cleaner output
            
            # Create WebSocket connection
            self.ws = websocket.WebSocketApp(
                self.server_url,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            
            # Start WebSocket connection in a separate thread
            self.ws_thread = threading.Thread(target=self.ws.run_forever, daemon=True)
            self.ws_thread.start()
            
            # Wait for connection to establish
            timeout = 5
            start_time = time.time()
            while not self.connected and time.time() - start_time < timeout:
                time.sleep(0.1)
            
            if self.connected:
                unreal.log(f"Connected to WebSocket server at {self.server_url}")
                return True
            else:
                unreal.log_error(f"Failed to connect to WebSocket server at {self.server_url}")
                return False
                
        except Exception as e:
            unreal.log_error(f"Error connecting to WebSocket server: {str(e)}")
            return False
    
    def disconnect(self):
        """Disconnect from the WebSocket server"""
        if self.ws:
            self.ws.close()
            unreal.log("Disconnected from WebSocket server")
    
    def send_audio(self, audio_file, callback=None):
        """Send audio file to the WebSocket server"""
        if not self.connected:
            unreal.log_error("Not connected to WebSocket server")
            return False
        
        self.response_callback = callback
        
        try:
            # Read and send audio file
            with open(audio_file, 'rb') as f:
                audio_data = f.read()
            
            self.ws.send(audio_data, opcode=websocket.ABNF.OPCODE_BINARY)
            unreal.log(f"Sent audio file: {audio_file}")
            return True
            
        except Exception as e:
            unreal.log_error(f"Error sending audio: {str(e)}")
            return False
    
    def send_text(self, text_message, callback=None):
        """Send text message to the WebSocket server"""
        if not self.connected:
            unreal.log_error("Not connected to WebSocket server")
            return False
        
        self.response_callback = callback
        
        try:
            # Create JSON message format
            message = json.dumps({
                "type": "text",
                "question": text_message
            })
            
            self.ws.send(message)
            unreal.log(f"Sent text message: {text_message}")
            return True
            
        except Exception as e:
            unreal.log_error(f"Error sending text: {str(e)}")
            return False
    
    def _on_open(self, ws):
        """Called when WebSocket connection is established"""
        self.connected = True
        unreal.log("WebSocket connection opened")
    
    def _on_message(self, ws, message):
        """Called when a message is received from the server"""
        try:
            # Check if message is binary (audio file)
            if isinstance(message, bytes):
                timestamp = int(time.time())
                response_filename = os.path.join(self.audio_dir, f"response_{timestamp}.wav")
                
                with open(response_filename, 'wb') as f:
                    f.write(message)
                
                unreal.log(f"Received audio response: {response_filename}")
                
                # Call the callback function in the main thread
                if self.response_callback:
                    response_data = {
                        "type": "audio", 
                        "file": response_filename,
                        "audio_url": response_filename
                    }
                    unreal.execute_in_main_thread(lambda: self.response_callback(response_data))
            else:
                # Process text message
                try:
                    json_data = json.loads(message)
                    unreal.log(f"Received JSON response: {json_data}")
                    
                    # Handle response according to the format from chat_ui.html
                    # The response should contain type, question, answer, and audio_url
                    if isinstance(json_data, dict):
                        # Pass the entire response data to the callback
                        if self.response_callback:
                            unreal.execute_in_main_thread(lambda: self.response_callback(json_data))
                    else:
                        # Fallback to plain text
                        if self.response_callback:
                            response_data = {"type": "text", "answer": message}
                            unreal.execute_in_main_thread(lambda: self.response_callback(response_data))
                
                except json.JSONDecodeError:
                    # If not JSON, treat as raw text
                    unreal.log(f"Received plain text message: {message}")
                    
                    if self.response_callback:
                        response_data = {"type": "text", "answer": message}
                        unreal.execute_in_main_thread(lambda: self.response_callback(response_data))
        
        except Exception as e:
            unreal.log_error(f"Error processing WebSocket message: {str(e)}")
    
    def _on_error(self, ws, error):
        """Called when a WebSocket error occurs"""
        unreal.log_error(f"WebSocket error: {str(error)}")
    
    def _on_close(self, ws, close_status_code, close_reason):
        """Called when WebSocket connection is closed"""
        self.connected = False
        unreal.log(f"WebSocket connection closed: {close_reason} (code: {close_status_code})")

# Create a global instance
websocket_client = WebSocketClient()

# Test functions to run in Unreal's Python console
def test_connection():
    """Test connecting to the WebSocket server"""
    return websocket_client.connect()

def test_send_text(text):
    """Test sending a text message to the WebSocket server"""
    def on_response(response):
        unreal.log(f"Received response: {response}")
    
    websocket_client.send_text(text, callback=on_response)

def test_send_audio(audio_file):
    """Test sending an audio file to the WebSocket server"""
    def on_response(response):
        unreal.log(f"Received response: {response}")
    
    websocket_client.send_audio(audio_file, callback=on_response) 