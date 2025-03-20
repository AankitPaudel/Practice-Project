# File: backend/audio/speech_to_text.py
from faster_whisper import WhisperModel
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SpeechToText:
    def __init__(self):
        try:
            # Simplified initialization with only required parameters
            self.model = WhisperModel(
                "tiny",  # Using tiny model for faster processing
                device="cpu"
            )
            logger.info("Speech to text model initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing speech to text model: {str(e)}")
            raise

    async def convert(self, audio_file: Path) -> str:
        """Convert speech to text"""
        try:
            logger.info(f"Processing audio file: {audio_file}")
            
            # Transcribe audio
            segments, _ = self.model.transcribe(
                str(audio_file),
                language="en"
            )
            
            # Join segments
            text = " ".join([segment.text for segment in segments])
            text = text.strip()
            
            logger.info(f"Successfully transcribed audio to: {text[:50]}...")
            return text
            
        except Exception as e:
            logger.error(f"Error in speech to text conversion: {str(e)}")
            raise