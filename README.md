# Voice-to-MIDI

A real-time Python application that converts voice input to MIDI notes. Similar to a simplified version of Dubler 2, but for personal use only.

## Features

- Real-time microphone input processing
- Pitch detection (voice frequency to MIDI note)
- Onset detection for note triggering
- MIDI output to DAWs via IAC MIDI Bus or other MIDI interfaces
- Low latency performance
- Simple GUI interface (coming soon)

## Requirements

- Python 3.8+
- Compatible with macOS, Windows, and Linux
- A DAW (Digital Audio Workstation) like Logic Pro, Ableton Live, GarageBand, FL Studio, etc.
- MIDI routing configuration (IAC Driver on macOS, loopMIDI on Windows, ALSA MIDI on Linux)

## Installation

### macOS

1. Clone this repository

   ```
   git clone https://github.com/yourusername/voicemidi.git
   cd voicemidi
   ```

2. Create and activate a virtual environment

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the package in development mode

   ```
   pip install -e .
   ```

### Windows

1. Clone this repository

   ```
   git clone https://github.com/yourusername/voicemidi.git
   cd voicemidi
   ```

2. Create and activate a virtual environment

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the package in development mode

   ```
   pip install -e .
   ```

4. Install loopMIDI for MIDI routing
   - Download and install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
   - Create a virtual MIDI port named "VoiceToMIDI"

### Linux

1. Clone this repository

   ```
   git clone https://github.com/yourusername/voicemidi.git
   cd voicemidi
   ```

2. Create and activate a virtual environment

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the package in development mode

   ```
   pip install -e .
   ```

4. Install ALSA and JACK dependencies
   ```
   sudo apt-get install libasound2-dev libjack-jackd2-dev
   ```

## Usage

Run the application:

```
python -m voicemidi
```

Command line options:

```
python -m voicemidi --help
python -m voicemidi --list-audio  # List available audio input devices
python -m voicemidi --list-midi   # List available MIDI output ports
python -m voicemidi --debug       # Run with debug logging enabled
python -m voicemidi --config custom_config.json  # Use a custom config file
```

### Test Scripts

We've included several test scripts in the `tests` directory to help you verify your setup:

- `test_mic.py`: Tests your microphone and audio input
- `test_midi.py`: Tests MIDI connectivity by sending notes to a selected MIDI port
- `test_tone.py`: Tests pitch detection with synthetic tones
- `test_voicemidi.py`: Tests the core Voice-to-MIDI functionality
- `run_terminal_test.py`: A simple terminal-based interface to test the voice-to-MIDI conversion

You can run tests using the test runner script:

```
# List available tests
python tests/run_tests.py --list

# Run a specific test
python tests/run_tests.py test_mic

# Run a specific test with arguments
python tests/run_tests.py test_mic --args --list
```

Alternatively, you can run each test script directly:

```
python tests/test_mic.py
python tests/test_midi.py
python tests/test_tone.py
python tests/test_voicemidi.py
python tests/run_terminal_test.py
```

### Configuration

The application uses a `config.json` file for configuration. You can edit this file to adjust various settings:

- Audio: sample rate, block size, input device
- Pitch detection: minimum confidence, frequency range
- Onset detection: threshold, silence level
- MIDI: port name, virtual port name, velocity

Example configuration:

```json
{
  "audio": {
    "sample_rate": 44100,
    "block_size": 1024,
    "channels": 1,
    "device": null
  },
  "pitch": {
    "min_confidence": 0.2,
    "min_frequency": 50,
    "max_frequency": 1000
  },
  "onset": {
    "threshold": 0.3,
    "silence": -70,
    "minimum_inter_onset_interval_ms": 80
  },
  "midi": {
    "virtual_port_name": "VoiceToMIDI",
    "port_name": null
  }
}
```

### Setting up MIDI Routing

#### macOS (IAC Driver)

1. Open the "Audio MIDI Setup" application (found in /Applications/Utilities)
2. From the menu, select Window > Show MIDI Studio (or press Cmd+2)
3. Double-click on the "IAC Driver" icon
4. Check "Device is online"
5. Add ports if needed by clicking the "+" button
6. Close the window to save the changes

#### Windows (loopMIDI)

1. Download and install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
2. Launch loopMIDI and click the "+" button to create a new port
3. Name the port "VoiceToMIDI" or update your config.json to match your chosen name

#### Linux (ALSA)

1. Install ALSA utilities if not already installed:
   ```
   sudo apt-get install alsa-utils
   ```
2. Create a virtual MIDI port:
   ```
   sudo modprobe snd-virmidi
   ```

## Troubleshooting

### No Audio Input Detected

- Check that your microphone is properly connected and selected in your system settings
- Try running `python test_mic.py` to verify your microphone works
- Adjust the silence threshold in config.json (try -80 to -60 dB)

### No MIDI Output

- Verify MIDI routing setup by running `python test_midi.py`
- Check that the MIDI port name in config.json matches an available port
- Make sure your DAW is configured to receive MIDI from the correct port

### Pitch Detection Issues

- Try adjusting the min_confidence setting in config.json
- Run `python test_tone.py` to verify pitch detection is working correctly
- Speak or sing more clearly and consistently into the microphone

## Architecture

This application uses:

- `sounddevice` for audio input
- `librosa` and `aubio` for pitch detection and onset detection
- `mido` and `python-rtmidi` for MIDI output
- `numpy` and `scipy` for signal processing

## Project Structure

- `audio/`: Audio input handling
- `pitch/`: Pitch detection algorithms
- `onset/`: Note onset detection
- `midi/`: MIDI output functionality
- `utils/`: Utility functions
- `gui/`: GUI interface (coming soon)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

Basic workflow:

```bash
# Clone the repository
git clone https://github.com/yourusername/voicemidi.git
cd voicemidi

# Create a virtual environment and activate it
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
make dev-install

# Run tests
make test

# Format code
make format

# Run linting
make lint

# Run the application
make run
```

## Development Tools

This project uses several development tools:

- [pytest](https://docs.pytest.org/) - For testing
- [Black](https://black.readthedocs.io/) - For code formatting
- [isort](https://pycqa.github.io/isort/) - For import sorting
- [flake8](https://flake8.pycqa.org/) - For code linting

All configuration is in `pyproject.toml`, `.flake8`, and `pytest.ini`.

## License

For personal use only.
