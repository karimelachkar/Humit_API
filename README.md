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
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Usage

Run the application:

```
python -m voicemidi.main
```

## Project Structure

- `audio/`: Audio input handling
- `pitch/`: Pitch detection algorithms
- `onset/`: Note onset detection
- `midi/`: MIDI output functionality
- `utils/`: Utility functions
- `gui/`: GUI interface (optional)

## License

For personal use only.
