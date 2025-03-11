"""
Tests for utility functions
"""

import pytest
import numpy as np
from utils import (
    generate_filename,
    get_file_path,
    log_error,
    analyze_frequency_spectrum,
    detect_pitch,
    Timer,
    AudioAnalyzer
)
import os
import time
from datetime import datetime

def test_generate_filename():
    # Test basic filename generation
    filename = generate_filename("test", "wav")
    assert filename.startswith("test_")
    assert filename.endswith(".wav")
    assert len(filename) > 10  # Should include timestamp
    
    # Test different prefix and extension
    filename = generate_filename("audio", "mid")
    assert filename.startswith("audio_")
    assert filename.endswith(".mid")

def test_get_file_path():
    # Test path joining
    path = get_file_path("/test/dir", "file.txt")
    assert path == os.path.join("/test/dir", "file.txt")
    
    # Test with different separators
    path = get_file_path("test\\dir", "file.txt")
    assert os.path.sep in path

def test_log_error():
    # Test basic error logging
    error_msg = log_error("Test error")
    assert error_msg == "Test error"
    
    # Test with context
    error_msg = log_error("Test error", "test_context")
    assert "Test error" in error_msg
    assert "test_context" in error_msg

def test_analyze_frequency_spectrum():
    # Create test signal
    sample_rate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    frequency = 440  # A4 note
    signal = np.sin(2 * np.pi * frequency * t)
    
    # Analyze spectrum
    analysis = analyze_frequency_spectrum(signal, sample_rate)
    
    assert 'frequencies' in analysis
    assert 'magnitudes' in analysis
    assert 'dominant_frequencies' in analysis
    assert 'times' in analysis
    
    # Check if dominant frequency is close to input frequency
    dominant_freq = np.mean(analysis['dominant_frequencies'])
    assert abs(dominant_freq - frequency) < 10

def test_detect_pitch():
    # Create test signal with known pitch
    sample_rate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    frequency = 440  # A4 note
    signal = np.sin(2 * np.pi * frequency * t)
    
    # Detect pitch
    detected_pitch = detect_pitch(signal, sample_rate)
    
    assert detected_pitch is not None
    assert abs(detected_pitch - frequency) < 10

def test_timer():
    # Test timer context manager
    with Timer("test_operation") as timer:
        time.sleep(0.1)
    
    assert hasattr(timer, 'duration')
    assert timer.duration >= 0.1
    assert timer.operation_name == "test_operation"

def test_audio_analyzer():
    analyzer = AudioAnalyzer()
    
    # Create test signal
    signal = np.array([0.5, -0.5, 0.25, -0.25])
    
    # Test RMS calculation
    rms = analyzer.calculate_rms(signal)
    assert abs(rms - np.sqrt(0.375)) < 1e-10
    
    # Test zero crossing rate
    zcr = analyzer.calculate_zero_crossing_rate(signal)
    assert zcr == 0.75  # 3 crossings in 4 samples
    
    # Test spectral centroid
    freqs = np.array([100, 200, 300])
    mags = np.array([0.5, 0.3, 0.2])
    centroid = analyzer.calculate_spectral_centroid(mags, freqs)
    assert centroid > 0
    
    # Test spectral rolloff
    rolloff = analyzer.calculate_spectral_rolloff(mags, freqs)
    assert rolloff in freqs