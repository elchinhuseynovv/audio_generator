import speech_recognition as sr
import os
from music_generator import generate_music

def recognize_speech():
    """
    Captures audio from the microphone and converts it to text using Google's speech recognition API.
    Returns the recognized text or None if recognition fails.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for voice input...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio)
        print(f"Recognized command: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand the audio. Please try again.")
    except sr.RequestError:
        print("Error connecting to the speech recognition service.")
    return None

def main():
    """
    Main function that runs speech recognition and music generation.
    """
    print("Welcome to the Voice-to-Music Generator!")
    print("Speak a sequence of words, and I will generate music from them.")
    
    command = recognize_speech()
    if command:
        print("Generating music based on your voice input...")
        midi_filename = generate_music(command)
        
        if os.name == "nt":
            os.system(f"start {midi_filename}")  # Windows
        else:
            os.system(f"open {midi_filename}")  # macOS/Linux
    else:
        print("No valid input detected. Please try again.")

if __name__ == "__main__":
    main()
