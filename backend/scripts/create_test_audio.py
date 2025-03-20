#!/usr/bin/env python
# File: backend/scripts/create_test_audio.py
import os
import sys
from pathlib import Path
import wave
import numpy as np
import argparse

def create_test_audio(output_path, duration=3, sample_rate=16000):
    """Create a simple test audio file with a sine wave"""
    print(f"Creating test audio file at: {output_path}")
    
    # Create directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate a simple sine wave
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    tone = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
    
    # Convert to 16-bit PCM
    audio = (tone * 32767).astype(np.int16)
    
    # Write to WAV file
    with wave.open(output_path, 'w') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    
    print(f"Created test audio file: {output_path}")
    print(f"Duration: {duration} seconds")
    print(f"Sample rate: {sample_rate} Hz")
    print(f"File size: {os.path.getsize(output_path)} bytes")

def main():
    parser = argparse.ArgumentParser(description="Create a test audio file for WebSocket testing")
    parser.add_argument("--output", type=str, default="C:/UnrealAudio/input.wav",
                        help="Output path for the test audio file")
    parser.add_argument("--duration", type=float, default=3.0,
                        help="Duration of the test audio in seconds")
    args = parser.parse_args()
    
    create_test_audio(args.output, args.duration)
    
    print("\nYou can now use this file to test the WebSocket connection:")
    print(f"python scripts/test_websocket.py --audio \"{args.output}\"")

if __name__ == "__main__":
    main() 