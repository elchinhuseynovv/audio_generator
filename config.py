"""
Configuration settings for the Voice-to-Music Generator
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Audio settings
SAMPLE_RATE = 44100
DEFAULT_DURATION = 5
CHANNELS = 1
DTYPE = 'int16'

# MIDI settings
TEMPO = 120
VELOCITY = 100  # Note velocity (volume)
DEFAULT_OCTAVE = 4

# File paths
OUTPUT_DIR = "output"
RECORDINGS_DIR = os.path.join(OUTPUT_DIR, "recordings")
MIDI_DIR = os.path.join(OUTPUT_DIR, "midi")

# Create directories if they don't exist
for directory in [OUTPUT_DIR, RECORDINGS_DIR, MIDI_DIR]:
    os.makedirs(directory, exist_ok=True)

# Speech recognition settings
LANGUAGE = "en-US"
AMBIENT_DURATION = 1  # Duration for ambient noise adjustment