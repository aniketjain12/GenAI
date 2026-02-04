# 🤖 GenAI Tasks Portfolio

A comprehensive collection of three AI-powered automation tools demonstrating advanced Generative AI capabilities using modern LLM APIs.

---

## 📋 Project Overview

This repository contains three distinct GenAI applications, each solving real-world automation challenges:

| Task | Project Name | Description | AI Technology |
|------|-------------|-------------|---------------|
| **Task 1** | AI Video Generator | Automated news video creation pipeline | Cohere LLM + OpenCV/PIL |
| **Task 2** | SEO Blog Creation Tool | E-commerce content generation system | Cohere LLM + Web Scraping |
| **Task 3** | AI Architecture Pipeline | Business requirements to technical specs | Cohere LLM + Multi-stage Pipeline |

---

## 🎬 Task 1: AI Video Generation Tool

### Overview
An AI-powered application that automatically generates short videos (30-60 seconds) from trending news articles on any topic.

### Pipeline Flow
```
User Input (Topic + Duration)
         ↓
┌─────────────────┐
│  News Fetcher   │ ← RSS Feeds (Google News)
└─────────────────┘
         ↓
┌─────────────────┐
│Script Generator │ ← Cohere API (LLM)
└─────────────────┘
         ↓
┌─────────────────┐
│Video Generator  │ ← PIL + OpenCV
└─────────────────┘
         ↓
    Output (MP4)
```

### Key Features
- 📰 **News Fetching**: Retrieves trending articles via Google News RSS feeds
- ✍️ **Script Generation**: Creates structured video scripts using Cohere AI
- 🎥 **Video Creation**: Generates MP4 videos with text overlays and scene transitions
- 🎨 **Streamlit UI**: User-friendly web interface for easy video generation

### Technologies
- **LLM**: Cohere API (command-r-plus, command-a-03-2025)
- **News Source**: Google News RSS Feeds
- **Video Processing**: PIL (Pillow), OpenCV, NumPy
- **Frontend**: Streamlit
- **Configuration**: python-dotenv

### Files
```
Task 1/ai-video-generator/
├── main.py              # CLI entry point
├── app.py               # Streamlit web interface
├── config.py            # Configuration settings
├── news_fetcher.py      # RSS-based news fetching
├── script_generator.py  # Cohere-powered script generation
├── video_generator.py   # PIL/OpenCV video creation
├── requirements.txt     # Dependencies
└── output/              # Generated videos
```

---

## 📝 Task 2: SEO Blog Creation Tool

### Overview
An AI-powered tool that automatically generates SEO-optimized blog posts from scraped e-commerce product data.

### Pipeline Flow
```
┌─────────────────┐
│ Product Scraper │ ← Books to Scrape (BeautifulSoup)
└────────┬────────┘
         ↓
┌─────────────────────┐
│ Data Preprocessor   │ ← Cleaning & Enrichment
└──────────┬──────────┘
         ↓
┌──────────────────────┐
│ SEO Keyword Generator│ ← Cohere API
└──────────┬───────────┘
         ↓
┌─────────────────────┐
│  SEO Blog Generator │ ← Cohere API (150-200 words)
└──────────┬──────────┘
         ↓
┌─────────────────────┐
│  Content Exporter   │ ← Markdown / HTML
└─────────────────────┘
```

### Key Features
- 🌐 **Web Scraping**: Extracts product data from e-commerce sites
- 🧹 **Data Preprocessing**: Cleans and enriches product information
- 🎯 **SEO Keyword Generation**: Creates search-optimized keywords using AI
- 📝 **Blog Generation**: Produces 150-200 word SEO-optimized blog posts
- 📤 **Multi-format Export**: Outputs to Markdown and HTML formats
- 🌍 **Publishing Integration**: Support for Medium, WordPress, Dev.to

### Technologies
- **LLM**: Cohere API (command-r-plus-08-2024)
- **Web Scraping**: BeautifulSoup4, Requests
- **Data Models**: Python Dataclasses
- **Export Formats**: Markdown, HTML
- **Frontend**: Streamlit

### Files
```
Task 2/
├── main.py                 # Pipeline orchestrator
├── app.py                  # Streamlit web interface
├── config.py               # Configuration (scraper, SEO, export)
├── models.py               # Data models (Book, BlogPost, etc.)
├── scraper.py              # Web scraper module
├── preprocessor.py         # Data preprocessing
├── keyword_generator.py    # SEO keyword generation
├── blog_generator.py       # Blog post generation
├── exporter.py             # Markdown/HTML export
├── publisher.py            # Platform publishing
├── requirements.txt        # Dependencies
└── output/                 # Generated blog posts
```

