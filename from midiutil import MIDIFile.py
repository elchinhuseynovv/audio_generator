from midiutil import MIDIFile
import random

def generate_music(command):
    """
    Generates a MIDI file based on the recognized command.
    Each word in the command is mapped to a musical note.
    """
    midi = MIDIFile(1)
    midi.addTempo(0, 0, 120)  # Set tempo to 120 BPM
    
    notes = {
        "C": 60, "D": 62, "E": 64, "F": 65, "G": 67, "A": 69, "B": 71,
        "DO": 60, "RE": 62, "MI": 64, "FA": 65, "SOL": 67, "LA": 69, "SI": 71
    }
    
    words = command.split()
    time = 0  # Start time for MIDI notes
    
    for word in words:
        note = notes.get(word.upper(), random.choice(list(notes.values())))
        midi.addNote(0, 0, note, time, 1, 100)  # Add note to track 0, channel 0
        time += 1  # Move to the next beat
    
    # Save the MIDI file
    midi_filename = "generated_music.mid"
    with open(midi_filename, "wb") as output_file:
        midi.writeFile(output_file)
    print(f"MIDI file '{midi_filename}' successfully created!")
    
    return midi_filename
