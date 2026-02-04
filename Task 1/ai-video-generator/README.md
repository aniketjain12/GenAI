# AI Video Generation Tool

An AI-powered application that automatically generates short videos (30-60 seconds) from trending news articles.

## 📋 Overview

This tool implements a complete pipeline to:
1. **Fetch trending news** on any topic using RSS feeds
2. **Generate a video script** using Google Gemini AI
3. **Create a video** with text overlays and visuals

The output is a professional-looking news explainer video in MP4 format.

## 🏗️ Architecture

```
User Input (Topic + Duration)
        ↓
┌───────────────────┐
│   News Fetcher    │ ← RSS Feeds (Google News)
└───────────────────┘
        ↓
┌───────────────────┐
│ Script Generator  │ ← Gemini API (LLM)
└───────────────────┘
        ↓
┌───────────────────┐
│ Video Generator   │ ← Gemini Veo / MoviePy
└───────────────────┘
        ↓
    Output (MP4 Video)
```

## 📁 Project Structure

```
ai-video-generator/
├── main.py              # Entry point & CLI interface
├── config.py            # Configuration settings
├── news_fetcher.py      # RSS-based news fetching
├── script_generator.py  # Gemini-powered script generation
├── video_generator.py   # Video creation with Veo/MoviePy
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── .env                 # Your API keys (create this)
├── README.md            # This documentation
└── output/              # Generated videos directory
```

## 🚀 How to Run on Your Desktop

