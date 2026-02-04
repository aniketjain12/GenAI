# SEO Blog Creation Tool

An AI-powered tool that automatically generates SEO-optimized blog posts from scraped e-commerce product data.

## 🎯 Overview

This tool implements a complete pipeline that:
1. **Scrapes** product data from e-commerce websites
2. **Preprocesses** and enriches the data
3. **Generates SEO keywords** using Cohere AI
4. **Creates SEO-optimized blog posts** using Cohere AI
5. **Exports** content in publishable formats (Markdown/HTML)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SEO Blog Creation Pipeline                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐                                            │
│  │ Product Scraper │ ─── requests + BeautifulSoup               │
│  │   (scraper.py)  │     Scrapes books.toscrape.com             │
│  └────────┬────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────────┐                                        │
│  │ Product Preprocessor │ ─── Data cleaning & enrichment        │
│  │  (preprocessor.py)   │     Price tiers, audiences            │
│  └──────────┬───────────┘                                       │
│             │                                                    │
│             ▼                                                    │
│  ┌──────────────────────┐                                       │
│  │ SEO Keyword Generator │ ─── Cohere API                       │
│  │ (keyword_generator.py)│     Generate 5 → Select 4            │
│  └──────────┬────────────┘                                      │
│             │                                                    │
│             ▼                                                    │
│  ┌─────────────────────┐                                        │
│  │  SEO Blog Generator  │ ─── Cohere API                        │
│  │  (blog_generator.py) │     150-200 word posts                │
│  └──────────┬───────────┘                                       │
│             │                                                    │
│             ▼                                                    │
│  ┌─────────────────────┐                                        │
│  │   Content Exporter   │ ─── Markdown or HTML                  │
│  │    (exporter.py)     │     With SEO metadata                 │
│  └──────────┬───────────┘                                       │
│             │                                                    │
│             ▼                                                    │
│        📁 output/                                                │
│           ├── book-title-one.md                                 │
│           ├── book-title-two.md                                 │
│           └── ...                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
Task 2/
├── main.py                 # Pipeline orchestrator (entry point)
├── config.py               # Configuration settings
├── models.py               # Data models (Book, BlogPost, etc.)
├── scraper.py              # Web scraper module
├── preprocessor.py         # Data preprocessing module
├── keyword_generator.py    # SEO keyword generation (Cohere)
├── blog_generator.py       # Blog post generation (Cohere)
├── exporter.py             # Content export (Markdown/HTML)
├── requirements.txt        # Python dependencies
├── README.md               # This documentation
└── output/                 # Generated blog posts
    ├── *.md                # Markdown files
    └── *.html              # HTML files
```

## 🚀 Quick Start

### Prerequisites

Before running this application, ensure you have:

- **Python 3.8+** installed on your system
- **pip** (Python package manager)
- **Cohere API Key** (free tier available)

---

## 📥 Step-by-Step Installation Guide

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd "Task 2"

# Or simply download and extract the zip file, then navigate to the folder
cd "path/to/Task 2"
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `requests` - HTTP library for web scraping
- `beautifulsoup4` - HTML parsing
- `cohere` - Cohere AI API client
- `python-dotenv` - Environment variable management
- `streamlit` - Web interface framework

### Step 4: Get Your Cohere API Key

1. Go to [https://dashboard.cohere.com/api-keys](https://dashboard.cohere.com/api-keys)
2. Sign up for a free account (no credit card required)
3. Click "Create API Key"
4. Copy your API key

### Step 5: Configure the API Key

**Option A: Using .env file (Recommended)**

Create a `.env` file in the project folder:

```bash
# Windows (PowerShell)
echo "COHERE_API_KEY=your-api-key-here" > .env

# Linux/Mac
echo "COHERE_API_KEY=your-api-key-here" > .env
```

Or manually create a file named `.env` with this content:
```
COHERE_API_KEY=your-api-key-here
```

**Option B: Using Environment Variable**

```bash
# Windows (Command Prompt)
set COHERE_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:COHERE_API_KEY="your-api-key-here"

# Linux/Mac
export COHERE_API_KEY=your-api-key-here
```

---

## ▶️ Running the Application

### Option 1: Command Line Interface (CLI)

```bash
# Default: 5 books, markdown output
python main.py

# Custom options
python main.py --books 3 --format html --min-rating 5
```

### Option 2: Web Interface (Streamlit)

```bash
# Windows
python -m streamlit run app.py

# Linux/Mac
streamlit run app.py
```

Then open your browser to: **http://localhost:8501**

---

## 🎯 Quick Test

Run a quick test to verify everything works:

```bash
# Generate 1 blog post
python main.py --books 1 --format markdown

