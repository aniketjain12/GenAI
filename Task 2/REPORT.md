# SEO Blog Creation Tool - Project Report

## 📋 Project Overview

This report documents the development of an AI-based SEO Blog Creation Tool that automates the process of generating SEO-optimized blog posts from scraped e-commerce product data.

**Project Date:** February 2026  
**Developer:** AI-Assisted Development

---

## 🎯 Objectives Achieved

| Objective | Status | Implementation |
|-----------|--------|----------------|
| Scrape trending products from e-commerce site | ✅ Complete | Books to Scrape (scraper.py) |
| Automate SEO keyword research | ✅ Complete | Cohere AI API (keyword_generator.py) |
| Generate 150-200 word blog posts | ✅ Complete | Cohere AI API (blog_generator.py) |
| Export to publishable format | ✅ Complete | Markdown & HTML (exporter.py) |
| Publish to external platforms | ✅ Complete | Medium, WordPress, Dev.to (publisher.py) |
| User-friendly interface | ✅ Complete | Streamlit Web App (app.py) |

---

## 🏗️ Architecture

### Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SEO Blog Creation Pipeline                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [E-Commerce Site]                                                   │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────────┐     requests + BeautifulSoup                   │
│  │ Product Scraper │ ──► Scrapes top-rated products                 │
│  │   (scraper.py)  │     Extracts: title, price, rating, category  │
│  └────────┬────────┘                                                │
│           │                                                          │
│           ▼                                                          │
│  ┌─────────────────────┐                                            │
│  │ Product Preprocessor │ ──► Cleans data, infers audience         │
│  │  (preprocessor.py)   │     Adds: price tier, rating label       │
│  └──────────┬───────────┘                                           │
│             │                                                        │
│             ▼                                                        │
│  ┌──────────────────────┐    Cohere Chat API                        │
│  │ SEO Keyword Generator │ ──► Generates 5 keywords                 │
│  │ (keyword_generator.py)│     Selects top 3-4 for use             │
│  └──────────┬────────────┘                                          │
│             │                                                        │
│             ▼                                                        │
│  ┌─────────────────────┐     Cohere Chat API                        │
│  │  SEO Blog Generator  │ ──► Creates 150-200 word posts           │
│  │  (blog_generator.py) │     SEO-optimized structure              │
│  └──────────┬───────────┘                                           │
│             │                                                        │
│             ▼                                                        │
│  ┌─────────────────────┐                                            │
│  │   Content Exporter   │ ──► Markdown with YAML front matter      │
│  │    (exporter.py)     │     HTML with full styling + SEO meta    │
│  └──────────┬───────────┘                                           │
│             │                                                        │
│             ▼                                                        │
│  ┌─────────────────────┐                                            │
│  │   Blog Publisher     │ ──► Medium, WordPress, Dev.to            │
│  │   (publisher.py)     │     Automatic publishing with APIs       │
│  └──────────────────────┘                                           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Module Descriptions

| Module | Purpose | Key Features |
|--------|---------|--------------|
| `config.py` | Centralized configuration | Dataclasses for all settings |
| `models.py` | Data structures | Book, ProcessedBook, SEOKeywords, BlogPost |
| `scraper.py` | Web scraping | BeautifulSoup, rating parsing, pagination |
| `preprocessor.py` | Data enrichment | Price tiers, audience inference |
| `keyword_generator.py` | SEO keywords | Cohere API, fallback generation |
| `blog_generator.py` | Blog content | Cohere API, structured prompts |
| `exporter.py` | File export | Markdown, HTML with SEO meta tags |
| `publisher.py` | Platform publishing | Medium, WordPress, Dev.to APIs |
| `main.py` | CLI interface | Argparse, pipeline orchestration |
| `app.py` | Web interface | Streamlit, interactive UI |

---

## 🔧 Technical Implementation

### 1. Product Scraping (scraper.py)

