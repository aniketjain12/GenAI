"""
SEO Blog Creation Pipeline - Main Orchestrator

This module orchestrates the complete pipeline:
1. Scrape products from e-commerce site
2. Preprocess product data
3. Generate SEO keywords using Cohere
4. Generate SEO blog posts using Cohere
5. Export content to Markdown/HTML

Usage:
    python main.py [--books N] [--format markdown|html] [--output DIR]
    
Environment Variables:
    COHERE_API_KEY: Your Cohere API key (required)
"""

import argparse
import logging
import sys
import os
from typing import List, Optional
from datetime import datetime

from config import PipelineConfig, ScraperConfig, CohereConfig, SEOConfig, ExporterConfig
from models import Book, ProcessedBook, SEOKeywords, BlogPost, ExportedContent
from scraper import ProductScraper
from preprocessor import ProductPreprocessor
from keyword_generator import SEOKeywordGenerator
from blog_generator import SEOBlogGenerator
from exporter import ContentExporter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class SEOBlogPipeline:
    """
    Main pipeline orchestrator for SEO blog generation.
    
    Coordinates all pipeline stages:
    Scraping → Preprocessing → Keywords → Blog → Export
    """
    
    def __init__(self, config: Optional[PipelineConfig] = None):
        """
        Initialize the pipeline with configuration.
        
        Args:
            config: Pipeline configuration. Uses defaults if not provided.
        """
        self.config = config or PipelineConfig()
        
        # Initialize components
        self.scraper = ProductScraper(self.config.scraper)
        self.preprocessor = ProductPreprocessor()
        self.keyword_generator = None  # Lazy initialization (needs API key)
        self.blog_generator = None     # Lazy initialization (needs API key)
        self.exporter = ContentExporter(self.config.exporter)
        
        # Pipeline state
        self.books: List[Book] = []
        self.processed_books: List[ProcessedBook] = []
        self.blogs: List[BlogPost] = []
        self.exported: List[ExportedContent] = []
    
    def _initialize_ai_components(self) -> None:
        """Initialize AI components (requires API key)."""
        if self.keyword_generator is None:
            self.keyword_generator = SEOKeywordGenerator(
                self.config.cohere,
                self.config.seo
            )
        if self.blog_generator is None:
            self.blog_generator = SEOBlogGenerator(
                self.config.cohere,
                self.config.seo
            )
    
    def run(
        self,
        num_books: Optional[int] = None,
        output_format: Optional[str] = None
    ) -> List[ExportedContent]:
        """
        Run the complete pipeline.
        
        Args:
            num_books: Number of books to process (overrides config)
            output_format: Export format (overrides config)
            
        Returns:
            List of exported content
        """
        start_time = datetime.now()
        logger.info("=" * 60)
        logger.info("SEO Blog Creation Pipeline - Starting")
        logger.info("=" * 60)
        
        try:
            # Stage 1: Scrape
            self._stage_scrape(num_books)
            
            # Stage 2: Preprocess
            self._stage_preprocess()
            
            # Initialize AI components
            self._initialize_ai_components()
            
            # Stage 3 & 4: Generate keywords and blogs
            self._stage_generate()
            
            # Stage 5: Export
            self._stage_export(output_format)
            
            # Summary
            self._print_summary(start_time)
            
            return self.exported
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise
    
    def _stage_scrape(self, num_books: Optional[int] = None) -> None:
        """Stage 1: Scrape products."""
        logger.info("\n📥 STAGE 1: Scraping Products")
        logger.info("-" * 40)
        
        count = num_books or self.config.scraper.max_books
        self.books = self.scraper.scrape_top_rated(count)
        
        logger.info(f"✓ Scraped {len(self.books)} books")
    
    def _stage_preprocess(self) -> None:
        """Stage 2: Preprocess products."""
        logger.info("\n🔧 STAGE 2: Preprocessing Products")
        logger.info("-" * 40)
        
        self.processed_books = self.preprocessor.process_books(self.books)
        
        logger.info(f"✓ Preprocessed {len(self.processed_books)} books")
    
    def _stage_generate(self) -> None:
        """Stage 3 & 4: Generate keywords and blogs."""
        logger.info("\n🧠 STAGE 3 & 4: Generating SEO Content")
        logger.info("-" * 40)
        
        self.blogs = []
        
        for i, book in enumerate(self.processed_books, 1):
            logger.info(f"\nProcessing [{i}/{len(self.processed_books)}]: {book.clean_title}")
            
            try:
                # Generate keywords
                logger.info("  → Generating keywords...")
                keywords = self.keyword_generator.generate_keywords(book)
                logger.info(f"  ✓ Keywords: {keywords.selected_keywords}")
                
                # Generate blog
                logger.info("  → Generating blog post...")
                blog = self.blog_generator.generate_blog(book, keywords)
                logger.info(f"  ✓ Blog generated: {blog.word_count} words")
                
                self.blogs.append(blog)
                
            except Exception as e:
                logger.error(f"  ✗ Failed to generate content: {e}")
        
        logger.info(f"\n✓ Generated {len(self.blogs)} blog posts")
    
    def _stage_export(self, output_format: Optional[str] = None) -> None:
        """Stage 5: Export content."""
        logger.info("\n📤 STAGE 5: Exporting Content")
        logger.info("-" * 40)
        
        format_to_use = output_format or self.config.exporter.format
        self.exported = self.exporter.export_all(self.blogs, format_to_use)
        
        for export in self.exported:
            logger.info(f"  ✓ Exported: {export.filepath}")
        
        logger.info(f"\n✓ Exported {len(self.exported)} files")
    
    def _print_summary(self, start_time: datetime) -> None:
        """Print pipeline execution summary."""
        duration = datetime.now() - start_time
        
        logger.info("\n" + "=" * 60)
        logger.info("PIPELINE SUMMARY")
        logger.info("=" * 60)
        logger.info(f"  Books scraped:    {len(self.books)}")
        logger.info(f"  Books processed:  {len(self.processed_books)}")
        logger.info(f"  Blogs generated:  {len(self.blogs)}")
        logger.info(f"  Files exported:   {len(self.exported)}")
        logger.info(f"  Total duration:   {duration.total_seconds():.2f} seconds")
        logger.info(f"  Output directory: {self.config.exporter.output_dir}")
        logger.info("=" * 60)


