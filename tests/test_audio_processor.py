"""
Tests for the audio processing module
"""

import pytest
import numpy as np
from audio_processor import AudioProcessor
import os
from config import RECORDINGS_DIR

@pytest.fixture
def audio_processor():
    return AudioProcessor()

def test_audio_processor_initialization(audio_processor):
    assert audio_processor.sample_rate == 44100
    assert audio_processor.channels == 1
    assert audio_processor.dtype == 'int16'

def test_process_audio(audio_processor, tmp_path):
    # Create a test WAV file with a sine wave
    duration = 1.0
    t = np.linspace(0, duration, int(44100 * duration))
    frequency = 440  # A4 note
    audio_data = np.sin(2 * np.pi * frequency * t)
    
    # Convert to int16
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Save test file
    test_file = os.path.join(tmp_path, "test_audio.wav")
    import scipy.io.wavfile as wav
    wav.write(test_file, 44100, audio_data)
    
    # Process the test file
    analysis = audio_processor.process_audio(test_file)
    
    # Verify analysis results
    assert isinstance(analysis, dict)
    assert analysis['sample_rate'] == 44100
    assert abs(analysis['duration'] - 1.0) < 0.1
    assert 'max_amplitude' in analysis
    assert 'rms' in analysis
    assert 'dominant_frequency' in analysis
    
    # Check if dominant frequency is close to 440 Hz
    assert abs(analysis['dominant_frequency'] - 440) < 10