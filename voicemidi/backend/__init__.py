"""Backend package for Voice-to-MIDI application.

This package contains all the core logic for the Voice-to-MIDI converter,
including audio processing, pitch detection, onset detection, and MIDI output.
"""

from voicemidi.backend.core import VoiceToMidi
from voicemidi.backend.audio import AudioInput
from voicemidi.backend.pitch import PitchDetector
from voicemidi.backend.onset import OnsetDetector
from voicemidi.backend.midi import MidiOutput

__all__ = [
    "VoiceToMidi",
    "AudioInput",
    "PitchDetector", 
    "OnsetDetector",
    "MidiOutput",
] 