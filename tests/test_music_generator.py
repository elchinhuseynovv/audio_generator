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
    
    # Test random mapping for unknown word
    note = music_generator.map_word_to_note("UNKNOWN")
    assert note in music_generator.scales['C_major']

def test_generate_music(music_generator):
    test_text = "DO RE MI FA"
    filepath = music_generator.generate_music(test_text)
    
    # Check if file was created
    assert os.path.exists(filepath)
    assert filepath.endswith('.mid')
    assert os.path.dirname(filepath) == MIDI_DIR
    
    # Check file size (should be non-zero)
    assert os.path.getsize(filepath) > 0