**Data Source:** [Books to Scrape](https://books.toscrape.com)

**Why This Source:**
- Static HTML (no JavaScript rendering needed)
- Designed for scraping practice
- No bot protection or CAPTCHAs
- Rich product data available

**Data Extracted:**
```python
@dataclass
class Book:
    title: str       # Book title
    price: float     # Price in GBP
    rating: int      # 1-5 stars (converted from text)
    category: str    # Genre/category
    url: str         # Product page URL
    in_stock: bool   # Availability
```

**Trending Definition:**
- Books with rating ≥ 4 stars
- Sorted by rating (descending), then price (ascending)

### 2. SEO Keyword Generation (keyword_generator.py)

**LLM Provider:** Cohere API (Chat endpoint)

**Prompt Engineering:**
```
Generate exactly 5 SEO keywords for the following book.

Book Details:
- Title: {title}
- Category: {category}
- Rating: {rating_label}
- Target Audience: {audience}

Requirements:
1. Short phrases (2-4 words each)
2. Commercial/search intent focused
3. Include book title variations
4. Include genre-related terms
```

**Keyword Selection:**
- Generate 5 keywords
- Automatically select top 3-4
- Primary keyword emphasized in blog intro

### 3. Blog Generation (blog_generator.py)

**Content Requirements:**
- 150-200 words
- Natural keyword placement
- SEO-friendly structure:
  1. Engaging introduction with primary keyword
  2. Book highlights and features
  3. Target audience / use cases
  4. Soft call-to-action

**Tone:**
- Informative
- Trust-building
- Neutral promotional (not hard-selling)

### 4. Content Export (exporter.py)

**Markdown Format:**
```markdown
---
title: "Book Title"
date: 2026-02-03
category: Fiction
keywords: [keyword1, keyword2, keyword3]
word_count: 175
---

# Blog Title

> **Category:** Fiction | **Rating:** ⭐⭐⭐⭐⭐ | **Price:** £19.99

[Content...]

---
**Related Searches:** keyword1 • keyword2 • keyword3
```

**HTML Format:**
- Full HTML5 document
- SEO meta tags (description, keywords, OpenGraph)
- Responsive CSS styling
- Star rating visualization
- CTA button

### 5. Platform Publishing (publisher.py)

**Supported Platforms:**

| Platform | API | Auth Method |
|----------|-----|-------------|
| Medium | REST API v1 | Integration Token |
| WordPress | REST API v2 | Application Password |
| Dev.to | Forem API | API Key |

**Publishing Options:**
- Publish as draft (recommended for review)
- Publish immediately as public
- Automatic tag/keyword assignment

---

## 🖥️ User Interfaces

### Command Line Interface (main.py)

```bash
# Basic usage
python main.py --books 5 --format markdown

# All options
python main.py --books 10 --format html --output ./blogs --min-rating 4 --verbose
```

### Streamlit Web Interface (app.py)

**Features:**
- Sidebar configuration panel
- Real-time progress tracking
- Blog preview with expandable cards
- Download buttons for exported files
- Publishing to external platforms
- Session state management

**Tabs:**
1. 🚀 Generate - Run pipeline
2. 📚 Scraped Books - View scraped data
3. 📄 Generated Blogs - Preview content
4. 📥 Exported Files - Download files
5. 🌐 Publish - Push to platforms

---

## 📂 Project Structure

```
Task 2/
├── main.py                 # CLI entry point
├── app.py                  # Streamlit web interface
├── config.py               # Configuration settings
├── models.py               # Data models
├── scraper.py              # Web scraper
├── preprocessor.py         # Data preprocessing
├── keyword_generator.py    # SEO keyword generation
├── blog_generator.py       # Blog content generation
├── exporter.py             # File export
├── publisher.py            # Platform publishing
├── requirements.txt        # Dependencies
├── README.md               # Documentation
├── REPORT.md               # This report
├── .env                    # Environment variables (API keys)
└── output/                 # Generated blog files
    ├── *.md                # Markdown files
    └── *.html              # HTML files
```

---

## 🚀 Setup & Usage

### Prerequisites

```bash
pip install -r requirements.txt
```

### Environment Variables

Create `.env` file:
```
COHERE_API_KEY=your-cohere-api-key

# Optional - for publishing
MEDIUM_ACCESS_TOKEN=your-medium-token
DEVTO_API_KEY=your-devto-key
WORDPRESS_URL=https://your-site.com
WORDPRESS_USERNAME=your-username
WORDPRESS_APP_PASSWORD=your-app-password
```

### Running the Application

**CLI Mode:**
```bash
python main.py --books 5 --format markdown
```

**Web Interface:**
```bash
streamlit run app.py
```

---

## 📊 Sample Output

### Generated Keywords Example
```
Primary: sapiens a brief history book
Selected:
  - sapiens a brief history book
  - buy sapiens book online
  - best history books 2026
  - human evolution reading
```

### Generated Blog Example

**Title:** Sapiens: A Brief History of Humankind - A Must-Read for History Buffs

**Word Count:** 178 words

**Content Preview:**
> Looking for an exceptional non-fiction book? "Sapiens: A Brief History of Humankind" is a highly rated choice that has captivated readers worldwide.
>
> This premium-priced book offers outstanding value for knowledge seekers and factual content lovers. With a solid 5/5 star rating, it delivers quality content that resonates with its audience...

---

## ⚠️ Limitations & Future Improvements

### Current Limitations

| Limitation | Impact | Potential Solution |
|------------|--------|-------------------|
| Cohere API rate limits | 5 calls/min on trial | Upgrade to production key |
| Fallback content generic | Lower quality when API fails | Improve fallback templates |
| Single data source | Limited to books | Add Amazon/eBay adapters |
| English only | No multilingual support | Add language parameter |

### Future Improvements

1. **Multiple E-commerce Sources**
   - Amazon Product API
   - eBay Browse API
   - Shopify stores

2. **Enhanced SEO**
   - Google Keyword Planner integration
   - Ubersuggest API
   - Search volume metrics

3. **Content Quality**
   - Image extraction and embedding
   - Longer-form content options
   - Multiple writing styles/tones

4. **Publishing**
   - Blogger/Blogspot support
   - LinkedIn articles
   - Scheduled publishing

5. **Analytics**
   - Track published post performance
   - SEO ranking monitoring
   - Keyword position tracking

---

## 📝 Conclusion

This project successfully demonstrates an end-to-end AI-powered SEO blog generation system. The modular architecture allows for easy extension and modification, while the dual CLI/Web interface provides flexibility for different use cases.

**Key Achievements:**
- ✅ Automated product scraping from e-commerce sites
- ✅ AI-powered SEO keyword generation
- ✅ SEO-optimized blog content creation
- ✅ Multi-format export (Markdown/HTML)
- ✅ Publishing to external platforms
- ✅ User-friendly web interface

The tool is production-ready for generating SEO content at scale, with proper API key configuration.

---

## 📎 Links

- **Source Code:** [Local Repository]
- **Output Directory:** `./output/`
- **Web Interface:** `http://localhost:8501` (when running Streamlit)

---

*Report generated: February 2026*
