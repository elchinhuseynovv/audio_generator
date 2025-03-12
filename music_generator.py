"""
Music generation module for the Voice-to-Music Generator
Using only Python standard library
"""

import wave
import struct
import math
import random
import logging
from config import *

logger = logging.getLogger(__name__)

class MusicGenerator:
    def __init__(self):
        self.sample_rate = SAMPLE_RATE
        self.note_mapping = {
            "DO": 261.63,  # C4
            "RE": 293.66,  # D4
            "MI": 329.63,  # E4
            "FA": 349.23,  # F4
            "SOL": 392.00, # G4
            "LA": 440.00,  # A4
            "SI": 493.88   # B4
        }
        logger.info("MusicGenerator initialized")

    def generate_music(self, text):
        """
        Generate simple sine wave based music
        """
        try:
            words = text.split()
            samples = []
            duration = 0.5  # seconds per note
            
            for word in words:
                word = word.upper()
                frequency = self.note_mapping.get(word, 440.0)  # default to A4
                
                # Generate sine wave
                for i in range(int(self.sample_rate * duration)):
                    t = float(i) / self.sample_rate
                    value = int(32767 * math.sin(2 * math.pi * frequency * t))
                    samples.append(value)
            
            # Convert to bytes
            audio_data = struct.pack('h' * len(samples), *samples)
            
            # Save as WAV file
            with wave.open('output.wav', 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_data)
            
            return 'output.wav'

        except Exception as e:
            logger.error(f"Error during music generation: {str(e)}")
            raise