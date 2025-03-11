# Author

Elchin Huseynov

# Voice-to-Music Generator

A Python application that converts spoken words into musical notes, creating MIDI files from voice input.

## Features

- Voice input recognition using Google's Speech Recognition API
- Audio recording and processing
- MIDI file generation based on voice input
- Multiple musical scales support
- Comprehensive error handling and logging
- Unit tests

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
└── output/           # Generated files
    ├── recordings/   # WAV recordings
    └── midi/         # Generated MIDI files
```

## Testing

Run the tests using pytest:
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed by Elchin Huseynov.