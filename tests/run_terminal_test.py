#!/usr/bin/env python3
"""
Terminal-based test script for Voice-to-MIDI application.

This script provides a simple terminal UI to test the Voice-to-MIDI application
without requiring a full GUI. It shows the detected pitch, note, and onsets
in real-time in the terminal.
"""

import time
import sys
import numpy as np
import threading
from voicemidi.backend.audio.audio_input import AudioInput
from voicemidi.backend.pitch.pitch_detector import PitchDetector
from voicemidi.backend.onset.onset_detector import OnsetDetector
from voicemidi.backend.midi.midi_output import MidiOutput

# ANSI color codes for terminal output
RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m" 
RED = "\033[31m"
BLUE = "\033[34m"
CYAN = "\033[36m"

def clear_line():
    """Clear the current terminal line."""
    sys.stdout.write("\r\033[K")  # Carriage return + clear line
    sys.stdout.flush()

def create_progress_bar(value, max_value=127, width=20):
    """Create a visual progress bar."""
    filled_width = int(width * value / max_value)
    bar = "█" * filled_width + "░" * (width - filled_width)
    return bar

def main():
    """Run the Voice-to-MIDI terminal test."""
    print("\n===== Voice-to-MIDI Terminal Test =====")
    print("This will test voice-to-MIDI conversion and show results in the terminal.")
    print("It will also send MIDI data to your MIDI devices/software.")
    print("\nMake sure your microphone is connected.")
    print("Press Ctrl+C to exit.")
    
    try:
        input("\nPress Enter to start...")
    except KeyboardInterrupt:
        return
    
    # Initialize components
    sample_rate = 44100
    block_size = 1024
    
    audio_input = AudioInput(sample_rate=sample_rate, block_size=block_size)
    pitch_detector = PitchDetector(sample_rate=sample_rate, block_size=block_size)
    onset_detector = OnsetDetector(sample_rate=sample_rate, block_size=block_size)
    midi_output = MidiOutput()
    
    # Start audio input
    try:
        audio_input.start()
    except Exception as e:
        print(f"Error starting audio input: {e}")
        return
    
    # Open MIDI port
    if not midi_output.open_port():
        print("Failed to open MIDI port. Continue anyway? (y/n)")
        if input().lower() != 'y':
            audio_input.stop()
            return
    
    # State
    is_running = True
    current_note = 0
    note_on = False
    onset_count = 0
    current_time = 0
    
    # Display header
    print("\n" + "=" * 60)
    print("  MIDI   Note   Frequency   Confidence   Onset   Status")
    print("=" * 60)
    
    try:
        # Main loop
        while is_running:
            # Get audio data
            audio_data = audio_input.get_audio_block()
            if audio_data is None:
                time.sleep(0.001)
                continue
            
            # Update time
            current_time += block_size / sample_rate
            
            # Detect pitch
            midi_note, confidence, note_name = pitch_detector.get_midi_note(audio_data)
            
            # Detect onset
            is_onset = onset_detector.detect_onset(audio_data, current_time)
            if is_onset:
                onset_count += 1
            
            # Convert frequency from midi note
            if midi_note > 0:
                frequency = 440.0 * (2.0 ** ((midi_note - 69) / 12.0))
            else:
                frequency = 0
            
            # Handle MIDI
            if is_onset and midi_note > 0 and not note_on:
                # New note
                midi_output.send_note_on(midi_note)
                current_note = midi_note
                note_on = True
                status = f"{GREEN}Note ON{RESET}"
            elif midi_note != current_note and midi_note > 0 and note_on:
                # Changed note
                midi_output.send_note_off(current_note)
                midi_output.send_note_on(midi_note)
                current_note = midi_note
                status = f"{BLUE}Note Change{RESET}"
            elif is_onset and note_on:
                # Retrigger
                midi_output.send_note_off(current_note)
                midi_output.send_note_on(midi_note if midi_note > 0 else current_note)
                status = f"{YELLOW}Retrigger{RESET}"
            elif midi_note == 0 and note_on:
                # Note off
                midi_output.send_note_off(current_note)
                note_on = False
                status = f"{RED}Note OFF{RESET}"
            else:
                status = "Listening"
            
            # Display info
            clear_line()
            if midi_note > 0:
                note_display = f"{CYAN}{midi_note:3d}{RESET}   {note_name:4s}"
                freq_display = f"{frequency:7.1f} Hz"
                conf_display = f"{confidence:6.2f}"
            else:
                note_display = f"---   ----"
                freq_display = f"  --- Hz"
                conf_display = f" -----"
            
            onset_display = "YES" if is_onset else " - "
            
            # Progress bar for MIDI note
            note_bar = create_progress_bar(midi_note if midi_note > 0 else 0, max_value=127, width=20)
            
            sys.stdout.write(f"\r  {note_display}   {freq_display}   {conf_display}    {onset_display}   {status}")
            sys.stdout.flush()
            
            # Small delay to prevent high CPU usage
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\n\nExiting...")
    finally:
        # Clean up
        midi_output.all_notes_off()
        midi_output.close_port()
        audio_input.stop()
        print("\nApplication stopped.")

if __name__ == "__main__":
    main() 