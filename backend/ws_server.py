from fastapi import FastAPI, WebSocket
import json
from pathlib import Path
import asyncio
import logging
from audio.speech_to_text import SpeechToText
from qa.pipeline import QAPipeline
from audio.text_to_speech import TextToSpeech

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
stt = SpeechToText()
qa_pipeline = QAPipeline()
tts = TextToSpeech()

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
            # Step 1: Receive Audio File Path from Unreal
            data = await websocket.receive_text()
            request = json.loads(data)
            audio_path = Path(request["audio_path"])
            
            logger.info(f"Received audio path: {audio_path}")

            # Step 2: Convert Speech to Text
            user_text = await stt.convert(audio_path)
            logger.info(f"Recognized Text: {user_text}")

            # Step 3: Retrieve AI Response
            response = await qa_pipeline.get_answer(user_text)
            answer_text = response["answer"]
            
            # Step 4: Get audio URL from response (already generated in qa_pipeline)
            audio_url = response["audio_url"]

            # Step 5: Send AI response + audio URL back to Unreal
            response_data = {
                "question": user_text,
                "answer": answer_text,
                "audio_url": audio_url
            }

            await websocket.send_text(json.dumps(response_data))
            logger.info(f"Sent response to client: {answer_text[:50]}...")

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()
        logger.info("WebSocket connection closed due to error") 