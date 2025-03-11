"""
Speech recognition module for the Voice-to-Music Generator
"""

import speech_recognition as sr
from config import *
from utils import Timer, log_error

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.language = LANGUAGE

    def adjust_for_noise(self, source):
        """
        Adjust the recognizer for ambient noise
        """
        print("Adjusting for ambient noise...")
        self.recognizer.adjust_for_ambient_noise(
            source,
            duration=AMBIENT_DURATION
        )

    def recognize_speech(self):
        """
        Captures audio from the microphone and converts it to text
        """
        try:
            with Timer("Speech recognition"):
                with sr.Microphone() as source:
                    print("Listening for voice input...")
                    self.adjust_for_noise(source)
                    
                    print("Speak now...")
                    audio = self.recognizer.listen(source)
                    
                    print("Processing speech...")
                    text = self.recognizer.recognize_google(
                        audio,
                        language=self.language
                    )
                    
                    print(f"Recognized text: {text}")
                    return text

        except sr.UnknownValueError:
            error_msg = "Could not understand the audio"
            log_error(error_msg)
            raise ValueError(error_msg)
            
        except sr.RequestError as e:
            error_msg = f"Error with the speech recognition service: {str(e)}"
            log_error(error_msg)
            raise
            
        except Exception as e:
            log_error(e, "speech_recognition")
            raise