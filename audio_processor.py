"""
Audio processing module for the Voice-to-Music Generator
"""

import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import logging
from config import *
from utils import (
    generate_filename, get_file_path, Timer, 
    analyze_frequency_spectrum, detect_pitch,
    AudioAnalyzer
)

logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self):
        self.sample_rate = SAMPLE_RATE
        self.channels = CHANNELS
        self.dtype = DTYPE
        self.analyzer = AudioAnalyzer()
        logger.info("AudioProcessor initialized")

    def record_audio(self, duration=DEFAULT_DURATION):
        """
        Records audio from the microphone and saves it as a WAV file.
        Returns the path to the recorded file.
        """
        try:
            with Timer("Audio recording"):
                logger.info(f"Starting audio recording for {duration} seconds")
                
                # Set up the recording stream
                stream = sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    dtype=self.dtype
                )
                
                # Record audio
                with stream:
                    audio_data = sd.rec(
                        int(duration * self.sample_rate),
                        samplerate=self.sample_rate,
                        channels=self.channels,
                        dtype=self.dtype
                    )
                    sd.wait()

                # Normalize audio
                audio_data = self._normalize_audio(audio_data)

            # Save the recorded audio
            filename = generate_filename("recording", "wav")
            filepath = get_file_path(RECORDINGS_DIR, filename)
            
            wav.write(filepath, self.sample_rate, audio_data)
            logger.info(f"Audio saved to {filepath}")
            
            return filepath

        except Exception as e:
            logger.error(f"Error during audio recording: {str(e)}")
            raise

    def process_audio(self, filepath):
        """
        Loads and analyzes the WAV file to extract audio features.
        Returns a dictionary containing comprehensive audio analysis results.
        """
        try:
            with Timer("Audio processing"):
                logger.info(f"Processing audio file: {filepath}")
                
                # Load audio file
                samplerate, data = wav.read(filepath)
                
                # Convert to mono if stereo
                if len(data.shape) > 1:
                    data = np.mean(data, axis=1)
                
                # Basic audio features
                duration = len(data) / samplerate
                max_amplitude = np.max(np.abs(data))
                rms = self.analyzer.calculate_rms(data)
                zero_crossing_rate = self.analyzer.calculate_zero_crossing_rate(data)
                
                # Frequency analysis
                spectrum_analysis = analyze_frequency_spectrum(data, samplerate)
                pitch = detect_pitch(data, samplerate)
                
                # Spectral features
                spectral_centroid = self.analyzer.calculate_spectral_centroid(
                    spectrum_analysis['magnitudes'],
                    spectrum_analysis['frequencies']
                )
                
                spectral_rolloff = self.analyzer.calculate_spectral_rolloff(
                    spectrum_analysis['magnitudes'],
                    spectrum_analysis['frequencies']
                )

                analysis = {
                    'filepath': filepath,
                    'sample_rate': samplerate,
                    'duration': duration,
                    'max_amplitude': max_amplitude,
                    'rms': rms,
                    'zero_crossing_rate': zero_crossing_rate,
                    'pitch': pitch,
                    'spectral_centroid': spectral_centroid,
                    'spectral_rolloff': spectral_rolloff,
                    'dominant_frequencies': spectrum_analysis['dominant_frequencies'],
                    'frequency_spectrum': {
                        'frequencies': spectrum_analysis['frequencies'].tolist(),
                        'magnitudes': spectrum_analysis['magnitudes'].tolist(),
                        'times': spectrum_analysis['times'].tolist()
                    }
                }

                logger.info("Audio analysis complete")
                return analysis

        except Exception as e:
            logger.error(f"Error during audio processing: {str(e)}")
            raise

    def _normalize_audio(self, audio_data):
        """
        Normalize audio data to prevent clipping
        """
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            scale_factor = MAX_AMPLITUDE / max_val
            return (audio_data * scale_factor).astype(self.dtype)
        return audio_data