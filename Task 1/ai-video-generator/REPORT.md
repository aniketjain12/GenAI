# AI Video Generation Tool - Project Report

## 📋 Project Overview

This report documents the development of an AI-powered Video Generation Tool that automatically creates short news videos (30-60 seconds) from trending articles on any topic.

**Project Date:** February 2026  
**Technology Stack:** Python, Cohere AI, PIL, OpenCV, Streamlit

---

## 🎯 Objectives Achieved

| Objective | Status | Implementation |
|-----------|--------|----------------|
| Fetch trending news articles | ✅ Complete | Google News RSS (news_fetcher.py) |
| Generate structured video scripts | ✅ Complete | Cohere AI API (script_generator.py) |
| Create MP4 videos with overlays | ✅ Complete | PIL + OpenCV (video_generator.py) |
| Support configurable duration | ✅ Complete | 30-60 seconds range |
| User-friendly interface | ✅ Complete | Streamlit + CLI (app.py, main.py) |

---

## 🏗️ Architecture

### Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AI VIDEO GENERATION PIPELINE                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  INPUT                                                               │
│  ├── Topic: "artificial intelligence"                               │
│  └── Duration: 30-60 seconds                                        │
│                                                                      │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────────┐                                                │
│  │   News Fetcher  │ ──► Google News RSS Feed                       │
│  │ (news_fetcher.py)│     Fetches up to 5 trending articles         │
│  └────────┬────────┘                                                │
│           │                                                          │
│           ▼                                                          │
│  ┌─────────────────────┐                                            │
│  │  Script Generator   │ ──► Cohere AI (command-a-03-2025)          │
│  │ (script_generator.py)│    Creates 4-6 structured segments        │
│  └──────────┬──────────┘                                            │
│             │                                                        │
│             ▼                                                        │
│  ┌─────────────────────┐                                            │
│  │   Video Generator   │ ──► PIL (images) + OpenCV (video)          │
│  │ (video_generator.py)│     1280x720 HD MP4 output                 │
│  └──────────┬──────────┘                                            │
│             │                                                        │
│             ▼                                                        │
│  OUTPUT: output/{topic}_{timestamp}.mp4                             │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Module Descriptions

| Module | Purpose | Key Features |
|--------|---------|--------------|
| `config.py` | Configuration | API keys, video settings, output paths |
| `news_fetcher.py` | News retrieval | RSS parsing with feedparser |
| `script_generator.py` | Script creation | Cohere LLM, segment generation |
| `video_generator.py` | Video production | PIL rendering, OpenCV encoding |
| `main.py` | CLI interface | Argparse, pipeline orchestration |
| `app.py` | Web interface | Streamlit interactive UI |

---

## 🔧 Technical Implementation

### 1. News Fetching (news_fetcher.py)

**Data Sources:**
```python
NEWS_RSS_FEEDS = {
    "general": "https://news.google.com/rss/search?q={topic}",
    "technology": "https://feeds.feedburner.com/TechCrunch/",
    "science": "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
    "business": "https://feeds.bbci.co.uk/news/business/rss.xml",
}
```

**Key Features:**
- Topic-based search using Google News RSS
- Extracts title, summary, link, published date
- Maximum 5 articles per query
- Error handling for network failures

### 2. Script Generation (script_generator.py)

**LLM Configuration:**
- **Provider:** Cohere API
- **Models (fallback order):**
  1. command-a-03-2025
  2. command-r-plus-08-2024
  3. command-r-08-2024
- **Temperature:** Default (balanced creativity)

**Script Structure:**
```
SEGMENT 1:
TITLE: [2-4 word title]
NARRATION: [Voice-over text]
TEXT_OVERLAY: [Key phrase, max 10 words]

SEGMENT 2:
...
```

**Word Count Calculation:**
- Target: ~2.5 words per second of video
- 30 seconds → ~75 words
- 60 seconds → ~150 words

### 3. Video Generation (video_generator.py)

**Technical Specifications:**
| Parameter | Value |
|-----------|-------|
| Resolution | 1280×720 (HD) |
| Codec | MP4V (MPEG-4) |
| Frame Rate | Dynamic based on duration |
| Color Scheme | 6 alternating dark blue gradients |

**Text Rendering:**
- **Title:** 55pt bold, white, top-center
- **Text Overlay:** 42pt, gold (#FFD700), center
- **Narration:** 24pt, white, bottom area

**Font Management:**
```python
font_options = [
    "C:/Windows/Fonts/arial.ttf",      # Windows
    "C:/Windows/Fonts/segoeui.ttf",    # Windows (alt)
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
]
```

**Text Wrapping Algorithm:**
- Calculates text width using font metrics
- Wraps to multiple lines if exceeding max width
- Centers each line independently

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| News Fetch Time | ~1-3 seconds |
| Script Generation | ~5-10 seconds |
| Video Rendering | ~3-8 seconds |
| Total Pipeline | ~10-20 seconds |
| Output File Size | ~2-5 MB (30s video) |

---

## 🧪 Sample Output

**Input:**
- Topic: "artificial intelligence"
- Duration: 30 seconds

**Generated Script Segments:**
1. **The AI Revolution** - "AI is transforming every industry"
2. **Latest Breakthroughs** - "GPT-5, Claude, and beyond"
3. **Industry Impact** - "Healthcare, finance, education"
4. **Future Outlook** - "What's next for AI technology"

**Output File:** `output/artificial_intelligence_1234567890.mp4`

---

## 🔄 Error Handling

### API Failures
- Retry logic with multiple model fallbacks
- Maximum 3 attempts per model
- Graceful degradation to simpler content

### Video Generation
- Font fallback chain for cross-platform support
- Default font if all options fail
- Exception handling for image/video operations

### News Fetching
- Empty result handling (uses topic description only)
- Network timeout protection
- RSS parsing error recovery

---

## 🚀 Future Improvements

1. **Voice Synthesis Integration**
   - Text-to-Speech for narration
   - Multiple voice options

2. **Enhanced Visuals**
   - Background images/videos
   - Animated transitions
   - Logo watermarks

3. **Multi-format Export**
   - Vertical format (9:16) for TikTok/Reels
   - Square format (1:1) for Instagram

4. **Advanced Features**
   - Subtitle generation
   - Thumbnail extraction
   - Background music

---

## 📝 Dependencies

```
feedparser>=6.0.0      # RSS parsing
cohere>=4.0.0          # LLM API
pillow>=9.0.0          # Image creation
opencv-python>=4.5.0   # Video encoding
numpy>=1.21.0          # Array operations
streamlit>=1.20.0      # Web interface
python-dotenv>=0.19.0  # Environment variables
```

---

## 🎯 Conclusion

The AI Video Generation Tool successfully demonstrates:

1. **LLM Integration** - Effective use of Cohere API for creative content generation
2. **Pipeline Architecture** - Clean, modular design with separation of concerns
3. **Media Processing** - Programmatic video creation without paid APIs
4. **User Experience** - Both CLI and web interfaces for flexibility

The tool transforms any topic into a watchable news video in under 30 seconds, making it suitable for content creation, news summarization, and educational purposes.

---

*Report Generated: February 2026*
