"""
Data models for the SEO Blog Creation Tool.
Defines the data structures used throughout the pipeline.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Book:
    """
    Represents a scraped book product.
    
    Attributes:
        title: The book's title
        price: Price as a float (in GBP)
        rating: Numeric rating (1-5)
        category: Book category/genre
        url: Full URL to the book's detail page
        in_stock: Whether the book is in stock
    """
    title: str
    price: float
    rating: int
    category: str
    url: str
    in_stock: bool = True
    
    def __str__(self) -> str:
        return f"{self.title} (Rating: {self.rating}/5, £{self.price:.2f})"


@dataclass
class ProcessedBook:
    """
    Preprocessed book data ready for SEO generation.
    
    Attributes:
        book: Original book data
        clean_title: Cleaned/normalized title
        price_tier: Price category (budget/mid-range/premium)
        rating_label: Human-readable rating (e.g., "Highly Rated")
        target_audience: Inferred target audience
    """
    book: Book
    clean_title: str
    price_tier: str
    rating_label: str
    target_audience: str
    
    @property
    def title(self) -> str:
        return self.clean_title
    
    @property
    def category(self) -> str:
        return self.book.category
    
    @property
    def url(self) -> str:
        return self.book.url
    
    @property
    def price(self) -> float:
        return self.book.price
    
    @property
    def rating(self) -> int:
        return self.book.rating


@dataclass
class SEOKeywords:
    """
    Generated SEO keywords for a book.
    
    Attributes:
        all_keywords: All generated keywords
        selected_keywords: Top keywords selected for use
        primary_keyword: The main keyword to emphasize
    """
    all_keywords: List[str]
    selected_keywords: List[str]
    primary_keyword: str
    
    def __str__(self) -> str:
        return f"Primary: {self.primary_keyword}, Others: {', '.join(self.selected_keywords[1:])}"


@dataclass
class BlogPost:
    """
    Generated SEO blog post.
    
    Attributes:
        title: Blog post title
        content: Main blog content
        keywords: SEO keywords used
        word_count: Number of words in content
        book: The book this blog is about
        generated_at: Timestamp of generation
    """
    title: str
    content: str
    keywords: SEOKeywords
    book: ProcessedBook
    word_count: int = 0
    generated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Calculate word count after initialization."""
        if self.word_count == 0:
            self.word_count = len(self.content.split())


@dataclass
class ExportedContent:
    """
    Exported blog content.
    
    Attributes:
        filepath: Path to the exported file
        format: Export format (markdown/html)
        blog_post: The exported blog post
    """
    filepath: str
    format: str
    blog_post: BlogPost
