"""
Audio processing module for the Voice-to-Music Generator
Using only Python standard library
"""

import array
import wave
import math
import logging
from config import *

logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self):
        self.sample_rate = SAMPLE_RATE
        self.channels = CHANNELS
        self.dtype = DTYPE
        logger.info("AudioProcessor initialized")

    def process_audio(self, data):
        """
        Basic audio processing using standard library
        """
        try:
            # Convert data to array
            audio_array = array.array('h', data)
            
            # Basic audio analysis
            max_amplitude = max(abs(min(audio_array)), abs(max(audio_array)))
            
            analysis = {
                'max_amplitude': max_amplitude,
                'length': len(audio_array),
                'sample_rate': self.sample_rate
            }
            
            return analysis

        except Exception as e:
            logger.error(f"Error during audio processing: {str(e)}")
            raise

    def _normalize_audio(self, audio_data):
        """
        Normalize audio data using standard library
        """
        try:
            max_val = max(abs(min(audio_data)), abs(max(audio_data)))
            if max_val > 0:
                scale = MAX_AMPLITUDE / max_val
                return [int(sample * scale) for sample in audio_data]
            return audio_data
        except Exception as e:
            logger.error(f"Error during normalization: {str(e)}")
            return audio_data