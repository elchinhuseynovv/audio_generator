"""
Utility functions for the Voice-to-Music Generator
"""

import os
import time
import logging
from datetime import datetime
import numpy as np
from scipy import signal
from config import *

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def generate_filename(prefix, extension):
    """
    Generate a unique filename with timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

def get_file_path(directory, filename):
    """
    Get the full path for a file in a specific directory
    """
    return os.path.join(directory, filename)

def log_error(error, context=""):
    """
    Log error messages with timestamp and context
    """
    error_msg = str(error)
    if context:
        error_msg = f"{error_msg} (Context: {context})"
    logger.error(error_msg)
    return error_msg

def analyze_frequency_spectrum(audio_data, sample_rate):
    """
    Analyze the frequency spectrum of audio data using STFT
    Returns frequencies and their magnitudes
    """
    frequencies, times, spectrogram = signal.stft(
        audio_data,
        fs=sample_rate,
        nperseg=FFT_SIZE,
        noverlap=FFT_SIZE - HOP_LENGTH,
        window=WINDOW_TYPE
    )
    
    # Calculate magnitude spectrum
    magnitudes = np.abs(spectrogram)
    
    # Find dominant frequencies
    dominant_freqs = frequencies[np.argmax(magnitudes, axis=0)]
    
    return {
        'frequencies': frequencies,
        'magnitudes': magnitudes,
        'dominant_frequencies': dominant_freqs,
        'times': times
    }

def detect_pitch(audio_data, sample_rate):
    """
    Detect the fundamental pitch of audio data using autocorrelation
    """
    correlation = signal.correlate(audio_data, audio_data, mode='full')
    correlation = correlation[len(correlation)//2:]
    
    # Find peaks in correlation
    peaks = signal.find_peaks(correlation)[0]
    if len(peaks) > 0:
        fundamental_period = peaks[0]
        if fundamental_period > 0:
            return sample_rate / fundamental_period
    return None

class Timer:
    """
    Context manager for timing operations
    """
    def __init__(self, operation_name):
        self.operation_name = operation_name
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        self.start_time = time.time()
        self.logger.info(f"Starting {self.operation_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        self.logger.info(f"{self.operation_name} completed in {self.duration:.2f} seconds")
        
        if exc_type is not None:
            self.logger.error(f"Error during {self.operation_name}: {exc_val}")
            return False  # Re-raise the exception
        return True

class AudioAnalyzer:
    """
    Class for analyzing audio features
    """
    @staticmethod
    def calculate_rms(audio_data):
        """Calculate Root Mean Square (RMS) amplitude"""
        return np.sqrt(np.mean(np.square(audio_data)))
    
    @staticmethod
    def calculate_zero_crossing_rate(audio_data):
        """Calculate Zero Crossing Rate"""
        return np.sum(np.abs(np.diff(np.signbit(audio_data)))) / len(audio_data)
    
    @staticmethod
    def calculate_spectral_centroid(magnitudes, frequencies):
        """Calculate Spectral Centroid"""
        return np.sum(magnitudes * frequencies) / np.sum(magnitudes)
    
    @staticmethod
    def calculate_spectral_rolloff(magnitudes, frequencies, percentile=0.85):
        """Calculate Spectral Rolloff"""
        threshold = np.sum(magnitudes) * percentile
        cumsum = np.cumsum(magnitudes)
        rolloff_index = np.where(cumsum >= threshold)[0][0]
        return frequencies[rolloff_index]