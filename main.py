"""
Main application module for the Voice-to-Music Generator
"""

import os
import sys
from audio_processor import AudioProcessor
from speech_recognizer import SpeechRecognizer
from music_generator import MusicGenerator
from utils import Timer

def play_midi(filepath):
    """
    Attempt to play the generated MIDI file using system default player
    """
    try:
        if os.name == "nt":  # Windows
            os.system(f'start {filepath}')
        else:  # macOS/Linux
            os.system(f'open {filepath}')
    except Exception as e:
        print(f"Could not play MIDI file: {e}")
        print(f"MIDI file saved at: {filepath}")

def main():
    """
    Main application flow
    """
    print("\n=== Voice-to-Music Generator ===")
    print("Speak words or phrases, and I'll convert them into music!")
    
    try:
        # Initialize components
        speech_recognizer = SpeechRecognizer()
        music_generator = MusicGenerator()
        
        while True:
            try:
                # Get voice input
                text = speech_recognizer.recognize_speech()
                
                # Generate music from recognized text
                midi_filepath = music_generator.generate_music(text)
                
                # Try to play the generated music
                play_midi(midi_filepath)
                
                # Ask if user wants to continue
                response = input("\nGenerate another piece? (y/n): ").lower()
                if response != 'y':
                    break
                    
            except ValueError as e:
                print(f"\nError: {e}")
                print("Please try again...")
                continue
                
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                print("Please try again...")
                continue
    
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
        sys.exit(0)
        
    print("\nThank you for using Voice-to-Music Generator!")

if __name__ == "__main__":
    main()