# Check the output folder
# Windows
dir output

# Linux/Mac
ls output
```

You should see a `.md` file generated in the `output` folder.

---

## 📖 Usage

### Command Line Examples

```bash
# Default: 5 books, markdown output
python main.py

# Custom options
python main.py --books 10 --format html --output ./blogs
```

## 📖 Usage

### Command Line Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--books` | `-n` | 5 | Number of books to process |
| `--format` | `-f` | markdown | Output format (markdown/html) |
| `--output` | `-o` | output | Output directory |
| `--min-rating` | `-r` | 3 | Minimum book rating (1-5) |
| `--api-key` | - | env var | Cohere API key |
| `--verbose` | `-v` | false | Enable debug logging |

### Examples

```bash
# Generate 10 blog posts in HTML format
python main.py --books 10 --format html

# Only process 5-star rated books
python main.py --min-rating 5

# Verbose output for debugging
python main.py --verbose

# Custom output directory
python main.py --output ./my-blogs
```

### Programmatic Usage

```python
from main import SEOBlogPipeline
from config import PipelineConfig

# Create custom config
config = PipelineConfig()
config.scraper.max_books = 10
config.exporter.format = 'html'

# Run pipeline
pipeline = SEOBlogPipeline(config)
exported = pipeline.run()

# Access results
for export in exported:
    print(f"Created: {export.filepath}")
```

## 📊 Data Source

### Books to Scrape (https://books.toscrape.com)

This tool uses **Books to Scrape** as its data source because:

| Feature | Benefit |
|---------|---------|
| Static HTML | Fast, reliable scraping |
| No JavaScript | Works with requests + BeautifulSoup |
| No bot protection | No CAPTCHAs or rate limits |
| Designed for practice | Ethical scraping |
| Rich data | Titles, prices, ratings, categories |

### Scraped Data Fields

| Field | Description | Example |
|-------|-------------|---------|
| Title | Book title | "A Light in the Attic" |
| Price | Price in GBP | 51.77 |
| Rating | 1-5 stars (numeric) | 4 |
| Category | Book genre | "Poetry" |
| URL | Product page link | https://books.toscrape.com/... |
| In Stock | Availability | true |

### "Trending" Definition

Books are considered "trending" if they:
- Have a rating of 4 or 5 stars
- Appear early on the homepage (higher visibility)

## 🧠 AI/LLM Integration

### Cohere API

This tool uses **Cohere's Generate API** for:

1. **Keyword Generation**
   - Input: Book title, category, rating
   - Output: 5 SEO keywords
   - Selection: Top 3-4 keywords used

2. **Blog Generation**
   - Input: Book details + keywords
   - Output: 150-200 word blog post
   - Structure: Intro → Highlights → Use Cases → CTA

### Keyword Generation Logic

```
Input:
  - Book: "The Art of War" 
  - Category: "Classics"

Cohere generates:
  1. the art of war book
  2. sun tzu art of war
  3. best strategy books
  4. classic military books
  5. business strategy reading

Selected (top 4):
  - the art of war book (primary)
  - sun tzu art of war
  - best strategy books
  - classic military books
```

### Blog Structure

Generated blogs follow this SEO-optimized structure:

1. **Introduction** - Hook with primary keyword
2. **Highlights** - Key book features/benefits
3. **Target Audience** - Who should read this
4. **Call-to-Action** - Soft, trust-building prompt

## 📄 Output Formats

### Markdown (.md)

Features:
- YAML front matter with metadata
- Clean heading structure
- Emoji-enhanced meta info
- Related searches section
- Book link included

Example:
```markdown
---
title: "A Light in the Attic: A Must-Read"
date: 2024-01-15
category: Poetry
keywords: [poetry book, shel silverstein, ...]
---

# A Light in the Attic: A Must-Read

> **Category:** Poetry | **Rating:** ⭐⭐⭐⭐⭐ | **Price:** £51.77

[Blog content here...]

---

**Related Searches:** poetry book • shel silverstein • ...

*[View Book Details](https://...)*
```

### HTML (.html)

Features:
- Complete HTML5 document
- SEO meta tags (description, keywords, OpenGraph)
- Responsive, modern CSS styling
- Star rating visualization
- Call-to-action button
- Mobile-friendly design

## ⚙️ Configuration

All settings are centralized in `config.py`:

### ScraperConfig

```python
ScraperConfig(
    base_url="https://books.toscrape.com",
    max_books=10,           # Books to scrape
    min_rating=3,           # Minimum rating filter
    request_timeout=10      # HTTP timeout
)
```

### CohereConfig

