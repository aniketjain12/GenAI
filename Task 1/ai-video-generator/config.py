"""
Configuration settings for the AI Video Generator.
"""
import os
from dotenv import load_dotenv

# Load environment variables from current dir or parent dir
load_dotenv()  # Try current directory first
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))  # Try parent directory

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "").strip()

# News RSS Feeds (structured, legal sources)
NEWS_RSS_FEEDS = {
    "general": "https://news.google.com/rss/search?q={topic}&hl=en-US&gl=US&ceid=US:en",
    "technology": "https://feeds.feedburner.com/TechCrunch/",
    "science": "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
    "business": "https://feeds.bbci.co.uk/news/business/rss.xml",
}

# Video Settings
DEFAULT_VIDEO_DURATION = 30  # seconds
MIN_VIDEO_DURATION = 30
MAX_VIDEO_DURATION = 60

# Output Settings
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
