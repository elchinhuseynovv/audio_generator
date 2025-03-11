"""
Tests for the music generation module
"""

import pytest
from music_generator import MusicGenerator
import os
from config import MIDI_DIR

@pytest.fixture
def music_generator():
    return MusicGenerator()

def test_music_generator_initialization(music_generator):
    assert isinstance(music_generator.scales, dict)
    assert isinstance(music_generator.note_mapping, dict)
    assert 'C_major' in music_generator.scales
    assert 'DO' in music_generator.note_mapping

def test_map_word_to_note(music_generator):
    # Test predefined mappings
    assert music_generator.map_word_to_note("DO") == 60
    assert music_generator.map_word_to_note("RE") == 62
    
    # Test case insensitivity
    assert music_generator.map_word_to_note("do") == 60
    assert music_generator.map_word_to_note("re") == 62
    
    # Test emotional word mapping
    assert music_generator.map_word_to_note("HAPPY") == 67
    assert music_generator.map_word_to_note("SAD") == 60
    
    # Test octave shift
    assert music_generator.map_word_to_note("DO", octave_shift=1) == 72
    assert music_generator.map_word_to_note("DO", octave_shift=-1) == 48
    
    # Test different scales
    note = music_generator.map_word_to_note("TEST", scale='pentatonic')
    assert note in music_generator.scales['pentatonic']['notes']

def test_generate_music(music_generator):
    # Test basic music generation
    test_text = "DO RE MI FA"
    filepath = music_generator.generate_music(test_text)
    
    # Check if file was created
    assert os.path.exists(filepath)
    assert filepath.endswith('.mid')
    assert os.path.dirname(filepath) == MIDI_DIR
    
    # Check file size (should be non-zero)
    assert os.path.getsize(filepath) > 0
    
    # Test with different scales
    filepath = music_generator.generate_music(test_text, scale='pentatonic')
    assert os.path.exists(filepath)
    
    # Test with different instruments
    filepath = music_generator.generate_music(test_text, instrument='guitar')
    assert os.path.exists(filepath)

def test_available_scales_and_instruments(music_generator):
    scales = music_generator.get_available_scales()
    instruments = music_generator.get_available_instruments()
    
    assert 'C_major' in scales
    assert 'pentatonic' in scales
    assert 'blues' in scales
    
    assert 'piano' in instruments
    assert 'guitar' in instruments
    assert 'violin' in instruments