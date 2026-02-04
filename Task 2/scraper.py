"""
Product Scraper Module

Scrapes book data from Books to Scrape (https://books.toscrape.com).
Extracts title, price, rating, category, and product URL.

This module is designed to be easily replaceable with other data sources
(e.g., Amazon) by implementing the same interface.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from urllib.parse import urljoin
import logging
import re

from models import Book
from config import ScraperConfig, DEFAULT_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProductScraper:
    """
    Scrapes product data from an e-commerce website.
    
    Current implementation: Books to Scrape
    Can be extended/replaced for other sources like Amazon.
    """
    
    # Mapping of text ratings to numeric values
    RATING_MAP = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5
    }
    
    def __init__(self, config: Optional[ScraperConfig] = None):
        """
        Initialize the scraper with configuration.
        
        Args:
            config: Scraper configuration. Uses default if not provided.
        """
        self.config = config or DEFAULT_CONFIG.scraper
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create a configured requests session."""
        session = requests.Session()
        session.headers.update({
            'User-Agent': self.config.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        return session
    
    def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a webpage.
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if fetch fails
        """
        try:
            response = self.session.get(url, timeout=self.config.request_timeout)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    def _parse_rating(self, rating_class: str) -> int:
        """
        Convert text rating class to numeric rating.
        
        Args:
            rating_class: CSS class like 'star-rating Three'
            
        Returns:
            Numeric rating (1-5)
        """
        # Extract rating word from class
        rating_match = re.search(r'(one|two|three|four|five)', rating_class.lower())
        if rating_match:
            return self.RATING_MAP.get(rating_match.group(1), 0)
        return 0
    
    def _parse_price(self, price_text: str) -> float:
        """
        Parse price from text.
        
        Args:
            price_text: Price string like '£51.77'
            
        Returns:
            Price as float
        """
        # Remove currency symbol and convert to float
        price_clean = re.sub(r'[^\d.]', '', price_text)
        try:
            return float(price_clean)
        except ValueError:
            return 0.0
    
    def _get_book_category(self, book_url: str) -> str:
        """
        Fetch the category of a book from its detail page.
        
        Args:
            book_url: URL to the book's detail page
            
        Returns:
            Category name or 'Uncategorized'
        """
        soup = self._fetch_page(book_url)
        if not soup:
            return 'Uncategorized'
        
        # Find breadcrumb navigation to get category
        breadcrumb = soup.select('ul.breadcrumb li')
        if len(breadcrumb) >= 3:
            # Category is usually the third item (Home > Category > Book)
            category_link = breadcrumb[2].find('a')
            if category_link:
                return category_link.text.strip()
        
        return 'Uncategorized'
    
    def _parse_book_card(self, article: BeautifulSoup) -> Optional[Book]:
        """
        Parse a single book from its HTML card element.
        
        Args:
            article: BeautifulSoup element for the book card
            
        Returns:
            Book object or None if parsing fails
        """
        try:
            # Extract title
            title_elem = article.select_one('h3 a')
            if not title_elem:
                return None
            title = title_elem.get('title', title_elem.text.strip())
            
            # Extract URL
            relative_url = title_elem.get('href', '')
            # Handle relative URLs properly
            # From homepage: "catalogue/book-name/index.html"
            # From catalogue pages: "../book-name/index.html" or "book-name/index.html"
            if relative_url.startswith('../'):
                # Remove ../ prefix for catalogue page links
                relative_url = relative_url[3:]  # Remove first ../
                while relative_url.startswith('../'):
                    relative_url = relative_url[3:]
            
            # Build proper URL - catalogue is the base for all book pages
            if relative_url.startswith('catalogue/'):
                url = urljoin(self.config.base_url + '/', relative_url)
            else:
                url = urljoin(self.config.base_url + '/catalogue/', relative_url)
            
            # Extract price
            price_elem = article.select_one('p.price_color')
            price = self._parse_price(price_elem.text) if price_elem else 0.0
            
            # Extract rating
            rating_elem = article.select_one('p.star-rating')
            rating = 0
            if rating_elem:
                rating_classes = ' '.join(rating_elem.get('class', []))
                rating = self._parse_rating(rating_classes)
            
            # Check stock
            stock_elem = article.select_one('p.instock')
            in_stock = stock_elem is not None
            
            # Get category from detail page (can be optimized to batch)
            category = self._get_book_category(url)
            
            return Book(
                title=title,
                price=price,
                rating=rating,
                category=category,
                url=url,
                in_stock=in_stock
            )
            
        except Exception as e:
            logger.error(f"Failed to parse book card: {e}")
            return None
    
    def scrape_books(self, max_books: Optional[int] = None, min_rating: Optional[int] = None) -> List[Book]:
        """
        Scrape books from the website.
        
        Args:
            max_books: Maximum number of books to scrape (default from config)
            min_rating: Minimum rating filter (default from config)
            
        Returns:
            List of Book objects
        """
        max_books = max_books or self.config.max_books
        min_rating = min_rating or self.config.min_rating
        
        books: List[Book] = []
        page = 1
        
        logger.info(f"Starting to scrape books (max: {max_books}, min_rating: {min_rating})")
        
        while len(books) < max_books:
            # Construct page URL
            if page == 1:
                page_url = self.config.base_url
            else:
                page_url = f"{self.config.base_url}/catalogue/page-{page}.html"
            
            logger.info(f"Scraping page {page}: {page_url}")
            
            soup = self._fetch_page(page_url)
            if not soup:
                break
            
            # Find all book articles
            articles = soup.select('article.product_pod')
            if not articles:
                logger.info("No more books found, stopping")
                break
            
            for article in articles:
                if len(books) >= max_books:
                    break
                
                book = self._parse_book_card(article)
                if book and book.rating >= min_rating:
                    books.append(book)
                    logger.info(f"Scraped: {book}")
            
            page += 1
            
            # Safety limit to prevent infinite loops
            if page > 50:
                logger.warning("Reached page limit, stopping")
                break
        
        logger.info(f"Scraping complete. Total books: {len(books)}")
        return books
    
    def scrape_top_rated(self, count: int = 5) -> List[Book]:
        """
        Scrape top-rated books.
        
        Args:
            count: Number of top-rated books to return
            
        Returns:
            List of top-rated Book objects
        """
        # Scrape more books than needed, then filter
        all_books = self.scrape_books(max_books=count * 3, min_rating=4)
        
        # Sort by rating (descending), then by price (ascending for value)
        sorted_books = sorted(all_books, key=lambda b: (-b.rating, b.price))
        
        return sorted_books[:count]


# Convenience function for quick usage
def scrape_trending_books(count: int = 5) -> List[Book]:
    """
    Quick function to scrape trending/top-rated books.
    
    Args:
        count: Number of books to scrape
        
    Returns:
        List of Book objects
    """
    scraper = ProductScraper()
    return scraper.scrape_top_rated(count)


if __name__ == "__main__":
    # Test the scraper
    print("Testing Product Scraper...")
    books = scrape_trending_books(3)
    for book in books:
        print(f"\n{book}")
        print(f"  Category: {book.category}")
        print(f"  URL: {book.url}")
