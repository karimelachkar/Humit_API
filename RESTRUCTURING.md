# Voice-to-MIDI Package Restructuring

This project has been restructured to follow a more organized package layout, separating the backend logic from potential frontend components.

## Changes Made

1. Moved all core functionality to a `backend` subpackage
2. Split the monolithic `main.py` file into:
   - `backend/core/voicemidi.py` - The main `VoiceToMidi` class
   - `backend/core/cli.py` - Command-line interface functionality
3. Added proper type hints and improved docstrings
4. Updated logging to use a proper logger hierarchy
5. Ensured all functions have return type annotations
6. Improved error handling throughout the codebase

## Directory Structure

The new package structure is as follows:

```
voicemidi/
├── __init__.py
├── __main__.py
├── backend/
│   ├── __init__.py
│   ├── audio/
│   │   ├── __init__.py
│   │   └── audio_input.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   └── voicemidi.py
│   ├── midi/
│   │   ├── __init__.py
│   │   └── midi_output.py
│   ├── onset/
│   │   ├── __init__.py
│   │   └── onset_detector.py
│   ├── pitch/
│   │   ├── __init__.py
│   │   └── pitch_detector.py
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       └── logger.py
```

## Benefits of the New Structure

1. **Maintainability**: Smaller, focused files are easier to understand and maintain
2. **Extensibility**: Clear separation of concerns makes it easier to add new features
3. **Testability**: Components can be tested in isolation
4. **Future-proofing**: Ready for adding a GUI or web interface without modifying the core logic

## Using the New Structure

The package can be used the same way as before:

```python
from voicemidi import VoiceToMidi

vm = VoiceToMidi()
vm.start()
```

The command-line interface also works the same:

```
python -m voicemidi
```

## Transition Process

1. The original package structure has been preserved in a backup
2. All imports have been updated to use the new structure
3. All test scripts have been updated to work with the new structure

If you find any issues with the new structure, please report them on the issue tracker.
