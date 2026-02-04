"""
Content Exporter Module

Exports generated blog posts to publishable formats (Markdown/HTML).
Handles file creation, formatting, and metadata inclusion.
"""

import os
from typing import List, Optional
from datetime import datetime
import logging
import re

from models import BlogPost, ExportedContent
from config import ExporterConfig, DEFAULT_CONFIG

# Configure logging
logger = logging.getLogger(__name__)


class ContentExporter:
    """
    Exports blog posts to Markdown or HTML format.
    
    Creates properly formatted, publishable content files
    with optional metadata headers.
    """
    
    def __init__(self, config: Optional[ExporterConfig] = None):
        """
        Initialize the exporter.
        
        Args:
            config: Exporter configuration
        """
        self.config = config or DEFAULT_CONFIG.exporter
        self._ensure_output_dir()
    
    def _ensure_output_dir(self) -> None:
        """Create output directory if it doesn't exist."""
        if not os.path.exists(self.config.output_dir):
            os.makedirs(self.config.output_dir)
            logger.info(f"Created output directory: {self.config.output_dir}")
    
    def _sanitize_filename(self, title: str) -> str:
        """
        Convert title to a safe filename.
        
        Args:
            title: Blog title
            
        Returns:
            Sanitized filename (without extension)
        """
        # Convert to lowercase and replace spaces with hyphens
        filename = title.lower().strip()
        
        # Remove or replace unsafe characters
        filename = re.sub(r'[^\w\s-]', '', filename)
        filename = re.sub(r'[\s_]+', '-', filename)
        filename = re.sub(r'-+', '-', filename)
        filename = filename.strip('-')
        
        # Limit length
        if len(filename) > 50:
            filename = filename[:50].rsplit('-', 1)[0]
        
        return filename
    
    def _generate_markdown(self, blog: BlogPost) -> str:
        """
        Generate Markdown content for a blog post.
        
        Args:
            blog: BlogPost object
            
        Returns:
            Markdown formatted string
        """
        lines = []
        
        # Add metadata header (YAML front matter)
        if self.config.include_metadata:
            lines.extend([
                "---",
                f"title: \"{blog.title}\"",
                f"date: {blog.generated_at.strftime('%Y-%m-%d')}",
                f"category: {blog.book.category}",
                f"keywords: [{', '.join(blog.keywords.selected_keywords)}]",
                f"word_count: {blog.word_count}",
                f"rating: {blog.book.rating}/5",
                f"price: £{blog.book.price:.2f}",
                "---",
                ""
            ])
        
        # Title
        lines.extend([
            f"# {blog.title}",
            ""
        ])
        
        # Meta info box
        lines.extend([
            f"> **Category:** {blog.book.category} | **Rating:** {'⭐' * blog.book.rating} | **Price:** £{blog.book.price:.2f}",
            ""
        ])
        
        # Main content
        lines.extend([
            blog.content,
            ""
        ])
        
        # Keywords section
        lines.extend([
            "---",
            "",
            "**Related Searches:** " + " • ".join(blog.keywords.selected_keywords),
            "",
        ])
        
        # Source link
        lines.extend([
            f"*[View Book Details]({blog.book.url})*",
            ""
        ])
        
        return '\n'.join(lines)
    
    def _generate_html(self, blog: BlogPost) -> str:
        """
        Generate HTML content for a blog post.
        
        Args:
            blog: BlogPost object
            
        Returns:
            HTML formatted string
        """
        # Escape HTML special characters in content
        content_html = blog.content.replace('&', '&amp;')
        content_html = content_html.replace('<', '&lt;')
        content_html = content_html.replace('>', '&gt;')
        
        # Convert paragraphs
        paragraphs = content_html.split('\n\n')
        content_html = '\n'.join(f'<p>{p.strip()}</p>' for p in paragraphs if p.strip())
        
        # Generate star rating HTML
        stars_html = ''.join(['<span class="star filled">★</span>' for _ in range(blog.book.rating)])
        stars_html += ''.join(['<span class="star">☆</span>' for _ in range(5 - blog.book.rating)])
        
        # Keywords meta tag
        keywords_meta = ', '.join(blog.keywords.selected_keywords)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{blog.content[:150]}...">
    <meta name="keywords" content="{keywords_meta}">
    <meta name="author" content="SEO Blog Generator">
    <meta property="og:title" content="{blog.title}">
    <meta property="og:type" content="article">
    <title>{blog.title}</title>
    <style>
        :root {{
            --primary-color: #2c3e50;
            --accent-color: #3498db;
            --star-color: #f39c12;
            --background: #f9f9f9;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background: var(--background);
            color: var(--primary-color);
        }}
        
        article {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: var(--primary-color);
            margin-bottom: 10px;
            font-size: 2em;
        }}
        
        .meta {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 1px solid #eee;
        }}
        
        .star {{ font-size: 1.2em; }}
        .star.filled {{ color: var(--star-color); }}
        
        .content p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        
        .keywords {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}
        
        .keyword-tag {{
            display: inline-block;
            background: var(--accent-color);
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            margin: 3px;
        }}
        
        .cta {{
            margin-top: 25px;
            text-align: center;
        }}
        
        .cta a {{
            display: inline-block;
            background: var(--accent-color);
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            transition: background 0.3s;
        }}
        
        .cta a:hover {{
            background: #2980b9;
        }}
        
        footer {{
            margin-top: 30px;
            text-align: center;
            color: #888;
            font-size: 0.85em;
        }}
    </style>
