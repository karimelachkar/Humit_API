# Quick Start Guide

This guide will get you up and running with Voice-to-MIDI in minutes.

## Basic Usage

### 1. Start the Application

After installation, run the application with:

```bash
python -m voicemidi
```

### 2. List Available Devices

To see available audio inputs and MIDI outputs:

```bash
# List audio devices
python -m voicemidi --list-audio

# List MIDI devices
python -m voicemidi --list-midi
```

### 3. Run with Specific Devices

```bash
# Using device IDs
python -m voicemidi --audio-device 1 --midi-port 0

# Using device names (enclose in quotes if it contains spaces)
python -m voicemidi --audio-device "Built-in Microphone" --midi-port "VoiceToMIDI"
```

### 4. Enable Debug Mode

For troubleshooting:

```bash
python -m voicemidi --debug
```

## Configuration

The application uses reasonable defaults, but you can customize its behavior:

1. Create a custom configuration file:

```bash
# Copy the default config
cp ~/.voicemidi/config.json myconfig.json

# Edit with your preferred text editor
nano myconfig.json
```

2. Run with your custom config:

```bash
python -m voicemidi --config myconfig.json
```

## Testing Your Setup

Run these test scripts to verify your setup:

```bash
# Test microphone
python -m voicemidi.tests.test_mic

# Test MIDI output
python -m voicemidi.tests.test_midi

# Terminal test interface
python -m voicemidi.tests.run_terminal_test
```

## Using with a DAW

1. Start your DAW (Logic, Ableton, FL Studio, etc.)
2. In your DAW, configure a MIDI track to receive input from "VoiceToMIDI"
3. Start Voice-to-MIDI
4. Sing or hum into your microphone and watch your DAW receive MIDI notes!

## Next Steps

- See the [Configuration Guide](configuration.md) for detailed settings
- Check [Troubleshooting](troubleshooting.md) if you encounter issues
