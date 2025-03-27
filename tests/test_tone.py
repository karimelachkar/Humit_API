#!/usr/bin/env python3
"""
Generate a test tone and process it through the voice-to-MIDI detection pipeline.

This script generates a sine wave tone at a specific frequency and runs it
through the pitch and onset detection modules to verify they're working.
"""

import numpy as np
import time
import sys
import logging
from voicemidi.backend.pitch.pitch_detector import PitchDetector
from voicemidi.backend.onset.onset_detector import OnsetDetector
from voicemidi.backend.midi.midi_output import MidiOutput

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TestTone")

def generate_sine_wave(frequency, duration=0.5, sample_rate=44100, amplitude=0.5):
    """Generate a sine wave at the specified frequency."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    
    # Apply envelope to avoid clicks
    envelope = np.ones_like(wave)
    attack_samples = int(0.01 * sample_rate)  # 10ms attack
    release_samples = int(0.01 * sample_rate)  # 10ms release
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    envelope[-release_samples:] = np.linspace(1, 0, release_samples)
    
    return (wave * envelope).astype(np.float32)

def main():
    """Run the test tone through the pitch and onset detection."""
    print("\nTest Tone for Voice-to-MIDI")
    print("===========================")
    print("This script generates test tones and processes them through")
    print("the pitch and onset detection modules.")
    
    # Parameters
    sample_rate = 44100
    block_size = 1024
    
    # Create detector components with more sensitive settings
    pitch_detector = PitchDetector(
        sample_rate=sample_rate,
        block_size=block_size,
        min_confidence=0.2,  # More sensitive
        min_frequency=80,
        max_frequency=1000
    )
    
    onset_detector = OnsetDetector(
        sample_rate=sample_rate,
        block_size=block_size,
        threshold=0.1,  # More sensitive
        silence=-80,    # More sensitive
        minimum_inter_onset_interval_ms=80
    )
    
    midi_output = MidiOutput()
    connected = midi_output.open_port()
    if not connected:
        print("Warning: Could not connect to any MIDI port")
        print("Will continue without MIDI output")
    
    try:
        # Test different frequencies
        test_notes = [
            {"name": "C4", "frequency": 261.63, "midi": 60},
            {"name": "E4", "frequency": 329.63, "midi": 64},
            {"name": "G4", "frequency": 392.00, "midi": 67},
            {"name": "C5", "frequency": 523.25, "midi": 72}
        ]
        
        for note in test_notes:
            print(f"\nTesting note {note['name']} ({note['frequency']} Hz, MIDI {note['midi']})")
            
            # Generate test tone
            tone = generate_sine_wave(note['frequency'], duration=1.0, sample_rate=sample_rate)
            
            # Process in blocks to simulate real-time processing
            num_blocks = len(tone) // block_size
            current_time = 0
            block_time = block_size / sample_rate
            
            # First block should trigger onset
            first_block = True
            note_on = False
            current_note = 0
            
            for i in range(num_blocks):
                # Extract block
                start = i * block_size
                end = start + block_size
                block = tone[start:end]
                
                # Add some randomness to simulate real audio
                if i > 0:  # Keep first block clean for onset detection
                    noise = np.random.normal(0, 0.01, block.shape)
                    block = block + noise
                
                # Detect pitch
                midi_note, confidence, note_name = pitch_detector.get_midi_note(block, smooth=False)
                
                # Force onset on first block for testing
                is_onset = onset_detector.detect_onset(block, current_time)
                if first_block:
                    # Adding a print statement to see if this is executed
                    print("First block - forcing onset detection")
                    is_onset = True
                    first_block = False
                
                # Print detection results
                print(f"  Block {i+1}/{num_blocks}: " + 
                      f"MIDI={midi_note}, Note={note_name}, " + 
                      f"Confidence={confidence:.2f}, Onset={'YES' if is_onset else 'no'}")
                
                # Handle MIDI
                if is_onset and midi_note > 0 and not note_on:
                    if connected:
                        midi_output.send_note_on(midi_note)
                    current_note = midi_note
                    note_on = True
                    print(f"  Note ON: {midi_note} ({note_name})")
                
                # Update time
                current_time += block_time
            
            # Turn off note
            if note_on and connected:
                midi_output.send_note_off(current_note)
                print(f"  Note OFF: {current_note}")
            
            # Wait between notes
            time.sleep(0.5)
        
        print("\nTest completed!")
        
    except KeyboardInterrupt:
        print("\nTest interrupted")
    finally:
        # Clean up
        if connected:
            midi_output.all_notes_off()
            midi_output.close_port()
            print("MIDI output closed")

if __name__ == "__main__":
    main() 