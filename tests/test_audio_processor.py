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
    assert 'zero_crossing_rate' in analysis
    assert 'pitch' in analysis
    assert 'spectral_centroid' in analysis
    assert 'spectral_rolloff' in analysis
    
    # Check frequency analysis
    assert 'frequency_spectrum' in analysis
    assert 'frequencies' in analysis['frequency_spectrum']
    assert 'magnitudes' in analysis['frequency_spectrum']
    assert 'times' in analysis['frequency_spectrum']

def test_normalize_audio(audio_processor):
    # Create test audio data that needs normalization
    audio_data = np.array([32768, -32768, 16384, -16384], dtype=np.int32)
    
    # Normalize the audio
    normalized = audio_processor._normalize_audio(audio_data)
    
    # Check that the output is within valid range
    assert np.max(np.abs(normalized)) <= 32767
    assert normalized.dtype == np.int16
    
    # Check that relative proportions are maintained
    assert normalized[0] == normalized[1] * -1
    assert normalized[2] == normalized[3] * -1
    assert abs(normalized[0]) == 2 * abs(normalized[2])