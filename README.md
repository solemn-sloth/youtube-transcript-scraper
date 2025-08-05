# YouTube Transcript Scraper

A command-line tool for extracting and saving transcripts from YouTube videos with a clean, interactive interface.

![YouTube Transcript Scraper](https://img.shields.io/badge/Python-Transcript%20Scraper-blue)

## Features

- 🎬 **Simple URL Input**: Works with various YouTube URL formats
- 📃 **Clean Output**: Saves transcripts to text files without timestamps
- ✨ **Interactive UI**: Terminal-based interface with progress indicators
- 🌈 **Color-coded Output**: Visual feedback with ANSI color formatting
- 🔄 **Batch Processing**: Process multiple videos in one session

## Requirements

- Python 3.6+
- `youtube-transcript-api` package

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/solemn-sloth/youtube-transcript-scraper.git
   cd youtube-transcript-scraper
   ```

2. Install the required dependency:
   ```
   pip install youtube-transcript-api
   ```

## Usage

Run the script:
```
python YT_Scraper.py
```

Enter a YouTube URL when prompted. The script accepts:
- Full YouTube URLs (e.g., `https://www.youtube.com/watch?v=VIDEO_ID`)
- Short YouTube URLs (e.g., `https://youtu.be/VIDEO_ID`)
- Embed URLs (e.g., `https://www.youtube.com/embed/VIDEO_ID`)
- Direct Video IDs (11-character alphanumeric strings)

## Output

Transcripts are saved as text files in the current directory with the naming format:
```
VIDEO_ID_DDMMYY.txt
```

The output includes:
- Full transcript text without timestamps
- File details (name, number of snippets)
- Video duration
- Transcript language

## Error Handling

The script provides informative error messages for common issues:
- Invalid URLs
- Videos without available transcripts
- Private or restricted videos

## Acknowledgments

This tool uses the [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) package by jdepoix.

## License

MIT

## Author

[solemn-sloth](https://github.com/solemn-sloth)