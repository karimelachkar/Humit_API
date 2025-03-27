# VoiceMIDI Frontend

The VoiceMIDI frontend is an Electron-based desktop application that provides a user interface for the VoiceMIDI voice-to-MIDI conversion engine.

## Structure

The frontend is organized as follows:

```
voicemidi/frontend/
├── assets/           # Static assets like images, icons, etc.
├── css/              # CSS stylesheets
│   ├── styles.css    # Main application styles
│   ├── keyboard.css  # Styles for the piano keyboard
│   └── visualizer.css # Styles for the audio visualizer
├── js/               # JavaScript modules
│   ├── app.js        # Main application logic
│   ├── keyboard.js   # Piano keyboard visualization
│   ├── visualizer.js # Audio waveform visualization
│   ├── calibration.js # Microphone calibration
│   ├── settings.js   # Settings management
│   └── ui.js         # UI initialization and management
├── index.html        # Main application HTML
├── main.js           # Electron main process
├── preload.js        # Preload script for Electron
└── package.json      # Node.js dependencies and scripts
```

## Setup and Development

### Prerequisites

- Node.js 16+ and npm

### Installation

```bash
# Navigate to the frontend directory
cd voicemidi/frontend

# Install dependencies
npm install
```

### Development

```bash
# Start the application in development mode
npm run dev
```

This will start the Electron application with hot-reloading enabled.

### Building

```bash
# Package the application for distribution
npm run build
```

This will create distributables for your current platform in the `dist` directory.

## Architecture

The frontend follows a modular architecture with separate concerns:

- **main.js**: Handles the Electron main process, window creation, and IPC communication
- **preload.js**: Provides secure communication between the renderer process and main process
- **app.js**: Contains the core application logic and state management
- **ui.js**: Handles UI initialization and common UI functionality
- **keyboard.js**: Manages the piano keyboard visualization
- **visualizer.js**: Handles the audio waveform visualization
- **calibration.js**: Manages microphone calibration
- **settings.js**: Handles application settings

## Features

- Real-time audio waveform visualization
- Visual piano keyboard with active note highlighting
- Scale and key restriction
- Microphone calibration
- MIDI port selection
- Configurable pitch correction
- Light and dark themes
- Custom scale creation
- Velocity sensitivity control

## Communication with Backend

The frontend communicates with the Python backend through the Electron main process. The main process spawns the Python backend as a child process and communicates with it through IPC.

Key API endpoints:

- `listAudioDevices()`: List available audio input devices
- `listMidiDevices()`: List available MIDI output ports
- `startAnalysis()`: Start audio analysis and MIDI conversion
- `stopAnalysis()`: Stop audio analysis and MIDI conversion
- `setAudioDevice(deviceId)`: Select audio input device
- `setMidiDevice(deviceId)`: Select MIDI output port
- `calibrateMicrophone()`: Run microphone calibration
- `setScale(scale, keyCenter)`: Set the current scale and key

## UI Components

- **Header**: Contains the logo and main control buttons (Start/Stop, Calibrate, Settings)
- **Left Panel**: Contains the audio visualizer, piano keyboard, and audio level meter
- **Right Panel**: Contains settings for scale, key, pitch controls, velocity, MIDI output, and audio input
- **Status Bar**: Shows the status of audio input and MIDI output
- **Dialogs**: Calibration and settings dialogs

## Adding New Features

To add new features to the frontend:

1. Identify the appropriate module for your feature
2. Add the necessary UI elements to `index.html`
3. Add styles to the appropriate CSS file
4. Implement the functionality in the JavaScript module
5. Connect the feature to the backend through the API if needed
