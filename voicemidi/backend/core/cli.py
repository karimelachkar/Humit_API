import sys
import time
import argparse
import signal
from typing import Optional

from voicemidi.backend.core.voicemidi import VoiceToMidi

# Global application instance used by signal handler
app: Optional[VoiceToMidi] = None

def signal_handler(sig, frame) -> None:
    """
    Handle interruption signals.
    
    Args:
        sig: Signal number
        frame: Current stack frame
    """
    print("\nInterrupted, shutting down...")
    global app
    if app:
        app.stop()
    sys.exit(0)

def main() -> None:
    """Main entry point for the Voice-to-MIDI application."""
    parser = argparse.ArgumentParser(description="Voice-to-MIDI Converter")
    parser.add_argument("--config", default="config.json", help="Path to configuration file")
    parser.add_argument("--list-audio", action="store_true", help="List available audio devices")
    parser.add_argument("--list-midi", action="store_true", help="List available MIDI ports")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()
    
    # Create the application
    global app
    app = VoiceToMidi(args.config)
    
    # Set debug mode if requested
    if args.debug:
        app.set_debug(True)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    
    # List devices if requested
    if args.list_audio:
        app.list_audio_devices()
        return
    
    if args.list_midi:
        app.list_midi_ports()
        return
    
    # Start the application
    if app.start():
        print("\nVoice-to-MIDI converter is running. Press Ctrl+C to stop.")
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            app.stop()

if __name__ == "__main__":
    main() 