```python
CohereConfig(
    api_key=None,           # From env or argument
    model="command",        # Cohere model
    max_tokens_keywords=100,
    max_tokens_blog=500,
    temperature=0.7         # Creativity (0-1)
)
```

### SEOConfig

```python
SEOConfig(
    num_keywords_to_generate=5,
    num_keywords_to_use=4,
    blog_min_words=150,
    blog_max_words=200
)
```

### ExporterConfig

```python
ExporterConfig(
    output_dir="output",
    format="markdown",      # or "html"
    include_metadata=True
)
```

## 🔄 Extending for Other Data Sources

The architecture is designed for easy source replacement:

### To Add Amazon Support

1. Create `amazon_scraper.py` implementing same interface:

```python
class AmazonScraper:
    def scrape_books(self, max_books, min_rating) -> List[Book]:
        # Amazon-specific scraping logic
        pass
    
    def scrape_top_rated(self, count) -> List[Book]:
        pass
```

2. Update `main.py` to use new scraper:

```python
# In SEOBlogPipeline.__init__
if config.scraper.source == 'amazon':
    self.scraper = AmazonScraper(config.scraper)
else:
    self.scraper = ProductScraper(config.scraper)
```

### Key Abstraction Points

| Component | Interface | Easy to Replace |
|-----------|-----------|-----------------|
| Scraper | `scrape_books()` → `List[Book]` | ✅ Yes |
| Preprocessor | `process_books()` → `List[ProcessedBook]` | ✅ Yes |
| Keyword Gen | `generate_keywords()` → `SEOKeywords` | ✅ Yes (swap LLM) |
| Blog Gen | `generate_blog()` → `BlogPost` | ✅ Yes (swap LLM) |
| Exporter | `export()` → `ExportedContent` | ✅ Yes (add formats) |

## ⚠️ Limitations

### Technical Limitations

| Limitation | Description | Workaround |
|------------|-------------|------------|
| No JavaScript rendering | Can't scrape JS-heavy sites | Use Selenium/Playwright |
| Rate limits | Cohere API has rate limits | Add delays, use batching |
| No image processing | Doesn't extract/include images | Future enhancement |
| English only | Keywords/blogs in English | Add language parameter |

### Content Quality Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| LLM hallucination | May generate incorrect facts | Human review recommended |
| Generic content | Similar books → similar blogs | Increase temperature |
| Word count variance | May exceed 200 words | Truncation applied |
| Keyword stuffing risk | Over-optimization possible | Natural prompt engineering |

### Scraping Limitations

| Limitation | Current Site | Real Sites |
|------------|--------------|------------|
| Bot detection | None | CAPTCHAs, rate limits |
| Dynamic content | None | JavaScript required |
| Structure changes | Stable | May break scraper |
| Legal concerns | Designed for scraping | Check robots.txt, ToS |

## 🛡️ Best Practices

### For Production Use

1. **Add rate limiting** to scraper
2. **Implement retry logic** for API calls
3. **Add human review** before publishing
4. **Monitor API costs** with usage tracking
5. **Validate output** word counts and quality

### For SEO Quality

1. Review generated keywords for relevance
2. Edit blogs for brand voice consistency
3. Add unique insights beyond generated content
4. Verify facts mentioned in blogs
5. Test with SEO analysis tools

## 📝 License

This project is for educational purposes. Ensure compliance with:
- Website Terms of Service
- Cohere API Terms
- Copyright laws for generated content

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. "COHERE_API_KEY not found" Error

```
Error: Cohere API key not provided
```

**Solution:**
- Create a `.env` file with `COHERE_API_KEY=your-key`
- Or set the environment variable before running

#### 2. "streamlit: command not found" Error

```
streamlit : The term 'streamlit' is not recognized
```

**Solution:**
```bash
# Use Python module syntax instead
python -m streamlit run app.py
```

#### 3. Module Import Errors

```
ModuleNotFoundError: No module named 'cohere'
```

**Solution:**
```bash
pip install -r requirements.txt
```

#### 4. API Timeout Errors

```
Connection timeout or API not responding
```

**Solution:**
- Check your internet connection
- Wait a few minutes and retry (API rate limits)
- Use `--verbose` flag to see detailed logs

#### 5. PowerShell Encoding Errors (Windows)

```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Solution:**
```powershell
$env:PYTHONIOENCODING='utf-8'
python main.py
```

#### 6. Permission Denied (Output Folder)

```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Create the output folder manually
mkdir output

# Or use a different output directory
python main.py --output ./my-blogs
```

---

## 📧 Support

For issues or questions:
1. Check the documentation above
2. Review error messages and logs
3. Ensure API key is valid
4. Verify network connectivity
