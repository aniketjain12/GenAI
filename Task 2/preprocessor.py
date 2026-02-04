"""
Product Preprocessor Module

Cleans and enriches scraped book data for SEO generation.
Normalizes titles, categorizes prices, and infers target audiences.
"""

import re
from typing import List
import logging

from models import Book, ProcessedBook
from config import DEFAULT_CONFIG

# Configure logging
logger = logging.getLogger(__name__)


class ProductPreprocessor:
    """
    Preprocesses raw book data for SEO content generation.
    
    Responsibilities:
    - Clean and normalize book titles
    - Categorize price tiers
    - Generate human-readable rating labels
    - Infer target audience based on category
    """
    
    # Price tier thresholds (in GBP)
    PRICE_TIERS = {
        'budget': (0, 15),
        'mid-range': (15, 35),
        'premium': (35, float('inf'))
    }
    
    # Rating labels
    RATING_LABELS = {
        5: 'Exceptional',
        4: 'Highly Rated',
        3: 'Well Received',
        2: 'Mixed Reviews',
        1: 'Needs Improvement'
    }
    
    # Target audience by category
    AUDIENCE_MAP = {
        'travel': 'travel enthusiasts and adventure seekers',
        'mystery': 'mystery lovers and thriller fans',
        'fiction': 'fiction readers and story enthusiasts',
        'romance': 'romance readers and love story fans',
        'historical fiction': 'history buffs and fiction lovers',
        'sequential art': 'comic book fans and graphic novel enthusiasts',
        'classics': 'literature enthusiasts and classic book collectors',
        'fantasy': 'fantasy fans and imaginative readers',
        'science fiction': 'sci-fi enthusiasts and futurist readers',
        'nonfiction': 'knowledge seekers and factual content lovers',
        'poetry': 'poetry lovers and literary enthusiasts',
        'humor': 'readers looking for light entertainment',
        'biography': 'readers interested in real-life stories',
        'self help': 'personal development enthusiasts',
        'business': 'entrepreneurs and business professionals',
        'childrens': 'young readers and parents',
        'young adult': 'teen readers and young adults',
        'horror': 'horror fans and thrill seekers',
        'philosophy': 'deep thinkers and philosophy enthusiasts',
        'psychology': 'psychology students and mind-curious readers',
        'science': 'science enthusiasts and curious minds',
        'default': 'avid readers and book enthusiasts'
    }
    
    def __init__(self):
        """Initialize the preprocessor."""
        pass
    
    def _clean_title(self, title: str) -> str:
        """
        Clean and normalize a book title.
        
        Args:
            title: Raw book title
            
        Returns:
            Cleaned title
        """
        # Remove extra whitespace
        clean = re.sub(r'\s+', ' ', title.strip())
        
        # Remove common suffixes that aren't useful for SEO
        clean = re.sub(r'\s*\(.*?\)\s*$', '', clean)
        
        # Ensure proper capitalization (title case)
        # But preserve all-caps acronyms
        words = clean.split()
        processed_words = []
        for word in words:
            if word.isupper() and len(word) <= 4:
                # Keep acronyms as-is
                processed_words.append(word)
            else:
                processed_words.append(word.capitalize() if word.islower() else word)
        
        return ' '.join(processed_words)
    
    def _get_price_tier(self, price: float) -> str:
        """
        Categorize price into tiers.
        
        Args:
            price: Book price in GBP
            
        Returns:
            Price tier label
        """
        for tier, (min_price, max_price) in self.PRICE_TIERS.items():
            if min_price <= price < max_price:
                return tier
        return 'mid-range'
    
    def _get_rating_label(self, rating: int) -> str:
        """
        Get human-readable rating label.
        
        Args:
            rating: Numeric rating (1-5)
            
        Returns:
            Rating label string
        """
        return self.RATING_LABELS.get(rating, 'Unrated')
    
    def _infer_audience(self, category: str) -> str:
        """
        Infer target audience from book category.
        
        Args:
            category: Book category
            
        Returns:
            Target audience description
        """
        # Normalize category for lookup
        category_lower = category.lower().strip()
        
        # Try exact match first
        if category_lower in self.AUDIENCE_MAP:
            return self.AUDIENCE_MAP[category_lower]
        
        # Try partial match
        for key, audience in self.AUDIENCE_MAP.items():
            if key in category_lower or category_lower in key:
                return audience
        
        return self.AUDIENCE_MAP['default']
    
    def process_book(self, book: Book) -> ProcessedBook:
        """
        Process a single book for SEO generation.
        
        Args:
            book: Raw Book object
            
        Returns:
            ProcessedBook with enriched data
        """
        return ProcessedBook(
            book=book,
            clean_title=self._clean_title(book.title),
            price_tier=self._get_price_tier(book.price),
            rating_label=self._get_rating_label(book.rating),
            target_audience=self._infer_audience(book.category)
        )
    
    def process_books(self, books: List[Book]) -> List[ProcessedBook]:
        """
        Process multiple books.
        
        Args:
            books: List of raw Book objects
            
        Returns:
            List of ProcessedBook objects
        """
        processed = []
        for book in books:
            try:
                processed_book = self.process_book(book)
                processed.append(processed_book)
                logger.info(f"Processed: {processed_book.clean_title}")
            except Exception as e:
                logger.error(f"Failed to process book {book.title}: {e}")
        
        return processed


# Convenience function
def preprocess_books(books: List[Book]) -> List[ProcessedBook]:
    """
    Quick function to preprocess a list of books.
    
    Args:
        books: List of Book objects
        
    Returns:
        List of ProcessedBook objects
    """
    preprocessor = ProductPreprocessor()
    return preprocessor.process_books(books)


if __name__ == "__main__":
    # Test the preprocessor
    from scraper import scrape_trending_books
    
    print("Testing Product Preprocessor...")
    books = scrape_trending_books(3)
    processed = preprocess_books(books)
    
    for pb in processed:
        print(f"\n{pb.clean_title}")
        print(f"  Price Tier: {pb.price_tier}")
        print(f"  Rating: {pb.rating_label}")
        print(f"  Audience: {pb.target_audience}")
