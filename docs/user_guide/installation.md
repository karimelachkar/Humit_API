# Installation Guide

This guide covers how to install the Voice-to-MIDI application on various operating systems.

## Prerequisites

- Python 3.8 or higher
- A working microphone
- MIDI routing configuration for your operating system

## Installation Options

### Method 1: Install from PyPI (Recommended)

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install voicemidi
```

### Method 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/voicemidi.git
cd voicemidi

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e .
```

## Platform-Specific Setup

### macOS

1. Configure the IAC Driver:
   - Open the "Audio MIDI Setup" application (in /Applications/Utilities)
   - From the menu, select Window > Show MIDI Studio
   - Double-click on the "IAC Driver" icon
   - Check "Device is online"
   - Add ports if needed

### Windows

1. Install loopMIDI:
   - Download and install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
   - Launch loopMIDI and create a new port named "VoiceToMIDI"

### Linux

1. Install ALSA and JACK dependencies:

   ```bash
   sudo apt-get install libasound2-dev libjack-jackd2-dev
   ```

2. Create a virtual MIDI port:
   ```bash
   sudo modprobe snd-virmidi
   ```

## Verifying Your Installation

Run the following command to verify that the installation was successful:

```bash
python -m voicemidi --help
```

You should see the help text for the application.
