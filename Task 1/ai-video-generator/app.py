"""
AI Video Generation Tool - Streamlit UI
A user-friendly interface for generating news videos from trending topics.
"""
import streamlit as st
import os
import time
from datetime import datetime

# Import our modules
from config import OUTPUT_DIR, MIN_VIDEO_DURATION, MAX_VIDEO_DURATION, DEFAULT_VIDEO_DURATION
from news_fetcher import fetch_news, format_news_for_script
from script_generator import generate_script
from video_generator import generate_video

# Page configuration
st.set_page_config(
    page_title="AI Video Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .step-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .success-card {
        background: #d4edda;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
    }
    .segment-card {
        background: #fff;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        border-radius: 8px;
    }
    .stButton>button:hover {
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if 'generated_video' not in st.session_state:
        st.session_state.generated_video = None
    if 'script_data' not in st.session_state:
        st.session_state.script_data = None
    if 'news_articles' not in st.session_state:
        st.session_state.news_articles = None
    if 'generation_complete' not in st.session_state:
        st.session_state.generation_complete = False


def display_header():
    """Display the main header."""
    st.markdown('<h1 class="main-header">🎬 AI Video Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform trending news into engaging video content</p>', unsafe_allow_html=True)


def display_sidebar():
    """Display sidebar with inputs and settings."""
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Topic input
        topic = st.text_input(
            "📰 Enter Topic/Keyword",
            placeholder="e.g., artificial intelligence, climate change",
            help="Enter a topic to generate a video about"
        )
        
        # Duration slider
        duration = st.slider(
            "⏱️ Video Duration (seconds)",
            min_value=MIN_VIDEO_DURATION,
            max_value=MAX_VIDEO_DURATION,
            value=DEFAULT_VIDEO_DURATION,
            step=5,
            help="Select the target duration for your video"
        )
        
        st.divider()
        
        # Generate button
        generate_btn = st.button("🚀 Generate Video", type="primary", use_container_width=True)
        
        st.divider()
        
        # Info section
        st.markdown("### 📋 How it works")
        st.markdown("""
        1. **Fetch News** - Gets trending articles on your topic
        2. **Generate Script** - AI creates a video script
        3. **Create Video** - Generates MP4 with text overlays
        """)
        
        st.divider()
        
        # Architecture info
        with st.expander("🔧 Technical Details"):
            st.markdown("""
            - **News Source**: Google News RSS
            - **Script AI**: Cohere API
            - **Video**: PIL + OpenCV
            - **Output**: MP4 (1280x720)
            """)
        
        return topic, duration, generate_btn


def display_news_articles(articles):
    """Display fetched news articles."""
    st.subheader("📰 Fetched News Articles")
    
    if not articles:
        st.warning("No articles found for this topic.")
        return
    
    for i, article in enumerate(articles, 1):
        with st.expander(f"Article {i}: {article.get('title', 'No title')[:60]}..."):
            st.write(f"**Title:** {article.get('title', 'N/A')}")
            #if article.get('summary'):
            #    st.write(f"**Summary:** {article.get('summary', 'N/A')[:200]}...")
            if article.get('published'):
                st.write(f"**Published:** {article.get('published', 'N/A')}")


def display_script(script_data):
    """Display the generated script."""
    st.subheader("📝 Generated Script")
    
    segments = script_data.get('segments', [])
    
    if not segments:
        st.warning("No segments in script.")
        return
    
    cols = st.columns(min(len(segments), 3))
    
    for i, segment in enumerate(segments):
        col_idx = i % 3
        with cols[col_idx]:
            st.markdown(f"""
            <div class="segment-card">
                <h4>🎬 Segment {i+1}</h4>
                <p><strong>Title:</strong> {segment.get('title', 'N/A')}</p>
                <p><strong>Overlay:</strong> {segment.get('text_overlay', 'N/A')}</p>
                <p style="font-size: 0.9em; color: #666;"><strong>Narration:</strong> {segment.get('narration', 'N/A')[:100]}...</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Show raw script in expander
    with st.expander("📄 View Full Script"):
        st.text(script_data.get('raw_script', 'No raw script available'))


def display_video(video_path):
    """Display the generated video."""
    st.subheader("🎥 Generated Video")
    
    if os.path.exists(video_path):
        # Display video
        video_file = open(video_path, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
        
        # Video info
        file_size = os.path.getsize(video_path) / (1024 * 1024)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("File Size", f"{file_size:.2f} MB")
        with col2:
            st.metric("Resolution", "1280x720")
        with col3:
            st.metric("Format", "MP4")
        
        # Download button
        st.download_button(
            label="📥 Download Video",
            data=video_bytes,
            file_name=os.path.basename(video_path),
            mime="video/mp4",
            use_container_width=True
        )
    else:
        st.error("Video file not found!")


def generate_video_pipeline(topic: str, duration: int):
    """Run the complete video generation pipeline with progress updates."""
    
    # Create progress container
    progress_container = st.container()
    
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Fetch News (0-30%)
            status_text.markdown("### 📰 Step 1/3: Fetching trending news...")
            progress_bar.progress(10)
            
            articles = fetch_news(topic, max_articles=5)
            st.session_state.news_articles = articles
            
            if articles:
                st.success(f"✓ Found {len(articles)} news articles")
            else:
                st.warning("No articles found. Using topic description.")
            
            news_content = format_news_for_script(articles) if articles else f"Topic: {topic}"
            progress_bar.progress(30)
            
            # Step 2: Generate Script (30-60%)
            status_text.markdown("### ✍️ Step 2/3: Generating script with AI...")
            progress_bar.progress(40)
            
            script_data = generate_script(topic, news_content, duration)
            st.session_state.script_data = script_data
            
            num_segments = len(script_data.get('segments', []))
            st.success(f"✓ Script generated with {num_segments} segments")
            progress_bar.progress(60)
            
            # Step 3: Generate Video (60-100%)
            status_text.markdown("### 🎬 Step 3/3: Creating video...")
            progress_bar.progress(70)
            
            video_path = generate_video(script_data)
            st.session_state.generated_video = video_path
            
            progress_bar.progress(100)
            status_text.markdown("### ✅ Video generation complete!")
            
            st.session_state.generation_complete = True
            
            return True
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            return False


def display_previous_videos():
    """Display list of previously generated videos."""
    st.subheader("📂 Previous Videos")
    
    if os.path.exists(OUTPUT_DIR):
        videos = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.mp4')]
        
        if videos:
            # Sort by modification time (newest first)
            videos.sort(key=lambda x: os.path.getmtime(os.path.join(OUTPUT_DIR, x)), reverse=True)
            
            for video in videos[:5]:  # Show last 5 videos
                video_path = os.path.join(OUTPUT_DIR, video)
                file_size = os.path.getsize(video_path) / (1024 * 1024)
                mod_time = datetime.fromtimestamp(os.path.getmtime(video_path))
                
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"📹 {video}")
                with col2:
                    st.write(f"{file_size:.1f} MB")
                with col3:
                    if st.button("View", key=f"view_{video}"):
                        st.session_state.generated_video = video_path
                        st.session_state.generation_complete = True
        else:
            st.info("No videos generated yet.")
    else:
        st.info("Output directory not found.")


def main():
    """Main application entry point."""
    init_session_state()
    display_header()
    
    # Sidebar inputs
    topic, duration, generate_btn = display_sidebar()
    
    # Main content area
    if generate_btn:
        if not topic or not topic.strip():
            st.error("⚠️ Please enter a topic!")
        else:
            # Reset state for new generation
            st.session_state.generation_complete = False
            st.session_state.generated_video = None
            st.session_state.script_data = None
            st.session_state.news_articles = None
            
            # Run pipeline
            success = generate_video_pipeline(topic.strip(), duration)
    
    # Display results if generation is complete
    if st.session_state.generation_complete:
        st.divider()
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["🎥 Video", "📝 Script", "📰 News", "📂 History"])
        
        with tab1:
            if st.session_state.generated_video:
                display_video(st.session_state.generated_video)
        
        with tab2:
            if st.session_state.script_data:
                display_script(st.session_state.script_data)
        
        with tab3:
            if st.session_state.news_articles:
                display_news_articles(st.session_state.news_articles)
        
        with tab4:
            display_previous_videos()
    
    else:
        # Show welcome message when no video is generated
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 10px; margin: 2rem 0;">
            <h2>👋 Welcome to AI Video Generator</h2>
            <p style="font-size: 1.2rem; color: #666;">
                Enter a topic in the sidebar and click "Generate Video" to create an AI-powered news video.
            </p>
            <p style="color: #999;">
                The tool will fetch trending news, generate a script, and create a 30-60 second video with text overlays.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show example topics
        st.markdown("### 💡 Example Topics")
        example_cols = st.columns(4)
        examples = ["artificial intelligence", "climate change", "space exploration", "cryptocurrency"]
        
        for i, example in enumerate(examples):
            with example_cols[i]:
                st.info(f"📌 {example}")


if __name__ == "__main__":
    main()
