"""
Main application module for the Voice-to-Music Generator
Using only Python standard library
"""

import sys
from audio_processor import AudioProcessor
from music_generator import MusicGenerator

def main():
    """
    Main application flow using standard library
    """
    print("\n=== Voice-to-Music Generator (Standard Library Version) ===")
    print("Enter text to convert to music (or 'q' to quit):")
    
    try:
        music_generator = MusicGenerator()
        
        while True:
            try:
                # Get text input instead of voice
                text = input("> ")
                
                if text.lower() == 'q':
                    break
                
                # Generate music from text
                output_file = music_generator.generate_music(text)
                print(f"\nMusic generated and saved to: {output_file}")
                
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