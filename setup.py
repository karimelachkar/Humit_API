from setuptools import setup, find_packages
import os

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

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
            "voicemidi=voicemidi.backend.core.cli:main",
        ],
    },
    author="Karim Elachkar",
    author_email="your.email@example.com",  # Update with your email
    description="A real-time application that converts voice input to MIDI notes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="voice, midi, audio, music, pitch detection, onset detection",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Musicians",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Multimedia :: Sound/Audio :: MIDI",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
    ],
    include_package_data=True,
    license="Proprietary",
) 