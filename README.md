# Author

Elchin Huseynov

# Voice-to-Music Generator

A Python application that converts spoken words into musical notes, creating MIDI files from voice input.

## Features

- Voice input recognition using Google's Speech Recognition API
- Audio recording and processing with advanced signal analysis
- MIDI file generation with multiple musical scales and instruments
- Comprehensive error handling and logging
- Extensive test coverage
- Real-time audio visualization
- Multiple musical scales (Major, Minor, Pentatonic, Blues)
- Various instrument support (Piano, Guitar, Violin, etc.)
- Emotional word-to-note mapping

## Requirements

- Python 3.7+
- See `requirements.txt` for Python package dependencies

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the main application:
   ```bash
   python main.py
   ```

2. Follow the prompts to:
   - Speak words or phrases
   - Generate music from your voice input
   - Play the generated MIDI file
   - Choose to continue or exit

## Project Structure

```
├── config.py           # Configuration settings
├── utils.py           # Utility functions
├── audio_processor.py # Audio recording and processing
├── speech_recognizer.py # Speech recognition
├── music_generator.py  # MIDI file generation
├── main.py            # Main application
├── requirements.txt   # Python dependencies
├── tests/            # Unit tests
│   ├── test_audio_processor.py
│   ├── test_music_generator.py
│   ├── test_speech_recognizer.py
│   └── test_utils.py
└── output/           # Generated files
    ├── recordings/   # WAV recordings
    ├── midi/        # Generated MIDI files
    └── logs/        # Application logs
```

## Testing

Run the tests using pytest:
```bash
pytest tests/
```

## Advanced Features

### Musical Scales
- C Major
- A Minor
- Pentatonic
- Chromatic
- Blues

### Instruments
- Piano
- Guitar
- Violin
- Flute
- Trumpet
- Drums

### Audio Analysis
- Frequency spectrum analysis
- Pitch detection
- Spectral centroid
- Zero crossing rate
- RMS amplitude
- Spectral rolloff

### Error Handling
- Comprehensive error logging
- Graceful failure recovery
- Detailed error messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed by Elchin Huseynov.