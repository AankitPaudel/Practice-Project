# File: backend/app/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    # Base directory
    BASE_DIR: Path = Path(__file__).parent.parent

    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./virtual_teacher.db")

    # Paths
    VECTOR_STORE_PATH: str = str(BASE_DIR / "data/vector_store")
    AUDIO_TEMP_DIR: str = str(BASE_DIR / "data/audio/temp")
    AUDIO_RESPONSE_DIR: str = str(BASE_DIR / "data/audio/responses")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields

settings = Settings()