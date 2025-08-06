# YouTube Transcript Scraper

A command-line tool for extracting and saving transcripts from YouTube videos with a clean, interactive interface.

![YouTube Transcript Scraper](https://img.shields.io/badge/Python-Transcript%20Scraper-blue)

## Features

- 🎬 **Simple URL Input**: Works with various YouTube URL formats
- 🔍 **Search Functionality**: Search YouTube videos by keywords and process top results
- 📃 **Clean Output**: Saves transcripts to text files without timestamps
- ✨ **Interactive UI**: Terminal-based interface with progress indicators
- 🌈 **Color-coded Output**: Visual feedback with ANSI color formatting
- 🔄 **Batch Processing**: Process multiple videos in one session

## Requirements

- Python 3.6+
- `youtube-transcript-api` package
- `selenium` package (for YouTube search functionality)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/solemn-sloth/youtube-transcript-scraper.git
   cd youtube-transcript-scraper
   ```

2. Install the required dependencies:
   ```
   pip install youtube-transcript-api selenium
   ```

## Usage

Run the script:
```
python YT_Scraper.py
```

Enter a YouTube URL or search query when prompted:

**For direct URL processing**, the script accepts:
- Full YouTube URLs (e.g., `https://www.youtube.com/watch?v=VIDEO_ID`)
- Short YouTube URLs (e.g., `https://youtu.be/VIDEO_ID`)
- Embed URLs (e.g., `https://www.youtube.com/embed/VIDEO_ID`)
- Direct Video IDs (11-character alphanumeric strings)

**For search functionality**:
- Enter any search term or phrase to find YouTube videos
- The script will search YouTube and process the top results (default: 3 videos)
- You can modify the `DEFAULT_VIDEO_COUNT` variable in the script to change the number of search results processed

## Output

Transcripts are saved as text files in the `Transcripts` folder with the naming format:
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