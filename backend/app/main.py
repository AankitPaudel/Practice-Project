# File: backend/app/main.py
import sys
from pathlib import Path
import logging
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.routes import audio, qa, lectures

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

# Import necessary components
from audio.speech_to_text import SpeechToText
from qa.pipeline import QAPipeline
from audio.text_to_speech import TextToSpeech

# Fix for Python 3.8 compatibility with type annotations
from typing import Dict, Any
if sys.version_info < (3, 9):
    import typing
    typing.Dict = Dict
    typing.Any = Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Virtual Teacher API")

# Configure CORS - Update to allow all origins and methods
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up audio directories
AUDIO_DIR = Path("data/audio")
RESPONSES_DIR = AUDIO_DIR / "responses"
TEMP_DIR = AUDIO_DIR / "temp"

# Create necessary directories
for directory in [AUDIO_DIR, RESPONSES_DIR, TEMP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Mount static directory for serving audio files
app.mount(
    "/api/audio/responses", 
    StaticFiles(directory=str(RESPONSES_DIR), check_dir=True), 
    name="audio_responses"
)

# Mount static directory for serving static files (HTML, CSS, JS)
app.mount(
    "/static", 
    StaticFiles(directory=str(backend_dir / "static"), check_dir=True), 
    name="static"
)

# Include routers
app.include_router(qa.router, prefix="/api/qa", tags=["qa"])
app.include_router(audio.router, prefix="/api/audio", tags=["audio"])
app.include_router(lectures.router, prefix="/api/lectures", tags=["lectures"])

# Initialize components for WebSocket
stt = SpeechToText()
qa_pipeline = QAPipeline()
tts = TextToSpeech()

# Simple test endpoint
@app.websocket("/echo")
async def websocket_echo(websocket: WebSocket):
    await websocket.accept()
    logger.info("Echo client connected")
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Echo received: {data}")
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        logger.info("Echo client disconnected")

# Add WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time communication with Unreal Engine.
    
    This function handles:
    1. Receiving audio file paths from Unreal Engine
    2. Converting speech to text
    3. Generating AI responses
    4. Sending text + audio back to Unreal Engine
    """
    await websocket.accept()
    logger.info("Client connected")

    try:
        while True:
            # Receive data (can be text or JSON with audio path)
            data = await websocket.receive()
            
            # Check if we received text or binary data
            if "text" in data:
                # Text message (JSON)
                text_data = data["text"]
                try:
                    # Parse as JSON
                    json_data = json.loads(text_data)
                    logger.info(f"Received JSON data: {json_data}")
                    
                    # Check message type
                    if json_data.get("type") == "text_input":
                        # Handle text input
                        user_text = json_data.get("content", "")
                        logger.info(f"Received text message: {user_text}")
                        
                        if not user_text:
                            await websocket.send_text(json.dumps({
                                "type": "text",
                                "content": "Error: Empty message"
                            }))
                            continue
                        
                        # Generate AI response using our QA pipeline
                        logger.info("Generating AI response...")
                        response = await qa_pipeline.get_answer(user_text)
                        answer_text = response["answer"]
                        audio_url = response["audio_url"]
                        
                        # Send response back to client
                        response_data = {
                            "type": "text",
                            "question": user_text,
                            "answer": answer_text,
                            "audio_url": audio_url
                        }
                        
                        await websocket.send_text(json.dumps(response_data))
                        logger.info(f"Sent response to client: {answer_text[:50]}...")
                        
                    elif json_data.get("type") == "start_voice_recording":
                        # Just send status back - actual recording happens in client
                        await websocket.send_text(json.dumps({
                            "type": "status",
                            "content": "Voice recording started"
                        }))
                    
                except json.JSONDecodeError:
                    logger.error("Invalid JSON received")
                    await websocket.send_text(json.dumps({
                        "type": "text",
                        "content": "Error: Invalid JSON format"
                    }))
                
            else:
                # Process as before with existing code
                try:
                    # For backward compatibility with the existing implementation
                    data_text = await websocket.receive_text()
                    logger.info(f"Received data: {data_text}")
                    
                    request = json.loads(data_text)
                    
                    # Check if this is a text input (from chat UI)
                    if "text_input" in request:
                        user_text = request["text_input"]
                        logger.info(f"Received text input: {user_text}")
                    else:
                        # Process audio file
                        audio_path = Path(request["audio_path"])
                        logger.info(f"Received audio path: {audio_path}")
                        
                        # Convert Speech to Text
                        user_text = await stt.convert(audio_path)
                        logger.info(f"Recognized Text: {user_text}")

                    # Retrieve AI Response
                    response = await qa_pipeline.get_answer(user_text)
                    answer_text = response["answer"]
                    
                    # Get audio URL from response
                    audio_url = response["audio_url"]

                    # Send AI response + audio URL back to client
                    response_data = {
                        "question": user_text,
                        "answer": answer_text,
                        "audio_url": audio_url
                    }

                    await websocket.send_text(json.dumps(response_data))
                    logger.info(f"Sent response to client: {answer_text[:50]}...")
                except Exception as e:
                    logger.error(f"Error processing request: {e}")
                    error_response = {
                        "error": str(e),
                        "message": "Error processing request"
                    }
                    await websocket.send_text(json.dumps(error_response))

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.close()
        except:
            pass
        logger.info("WebSocket connection closed due to error")

@app.get("/")
async def root():
    return {
        "message": "Virtual Teacher API is running",
        "status": "ok",
        "chat_ui": "/static/chat_ui.html"
    }

@app.on_event("startup")
async def startup_event():
    # Log application startup and directory setup
    logger.info("Creating required directories...")
    logger.info(f"Audio responses directory: {RESPONSES_DIR}")
    logger.info(f"Temporary audio directory: {TEMP_DIR}")
    logger.info("WebSocket endpoint available at /ws")
    logger.info("Echo WebSocket endpoint available at /echo")
    logger.info("Chat UI available at /static/chat_ui.html")
    logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    # Cleanup on shutdown
    logger.info("Application shutting down...")
    try:
        # Cleanup temporary files
        for file in TEMP_DIR.glob("*.*"):
            try:
                file.unlink()
            except Exception as e:
                logger.error(f"Error deleting temp file {file}: {e}")
        
        logger.info("Cleanup completed")
    except Exception as e:
        logger.error(f"Error during shutdown cleanup: {e}")