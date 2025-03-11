"""
Audio processing module for the Voice-to-Music Generator
"""

import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
from config import *
from utils import generate_filename, get_file_path, Timer, log_error

class AudioProcessor:
    def __init__(self):
        self.sample_rate = SAMPLE_RATE
        self.channels = CHANNELS
        self.dtype = DTYPE

    def record_audio(self, duration=DEFAULT_DURATION):
        """
        Records audio from the microphone and saves it as a WAV file.
        Returns the path to the recorded file.
        """
        try:
            with Timer("Audio recording"):
                print(f"Recording audio for {duration} seconds...")
                audio_data = sd.rec(
                    int(duration * self.sample_rate),
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    dtype=self.dtype
                )
                sd.wait()

            filename = generate_filename("recording", "wav")
            filepath = get_file_path(RECORDINGS_DIR, filename)
            
            wav.write(filepath, self.sample_rate, audio_data)
            print(f"Audio recorded and saved as {filepath}")
            return filepath

        except Exception as e:
            log_error(e, "audio_recording")
            raise

    def process_audio(self, filepath):
        """
        Loads and analyzes the WAV file to extract audio features.
        Returns a dictionary containing audio analysis results.
        """
        try:
            with Timer("Audio processing"):
                samplerate, data = wav.read(filepath)
                
                # Calculate audio features
                duration = len(data) / samplerate
                max_amplitude = np.max(np.abs(data))
                rms = np.sqrt(np.mean(np.square(data)))
                
                # Calculate frequency spectrum
                spectrum = np.fft.fft(data)
                frequencies = np.fft.fftfreq(len(data), 1/samplerate)
                dominant_frequency = frequencies[np.argmax(np.abs(spectrum))]

                analysis = {
                    'filepath': filepath,
                    'sample_rate': samplerate,
                    'duration': duration,
                    'max_amplitude': max_amplitude,
                    'rms': rms,
                    'dominant_frequency': abs(dominant_frequency)
                }

                print(f"Audio analysis complete for {filepath}")
                return analysis

        except Exception as e:
            log_error(e, "audio_processing")
            raise