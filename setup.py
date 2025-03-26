from setuptools import setup, find_packages

setup(
    name="voicemidi",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "sounddevice>=0.4.4",
        "aubio>=0.4.9",
        "librosa>=0.9.0",
        "mido>=1.2.10",
        "python-rtmidi>=1.4.9",
        "scipy>=1.7.0",
        "matplotlib>=3.5.0",
        "PyQt5>=5.15.0",
    ],
    entry_points={
        "console_scripts": [
            "voicemidi=voicemidi.main:main",
        ],
    },
    author="Karim Elachkar",
    description="Voice to MIDI converter for personal use",
    keywords="voice, midi, audio, music",
    python_requires=">=3.8",
) 