---

## 🏗️ Task 3: AI Architecture Pipeline

### Overview
An AI-powered automation tool that converts high-level business requirements into detailed low-level technical specifications.

### Pipeline Flow
```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Business   │───▶│  Requirement │───▶│    Module    │
│ Requirement  │    │   Analyzer   │    │  Identifier  │
└──────────────┘    └──────────────┘    └──────────────┘
                                               │
                    ┌──────────────────────────┘
                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Output     │◀───│  Pseudocode  │◀───│    Schema    │
│  Formatter   │    │  Generator   │    │  Generator   │
└──────────────┘    └──────────────┘    └──────────────┘
```

### Pipeline Stages

| Stage | Description | Output |
|-------|-------------|--------|
| **Requirement Analyzer** | Extracts actors, actions, entities, relationships | Structured analysis JSON |
| **Module Identifier** | Designs system modules with interfaces | Module architecture |
| **Schema Generator** | Creates database tables, fields, relationships | Database schema |
| **Pseudocode Generator** | Generates implementation logic and APIs | Pseudocode + API contracts |

### Key Features
- 📊 **Requirement Analysis**: Identifies actors, actions, and entities
- 🧩 **Module Design**: Creates modular system architecture
- 🗄️ **Schema Generation**: Designs database structures with relationships
- 💻 **Pseudocode Generation**: Produces implementation-ready logic
- 📄 **Multiple Output Formats**: JSON and Markdown exports
- 🎨 **Interactive UI**: Streamlit web interface with tabbed outputs

### Technologies
- **LLM**: Cohere API (command-a-03-2025)
- **Pipeline**: Custom multi-stage architecture
- **Output**: JSON, Markdown
- **Frontend**: Streamlit
- **Configuration**: python-dotenv, dataclasses

### Files
```
Task 3/
├── main.py              # CLI entry point
├── app.py               # Streamlit web interface
├── config.py            # Pipeline configuration
├── requirements.txt     # Dependencies
├── pipeline/
│   ├── __init__.py
│   ├── base.py              # Base pipeline stage
│   ├── pipeline.py          # Main orchestrator
│   ├── analyzer.py          # Requirement analyzer
│   ├── module_identifier.py # Module identifier
│   ├── schema_generator.py  # Schema generator
│   └── pseudocode_generator.py # Pseudocode generator
├── utils/
│   ├── __init__.py
│   └── formatter.py     # Output formatting
└── outputs/             # Generated specifications
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Cohere API Key** ([Get one here](https://dashboard.cohere.com/api-keys))

### Installation

1. **Clone/Download the repository**

2. **Install dependencies for each task:**
   ```bash
   # Task 1
   cd "Task 1/ai-video-generator"
   pip install -r requirements.txt

   # Task 2
   cd "Task 2"
   pip install -r requirements.txt

   # Task 3
   cd "Task 3"
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in each task folder:
   ```env
   COHERE_API_KEY=your-api-key-here
   ```

### Running the Applications

#### Task 1 - AI Video Generator
```bash
cd "Task 1/ai-video-generator"

# Web Interface
python -m streamlit run app.py

# CLI
python main.py --topic "artificial intelligence" --duration 30
```

#### Task 2 - SEO Blog Creator
```bash
cd "Task 2"

# Web Interface
python -m streamlit run app.py

# CLI
python main.py --books 5 --format markdown
```

#### Task 3 - Architecture Pipeline
```bash
cd "Task 3"

# Web Interface
python -m streamlit run app.py

# CLI
python main.py
```

---

## 📊 Technology Stack Summary

| Component | Task 1 | Task 2 | Task 3 |
|-----------|--------|--------|--------|
| **LLM API** | Cohere | Cohere | Cohere |
| **Data Source** | RSS Feeds | Web Scraping | User Input |
| **Processing** | Video/Image | Text/SEO | JSON/Analysis |
| **Output** | MP4 Video | Markdown/HTML | Markdown/JSON |
| **Frontend** | Streamlit | Streamlit | Streamlit |

---

## 🎯 Learning Outcomes

These projects demonstrate proficiency in:

1. **LLM Integration**: Working with Cohere API for text generation
2. **Pipeline Architecture**: Building multi-stage processing pipelines
3. **Web Scraping**: Ethical data extraction from websites
4. **Content Generation**: Creating SEO-optimized, structured content
5. **Video Processing**: Programmatic video creation with Python
6. **Web Development**: Building interactive UIs with Streamlit


---