### Prerequisites

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **Cohere API Key** - [Get one here](https://dashboard.cohere.com/api-keys) (Free tier available)
- **Git** (optional) - For cloning the repository

---

### Step 1: Download the Project

**Option A - Clone with Git:**
```bash
git clone <repository-url>
cd ai-video-generator
```

**Option B - Download ZIP:**
1. Download the project as a ZIP file
2. Extract it to your desired location
3. Open a terminal/command prompt in the extracted folder

---

### Step 2: Create Virtual Environment (Recommended)

Open a terminal in the project folder and run:

**Windows (Command Prompt or PowerShell):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> 💡 You'll know it worked when you see `(venv)` at the beginning of your terminal prompt.

---

### Step 3: Install Dependencies

With your virtual environment activated, run:

```bash
pip install -r requirements.txt
```

This installs all required packages: `cohere`, `feedparser`, `opencv-python`, `Pillow`, `streamlit`, etc.

---

### Step 4: Configure API Keys

1. **Copy the example environment file:**

   **Windows:**
   ```bash
   copy .env.example .env
   ```

   **Linux/Mac:**
   ```bash
   cp .env.example .env
   ```

2. **Open `.env` file** in any text editor (Notepad, VS Code, etc.)

3. **Add your Cohere API key:**
   ```
   COHERE_API_KEY=your_actual_cohere_api_key_here
   ```

   > 📝 Get your free API key from: https://dashboard.cohere.com/api-keys

---

### Step 5: Run the Application

You have **two options** to run the application:

#### Option A: Streamlit Web UI (Recommended for beginners)

```bash
streamlit run app.py
```

This opens a user-friendly web interface in your browser at `http://localhost:8501`

#### Option B: Command Line Interface (CLI)

```bash
python main.py --topic "artificial intelligence" --duration 30
```

---

## 🎮 Quick Start Examples

**Generate a 30-second AI video:**
```bash
python main.py --topic "artificial intelligence"
```

**Generate a 45-second climate change video:**
```bash
python main.py --topic "climate change" --duration 45
```

**Generate a 60-second video using short flags:**
```bash
python main.py -t "space exploration" -d 60
```

**View all options:**
```bash
python main.py --help
```

## 📖 Usage

### Basic Usage

Generate a 30-second video on any topic:

```bash
python main.py --topic "artificial intelligence"
```

### Custom Duration

Specify video duration (30-60 seconds):

```bash
python main.py --topic "climate change" --duration 45
```

### Short Form

```bash
python main.py -t "space exploration" -d 60
```

### Help

```bash
python main.py --help
```

## 📝 Example Output

Running the tool produces:

1. **Video file**: `output/artificial_intelligence_1706889600.mp4`
2. **Script file**: `output/artificial_intelligence_1706889600_script.txt`

### Sample Console Output

```
╔═══════════════════════════════════════════════════════════╗
║           AI VIDEO GENERATION TOOL                        ║
║     Trending News → Script → Video (30-60 seconds)        ║
╚═══════════════════════════════════════════════════════════╝

📌 Topic: artificial intelligence
⏱️  Duration: 30 seconds
--------------------------------------------------

[1/3] 📰 Fetching trending news...
    ✓ Found 5 articles

[2/3] ✍️  Generating script with Cohere...
    ✓ Script generated with 4 segments

    Script Preview:
    ----------------------------------------
    Segment 1: AI Revolution
      Text: Artificial intelligence transforms industries...
    Segment 2: Major Investments
      Text: Tech giants invest billions in AI...

[3/3] 🎬 Generating video...
    ✓ Video generated successfully!

==================================================
✅ VIDEO GENERATION COMPLETE!
==================================================

📁 Output: output/artificial_intelligence_1706889600.mp4
📊 Duration: 30 seconds
📝 Segments: 4

🎉 Success! Your video is ready!
```

## 🔧 Configuration

### Video Settings (config.py)

| Setting | Default | Description |
|---------|---------|-------------|
| `DEFAULT_VIDEO_DURATION` | 30 | Default video length in seconds |
| `MIN_VIDEO_DURATION` | 30 | Minimum allowed duration |
| `MAX_VIDEO_DURATION` | 60 | Maximum allowed duration |
| `OUTPUT_DIR` | `./output` | Directory for generated videos |

### News Sources

The tool uses Google News RSS feed for topic-based news fetching. This is a legal, structured data source that provides trending articles.

## 🛠️ Technical Details

### News Fetching (`news_fetcher.py`)

- Uses `feedparser` library to parse RSS feeds
- Fetches from Google News RSS (structured, legal source)
- Extracts title, summary, and publication date
- Formats content for script generation

### Script Generation (`script_generator.py`)

- Uses Cohere Command model for AI text generation
- Generates 4-6 segment scripts
- Each segment includes:
  - Title
  - Narration text
  - Text overlay for display
- Word count calibrated for target duration (~2.5 words/second)

### Video Generation (`video_generator.py`)

- **Primary**: Attempts Gemini Veo API for AI video generation
- **Fallback**: Uses MoviePy for local video creation
- Creates professional news-style videos with:
  - Colored backgrounds
  - Title text
  - Key phrase overlays
  - Narration text display
  - Topic watermark
  - Progress indicator

## 📊 Sample Videos

After running the tool, you'll find generated videos in the `output/` folder:

- `{topic}_{timestamp}.mp4` - The video file
- `{topic}_{timestamp}_script.txt` - The generated script

## ⚠️ Troubleshooting

### "COHERE_API_KEY not set"

Make sure you've created a `.env` file with your API key:
```bash
copy .env.example .env
# Then edit .env and add your Cohere API key
```

### "ModuleNotFoundError"

Make sure you've activated your virtual environment and installed dependencies:
```bash
# Windows
venv\Scripts\activate
pip install -r requirements.txt
```

### "No news articles found"

- Check your internet connection
- Try a more general topic keyword
- The tool will still generate a video using the topic description

### Streamlit not opening in browser

- Manually open `http://localhost:8501` in your browser
- Make sure no other application is using port 8501

### MoviePy font errors

On some systems, you may see font warnings. The tool uses fallback fonts automatically.

## 📜 License

This project is for educational purposes.

## 🙏 Acknowledgments

- Cohere AI for script generation
- MoviePy/OpenCV for video processing
- Feedparser for RSS parsing
- Streamlit for the web interface

---

## 📌 Requirements Mapping

| Requirement | Implementation |
|------------|----------------|
| Trending news collection | `news_fetcher.py` - RSS feeds |
| AI script generation | `script_generator.py` - Gemini API |
| 30-60 second videos | Duration validation & segment timing |
| Text overlays | MoviePy TextClip compositing |
| Images in video | Background colors + text graphics |
| MP4 output | MoviePy video encoding |
| Minimal user input | CLI: topic (required) + duration (optional) |
| Clean project structure | Modular Python files |
| README documentation | This file |

---

