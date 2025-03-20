# File: backend/scripts/system_check.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_system():
    print("Checking Virtual Teacher System Setup...")
    
    # Get the backend directory (two levels up from the script)
    backend_dir = Path(__file__).parent.parent
    
    # Check OpenAI API Key
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"\n1. OpenAI API Key: {'✓ Set' if api_key else '✗ Not Set'}")
    if not api_key:
        print("   Please set your OpenAI API key in the .env file")
    
    # Check Directories
    dirs_to_check = [
        'data/lectures',
        'data/audio',
        'data/vector_store'
    ]
    
    print("\n2. Directory Structure:")
    for dir_path in dirs_to_check:
        path = backend_dir / dir_path
        exists = path.exists()
        print(f"   {dir_path}: {'✓ Exists' if exists else '✗ Missing'}")
        
        # Create directory if it doesn't exist
        if not exists:
            path.mkdir(parents=True, exist_ok=True)
            print(f"   Created directory: {dir_path}")
    
    # Check Lecture Files
    lecture_dir = backend_dir / 'data/lectures'
    lecture_files = list(lecture_dir.glob('*.txt'))
    print(f"\n3. Lecture Files Found: {len(lecture_files)}")
    for file in lecture_files:
        print(f"   - {file.name}")
    
    # Additional Checks
    print("\n4. Database:")
    db_file = backend_dir / 'virtual_teacher.db'
    print(f"   SQLite DB: {'✓ Exists' if db_file.exists() else '✗ Missing'}")

    # Create a test lecture if no lectures exist
    if not lecture_files:
        print("\nNo lecture files found. Creating a test lecture...")
        create_test_lecture(lecture_dir)

def create_test_lecture(lecture_dir: Path):
    """Create a test lecture file"""
    test_content = """Introduction to Computer Science

Computer Science is the study of computation and information.
Computers are tools that help us solve complex problems.

Key Concepts:
1. Algorithms
2. Data Structures
3. Programming Languages

This introduction covers the basic concepts that all computer scientists should know."""
    
    test_file = lecture_dir / 'test_lecture.txt'
    test_file.write_text(test_content)
    print(f"Created test lecture: {test_file}")

if __name__ == "__main__":
    check_system()