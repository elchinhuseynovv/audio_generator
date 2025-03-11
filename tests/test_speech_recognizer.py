"""
Tests for the speech recognition module
"""

import pytest
from speech_recognizer import SpeechRecognizer
import speech_recognition as sr
from unittest.mock import MagicMock, patch

@pytest.fixture
def speech_recognizer():
    return SpeechRecognizer()

def test_speech_recognizer_initialization(speech_recognizer):
    assert isinstance(speech_recognizer.recognizer, sr.Recognizer)
    assert speech_recognizer.language == "en-US"

@patch('speech_recognition.Recognizer.adjust_for_ambient_noise')
def test_adjust_for_noise(mock_adjust, speech_recognizer):
    source = MagicMock()
    speech_recognizer.adjust_for_noise(source)
    mock_adjust.assert_called_once_with(source, duration=1)

@patch('speech_recognition.Recognizer.listen')
@patch('speech_recognition.Recognizer.recognize_google')
def test_recognize_speech_success(mock_recognize, mock_listen, speech_recognizer):
    # Mock the audio input and recognition
    mock_audio = MagicMock()
    mock_listen.return_value = mock_audio
    mock_recognize.return_value = "test speech"
    
    # Test successful speech recognition
    with patch('speech_recognition.Microphone') as mock_mic:
        result = speech_recognizer.recognize_speech()
        assert result == "test speech"
        mock_recognize.assert_called_once_with(mock_audio, language="en-US")

@patch('speech_recognition.Recognizer.listen')
@patch('speech_recognition.Recognizer.recognize_google')
def test_recognize_speech_unknown_value(mock_recognize, mock_listen, speech_recognizer):
    # Mock recognition failure
    mock_recognize.side_effect = sr.UnknownValueError()
    
    # Test handling of unrecognized speech
    with patch('speech_recognition.Microphone'):
        with pytest.raises(ValueError) as exc_info:
            speech_recognizer.recognize_speech()
        assert "Could not understand the audio" in str(exc_info.value)

@patch('speech_recognition.Recognizer.listen')
@patch('speech_recognition.Recognizer.recognize_google')
def test_recognize_speech_request_error(mock_recognize, mock_listen, speech_recognizer):
    # Mock service error
    mock_recognize.side_effect = sr.RequestError("Service unavailable")
    
    # Test handling of service errors
    with patch('speech_recognition.Microphone'):
        with pytest.raises(sr.RequestError) as exc_info:
            speech_recognizer.recognize_speech()
        assert "Service unavailable" in str(exc_info.value)