# File: backend/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the base directory (where the backend folder is)
BASE_DIR = Path(__file__).parent.parent

# Configure database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    default=f"sqlite:///{BASE_DIR}/virtual_teacher.db"
)

# Create the SQLite database engine
try:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # Only needed for SQLite
        pool_pre_ping=True  # Add connection testing
    )
except Exception as e:
    print(f"Error creating database engine: {e}")
    raise

# Create the SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """
    Dependency function to get database session.
    Use this in FastAPI route dependencies.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database by creating all tables.
    Call this when setting up the application.
    """
    from .models.lecture import Base
    try:
        Base.metadata.create_all(bind=engine)
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

def test_db_connection():
    """
    Test database connection.
    Returns True if connection is successful, False otherwise.
    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False