#!/usr/bin/env python
"""
Test script to run the Voice-to-MIDI application.

This script provides a simple way to test the Voice-to-MIDI
application without installing it as a package.
"""

import sys
import time
import argparse
from voicemidi.backend.core.voicemidi import VoiceToMidi

def main():
    """Run the Voice-to-MIDI test."""
    parser = argparse.ArgumentParser(description="Test Voice-to-MIDI Converter")
    parser.add_argument("--config", default="config.json", help="Path to configuration file")
    parser.add_argument("--list-audio", action="store_true", help="List available audio devices")
    parser.add_argument("--list-midi", action="store_true", help="List available MIDI ports")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--duration", type=int, default=0, help="Test duration in seconds (0 for infinite)")
    
    args = parser.parse_args()
    
    # Create the application
    app = VoiceToMidi(args.config)
    
    # Set debug mode if requested
    if args.debug:
        app.set_debug(True)
    
    # List devices if requested
    if args.list_audio:
        app.list_audio_devices()
        return
    
    if args.list_midi:
        app.list_midi_ports()
        return
    
    # Print test information
    print("\n=== Voice-to-MIDI Test ===")
    print("Make sure your audio input (microphone) is connected")
    print("Make sure your DAW (e.g., Logic Pro X) is running and configured to receive MIDI from IAC Driver")
    print("\nPress Ctrl+C to stop the test")
    
    # Wait for user to be ready
    try:
        input("\nPress Enter to start the test...")
    except KeyboardInterrupt:
        print("\nTest canceled")
        return
    
    # Start the application
    if app.start():
        print("\nVoice-to-MIDI test running. Press Ctrl+C to stop.")
        
        try:
            if args.duration > 0:
                print(f"Test will run for {args.duration} seconds")
                time.sleep(args.duration)
            else:
                while True:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nTest interrupted")
        finally:
            app.stop()
            print("\nTest completed")
    else:
        print("\nFailed to start Voice-to-MIDI application")

if __name__ == "__main__":
    main() 