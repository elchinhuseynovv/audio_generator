"""
Music generation module for the Voice-to-Music Generator
"""

from midiutil import MIDIFile
import random
from config import *
from utils import generate_filename, get_file_path, Timer, log_error

class MusicGenerator:
    def __init__(self):
        self.midi = MIDIFile(1)  # 1 track
        self.midi.addTempo(0, 0, TEMPO)
        
        # Define musical scales
        self.scales = {
            'C_major': [60, 62, 64, 65, 67, 69, 71],  # C major scale
            'A_minor': [57, 59, 60, 62, 64, 65, 67],  # A minor scale
            'pentatonic': [60, 62, 64, 67, 69],       # C pentatonic scale
        }
        
        # Word-to-note mapping
        self.note_mapping = {
            # Basic notes
            "DO": 60, "RE": 62, "MI": 64, "FA": 65,
            "SOL": 67, "LA": 69, "SI": 71,
            # English notation
            "C": 60, "D": 62, "E": 64, "F": 65,
            "G": 67, "A": 69, "B": 71,
            # Common words
            "HAPPY": 67, "SAD": 60, "BRIGHT": 69,
            "DARK": 62, "SOFT": 64, "LOUD": 71
        }

    def map_word_to_note(self, word, scale='C_major'):
        """
        Maps a word to a musical note, either using predefined mappings
        or generating a note from the selected scale
        """
        word = word.upper()
        if word in self.note_mapping:
            return self.note_mapping[word]
        return random.choice(self.scales[scale])

    def generate_music(self, text, scale='C_major'):
        """
        Generates a MIDI file based on the input text
        """
        try:
            with Timer("Music generation"):
                words = text.split()
                time = 0

                for word in words:
                    # Get note from word
                    note = self.map_word_to_note(word, scale)
                    
                    # Add note to track 0, channel 0
                    self.midi.addNote(
                        track=0,
                        channel=0,
                        pitch=note,
                        time=time,
                        duration=1,
                        volume=VELOCITY
                    )
                    time += 1

                # Generate filename and save MIDI file
                filename = generate_filename("music", "mid")
                filepath = get_file_path(MIDI_DIR, filename)
                
                with open(filepath, "wb") as output_file:
                    self.midi.writeFile(output_file)
                
                print(f"MIDI file generated: {filepath}")
                return filepath

        except Exception as e:
            log_error(e, "music_generation")
            raise