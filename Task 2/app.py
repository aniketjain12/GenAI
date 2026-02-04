"""
SEO Blog Creation Tool - Streamlit Frontend

A user-friendly web interface for generating SEO-optimized blog posts
from scraped e-commerce product data.
"""

import streamlit as st
import os
import time
from datetime import datetime
from typing import List, Optional

# Import pipeline components
from config import PipelineConfig, ScraperConfig, CohereConfig, SEOConfig, ExporterConfig
from models import Book, ProcessedBook, SEOKeywords, BlogPost, ExportedContent
from scraper import ProductScraper
from preprocessor import ProductPreprocessor
from keyword_generator import SEOKeywordGenerator
from blog_generator import SEOBlogGenerator
from exporter import ContentExporter
from publisher import MultiPublisher, MediumPublisher, WordPressPublisher, DevToPublisher

# Page configuration
st.set_page_config(
    page_title="SEO Blog Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #e7f3ff;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .book-card {
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
    .metric-card {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 0.5rem;
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if 'scraped_books' not in st.session_state:
        st.session_state.scraped_books = []
    if 'processed_books' not in st.session_state:
        st.session_state.processed_books = []
    if 'generated_blogs' not in st.session_state:
        st.session_state.generated_blogs = []
    if 'exported_files' not in st.session_state:
        st.session_state.exported_files = []
    if 'pipeline_complete' not in st.session_state:
        st.session_state.pipeline_complete = False


def render_sidebar():
    """Render the sidebar with configuration options."""
    st.sidebar.markdown("## ⚙️ Configuration")
    
    # API Key
    st.sidebar.markdown("### 🔑 API Settings")
    api_key = st.sidebar.text_input(
        "Cohere API Key",
        value=os.getenv("COHERE_API_KEY", ""),
        type="password",
        help="Get your API key from https://dashboard.cohere.com/api-keys"
    )
    
    # Scraper settings
    st.sidebar.markdown("### 🌐 Scraper Settings")
    
    data_source = st.sidebar.selectbox(
        "Data Source",
        options=["Books to Scrape", "Custom URL (Coming Soon)"],
        index=0,
        help="Select the e-commerce source to scrape"
    )
    
    num_books = st.sidebar.slider(
        "Number of Books",
        min_value=1,
        max_value=20,
        value=5,
        help="Number of books to scrape and process"
    )
    
    min_rating = st.sidebar.slider(
        "Minimum Rating",
        min_value=1,
        max_value=5,
        value=4,
        help="Only include books with this rating or higher"
    )
    
    # SEO settings
    st.sidebar.markdown("### 🎯 SEO Settings")
    
    num_keywords = st.sidebar.slider(
        "Keywords to Generate",
        min_value=3,
        max_value=10,
        value=5,
        help="Number of SEO keywords to generate per book"
    )
    
    keywords_to_use = st.sidebar.slider(
        "Keywords to Use",
        min_value=2,
        max_value=6,
        value=4,
        help="Number of top keywords to include in blog"
    )
    
    # Export settings
    st.sidebar.markdown("### 📤 Export Settings")
    
    export_format = st.sidebar.selectbox(
        "Export Format",
        options=["markdown", "html", "both"],
        index=0,
        help="Format for exported blog posts"
    )
    
    output_dir = st.sidebar.text_input(
        "Output Directory",
        value="output",
        help="Directory to save generated blogs"
    )
    
    # Advanced settings
    with st.sidebar.expander("🔧 Advanced Settings"):
        model = st.selectbox(
            "Cohere Model",
            options=["command-r-plus-08-2024", "command-a-03-2025", "command-r7b-12-2024"],
            index=0,
            help="AI model to use for generation"
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher = more creative, Lower = more focused"
        )
        
        request_delay = st.slider(
            "API Request Delay (seconds)",
            min_value=0.0,
            max_value=5.0,
            value=1.0,
            step=0.5,
            help="Delay between API calls (for rate limiting)"
        )
    
    return {
        'api_key': api_key,
        'data_source': data_source,
        'num_books': num_books,
        'min_rating': min_rating,
        'num_keywords': num_keywords,
        'keywords_to_use': keywords_to_use,
        'export_format': export_format,
        'output_dir': output_dir,
        'model': model,
        'temperature': temperature,
        'request_delay': request_delay
    }


def create_config(settings: dict) -> PipelineConfig:
    """Create pipeline configuration from settings."""
    return PipelineConfig(
        scraper=ScraperConfig(
            max_books=settings['num_books'],
            min_rating=settings['min_rating']
        ),
        cohere=CohereConfig(
            api_key=settings['api_key'],
            model=settings['model'],
            temperature=settings['temperature']
        ),
        seo=SEOConfig(
            num_keywords_to_generate=settings['num_keywords'],
            num_keywords_to_use=settings['keywords_to_use']
        ),
        exporter=ExporterConfig(
            output_dir=settings['output_dir'],
            format=settings['export_format'] if settings['export_format'] != 'both' else 'markdown'
        )
    )


def run_scraper(config: PipelineConfig, progress_bar, status_text) -> List[Book]:
    """Run the scraping stage."""
    status_text.text("🌐 Scraping products from website...")
    scraper = ProductScraper(config.scraper)
    books = scraper.scrape_top_rated(config.scraper.max_books)
    progress_bar.progress(25)
    return books


def run_preprocessor(books: List[Book], progress_bar, status_text) -> List[ProcessedBook]:
    """Run the preprocessing stage."""
    status_text.text("🔧 Preprocessing book data...")
    preprocessor = ProductPreprocessor()
    processed = preprocessor.process_books(books)
    progress_bar.progress(40)
    return processed


def run_keyword_generation(
    processed_books: List[ProcessedBook],
    config: PipelineConfig,
    delay: float,
    progress_bar,
    status_text
) -> List[tuple]:
    """Run keyword generation for all books."""
    generator = SEOKeywordGenerator(config.cohere, config.seo)
    results = []
    
    total = len(processed_books)
    for i, book in enumerate(processed_books):
        status_text.text(f"🔑 Generating keywords for: {book.clean_title[:40]}...")
        keywords = generator.generate_keywords(book)
        results.append((book, keywords))
        progress_bar.progress(40 + int(20 * (i + 1) / total))
        if delay > 0 and i < total - 1:
            time.sleep(delay)
    
    return results


def run_blog_generation(
    book_keywords: List[tuple],
    config: PipelineConfig,
    delay: float,
    progress_bar,
    status_text
) -> List[BlogPost]:
    """Run blog generation for all books."""
    generator = SEOBlogGenerator(config.cohere, config.seo)
    blogs = []
    
    total = len(book_keywords)
    for i, (book, keywords) in enumerate(book_keywords):
        status_text.text(f"✍️ Generating blog for: {book.clean_title[:40]}...")
        blog = generator.generate_blog(book, keywords)
        blogs.append(blog)
        progress_bar.progress(60 + int(25 * (i + 1) / total))
        if delay > 0 and i < total - 1:
            time.sleep(delay)
    
    return blogs


def run_export(
    blogs: List[BlogPost],
    config: PipelineConfig,
    export_both: bool,
    progress_bar,
    status_text
) -> List[ExportedContent]:
    """Export blogs to files."""
    status_text.text("📤 Exporting blog posts...")
    exporter = ContentExporter(config.exporter)
    exported = exporter.export_all(blogs, 'markdown')
    
    if export_both:
        html_config = ExporterConfig(
            output_dir=config.exporter.output_dir,
            format='html'
        )
        html_exporter = ContentExporter(html_config)
        exported.extend(html_exporter.export_all(blogs, 'html'))
    
    progress_bar.progress(100)
    return exported


def display_book_card(book: ProcessedBook, index: int):
    """Display a book as a card."""
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{index}. {book.clean_title}**")
            st.caption(f"📚 {book.category} | {'⭐' * book.rating} | £{book.price:.2f}")
        with col2:
            st.markdown(f"<span style='color: green;'>{book.rating_label}</span>", unsafe_allow_html=True)
        st.markdown("---")


def display_blog_preview(blog: BlogPost, index: int):
    """Display a blog post preview."""
    with st.expander(f"📄 {blog.title}", expanded=index == 0):
        # Metadata
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Word Count", blog.word_count)
        with col2:
            st.metric("Keywords", len(blog.keywords.selected_keywords))
        with col3:
            st.metric("Rating", f"{blog.book.rating}/5")
        
        # Keywords
        st.markdown("**🔑 SEO Keywords:**")
        keyword_html = " ".join([f"`{kw}`" for kw in blog.keywords.selected_keywords])
        st.markdown(keyword_html)
        
        # Content preview
        st.markdown("**📝 Content:**")
        st.markdown(blog.content)
        
        # Link
        st.markdown(f"[View Book Details]({blog.book.url})")


def main():
    """Main application entry point."""
    init_session_state()
    
    # Header
    st.markdown('<p class="main-header">📝 SEO Blog Generator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Generate SEO-optimized blog posts from product data automatically</p>', unsafe_allow_html=True)
    
    # Sidebar configuration
    settings = render_sidebar()
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚀 Generate", "📚 Scraped Books", "📄 Generated Blogs", "📥 Exported Files", "🌐 Publish"])
    
    with tab1:
        st.markdown("### Start Generation Pipeline")
        
        # Validation
        if not settings['api_key']:
            st.warning("⚠️ Please enter your Cohere API key in the sidebar to continue.")
            st.info("Get your free API key at: https://dashboard.cohere.com/api-keys")
            st.stop()
        
        # Pipeline overview
        st.markdown("""
        <div class="info-box">
            <strong>Pipeline Steps:</strong><br>
            1️⃣ Scrape top-rated books from website<br>
            2️⃣ Preprocess and enrich book data<br>
            3️⃣ Generate SEO keywords using AI<br>
            4️⃣ Generate optimized blog posts<br>
            5️⃣ Export to Markdown/HTML files
        </div>
        """, unsafe_allow_html=True)
        
        # Settings summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Books to Process", settings['num_books'])
        with col2:
            st.metric("Min Rating", f"{settings['min_rating']}⭐")
        with col3:
            st.metric("Keywords/Book", settings['num_keywords'])
        with col4:
            st.metric("Export Format", settings['export_format'].upper())
        
        st.markdown("---")
        
        # Generate button
        if st.button("🚀 Start Generation", type="primary", use_container_width=True):
            config = create_config(settings)
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Stage 1: Scrape
                st.session_state.scraped_books = run_scraper(config, progress_bar, status_text)
                
                if not st.session_state.scraped_books:
                    st.error("❌ No books were scraped. Please check your internet connection.")
                    st.stop()
                
                # Stage 2: Preprocess
                st.session_state.processed_books = run_preprocessor(
                    st.session_state.scraped_books, progress_bar, status_text
                )
                
                # Stage 3: Keywords
                book_keywords = run_keyword_generation(
                    st.session_state.processed_books,
                    config,
                    settings['request_delay'],
                    progress_bar,
                    status_text
                )
                
                # Stage 4: Blogs
                st.session_state.generated_blogs = run_blog_generation(
                    book_keywords,
                    config,
                    settings['request_delay'],
                    progress_bar,
                    status_text
                )
                
                # Stage 5: Export
                export_both = settings['export_format'] == 'both'
                st.session_state.exported_files = run_export(
                    st.session_state.generated_blogs,
                    config,
                    export_both,
                    progress_bar,
                    status_text
                )
                
                st.session_state.pipeline_complete = True
                status_text.text("✅ Pipeline complete!")
                
                # Success message
                st.markdown(f"""
                <div class="success-box">
                    <strong>✅ Success!</strong><br>
                    Generated {len(st.session_state.generated_blogs)} blog posts.<br>
                    Exported to: <code>{os.path.abspath(settings['output_dir'])}</code>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Pipeline failed: {str(e)}")
                raise e
    
    with tab2:
        st.markdown("### 📚 Scraped Books")
        
        if st.session_state.processed_books:
            st.success(f"Found {len(st.session_state.processed_books)} books")
            
            for i, book in enumerate(st.session_state.processed_books, 1):
                display_book_card(book, i)
        else:
            st.info("No books scraped yet. Click 'Start Generation' to begin.")
    
    with tab3:
        st.markdown("### 📄 Generated Blog Posts")
        
        if st.session_state.generated_blogs:
            st.success(f"Generated {len(st.session_state.generated_blogs)} blog posts")
            
            # Statistics
            total_words = sum(b.word_count for b in st.session_state.generated_blogs)
            avg_words = total_words // len(st.session_state.generated_blogs)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Blogs", len(st.session_state.generated_blogs))
            with col2:
                st.metric("Total Words", total_words)
            with col3:
                st.metric("Avg Words/Blog", avg_words)
            
            st.markdown("---")
            
            for i, blog in enumerate(st.session_state.generated_blogs):
                display_blog_preview(blog, i)
        else:
            st.info("No blogs generated yet. Click 'Start Generation' to begin.")
    
    with tab4:
        st.markdown("### 📥 Exported Files")
        
        if st.session_state.exported_files:
            st.success(f"Exported {len(st.session_state.exported_files)} files")
            
            for export in st.session_state.exported_files:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.text(export.filepath)
                with col2:
                    st.caption(export.format.upper())
                with col3:
                    # Read file for download
                    try:
                        with open(export.filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        st.download_button(
                            "⬇️",
                            data=content,
                            file_name=os.path.basename(export.filepath),
                            mime="text/markdown" if export.format == 'markdown' else "text/html",
                            key=export.filepath
                        )
                    except:
                        st.text("N/A")
            
            # Bulk download info
            st.markdown("---")
            st.info(f"📂 All files saved to: `{os.path.abspath(settings['output_dir'])}`")
        else:
            st.info("No files exported yet. Click 'Start Generation' to begin.")
    
    with tab5:
        st.markdown("### 🌐 Publish to Platforms")
        
        if not st.session_state.generated_blogs:
            st.info("Generate blogs first before publishing.")
        else:
            st.success(f"{len(st.session_state.generated_blogs)} blogs ready to publish")
            
            # Platform configuration
            st.markdown("#### Configure Publishing Platforms")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Medium**")
                medium_token = st.text_input(
                    "Medium Access Token",
                    type="password",
                    value=os.getenv("MEDIUM_ACCESS_TOKEN", ""),
                    help="Get from: Medium Settings → Integration Tokens"
                )
                
                st.markdown("**Dev.to**")
                devto_key = st.text_input(
                    "Dev.to API Key",
                    type="password",
                    value=os.getenv("DEVTO_API_KEY", ""),
                    help="Get from: Dev.to Settings → Account → DEV API Keys"
                )
            
            with col2:
                st.markdown("**WordPress**")
                wp_url = st.text_input(
                    "WordPress Site URL",
                    value=os.getenv("WORDPRESS_URL", ""),
                    placeholder="https://your-site.com"
                )
                wp_user = st.text_input(
                    "WordPress Username",
                    value=os.getenv("WORDPRESS_USERNAME", "")
                )
                wp_pass = st.text_input(
                    "WordPress App Password",
                    type="password",
                    value=os.getenv("WORDPRESS_APP_PASSWORD", ""),
                    help="Create in: WordPress → Users → Application Passwords"
                )
            
            st.markdown("---")
            
            # Select blogs to publish
            st.markdown("#### Select Blogs to Publish")
            blog_options = {blog.title: i for i, blog in enumerate(st.session_state.generated_blogs)}
            selected_blogs = st.multiselect(
                "Select blogs",
                options=list(blog_options.keys()),
                default=list(blog_options.keys())
            )
            
            # Platform selection
            st.markdown("#### Select Platforms")
            col1, col2, col3 = st.columns(3)
            with col1:
                pub_medium = st.checkbox("Medium", value=bool(medium_token))
            with col2:
                pub_devto = st.checkbox("Dev.to", value=bool(devto_key))
            with col3:
                pub_wordpress = st.checkbox("WordPress", value=bool(wp_url and wp_user and wp_pass))
            
            publish_as_draft = st.checkbox("Publish as Draft", value=True, help="Recommended: Review before making public")
            
            if st.button("🚀 Publish Selected Blogs", type="primary", use_container_width=True):
                if not selected_blogs:
                    st.warning("Please select at least one blog to publish.")
                elif not (pub_medium or pub_devto or pub_wordpress):
                    st.warning("Please select at least one platform.")
                else:
                    results = []
                    progress = st.progress(0)
                    status = st.empty()
                    
                    selected_indices = [blog_options[title] for title in selected_blogs]
                    total_ops = len(selected_indices) * (pub_medium + pub_devto + pub_wordpress)
                    current_op = 0
                    
                    for idx in selected_indices:
                        blog = st.session_state.generated_blogs[idx]
                        blog_results = {"title": blog.title, "platforms": {}}
                        
                        if pub_medium and medium_token:
                            status.text(f"Publishing to Medium: {blog.title[:40]}...")
                            publisher = MediumPublisher(medium_token)
                            result = publisher.publish(blog, "draft" if publish_as_draft else "public")
                            blog_results["platforms"]["medium"] = result
                            current_op += 1
                            progress.progress(current_op / total_ops)
                        
                        if pub_devto and devto_key:
                            status.text(f"Publishing to Dev.to: {blog.title[:40]}...")
                            publisher = DevToPublisher(devto_key)
                            result = publisher.publish(blog, not publish_as_draft)
                            blog_results["platforms"]["devto"] = result
                            current_op += 1
                            progress.progress(current_op / total_ops)
                        
                        if pub_wordpress and wp_url and wp_user and wp_pass:
                            status.text(f"Publishing to WordPress: {blog.title[:40]}...")
                            publisher = WordPressPublisher(wp_url, wp_user, wp_pass)
                            result = publisher.publish(blog, "draft" if publish_as_draft else "publish")
                            blog_results["platforms"]["wordpress"] = result
                            current_op += 1
                            progress.progress(current_op / total_ops)
                        
                        results.append(blog_results)
                        time.sleep(0.5)  # Rate limiting
                    
                    status.text("✅ Publishing complete!")
                    
                    # Display results
                    st.markdown("#### Publishing Results")
                    for result in results:
                        with st.expander(result["title"][:50] + "..."):
                            for platform, data in result["platforms"].items():
                                if data.get("status") == "success":
                                    st.success(f"✅ {platform.title()}: {data.get('url', 'Published')}")
                                else:
                                    st.error(f"❌ {platform.title()}: {data.get('error', 'Failed')}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #888;'>SEO Blog Generator v1.0 | Powered by Cohere AI</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