def create_config_from_args(args: argparse.Namespace) -> PipelineConfig:
    """Create pipeline config from command line arguments."""
    scraper_config = ScraperConfig(
        max_books=args.books,
        min_rating=args.min_rating
    )
    
    cohere_config = CohereConfig(
        api_key=args.api_key or os.getenv("COHERE_API_KEY")
    )
    
    seo_config = SEOConfig()
    
    exporter_config = ExporterConfig(
        output_dir=args.output,
        format=args.format
    )
    
    return PipelineConfig(
        scraper=scraper_config,
        cohere=cohere_config,
        seo=seo_config,
        exporter=exporter_config
    )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='SEO Blog Creation Tool - Generate SEO-optimized blog posts from product data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Default: 5 books, markdown output
  python main.py --books 10 --format html  # 10 books, HTML output
  python main.py --output ./blogs          # Custom output directory
  
Environment Variables:
  COHERE_API_KEY    Your Cohere API key (required)
        """
    )
    
    parser.add_argument(
        '--books', '-n',
        type=int,
        default=5,
        help='Number of books to process (default: 5)'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['markdown', 'html'],
        default='markdown',
        help='Output format (default: markdown)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='output',
        help='Output directory (default: output)'
    )
    
    parser.add_argument(
        '--min-rating', '-r',
        type=int,
        default=3,
        choices=[1, 2, 3, 4, 5],
        help='Minimum book rating to include (default: 3)'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        default=None,
        help='Cohere API key (or set COHERE_API_KEY env var)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Check for API key
    api_key = args.api_key or os.getenv("COHERE_API_KEY")
    if not api_key:
        print("\n❌ ERROR: Cohere API key not found!")
        print("Please set the COHERE_API_KEY environment variable or use --api-key")
        print("\nExample:")
        print("  set COHERE_API_KEY=your-api-key-here")
        print("  python main.py")
        sys.exit(1)
    
    # Create config and run pipeline
    config = create_config_from_args(args)
    
    print("\n🚀 SEO Blog Creation Tool")
    print(f"   Processing {args.books} books → {args.format.upper()} output")
    print()
    
    pipeline = SEOBlogPipeline(config)
    exported = pipeline.run()
    
    if exported:
        print(f"\n✅ Success! Generated {len(exported)} blog posts.")
        print(f"📂 Output directory: {os.path.abspath(args.output)}")
    else:
        print("\n⚠️ No blog posts were generated.")
        sys.exit(1)


if __name__ == "__main__":
    main()
