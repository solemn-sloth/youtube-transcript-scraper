#!/usr/bin/env python3
import sys
import re
import time
import os
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote_plus

# Configuration
DEFAULT_VIDEO_COUNT = 3  # Change this to scrape more/fewer videos
TRANSCRIPTS_FOLDER = "Transcripts"  # Folder name for saving transcripts

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

def ensure_transcripts_folder():
    """Create Transcripts folder if it doesn't exist"""
    if not os.path.exists(TRANSCRIPTS_FOLDER):
        os.makedirs(TRANSCRIPTS_FOLDER)

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    # Handle the format: https://www.youtube.com/watch?v=VIDEO_ID&other_params
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([0-9A-Za-z_-]{11})(?:&|$)',
        r'(?:v=|\/)([0-9A-Za-z_-]{11})(?:&|$)',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
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

def search_youtube_videos(query, num_videos=DEFAULT_VIDEO_COUNT):
    """Search YouTube and return video URLs"""
    animate_loading("Searching YouTube...", 1)
    
    # Setup Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    videos = []
    
    try:
        # Construct search URL
        search_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
        driver.get(search_url)
        
        # Wait for results to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "ytd-video-renderer")))
        
        # Give page time to fully load
        time.sleep(2)
        
        # Find all video renderers (excluding ads)
        video_elements = driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer")
        
        for element in video_elements:
            if len(videos) >= num_videos:
                break
                
            try:
                # Skip if it's an ad (check for ad badges)
                ad_badges = element.find_elements(By.CSS_SELECTOR, "[aria-label='Sponsored']")
                if ad_badges:
                    continue
                
                # Get video title and URL
                title_element = element.find_element(By.CSS_SELECTOR, "#video-title")
                video_url = title_element.get_attribute("href")
                video_title = title_element.get_attribute("title") or title_element.text
                
                # Skip if no valid URL
                if not video_url or "googleadservices" in video_url:
                    continue
                
                # Extract video ID from the URL
                video_id = extract_video_id(video_url)
                if not video_id:
                    continue
                
                videos.append({
                    "title": video_title,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "id": video_id
                })
                
            except Exception as e:
                continue
        
    except Exception as e:
        clear_line()
        print(f"    {Colors.RED}❌ Search failed: {str(e)}{Colors.END}")
        
    finally:
        driver.quit()
    
    return videos

def save_transcript(video_id, url):
    """Fetch and save transcript to a text file"""
    try:
        # Show loading animation
        animate_loading("Fetching transcript...", 1)
        
        # Create API instance and fetch transcript
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)
        
        # Convert to list for counting
        transcript_list = list(fetched_transcript)
        
        # Show progress bar animation
        print(f"\n    {Colors.CYAN}📊{Colors.END} Processing transcript")
        total_snippets = len(transcript_list)
        
        # Simulate progress
        for i in range(0, 101, 5):
            print(f"\r    {progress_bar(i, 100)}", end='', flush=True)
            time.sleep(0.05)
        print()  # New line after progress bar
        
        # Ensure Transcripts folder exists
        ensure_transcripts_folder()
        
        # Create filename with ddmmyy format
        date_str = datetime.now().strftime("%d%m%y")
        filename = f"{video_id}_{date_str}.txt"
        filepath = os.path.join(TRANSCRIPTS_FOLDER, filename)
        
        # Save ONLY the transcript text
        with open(filepath, 'w', encoding='utf-8') as f:
            for snippet in transcript_list:
                f.write(f"{snippet.text} ")
        
        # Success message
        print(f"\n    {Colors.GREEN}✨ Success! Transcript saved{Colors.END}")
        print()
        print(f"    📄 File: {Colors.BOLD}{filename}{Colors.END}")
        print(f"    📁 Location: {Colors.BOLD}{TRANSCRIPTS_FOLDER}/{Colors.END}")
        print(f"    📝 Size: {Colors.BOLD}{total_snippets:,}{Colors.END} snippets")
        
        # Get video duration if available
        if transcript_list and hasattr(transcript_list[-1], 'start'):
            duration_seconds = transcript_list[-1].start
            minutes = int(duration_seconds // 60)
            seconds = int(duration_seconds % 60)
            print(f"    ⏱️  Video duration: {Colors.BOLD}{minutes}:{seconds:02d}{Colors.END}")
        
        # Get language info
        if hasattr(fetched_transcript, 'language'):
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
        
        # Get URL or search query input
        user_input = input(f"    🎬 Enter YouTube URL or search query: {Colors.CYAN}").strip()
        print(Colors.END, end='')
        
        if not user_input:
            print(f"\n    {Colors.YELLOW}Goodbye! 👋{Colors.END}\n")
            break
        
        print()  # Empty line for spacing
        
        # Check if it's a URL or search query
        if "youtube.com" in user_input or "youtu.be" in user_input or re.match(r'^[0-9A-Za-z_-]{11}$', user_input):
            # It's a URL - process single video
            video_id = extract_video_id(user_input)
            if not video_id:
                print(f"    {Colors.RED}❌ Invalid YouTube URL{Colors.END}")
                print(f"    {Colors.GRAY}────────────────────────────────────────{Colors.END}")
                print(f"\n    🔄 Press Enter to try again or Ctrl+C to exit")
                input()
                continue
            
            # Save transcript
            save_transcript(video_id, user_input)
            
        else:
            # It's a search query
            # Search for videos (using default count)
            videos = search_youtube_videos(user_input, DEFAULT_VIDEO_COUNT)
            
            if not videos:
                print(f"    {Colors.RED}❌ No videos found{Colors.END}")
                print(f"    {Colors.GRAY}────────────────────────────────────────{Colors.END}")
                print(f"\n    🔄 Press Enter to try again or Ctrl+C to exit")
                input()
                continue
            
            # Process each video
            for i, video in enumerate(videos, 1):
                if i > 1:
                    print(f"\n    {Colors.GRAY}────────────────────────────────────────{Colors.END}")
                
                print(f"\n    [{i}/{len(videos)}] {video['title'][:60]}...")
                save_transcript(video['id'], video['url'])
        
        # Footer
        print(f"\n    {Colors.GRAY}────────────────────────────────────────{Colors.END}")
        print(f"\n    🔄 Process another? (Enter URL/search or press Ctrl+C to exit)")
        
        try:
            next_input = input(f"    {Colors.CYAN}").strip()
            print(Colors.END, end='')
            if not next_input:
                print(f"\n    {Colors.YELLOW}Goodbye! 👋{Colors.END}\n")
                break
            # If they entered something, use it in the next loop
            user_input = next_input
            continue
        except KeyboardInterrupt:
            print(f"\n\n    {Colors.YELLOW}Goodbye! 👋{Colors.END}\n")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n    {Colors.YELLOW}Goodbye! 👋{Colors.END}\n")