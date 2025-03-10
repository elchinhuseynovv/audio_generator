import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav

def record_audio(duration=5, samplerate=44100):
    """
    Records audio from the microphone and saves it as a WAV file.
    """
    print("Recording audio...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    
    filename = "recorded_audio.wav"
    wav.write(filename, samplerate, audio_data)
    print(f"Audio recorded and saved as {filename}")
    return filename

def process_audio(filename):
    """
    Loads and analyzes the WAV file to extract audio features.
    """
    samplerate, data = wav.read(filename)
    duration = len(data) / samplerate
    print(f"Audio file: {filename}")
    print(f"Sample rate: {samplerate} Hz")
    print(f"Duration: {duration:.2f} seconds")
    return samplerate, data
