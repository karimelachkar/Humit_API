"""
This is a setup.py script generated for creating a macOS application bundle
using py2app.

Usage:
    python setup_mac.py py2app
"""

from setuptools import setup
import os
import sys

# Check if we're on macOS
if sys.platform != 'darwin':
    print("This script is for macOS only.")
    sys.exit(1)

APP = ['voicemidi/main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',  # You'll need to create an icon file
    'plist': {
        'CFBundleName': 'VoiceToMIDI',
        'CFBundleDisplayName': 'Voice to MIDI',
        'CFBundleGetInfoString': 'Voice to MIDI Converter',
        'CFBundleIdentifier': 'com.voicemidi.app',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'NSHumanReadableCopyright': 'For personal use only.',
        'NSHighResolutionCapable': True,
    },
    'packages': [
        'numpy',
        'aubio',
        'sounddevice',
        'mido',
        'rtmidi',
    ],
    'includes': [
        'numpy',
        'aubio',
        'sounddevice',
        'mido',
        'rtmidi',
    ],
    'excludes': [
        'tkinter',
        'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtWebEngine',
    ],
    'resources': [
        'config.json',
    ],
    'optimize': 2,
}

setup(
    name='VoiceToMIDI',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 