# Voice-to-MIDI

A real-time Python application that converts voice input to MIDI notes. Similar to a simplified version of Dubler 2, but for personal use only.

## Features

- Real-time microphone input processing
- Pitch detection (voice frequency to MIDI note)
- Onset detection for note triggering
- MIDI output to DAWs via IAC MIDI Bus
- Low latency performance
- Simple GUI interface (coming soon)

## Requirements

- Python 3.8+
- macOS with Logic Pro X or other DAW
- IAC Driver configured for MIDI routing

## Installation

1. Clone this repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Usage

Run the application:

```
python -m voicemidi.main
```

### Test Scripts

We've included several test scripts to help you verify your setup:

- `test_mic.py`: Tests your microphone and audio input
- `test_midi.py`: Tests MIDI connectivity by sending notes to a selected MIDI port
- `run_terminal_test.py`: A simple terminal-based interface to test the voice-to-MIDI conversion

These scripts can be run directly with Python:

```
python test_mic.py
python test_midi.py
python run_terminal_test.py
```

### Setting up IAC Driver on macOS

1. Open the "Audio MIDI Setup" application (found in /Applications/Utilities)
2. From the menu, select Window > Show MIDI Studio (or press Cmd+2)
3. Double-click on the "IAC Driver" icon
4. Check "Device is online"
5. Add ports if needed by clicking the "+" button
6. Close the window to save the changes

## Architecture

This application uses:

- `sounddevice` for audio input
- `librosa` for pitch detection and onset detection
- `mido` and `python-rtmidi` for MIDI output
- `numpy` and `scipy` for signal processing

## Project Structure

- `audio/`: Audio input handling
- `pitch/`: Pitch detection algorithms
- `onset/`: Note onset detection
- `midi/`: MIDI output functionality
- `utils/`: Utility functions
- `gui/`: GUI interface (optional)

## License

For personal use only.
