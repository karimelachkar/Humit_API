"""Voice-to-MIDI Application.

A real-time Python application that converts voice input to MIDI notes.
Detects pitch from microphone input and converts it to MIDI notes,
with onset detection for note triggering.

Version: 0.1.0
"""

__version__ = "0.1.0"

from voicemidi.backend import VoiceToMidi

__all__ = ["VoiceToMidi"] 