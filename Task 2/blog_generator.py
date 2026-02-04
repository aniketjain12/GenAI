"""
SEO Blog Generator Module

Generates SEO-optimized blog posts for books using Cohere API.
Creates engaging, keyword-rich content in the 150-200 word range.
"""

import cohere
from typing import Optional
import logging
import re

from models import ProcessedBook, SEOKeywords, BlogPost
from config import CohereConfig, SEOConfig, DEFAULT_CONFIG

# Configure logging
logger = logging.getLogger(__name__)


class SEOBlogGenerator:
    """
    Generates SEO-optimized blog posts using Cohere LLM.
    
    Creates structured, engaging content with natural keyword placement.
    """
    
    def __init__(
        self,
        cohere_config: Optional[CohereConfig] = None,
        seo_config: Optional[SEOConfig] = None
    ):
        """
        Initialize the blog generator.
        
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
    
    def _build_blog_prompt(self, book: ProcessedBook, keywords: SEOKeywords) -> str:
        """
        Build the prompt for blog generation.
        
        Args:
            book: Processed book data
            keywords: Generated SEO keywords
            
        Returns:
            Prompt string
        """
        keywords_str = ', '.join(keywords.selected_keywords)
        
        prompt = f"""Write an SEO-optimized blog post for the following book.

Book Details:
- Title: {book.clean_title}
- Category: {book.category}
- Price: £{book.price:.2f} ({book.price_tier})
- Rating: {book.rating_label} ({book.rating}/5 stars)
- Target Audience: {book.target_audience}

SEO Keywords to Include (use naturally):
{keywords_str}

Primary Keyword (use in first paragraph): {keywords.primary_keyword}

Requirements:
1. Length: Exactly 150-200 words
2. Structure:
   - Engaging introduction with primary keyword
   - Book highlights and key features
   - Who should read this book / use cases
   - Soft call-to-action (avoid hard selling)
3. Tone: Informative, trust-building, neutral promotional
4. Use keywords naturally - don't force them
5. Make it reader-friendly and engaging

