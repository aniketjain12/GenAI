"""
AI Video Generation Tool
========================
Main entry point for the application.

This tool generates short videos by:
1. Fetching trending news on a topic (via RSS feeds)
2. Generating a script using Gemini API
3. Creating a video with text overlays using Gemini Veo / MoviePy

Usage:
    python main.py --topic "artificial intelligence" --duration 30
"""
import argparse
import os
import sys
from datetime import datetime

from config import DEFAULT_VIDEO_DURATION, MIN_VIDEO_DURATION, MAX_VIDEO_DURATION, OUTPUT_DIR
from news_fetcher import fetch_news, format_news_for_script
from script_generator import generate_script
from video_generator import generate_video


def print_banner():
    """Print application banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║           AI VIDEO GENERATION TOOL                        ║
    ║     Trending News → Script → Video (30-60 seconds)        ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def validate_duration(duration: int) -> int:
    """Validate and adjust video duration to acceptable range."""
    if duration < MIN_VIDEO_DURATION:
        print(f"Duration too short. Setting to minimum: {MIN_VIDEO_DURATION}s")
        return MIN_VIDEO_DURATION
    if duration > MAX_VIDEO_DURATION:
        print(f"Duration too long. Setting to maximum: {MAX_VIDEO_DURATION}s")
        return MAX_VIDEO_DURATION
    return duration


def run_pipeline(topic: str, duration: int = DEFAULT_VIDEO_DURATION) -> str:
    """
    Run the complete video generation pipeline.
    
    Pipeline:
        User Input → Fetch News → Generate Script → Generate Video → Output MP4
    
    Args:
        topic: The topic/keyword to create video about
        duration: Target video duration in seconds (30-60)
        
    Returns:
        Path to the generated video file
    """
    print_banner()
    
    # Validate inputs
    if not topic or not topic.strip():
        raise ValueError("Topic is required and cannot be empty.")
    
    topic = topic.strip()
    duration = validate_duration(duration)
    
    print(f"\n📌 Topic: {topic}")
    print(f"⏱️  Duration: {duration} seconds")
    print("-" * 50)
    
    # Step 1: Fetch News
    print("\n[1/3] 📰 Fetching trending news...")
    articles = fetch_news(topic, max_articles=5)
    
    if not articles:
        print("⚠️  No news articles found. Using topic description only.")
        news_content = f"Topic: {topic} - Create an informative explainer video."
    else:
        print(f"    ✓ Found {len(articles)} articles")
        news_content = format_news_for_script(articles)
    
    # Step 2: Generate Script
    print("\n[2/3] ✍️  Generating script with Cohere...")
    try:
        script_data = generate_script(topic, news_content, duration)
        print(f"    ✓ Script generated with {len(script_data['segments'])} segments")
        
        # Display script preview
        print("\n    Script Preview:")
        print("    " + "-" * 40)
        for i, seg in enumerate(script_data['segments'], 1):
            print(f"    Segment {i}: {seg.get('title', 'N/A')}")
            print(f"      Text: {seg.get('text_overlay', 'N/A')[:50]}...")
    except Exception as e:
        print(f"    ✗ Error generating script: {e}")
        raise
    
    # Step 3: Generate Video
    print("\n[3/3] 🎬 Generating video...")
    try:
        video_path = generate_video(script_data)
        print(f"    ✓ Video generated successfully!")
    except Exception as e:
        print(f"    ✗ Error generating video: {e}")
        raise
    
    # Summary
    print("\n" + "=" * 50)
    print("✅ VIDEO GENERATION COMPLETE!")
    print("=" * 50)
    print(f"\n📁 Output: {video_path}")
    print(f"📊 Duration: {duration} seconds")
    print(f"📝 Segments: {len(script_data['segments'])}")
    
    # Save script as text file for reference
    script_path = video_path.replace('.mp4', '_script.txt')
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(f"Topic: {topic}\n")
        f.write(f"Duration: {duration} seconds\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write("=" * 50 + "\n\n")
        f.write(script_data['raw_script'])
    print(f"📄 Script saved: {script_path}")
    
    return video_path


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="AI Video Generation Tool - Create news videos from trending topics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py --topic "artificial intelligence"
    python main.py --topic "climate change" --duration 45
    python main.py -t "space exploration" -d 60
        """
    )
    
    parser.add_argument(
        '-t', '--topic',
        type=str,
        required=True,
        help='Topic or keyword for the video (required)'
    )
    
    parser.add_argument(
        '-d', '--duration',
        type=int,
        default=DEFAULT_VIDEO_DURATION,
        help=f'Video duration in seconds (default: {DEFAULT_VIDEO_DURATION}, range: {MIN_VIDEO_DURATION}-{MAX_VIDEO_DURATION})'
    )
    
    args = parser.parse_args()
    
    try:
        video_path = run_pipeline(args.topic, args.duration)
        print(f"\n🎉 Success! Your video is ready: {video_path}\n")
        return 0
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
