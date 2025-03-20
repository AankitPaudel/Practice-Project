# File: backend/audio/text_to_speech.py
from gtts import gTTS
from pathlib import Path
import uuid
import logging
import time
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextToSpeech:
    def __init__(self):
        """Initialize TextToSpeech with proper directory structure"""
        self.audio_dir = Path("data/audio")
        self.responses_dir = self.audio_dir / "responses"
        self.temp_dir = self.audio_dir / "temp"
        
        # Create all necessary directories
        for directory in [self.audio_dir, self.responses_dir, self.temp_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            
        logger.info("TextToSpeech initialized with directories setup")

    def _generate_unique_filename(self) -> str:
        """Generate a unique filename for the audio response"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"response_{timestamp}_{unique_id}.mp3"

    async def convert(self, text: str) -> Path:
        """Convert text to speech using gTTS and return the file path"""
        logger.info("Converting text to speech...")
        
        try:
            # Generate unique filename
            filename = self._generate_unique_filename()
            file_path = self.responses_dir / filename
            
            # Generate speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(str(file_path))
            
            logger.info(f"Successfully created audio file: {filename}")
            return file_path
            
        except Exception as e:
            logger.error(f"Text to speech conversion failed: {str(e)}")
            raise Exception(f"Text to speech conversion failed: {str(e)}")

    async def cleanup_old_files(self, max_age_hours: int = 1):
        """Clean up old audio files from both temp and responses directories"""
        try:
            current_time = time.time()
            max_age = max_age_hours * 3600
            
            # Clean up temp directory
            for file in self.temp_dir.glob("*.mp3"):
                if (current_time - file.stat().st_mtime) > max_age:
                    try:
                        file.unlink()
                        logger.info(f"Cleaned up temp file: {file}")
                    except Exception as e:
                        logger.error(f"Error deleting temp file {file}: {e}")
            
            # Clean up responses directory
            for file in self.responses_dir.glob("*.mp3"):
                if (current_time - file.stat().st_mtime) > max_age:
                    try:
                        file.unlink()
                        logger.info(f"Cleaned up response file: {file}")
                    except Exception as e:
                        logger.error(f"Error deleting response file {file}: {e}")
                        
            logger.info("Cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            raise Exception(f"Cleanup failed: {str(e)}")

    async def remove_file(self, file_path: Path):
        """Remove a specific file"""
        try:
            if file_path.exists():
                file_path.unlink()
                logger.info(f"Removed file: {file_path}")
        except Exception as e:
            logger.error(f"Error removing file {file_path}: {e}")