</head>
<body>
    <article>
        <header>
            <h1>{blog.title}</h1>
            <div class="meta">
                <span class="category">📚 {blog.book.category}</span> | 
                <span class="rating">{stars_html}</span> | 
                <span class="price">💷 £{blog.book.price:.2f}</span> |
                <span class="date">📅 {blog.generated_at.strftime('%B %d, %Y')}</span>
            </div>
        </header>
        
        <div class="content">
            {content_html}
        </div>
        
        <div class="keywords">
            <strong>Related Searches:</strong><br>
            {''.join(f'<span class="keyword-tag">{kw}</span>' for kw in blog.keywords.selected_keywords)}
        </div>
        
        <div class="cta">
            <a href="{blog.book.url}" target="_blank" rel="noopener">View Book Details →</a>
        </div>
    </article>
    
    <footer>
        <p>Generated by SEO Blog Creation Tool | Word Count: {blog.word_count}</p>
    </footer>
</body>
</html>"""
        
        return html
    
    def export(self, blog: BlogPost, format: Optional[str] = None) -> ExportedContent:
        """
        Export a blog post to file.
        
        Args:
            blog: BlogPost to export
            format: Output format ('markdown' or 'html'), uses config default if not specified
            
        Returns:
            ExportedContent with file path
        """
        format = format or self.config.format
        
        # Generate filename
        base_filename = self._sanitize_filename(blog.title)
        extension = '.md' if format == 'markdown' else '.html'
        filename = f"{base_filename}{extension}"
        filepath = os.path.join(self.config.output_dir, filename)
        
        # Generate content
        if format == 'markdown':
            content = self._generate_markdown(blog)
        else:
            content = self._generate_html(blog)
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Exported blog to: {filepath}")
        
        return ExportedContent(
            filepath=filepath,
            format=format,
            blog_post=blog
        )
    
    def export_all(
        self,
        blogs: List[BlogPost],
        format: Optional[str] = None
    ) -> List[ExportedContent]:
        """
        Export multiple blog posts.
        
        Args:
            blogs: List of BlogPost objects
            format: Output format
            
        Returns:
            List of ExportedContent objects
        """
        exported = []
        for blog in blogs:
            try:
                result = self.export(blog, format)
                exported.append(result)
            except Exception as e:
                logger.error(f"Failed to export blog '{blog.title}': {e}")
        
        return exported


# Convenience function
def export_blog(
    blog: BlogPost,
    output_dir: str = "output",
    format: str = "markdown"
) -> ExportedContent:
    """
    Quick function to export a blog post.
    
    Args:
        blog: BlogPost to export
        output_dir: Output directory path
        format: Output format ('markdown' or 'html')
        
    Returns:
        ExportedContent object
    """
    config = ExporterConfig(output_dir=output_dir, format=format)
    exporter = ContentExporter(config)
    return exporter.export(blog)


if __name__ == "__main__":
    # Test the exporter with mock data
    from models import Book, ProcessedBook, SEOKeywords
    
    print("Testing Content Exporter...")
    
    # Create mock data
    book = Book(
        title="Test Book Title",
        price=19.99,
        rating=4,
        category="Fiction",
        url="https://books.toscrape.com/test-book"
    )
    
    processed = ProcessedBook(
        book=book,
        clean_title="Test Book Title",
        price_tier="mid-range",
        rating_label="Highly Rated",
        target_audience="fiction readers"
    )
    
    keywords = SEOKeywords(
        all_keywords=["test book", "fiction book", "best fiction"],
        selected_keywords=["test book", "fiction book", "best fiction"],
        primary_keyword="test book"
    )
    
    blog = BlogPost(
        title="Test Book Title: A Must-Read for Fiction Lovers",
        content="This is a test blog post content. It demonstrates the export functionality of the SEO Blog Creation Tool. The content would normally be generated by the Cohere API and would be 150-200 words long with proper SEO optimization.",
        keywords=keywords,
        book=processed
    )
    
    # Export to both formats
    exporter = ContentExporter()
    
    md_result = exporter.export(blog, format='markdown')
    print(f"Markdown exported to: {md_result.filepath}")
    
    html_result = exporter.export(blog, format='html')
    print(f"HTML exported to: {html_result.filepath}")
