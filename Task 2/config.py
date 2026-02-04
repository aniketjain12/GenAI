"""
Configuration settings for the SEO Blog Creation Tool.
Centralizes all configurable parameters for easy modification.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class ScraperConfig:
    """Configuration for the web scraper."""
    base_url: str = "https://books.toscrape.com"
    max_books: int = 10  # Number of books to scrape
    min_rating: int = 3  # Minimum rating (1-5) to consider as "top-rated"
    request_timeout: int = 10  # Timeout for HTTP requests in seconds
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SEO-Blog-Tool/1.0"


@dataclass
class CohereConfig:
    """Configuration for Cohere API."""
    api_key: Optional[str] = None
    model: str = "command-r-plus-08-2024"  # Current Cohere model (Chat API)
    max_tokens_keywords: int = 150  # Max tokens for keyword generation
    max_tokens_blog: int = 600  # Max tokens for blog generation
    temperature: float = 0.7  # Creativity level (0-1)
    
    def __post_init__(self):
        """Load API key from environment if not provided."""
        if self.api_key is None:
            self.api_key = os.getenv("COHERE_API_KEY")


@dataclass
class SEOConfig:
    """Configuration for SEO generation."""
    num_keywords_to_generate: int = 5  # Keywords to request from LLM
    num_keywords_to_use: int = 4  # Keywords to use in blog (top N)
    blog_min_words: int = 150
    blog_max_words: int = 200


@dataclass
class ExporterConfig:
    """Configuration for content export."""
    output_dir: str = "output"
    format: str = "markdown"  # "markdown" or "html"
    include_metadata: bool = True  # Include generation metadata


@dataclass
class PipelineConfig:
    """Master configuration combining all sub-configs."""
    scraper: ScraperConfig = None
    cohere: CohereConfig = None
    seo: SEOConfig = None
    exporter: ExporterConfig = None
    
    def __post_init__(self):
        """Initialize default configs if not provided."""
        if self.scraper is None:
            self.scraper = ScraperConfig()
        if self.cohere is None:
            self.cohere = CohereConfig()
        if self.seo is None:
            self.seo = SEOConfig()
        if self.exporter is None:
            self.exporter = ExporterConfig()


# Default configuration instance
DEFAULT_CONFIG = PipelineConfig()
