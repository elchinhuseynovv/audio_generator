"""
Configuration settings for the Voice-to-Music Generator
Using only Python standard library
"""

import os

# Audio settings
SAMPLE_RATE = 44100
DEFAULT_DURATION = 5
CHANNELS = 1
DTYPE = 'int16'
MAX_AMPLITUDE = 32767  # Maximum amplitude for 16-bit audio

# File paths
OUTPUT_DIR = "output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Logging settings
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"