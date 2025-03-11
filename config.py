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
MAX_AMPLITUDE = 32767  # Maximum amplitude for 16-bit audio
MIN_FREQUENCY = 20     # Minimum audible frequency (Hz)
MAX_FREQUENCY = 20000  # Maximum audible frequency (Hz)

# MIDI settings
TEMPO = 120
VELOCITY = 100  # Note velocity (volume)
DEFAULT_OCTAVE = 4
TICKS_PER_BEAT = 480  # MIDI resolution
DEFAULT_PROGRAM = 0   # Default MIDI program (piano)

# File paths
OUTPUT_DIR = "output"
RECORDINGS_DIR = os.path.join(OUTPUT_DIR, "recordings")
MIDI_DIR = os.path.join(OUTPUT_DIR, "midi")
LOG_DIR = os.path.join(OUTPUT_DIR, "logs")

# Create directories if they don't exist
for directory in [OUTPUT_DIR, RECORDINGS_DIR, MIDI_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)

# Speech recognition settings
LANGUAGE = "en-US"
AMBIENT_DURATION = 1  # Duration for ambient noise adjustment
ENERGY_THRESHOLD = 4000  # Energy level for speech detection
DYNAMIC_ENERGY_THRESHOLD = True
PAUSE_THRESHOLD = 0.8  # Minimum length of silence to stop recording

# Logging settings
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE = os.path.join(LOG_DIR, "voice_to_music.log")

# Analysis settings
FFT_SIZE = 2048  # Size of FFT window
HOP_LENGTH = 512  # Number of samples between successive FFT windows
WINDOW_TYPE = 'hann'  # Type of window function for FFT