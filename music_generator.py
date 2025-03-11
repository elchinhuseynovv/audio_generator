"""
Music generation module for the Voice-to-Music Generator
"""

from midiutil import MIDIFile
import random
import logging
import numpy as np
from config import *
from utils import generate_filename, get_file_path, Timer

logger = logging.getLogger(__name__)

class MusicGenerator:
    def __init__(self):
        self.midi = MIDIFile(1)  # 1 track
        self.midi.addTempo(0, 0, TEMPO)
        
        # Define musical scales with octave variations
        self.scales = {
            'C_major': {
                'notes': [60, 62, 64, 65, 67, 69, 71],  # C major scale
                'intervals': [2, 2, 1, 2, 2, 2, 1]      # Whole and half steps
            },
            'A_minor': {
                'notes': [57, 59, 60, 62, 64, 65, 67],  # A minor scale
                'intervals': [2, 1, 2, 2, 1, 2, 2]
            },
            'pentatonic': {
                'notes': [60, 62, 64, 67, 69],          # C pentatonic scale
                'intervals': [2, 2, 3, 2, 3]
            },
            'chromatic': {
                'notes': list(range(60, 72)),           # Chromatic scale
                'intervals': [1] * 12
            },
            'blues': {
                'notes': [60, 63, 65, 66, 67, 70],      # Blues scale
                'intervals': [3, 2, 1, 1, 3, 2]
            }
        }
        
        # Word-to-note mapping with emotional context
        self.note_mapping = {
            # Basic notes
            "DO": 60, "RE": 62, "MI": 64, "FA": 65,
            "SOL": 67, "LA": 69, "SI": 71,
            # English notation
            "C": 60, "D": 62, "E": 64, "F": 65,
            "G": 67, "A": 69, "B": 71,
            # Emotional words (mapped to appropriate notes)
            "HAPPY": 67, "SAD": 60, "BRIGHT": 69,
            "DARK": 62, "SOFT": 64, "LOUD": 71,
            "PEACE": 65, "ANGER": 70, "JOY": 68,
            "CALM": 63, "EXCITED": 72, "GENTLE": 66
        }
        
        # Initialize instruments
        self.instruments = {
            'piano': 0,
            'guitar': 25,
            'violin': 40,
            'flute': 73,
            'trumpet': 56,
            'drums': 118
        }
        
        logger.info("MusicGenerator initialized")

    def map_word_to_note(self, word, scale='C_major', octave_shift=0):
        """
        Maps a word to a musical note with advanced features
        """
        word = word.upper()
        base_note = None
        
        # Check direct mapping
        if word in self.note_mapping:
            base_note = self.note_mapping[word]
        else:
            # Generate note based on word characteristics
            word_length = len(word)
            word_sum = sum(ord(c) for c in word)
            scale_notes = self.scales[scale]['notes']
            base_note = scale_notes[word_sum % len(scale_notes)]
        
        # Apply octave shift
        final_note = base_note + (12 * octave_shift)
        
        # Ensure note is in valid MIDI range (0-127)
        return max(0, min(127, final_note))

    def generate_music(self, text, scale='C_major', instrument='piano'):
        """
        Generates a MIDI file with advanced musical features
        """
        try:
            with Timer("Music generation"):
                logger.info(f"Generating music from text: {text}")
                words = text.split()
                time = 0
                track = 0
                channel = 0
                
                # Set instrument
                program = self.instruments.get(instrument.lower(), DEFAULT_PROGRAM)
                self.midi.addProgramChange(track, channel, time, program)
                
                # Generate notes with varying duration and velocity
                for i, word in enumerate(words):
                    # Determine note parameters
                    octave_shift = (i % 3) - 1  # Varies between -1, 0, and 1
                    note = self.map_word_to_note(word, scale, octave_shift)
                    
                    # Vary duration based on word length
                    duration = max(1, min(4, len(word) / 2))
                    
                    # Vary velocity based on word position
                    velocity = min(100, max(60, 
                        VELOCITY + (10 * (-1 if i % 2 == 0 else 1))
                    ))
                    
                    # Add note with effects
                    self._add_note_with_effects(
                        track, channel, note, time,
                        duration, velocity, word
                    )
                    
                    time += duration

                # Generate filename and save MIDI file
                filename = generate_filename("music", "mid")
                filepath = get_file_path(MIDI_DIR, filename)
                
                with open(filepath, "wb") as output_file:
                    self.midi.writeFile(output_file)
                
                logger.info(f"MIDI file generated: {filepath}")
                return filepath

        except Exception as e:
            logger.error(f"Error during music generation: {str(e)}")
            raise

    def _add_note_with_effects(self, track, channel, note, time, 
                             duration, velocity, word):
        """
        Add a note with musical effects based on word characteristics
        """
        # Add main note
        self.midi.addNote(track, channel, note, time, duration, velocity)
        
        # Add harmony for longer words
        if len(word) > 4:
            harmony_note = note + 4  # Add a third
            self.midi.addNote(track, channel, harmony_note, time, 
                            duration, int(velocity * 0.8))
        
        # Add grace note for emphasized words
        if word.isupper():
            grace_note = note + 1
            self.midi.addNote(track, channel, grace_note, time - 0.1, 
                            0.1, int(velocity * 0.7))

    def get_available_scales(self):
        """Return list of available musical scales"""
        return list(self.scales.keys())

    def get_available_instruments(self):
        """Return list of available instruments"""
        return list(self.instruments.keys())