#!/usr/bin/env python3
import sys
import re
import time
import os
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi

# ANSI color codes
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    END = '\033[0m'

def clear_line():
    """Clear current line in terminal"""
    print('\r' + ' ' * 80 + '\r', end='', flush=True)

def spinning_cursor():
    """Generator for spinning cursor animation"""
    while True:
        for cursor in '⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏':
            yield cursor

def print_header():
    """Print the application header"""
    print("\n")
    print(f"    {Colors.CYAN}✨ YT TRANSCRIPT ✨{Colors.END}")
    print(f"    {Colors.GRAY}═══════════════════{Colors.END}")
    print()

def progress_bar(current, total, width=30):
    """Display a progress bar"""
    progress = int((current / total) * width)
    bar = '▓' * progress + '░' * (width - progress)
    percentage = int((current / total) * 100)
    return f"{Colors.CYAN}{bar}{Colors.END} {percentage}%"

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:watch\?v=)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    if re.match(r'^[0-9A-Za-z_-]{11}$', url):
        return url
    
    return None

def animate_loading(message, duration=2):
    """Show animated loading message"""
    spinner = spinning_cursor()
    start_time = time.time()
    
    while time.time() - start_time < duration:
        print(f"\r    {next(spinner)} {message}", end='', flush=True)
        time.sleep(0.1)
    
    clear_line()

def save_transcript(video_id, url):
    """Fetch and save transcript to a text file"""
    try:
        # Show loading animation
        animate_loading("Fetching transcript...", 1)
        
        # Create API instance and fetch transcript
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)
        
        # Show progress bar animation
        print(f"\n    {Colors.CYAN}📊{Colors.END} Processing transcript")
        total_snippets = len(fetched_transcript)
        
        # Simulate progress
        for i in range(0, 101, 5):
            print(f"\r    {progress_bar(i, 100)}", end='', flush=True)
            time.sleep(0.05)
        print()  # New line after progress bar
        
        # Create filename with ddmmyy format
        date_str = datetime.now().strftime("%d%m%y")
        filename = f"{video_id}_{date_str}.txt"
        
        # Save ONLY the transcript text
        with open(filename, 'w', encoding='utf-8') as f:
            for snippet in fetched_transcript:
                f.write(f"{snippet.text} ")
        
        # Success message
        print(f"\n    {Colors.GREEN}✨ Success! Transcript saved{Colors.END}")
        print()
        print(f"    📄 File: {Colors.BOLD}{filename}{Colors.END}")
        print(f"    📝 Size: {Colors.BOLD}{len(fetched_transcript):,}{Colors.END} snippets")
        
        # Get video duration if available
        if fetched_transcript and hasattr(fetched_transcript[-1], 'start'):
            duration_seconds = fetched_transcript[-1].start
            minutes = int(duration_seconds // 60)
            seconds = int(duration_seconds % 60)
            print(f"    ⏱️  Video duration: {Colors.BOLD}{minutes}:{seconds:02d}{Colors.END}")
        
        print(f"    🌍 Language: {Colors.BOLD}{fetched_transcript.language}{Colors.END}")
        
        return True
        
    except Exception as e:
        clear_line()
        print(f"\n    {Colors.RED}❌ Oops! Something went wrong{Colors.END}")
        print()
        print(f"    {Colors.YELLOW}💡{Colors.END} {str(e)}")
        
        if "No transcripts" in str(e):
            print(f"       • Check if the video is public")
            print(f"       • Some videos disable captions")
            print(f"       • Try a different video")
        
        return False

def main():
    while True:
        print_header()
        
        # Get URL input
        url = input(f"    🎬 Enter YouTube URL: {Colors.CYAN}").strip()
        print(Colors.END, end='')
        
        if not url:
            print(f"\n    {Colors.YELLOW}Goodbye! 👋{Colors.END}\n")
            break
        
        print()  # Empty line for spacing
        
        # Extract video ID
        video_id = extract_video_id(url)
        if not video_id:
            print(f"    {Colors.RED}❌ Invalid YouTube URL{Colors.END}")
            print(f"    {Colors.GRAY}────────────────────────────────────────{Colors.END}")
            print(f"\n    🔄 Press Enter to try again or Ctrl+C to exit")
            input()
            continue
        
        # Save transcript
        success = save_transcript(video_id, url)
        
        # Footer
        print(f"\n    {Colors.GRAY}────────────────────────────────────────{Colors.END}")
        print(f"\n    🔄 Process another? (Enter URL or press Ctrl+C to exit)")
        
        try:
            next_url = input(f"    {Colors.CYAN}").strip()
            print(Colors.END, end='')
            if not next_url:
                print(f"\n    {Colors.YELLOW}Goodbye! 👋{Colors.END}\n")
                break
            # If they entered a URL directly, process it in the next loop
            url = next_url
            continue
        except KeyboardInterrupt:
            print(f"\n\n    {Colors.YELLOW}Goodbye! 👋{Colors.END}\n")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n    {Colors.YELLOW}Goodbye! 👋{Colors.END}\n")