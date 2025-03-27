#!/usr/bin/env python3
"""
Simple microphone test script to verify audio input.
"""

import numpy as np
import sounddevice as sd
import time

def main():
    """Run a simple microphone test."""
    print("\nMicrophone Test")
    print("==============")
    print("This will test your microphone to make sure audio input is working.")
    print("Press Ctrl+C to exit.")
    
    # Audio parameters
    sample_rate = 44100
    block_size = 1024
    channels = 1
    duration = 5  # seconds
    
    # List audio devices
    print("\nAvailable audio devices:")
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        print(f"  {i}: {device['name']} (in={device['max_input_channels']}, out={device['max_output_channels']})")
    
    # Ask for input device
    try:
        default_device = sd.query_devices(kind='input')['name']
        print(f"\nDefault input device: {default_device}")
        choice = input("Select device number (or press Enter for default): ")
        
        device = None if not choice else int(choice)
        
        print(f"\nRecording for {duration} seconds...")
        
        # Start recording
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=channels,
            device=device
        )
        
        # Show audio level during recording
        start_time = time.time()
        try:
            while time.time() - start_time < duration:
                # Get the current recorded audio
                elapsed = time.time() - start_time
                current_samples = int(elapsed * sample_rate)
                if current_samples > 0 and current_samples < len(recording):
                    # Calculate RMS (audio level)
                    current_audio = recording[:current_samples]
                    rms = np.sqrt(np.mean(np.square(current_audio)))
                    db = 20 * np.log10(rms) if rms > 0 else -100
                    
                    # Create level meter
                    level = max(0, min(60, 60 + db)) / 60  # Normalize to 0-1 range
                    meter_width = 50
                    bar = '█' * int(level * meter_width) + '░' * (meter_width - int(level * meter_width))
                    
                    # Display
                    print(f"\rLevel: {bar} {db:.1f} dB", end='', flush=True)
                    
                time.sleep(0.05)
        except KeyboardInterrupt:
            pass
        
        # Wait for recording to complete
        sd.wait()
        
        # Calculate stats on the recording
        rms = np.sqrt(np.mean(np.square(recording)))
        db = 20 * np.log10(rms) if rms > 0 else -100
        peak = np.max(np.abs(recording))
        peak_db = 20 * np.log10(peak) if peak > 0 else -100
        
        print(f"\n\nRecording complete!")
        print(f"Average level: {db:.1f} dB")
        print(f"Peak level: {peak_db:.1f} dB")
        
        if db < -50:
            print("\nAudio level seems very low. Please check your microphone connection and settings.")
        elif db > -10:
            print("\nAudio level seems high. You might want to lower your microphone input volume.")
        else:
            print("\nAudio level looks good!")
            
        print("\nMicrophone test completed.")
        
    except KeyboardInterrupt:
        print("\nTest cancelled.")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main() 