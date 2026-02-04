# 📊 GenAI Tasks - Technical Report

## Executive Summary

This report provides a comprehensive technical analysis of three Generative AI applications developed as part of the GenAI Tasks portfolio. Each application demonstrates different aspects of LLM integration, pipeline architecture, and practical AI implementation.

---

## 📑 Table of Contents

1. [Task 1: AI Video Generation Tool](#task-1-ai-video-generation-tool)
2. [Task 2: SEO Blog Creation Tool](#task-2-seo-blog-creation-tool)
3. [Task 3: AI Architecture Pipeline](#task-3-ai-architecture-pipeline)
4. [Comparative Analysis](#comparative-analysis)
5. [Technical Challenges & Solutions](#technical-challenges--solutions)
6. [Recommendations](#recommendations)

---

## Task 1: AI Video Generation Tool

### 1.1 Project Description

An automated system that generates short-form news videos (30-60 seconds) by:
- Fetching trending news articles via RSS feeds
- Generating structured video scripts using LLM
- Creating MP4 videos with text overlays and transitions

### 1.2 Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VIDEO GENERATION PIPELINE                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  INPUT                                                       │
│  ├── Topic (string): User-specified subject                 │
│  └── Duration (int): 30-60 seconds                          │
│                                                              │
│  STAGE 1: NEWS FETCHING                                     │
│  ├── Source: Google News RSS                                │
│  ├── Library: feedparser                                    │
│  ├── Output: List[Dict] with title, summary, link           │
│  └── Max Articles: 5                                        │
│                                                              │
│  STAGE 2: SCRIPT GENERATION                                 │
│  ├── Model: Cohere (command-a-03-2025)                      │
│  ├── Input: Topic + News content                            │
│  ├── Output: Structured segments (4-6 scenes)               │
│  │   ├── Title                                              │
│  │   ├── Narration                                          │
│  │   └── Text Overlay                                       │
│  └── Word Target: ~2.5 words/second                         │
│                                                              │
│  STAGE 3: VIDEO GENERATION                                  │
│  ├── Image Creation: PIL (Pillow)                           │
│  ├── Video Encoding: OpenCV (cv2)                           │
│  ├── Resolution: 1280x720 (HD)                              │
│  ├── FPS: Variable based on duration                        │
│  └── Output: MP4 file                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Key Components Analysis

#### news_fetcher.py
- **Purpose**: Fetch trending news via RSS feeds
- **Key Function**: `fetch_news(topic, max_articles=5)`
- **Data Source**: Google News RSS (legal, structured)
- **Output Format**: List of dictionaries with title, summary, link, published date

#### script_generator.py
- **Purpose**: Generate video scripts using Cohere LLM
- **Key Function**: `generate_script(topic, news_content, duration)`
- **Prompt Engineering**: Structured prompt requesting 4-6 segments
- **Fallback Models**: Tries multiple Cohere models for resilience

#### video_generator.py
- **Purpose**: Create MP4 videos with text overlays
- **Key Function**: `generate_video(script_data, topic)`
- **Visual Design**: Color-coded backgrounds, centered text, font management
- **Text Wrapping**: Automatic text fitting within frame bounds

### 1.4 Implementation Highlights

| Feature | Implementation |
|---------|----------------|
| **Error Handling** | Retry logic with multiple model fallbacks |
| **Font Management** | Cross-platform font detection (Windows/Linux) |
| **Text Rendering** | Dynamic text wrapping and positioning |
| **Output Management** | Automatic output directory creation |
| **User Interface** | Both CLI and Streamlit web interface |

### 1.5 Metrics & Performance

- **Video Resolution**: 1280x720 (HD)
- **Duration Range**: 30-60 seconds configurable
- **Segments**: 4-6 scenes per video
- **Processing Time**: ~10-30 seconds depending on API response

---

## Task 2: SEO Blog Creation Tool

### 2.1 Project Description

An automated content generation system that:
- Scrapes product data from e-commerce websites
- Generates SEO-optimized keywords using AI
- Creates publishable blog posts (150-200 words)
- Exports content in multiple formats

### 2.2 Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   SEO BLOG CREATION PIPELINE                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  STAGE 1: WEB SCRAPING                                      │
│  ├── Target: books.toscrape.com                             │
│  ├── Library: BeautifulSoup4 + Requests                     │
│  ├── Data Extracted:                                        │
│  │   ├── Title                                              │
│  │   ├── Price (£)                                          │
│  │   ├── Rating (1-5 stars)                                 │
│  │   ├── Category                                           │
│  │   └── Product URL                                        │
│  └── Ethics: Respects robots.txt, rate limiting             │
│                                                              │
│  STAGE 2: DATA PREPROCESSING                                │
│  ├── Title Cleaning: Remove special characters              │
│  ├── Price Tier: Budget/Mid-range/Premium                   │
│  ├── Rating Label: Good/Very Good/Excellent                 │
│  └── Audience Mapping: Based on category                    │
│                                                              │
│  STAGE 3: SEO KEYWORD GENERATION                            │
│  ├── Model: Cohere (command-r-plus-08-2024)                 │
│  ├── Keywords Generated: 5                                  │
│  ├── Keywords Used: Top 4                                   │
│  └── Focus: Commercial/Search intent                        │
│                                                              │
│  STAGE 4: BLOG GENERATION                                   │
│  ├── Model: Cohere (command-r-plus-08-2024)                 │
│  ├── Word Count: 150-200 words                              │
│  ├── Structure:                                             │
│  │   ├── Hook introduction                                  │
│  │   ├── Product highlights                                 │
│  │   ├── Target audience                                    │
│  │   └── Soft call-to-action                                │
│  └── Tone: Informative, trust-building                      │
│                                                              │
│  STAGE 5: CONTENT EXPORT                                    │
│  ├── Formats: Markdown, HTML                                │
│  ├── Metadata: YAML front matter                            │
│  └── File Naming: Sanitized title + date                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Data Models

```python
# Core Data Models (from models.py)

Book:
├── title: str
├── price: float
├── rating: int (1-5)
├── category: str
└── product_url: str

ProcessedBook (extends Book):
├── clean_title: str
├── price_tier: str (Budget/Mid-range/Premium)
├── rating_label: str (Good/Very Good/Excellent)
└── target_audience: str

SEOKeywords:
├── primary_keyword: str
├── selected_keywords: List[str]
└── all_keywords: List[str]

BlogPost:
├── title: str
├── content: str
├── book: ProcessedBook
├── keywords: SEOKeywords
├── word_count: int
└── generated_at: datetime

ExportedContent:
├── file_path: str
├── format: str
├── blog: BlogPost
└── created_at: datetime
```

### 2.4 Configuration System

```python
# Modular configuration using dataclasses

ScraperConfig:
├── base_url: str = "https://books.toscrape.com"
├── max_books: int = 10
├── min_rating: int = 3
├── request_timeout: int = 10
└── user_agent: str

CohereConfig:
├── api_key: str (from env)
├── model: str = "command-r-plus-08-2024"
├── max_tokens_keywords: int = 150
├── max_tokens_blog: int = 600
└── temperature: float = 0.7

SEOConfig:
├── num_keywords_to_generate: int = 5
├── num_keywords_to_use: int = 4
├── blog_min_words: int = 150
└── blog_max_words: int = 200

ExporterConfig:
├── output_dir: str = "output"
├── format: str = "markdown"
└── include_metadata: bool = True
```

### 2.5 SEO Optimization Techniques

| Technique | Implementation |
|-----------|----------------|
| **Primary Keyword Placement** | First paragraph, title |
| **Keyword Density** | Natural integration (4 keywords per 150-200 words) |
| **Meta Description** | Auto-generated from content |
| **Title Optimization** | Include primary keyword |
| **Content Structure** | Introduction → Features → Audience → CTA |
| **YAML Front Matter** | Title, date, category, keywords for CMS |

---

## Task 3: AI Architecture Pipeline

### 3.1 Project Description

An intelligent system that transforms high-level business requirements into:
- Structured requirement analysis
- Modular system architecture
- Database schema design
- Implementation pseudocode

### 3.2 Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  AI ARCHITECTURE PIPELINE                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  INPUT: Business Requirement (Natural Language)             │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ STAGE 1: REQUIREMENT ANALYZER                           ││
│  │ ├── Extracts: Actors, Actions, Entities                 ││
│  │ ├── Identifies: Relationships, Business Rules           ││
│  │ └── Output: Structured analysis JSON                    ││
│  └─────────────────────────────────────────────────────────┘│
│                           ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ STAGE 2: MODULE IDENTIFIER                              ││
│  │ ├── Designs: System modules and services                ││
│  │ ├── Defines: Interfaces, dependencies                   ││
│  │ ├── Maps: Module interactions                           ││
│  │ └── Output: Modular architecture JSON                   ││
│  └─────────────────────────────────────────────────────────┘│
│                           ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ STAGE 3: SCHEMA GENERATOR                               ││
│  │ ├── Creates: Database tables                            ││
│  │ ├── Defines: Fields, types, constraints                 ││
│  │ ├── Maps: Relationships (1:1, 1:N, M:N)                 ││
│  │ └── Output: Database schema JSON                        ││
│  └─────────────────────────────────────────────────────────┘│
│                           ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ STAGE 4: PSEUDOCODE GENERATOR                           ││
│  │ ├── Generates: Function implementations                 ││
│  │ ├── Defines: API contracts                              ││
│  │ ├── Documents: Data flows                               ││
│  │ └── Output: Pseudocode + APIs JSON                      ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  OUTPUT: Complete Technical Specification                    │
│  ├── Markdown document                                       │
│  └── JSON data files                                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Pipeline Stage Details

#### Stage 1: Requirement Analyzer
```json
Output Structure:
{
    "requirement_summary": "Brief summary",
    "actors": [
        {
            "name": "Actor name",
            "type": "user/system/external",
            "description": "Role description"
        }
    ],
    "actions": [
        {
            "name": "Action verb",
            "actor": "Who performs",
            "description": "What it does",
            "priority": "high/medium/low"
        }
    ],
    "entities": [
        {
            "name": "Entity name",
            "description": "Purpose",
            "attributes": ["attr1", "attr2"]
        }
    ],
    "relationships": [...],
    "business_rules": [...]
}
```

#### Stage 2: Module Identifier
```json
Output Structure:
{
    "system_overview": "Description",
    "architecture_pattern": "layered/microservices/MVC",
    "modules": [
        {
            "name": "ModuleName",
            "type": "service/controller/repository",
            "purpose": "What it does",
            "responsibilities": [...],
            "interfaces": [...],
            "dependencies": [...]
        }
    ],
    "module_interactions": [...],
    "cross_cutting_concerns": [...]
}
```

#### Stage 3: Schema Generator
```json
Output Structure:
{
    "database_type": "relational",
    "tables": [
        {
            "name": "table_name",
            "fields": [
                {
                    "name": "field",
                    "data_type": "VARCHAR(255)",
                    "nullable": false,
                    "primary_key": true
                }
            ],
            "indexes": [...]
        }
    ],
    "relationships": [...],
    "enums": [...]
}
```

#### Stage 4: Pseudocode Generator
```json
Output Structure:
{
    "functions": [
        {
            "module": "ModuleName",
            "name": "functionName",
            "parameters": [...],
            "returns": {...},
            "pseudocode": [...],
            "error_handling": [...],
            "complexity": {"time": "O(n)", "space": "O(1)"}
        }
    ],
    "data_flows": [...],
    "api_contracts": [...]
}
```

### 3.4 Design Patterns Used

| Pattern | Application |
|---------|-------------|
| **Pipeline Pattern** | Sequential stage execution |
| **Template Method** | Base class for all stages |
| **Strategy Pattern** | Different LLM models per stage |
| **Factory Pattern** | Stage initialization |
| **Observer Pattern** | Execution logging |

---

## Comparative Analysis

### Technology Comparison

| Aspect | Task 1 | Task 2 | Task 3 |
|--------|--------|--------|--------|
| **Input Type** | Topic + Duration | URL/Product Data | Natural Language |
| **Output Type** | MP4 Video | Markdown/HTML | JSON + Markdown |
| **LLM Usage** | Script generation | Keywords + Blog | Multi-stage analysis |
| **External Data** | RSS Feeds | Web Scraping | None |
| **Processing** | Media generation | Text processing | Data structuring |
| **Complexity** | Medium | Medium | High |

### Pipeline Complexity

```
Task 1: Linear (3 stages)
Input → News → Script → Video → Output

Task 2: Linear (5 stages)
Scrape → Preprocess → Keywords → Blog → Export

Task 3: Hierarchical (4 stages, cumulative data)
Analyze → Modules → Schema → Pseudocode
    └─────────┴─────────┴─────────→ All data flows forward
```

### LLM Prompt Engineering Comparison

| Task | Prompt Style | Output Format | Complexity |
|------|-------------|---------------|------------|
| Task 1 | Structured template | Text segments | Medium |
| Task 2 | Keyword + Content prompts | Natural text | Low-Medium |
| Task 3 | JSON schema definition | Strict JSON | High |

---

## Technical Challenges & Solutions

### Challenge 1: LLM Model Availability
**Problem**: Cohere models get deprecated over time
**Solution**: Implemented fallback model list in script_generator.py
```python
models_to_try = ["command-a-03-2025", "command-r-plus-08-2024", "command-r-08-2024"]
```

### Challenge 2: JSON Parsing from LLM Output
**Problem**: LLMs sometimes return invalid JSON or markdown-wrapped JSON
**Solution**: Robust parsing in base.py with regex cleanup
```python
# Strip markdown code blocks
response = re.sub(r'```json\s*', '', response)
response = re.sub(r'```\s*', '', response)
```

### Challenge 3: Cross-Platform Font Handling
**Problem**: Font paths differ between Windows and Linux
**Solution**: Multi-path font detection in video_generator.py
```python
font_options = [
    "C:/Windows/Fonts/arial.ttf",  # Windows
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
]
```

### Challenge 4: Rate Limiting & API Errors
**Problem**: API rate limits and transient failures
**Solution**: Retry logic with exponential backoff
```python
for attempt in range(max_retries):
    try:
        response = client.chat(...)
    except Exception as e:
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)
```

---

## Recommendations

### Future Improvements

1. **Task 1 - Video Generator**
   - Add voice synthesis (Text-to-Speech)
   - Support multiple video aspect ratios (9:16 for TikTok/Reels)
   - Add background music integration
   - Implement video thumbnail generation

2. **Task 2 - SEO Blog Creator**
   - Add support for more e-commerce platforms
   - Implement A/B testing for headlines
   - Add readability score analysis
   - Support multi-language content generation

3. **Task 3 - Architecture Pipeline**
   - Add UML diagram generation
   - Support for multiple programming languages
   - Code template generation (not just pseudocode)
   - Integration with project scaffolding tools

### Best Practices Applied

- ✅ Environment-based configuration (`.env` files)
- ✅ Modular architecture with separation of concerns
- ✅ Comprehensive error handling
- ✅ Both CLI and Web interfaces
- ✅ Type hints and documentation
- ✅ Retry logic for API resilience

---

## Conclusion

These three GenAI applications demonstrate:

1. **Practical LLM Integration**: Real-world use of Cohere API for different content generation tasks
2. **Pipeline Architecture**: Well-structured, multi-stage processing pipelines
3. **Full-Stack Development**: Both backend logic and frontend UI (Streamlit)
4. **Production Readiness**: Error handling, configuration management, and documentation

Each project solves a distinct problem while showcasing different aspects of AI-powered automation, from media generation to content creation to technical specification.

---

*Report Generated: February 2026*
*GenAI Tasks Portfolio - Technical Documentation*
