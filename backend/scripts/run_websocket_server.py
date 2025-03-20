#!/usr/bin/env python
# File: backend/scripts/run_websocket_server.py
import uvicorn
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent.absolute()
sys.path.append(str(backend_dir))

# Change working directory to backend
os.chdir(backend_dir)

if __name__ == "__main__":
    print("Starting WebSocket server...")
    print(f"Current working directory: {os.getcwd()}")
    print("WebSocket endpoint will be available at ws://localhost:8000/ws")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 