Write the blog post now:"""
        
        return prompt
    
    def _generate_title(self, book: ProcessedBook, keywords: SEOKeywords) -> str:
        """
        Generate an SEO-friendly blog title.
        
        Args:
            book: Processed book data
            keywords: SEO keywords
            
        Returns:
            Blog title
        """
        # Create variations and pick one based on category
        title_templates = [
            f"{book.clean_title}: A Must-Read for {book.target_audience.title()}",
            f"Discover {book.clean_title} - {book.rating_label} {book.category} Book",
            f"Why {book.clean_title} is the Perfect {book.category} Read",
            f"{book.clean_title} Review: Your Next Favorite {book.category} Book",
        ]
        
        # Use the first template for consistency
        return title_templates[0]
    
    def _count_words(self, text: str) -> int:
        """Count words in text."""
        return len(text.split())
    
    def _clean_blog_content(self, content: str) -> str:
        """
        Clean and format the generated blog content.
        
        Args:
            content: Raw generated content
            
        Returns:
            Cleaned content
        """
        # Remove any prompt leakage
        content = re.sub(r'^(Blog Post|Here\'s the blog|Here is).*?:\s*', '', content, flags=re.IGNORECASE)
        
        # Clean up whitespace
        content = content.strip()
        
        # Ensure proper paragraph spacing
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content
    
    def _truncate_to_word_limit(self, content: str, max_words: int) -> str:
        """
        Truncate content to word limit while keeping sentences complete.
        
        Args:
            content: Blog content
            max_words: Maximum word count
            
        Returns:
            Truncated content
        """
        words = content.split()
        if len(words) <= max_words:
            return content
        
        # Find the last sentence boundary within the limit
        truncated = ' '.join(words[:max_words])
        
        # Try to end at a sentence
        last_period = truncated.rfind('.')
        last_question = truncated.rfind('?')
        last_exclaim = truncated.rfind('!')
        
        last_sentence = max(last_period, last_question, last_exclaim)
        
        if last_sentence > len(truncated) * 0.7:  # At least 70% of content
            return truncated[:last_sentence + 1]
        
        return truncated + '.'
    
    def generate_blog(self, book: ProcessedBook, keywords: SEOKeywords) -> BlogPost:
        """
        Generate an SEO-optimized blog post.
        
        Args:
            book: Processed book data
            keywords: SEO keywords
            
        Returns:
            BlogPost object
        """
        prompt = self._build_blog_prompt(book, keywords)
        title = self._generate_title(book, keywords)
        
        logger.info(f"Generating blog for: {book.clean_title}")
        
        try:
            response = self.client.chat(
                model=self.cohere_config.model,
                message=prompt,
                max_tokens=self.cohere_config.max_tokens_blog,
                temperature=self.cohere_config.temperature
            )
            
            raw_content = response.text
            content = self._clean_blog_content(raw_content)
            
            # Ensure word count is within limits
            word_count = self._count_words(content)
            if word_count > self.seo_config.blog_max_words:
                content = self._truncate_to_word_limit(content, self.seo_config.blog_max_words)
            
            logger.info(f"Generated blog with {self._count_words(content)} words")
            
            return BlogPost(
                title=title,
                content=content,
                keywords=keywords,
                book=book,
                word_count=self._count_words(content)
            )
            
        except Exception as e:
            logger.error(f"Cohere API error: {e}")
            # Return a basic fallback blog
            return self._generate_fallback_blog(book, keywords, title)
    
    def _generate_fallback_blog(
        self,
        book: ProcessedBook,
        keywords: SEOKeywords,
        title: str
    ) -> BlogPost:
        """
        Generate a basic fallback blog without API.
        
        Args:
            book: Processed book data
            keywords: SEO keywords
            title: Blog title
            
        Returns:
            Basic BlogPost
        """
        content = f"""Looking for an exceptional {book.category.lower()} book? "{book.clean_title}" is a {book.rating_label.lower()} choice that has captivated readers worldwide.

This {book.price_tier}-priced book offers outstanding value for {book.target_audience}. With a solid {book.rating}/5 star rating, it delivers quality content that resonates with its audience.

What makes this book special is its ability to engage readers from the first page. Whether you're a dedicated fan of {book.category.lower()} or new to the genre, you'll find something to appreciate here.

Perfect for {book.target_audience}, this book makes an excellent addition to any collection. Consider picking up your copy today and discover why readers rate it so highly."""

        return BlogPost(
            title=title,
            content=content,
            keywords=keywords,
            book=book
        )


# Convenience function
def generate_blog(
    book: ProcessedBook,
    keywords: SEOKeywords,
    api_key: Optional[str] = None
) -> BlogPost:
    """
    Quick function to generate a blog post.
    
    Args:
        book: Processed book data
        keywords: SEO keywords
        api_key: Optional Cohere API key
        
    Returns:
        BlogPost object
    """
    config = CohereConfig(api_key=api_key) if api_key else None
    generator = SEOBlogGenerator(cohere_config=config)
    return generator.generate_blog(book, keywords)


if __name__ == "__main__":
    # Test the blog generator (requires API key)
    import os
    
    print("Testing SEO Blog Generator...")
    
    if not os.getenv("COHERE_API_KEY"):
        print("Set COHERE_API_KEY environment variable to test")
    else:
        from scraper import scrape_trending_books
        from preprocessor import preprocess_books
        from keyword_generator import generate_keywords
        
        books = scrape_trending_books(1)
        processed = preprocess_books(books)
        
        if processed:
            book = processed[0]
            keywords = generate_keywords(book)
            blog = generate_blog(book, keywords)
            
            print(f"\n{'='*60}")
            print(f"Title: {blog.title}")
            print(f"Word Count: {blog.word_count}")
            print(f"{'='*60}")
            print(blog.content)
            print(f"{'='*60}")
