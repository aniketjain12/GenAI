"""
SEO Keyword Generator Module

Generates SEO-optimized keywords for books using Cohere API.
Produces commercial/search-intent focused keywords.
"""

import cohere
from typing import List, Optional
import logging
import re

from models import ProcessedBook, SEOKeywords
from config import CohereConfig, SEOConfig, DEFAULT_CONFIG

# Configure logging
logger = logging.getLogger(__name__)


class SEOKeywordGenerator:
    """
    Generates SEO keywords using Cohere LLM.
    
    Produces short, commercial-intent focused keyword phrases
    optimized for search engines.
    """
    
    def __init__(
        self,
        cohere_config: Optional[CohereConfig] = None,
        seo_config: Optional[SEOConfig] = None
    ):
        """
        Initialize the keyword generator.
        
        Args:
            cohere_config: Cohere API configuration
            seo_config: SEO generation configuration
        """
        self.cohere_config = cohere_config or DEFAULT_CONFIG.cohere
        self.seo_config = seo_config or DEFAULT_CONFIG.seo
        
        if not self.cohere_config.api_key:
            raise ValueError(
                "Cohere API key not found. Set COHERE_API_KEY environment variable "
                "or pass it in CohereConfig."
            )
        
        self.client = cohere.Client(self.cohere_config.api_key)
    
    def _build_keyword_prompt(self, book: ProcessedBook) -> str:
        """
        Build the prompt for keyword generation.
        
        Args:
            book: Processed book data
            
        Returns:
            Prompt string
        """
        prompt = f"""Generate exactly {self.seo_config.num_keywords_to_generate} SEO keywords for the following book.

Book Details:
- Title: {book.clean_title}
- Category: {book.category}
- Rating: {book.rating_label}
- Target Audience: {book.target_audience}

Requirements for keywords:
1. Short phrases (2-4 words each)
2. Commercial/search intent focused (what people would search to find this book)
3. Include the book title or variations
4. Include genre-related terms
5. Be specific and actionable

Return ONLY the keywords, one per line, numbered 1-{self.seo_config.num_keywords_to_generate}.
Example format:
1. keyword phrase one
2. keyword phrase two

Keywords:"""
        
        return prompt
    
    def _parse_keywords(self, response_text: str) -> List[str]:
        """
        Parse keywords from LLM response.
        
        Args:
            response_text: Raw LLM response
            
        Returns:
            List of keyword strings
        """
        keywords = []
        lines = response_text.strip().split('\n')
        
        for line in lines:
            # Remove numbering and clean up
            clean = re.sub(r'^\d+[\.\)\-\s]+', '', line.strip())
            clean = clean.strip('"\'')
            
            if clean and len(clean) > 2:
                # Normalize whitespace and lowercase for consistency
                keyword = ' '.join(clean.lower().split())
                keywords.append(keyword)
        
        return keywords
    
    def _select_top_keywords(self, keywords: List[str]) -> List[str]:
        """
        Select top keywords for use in blog.
        
        Args:
            keywords: All generated keywords
            
        Returns:
            Selected top keywords
        """
        # For now, simply take the first N keywords
        # Future: Could implement relevance scoring
        return keywords[:self.seo_config.num_keywords_to_use]
    
    def generate_keywords(self, book: ProcessedBook) -> SEOKeywords:
        """
        Generate SEO keywords for a book.
        
        Args:
            book: Processed book data
            
        Returns:
            SEOKeywords object with generated keywords
        """
        prompt = self._build_keyword_prompt(book)
        
        logger.info(f"Generating keywords for: {book.clean_title}")
        
        try:
            response = self.client.chat(
                model=self.cohere_config.model,
                message=prompt,
                max_tokens=self.cohere_config.max_tokens_keywords,
                temperature=self.cohere_config.temperature
            )
            
            response_text = response.text
            all_keywords = self._parse_keywords(response_text)
            
            # Ensure we have at least some keywords
            if not all_keywords:
                # Fallback: generate basic keywords from title and category
                all_keywords = self._generate_fallback_keywords(book)
            
            selected = self._select_top_keywords(all_keywords)
            primary = selected[0] if selected else book.clean_title.lower()
            
            logger.info(f"Generated {len(all_keywords)} keywords, selected {len(selected)}")
            
            return SEOKeywords(
                all_keywords=all_keywords,
                selected_keywords=selected,
                primary_keyword=primary
            )
            
        except Exception as e:
            logger.error(f"Cohere API error: {e}")
            # Return fallback keywords
            fallback = self._generate_fallback_keywords(book)
            return SEOKeywords(
                all_keywords=fallback,
                selected_keywords=fallback[:self.seo_config.num_keywords_to_use],
                primary_keyword=fallback[0]
            )
    
    def _generate_fallback_keywords(self, book: ProcessedBook) -> List[str]:
        """
        Generate fallback keywords without API.
        
        Args:
            book: Processed book data
            
        Returns:
            List of basic keywords
        """
        title_words = book.clean_title.lower()
        category = book.category.lower()
        
        return [
            f"{title_words} book",
            f"buy {title_words}",
            f"best {category} books",
            f"{category} book recommendations",
            f"{title_words} review"
        ]


# Convenience function
def generate_keywords(book: ProcessedBook, api_key: Optional[str] = None) -> SEOKeywords:
    """
    Quick function to generate keywords for a book.
    
    Args:
        book: Processed book data
        api_key: Optional Cohere API key
        
    Returns:
        SEOKeywords object
    """
    config = CohereConfig(api_key=api_key) if api_key else None
    generator = SEOKeywordGenerator(cohere_config=config)
    return generator.generate_keywords(book)


if __name__ == "__main__":
    # Test the keyword generator (requires API key)
    import os
    
    print("Testing SEO Keyword Generator...")
    
    if not os.getenv("COHERE_API_KEY"):
        print("Set COHERE_API_KEY environment variable to test")
    else:
        from scraper import scrape_trending_books
        from preprocessor import preprocess_books
        
        books = scrape_trending_books(1)
        processed = preprocess_books(books)
        
        if processed:
            keywords = generate_keywords(processed[0])
            print(f"\nKeywords for: {processed[0].clean_title}")
            print(f"Primary: {keywords.primary_keyword}")
            print(f"Selected: {keywords.selected_keywords}")
            print(f"All: {keywords.all_keywords}")
