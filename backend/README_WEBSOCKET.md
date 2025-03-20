# WebSocket Communication for Virtual Teacher

This document explains how to set up and use the WebSocket communication between Unreal Engine and the FastAPI backend for real-time voice-based AI conversations.

## Overview

The WebSocket communication enables:
- Sending audio from Unreal Engine to the FastAPI backend
- Processing speech-to-text using Whisper
- Retrieving relevant context using RAG
- Generating AI responses using OpenAI
- Converting responses to speech using TTS
- Sending text + audio back to Unreal Engine

## Setup Instructions

### 1. Install Dependencies

Make sure you have all the required dependencies installed:

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the WebSocket Server

Run the FastAPI WebSocket server:

```bash
python scripts/run_websocket_server.py
```

This will start the server on `ws://localhost:8000/ws`.

### 3. Test the WebSocket Connection

You can test the WebSocket connection using the provided test script:

```bash
python scripts/test_websocket.py --audio "path/to/your/audio.wav"
```

Make sure you have a WAV file available for testing. By default, the script looks for a file at `C:/UnrealAudio/input.wav`.

## Unreal Engine Integration

### Option 1: Using the Python API in Unreal Engine

1. Make sure Unreal Engine has Python 3.9+ installed with the required packages:
   - websocket-client
   - urllib
   - pathlib

2. Copy the `scripts/unreal_engine_ws.py` file to your Unreal Engine project's Python scripts directory.

3. In Unreal Engine, you can call the WebSocket client from Python:

```python
import unreal_engine_ws

# Process voice input and get AI response
response = unreal_engine_ws.process_voice_input('C:/UnrealAudio/input.wav')

# Access the response
if response:
    answer_text = response['answer']
    audio_path = response['local_audio_path']
    
    # Do something with the response in Unreal Engine
    print(f"AI Answer: {answer_text}")
```

### Option 2: Using Unreal Engine Blueprint with Python

1. Enable the "Python Editor Script Plugin" in Unreal Engine:
   - Go to Edit > Plugins
   - Search for "Python"
   - Enable "Python Editor Script Plugin"
   - Restart Unreal Engine

2. Create a Python Blueprint Function:
   - Create a new Blueprint
   - Add a Python Script Component
   - Create a function that calls the WebSocket client

3. Example Blueprint Python Script:

```python
import unreal
import unreal_engine_ws

class WebSocketBlueprintFunction:
    @unreal.ufunction(ret=str, params=[str])
    def process_voice(self, audio_path):
        """Process voice input and return AI response text"""
        response = unreal_engine_ws.process_voice_input(audio_path)
        if response:
            return response['answer']
        return "Error processing voice input"
```

## Directory Structure

The WebSocket functionality is organized as follows:

- `backend/websockets.py` - WebSocket server implementation
- `backend/scripts/unreal_ws_client.py` - WebSocket client for testing
- `backend/scripts/unreal_engine_ws.py` - WebSocket client for Unreal Engine
- `backend/scripts/run_websocket_server.py` - Script to run the WebSocket server
- `backend/scripts/test_websocket.py` - Script to test the WebSocket connection

## Workflow

1. User speaks into a microphone in Unreal Engine
2. Unreal Engine saves the voice input (e.g., `C:/UnrealAudio/input.wav`)
3. Unreal Engine sends the audio file path to the FastAPI backend via WebSockets
4. FastAPI processes the audio:
   - Converts speech to text using Whisper
   - Retrieves relevant context using RAG
   - Generates AI response using OpenAI
   - Converts response to speech using TTS
5. FastAPI sends the text response and audio URL back to Unreal Engine
6. Unreal Engine downloads the audio file and plays it

## Troubleshooting

- **Connection Issues**: Make sure the WebSocket server is running and accessible from Unreal Engine.
- **Audio File Not Found**: Ensure the audio file exists at the specified path.
- **Audio Playback Issues**: Check if the audio file is downloaded correctly and the player is working.
- **Missing Dependencies**: Verify all required packages are installed in both environments.

## Additional Resources

- [FastAPI WebSockets Documentation](https://fastapi.tiangolo.com/advanced/websockets/)
- [Unreal Engine Python API Documentation](https://docs.unrealengine.com/4.27/en-US/PythonAPI/)
- [WebSocket Client Documentation](https://websocket-client.readthedocs.io/) 