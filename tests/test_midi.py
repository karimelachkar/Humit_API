#!/usr/bin/env python3
"""
Simple MIDI test script to verify MIDI output connectivity.
"""

import mido
import time
import random

def main():
    """Run a simple MIDI test."""
    print("\nMIDI Output Test")
    print("===============")
    print("This will test MIDI output connectivity by sending notes to the selected port.")
    print("Press Ctrl+C to exit.")
    
    # List available MIDI output ports
    midi_ports = mido.get_output_names()
    print("\nAvailable MIDI output ports:")
    for i, port in enumerate(midi_ports):
        print(f"  {i}: {port}")
    
    # Check if there are any MIDI ports
    if not midi_ports:
        print("\nNo MIDI ports found!")
        print("On macOS, you can set up the IAC Driver in Audio MIDI Setup")
        print("to create virtual MIDI ports for use with software like Logic Pro X.")
        return
    
    # Ask user to select MIDI port
    try:
        choice = input("\nSelect MIDI port number: ")
        if not choice:
            print("No MIDI port selected. Exiting.")
            return
            
        port_idx = int(choice)
        if port_idx < 0 or port_idx >= len(midi_ports):
            print("Invalid port number. Exiting.")
            return
            
        port_name = midi_ports[port_idx]
        print(f"\nConnecting to MIDI port: {port_name}")
        
        # Open the MIDI port
        try:
            midi_out = mido.open_output(port_name)
            print("Connected successfully!")
            
            # Send MIDI messages
            print("\nSending MIDI notes...")
            print("Press Ctrl+C to stop.")
            
            notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C Major scale
            try:
                while True:
                    # Play a random note
                    note = random.choice(notes)
                    velocity = random.randint(64, 100)
                    
                    print(f"\rPlaying note: {note} (velocity: {velocity})   ", end='', flush=True)
                    
                    # Note On
                    midi_out.send(mido.Message('note_on', note=note, velocity=velocity))
                    
                    # Wait
                    time.sleep(0.2)
                    
                    # Note Off
                    midi_out.send(mido.Message('note_off', note=note, velocity=0))
                    
                    # Pause between notes
                    time.sleep(0.1)
                    
            except KeyboardInterrupt:
                print("\n\nStopping...")
                
            # Turn off all notes
            midi_out.send(mido.Message('control_change', control=123, value=0))
            midi_out.close()
            print("MIDI port closed. Test completed.")
            
        except Exception as e:
            print(f"Error connecting to MIDI port: {e}")
    
    except KeyboardInterrupt:
        print("\nTest cancelled.")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main() 