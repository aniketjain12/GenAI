"""
Video Generator Module
Generates videos using PIL for image creation and OpenCV for video encoding.
Simple and reliable - no paid API required.
"""
import os
import time
import cv2
import numpy as np
from typing import Dict, List
from PIL import Image, ImageDraw, ImageFont
from config import OUTPUT_DIR


def get_font(size: int, bold: bool = False):
    """Get a font, with fallbacks for different systems."""
    font_options = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    
    if bold:
        font_options = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
        ] + font_options
    
    for font_path in font_options:
        try:
            return ImageFont.truetype(font_path, size)
        except (OSError, IOError):
            continue
    
    try:
        return ImageFont.load_default()
    except:
        return None


def wrap_text(text: str, font, max_width: int, draw: ImageDraw) -> List[str]:
    """Wrap text to fit within a given width."""
    if not font or not text:
        return [text] if text else [""]
    
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        try:
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
        except:
            width = len(test_line) * 10
        
        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines if lines else [text]


def create_segment_frame(
    segment: Dict,
    topic: str,
    segment_num: int,
    total_segments: int,
    width: int = 1280,
    height: int = 720
) -> np.ndarray:
    """Create a single frame image for a segment."""
    
    # Color scheme (RGB for PIL)
    colors = [
        (26, 26, 46),    # Dark blue
        (22, 33, 62),    # Navy
        (15, 52, 96),    # Deep blue
        (52, 73, 94),    # Steel blue
        (44, 62, 80),    # Dark slate
        (30, 39, 46),    # Charcoal
    ]
    
    bg_color = colors[segment_num % len(colors)]
    
    # Create image with PIL
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Get fonts
    title_font = get_font(55, bold=True)
    overlay_font = get_font(42)
    narration_font = get_font(24)
    small_font = get_font(22)
    
    # Get segment content
    title = segment.get('title', f'Scene {segment_num + 1}').upper()
    text_overlay = segment.get('text_overlay', '')
    narration = segment.get('narration', '')
    
    if len(narration) > 150:
        narration = narration[:150] + "..."
    
    # Draw title at top
    title_lines = wrap_text(title, title_font, width - 100, draw)
    y_pos = 80
    for line in title_lines:
        if title_font:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]
        else:
            text_width = len(line) * 20
            line_height = 50
        x_pos = (width - text_width) // 2
        draw.text((x_pos, y_pos), line, fill='white', font=title_font)
        y_pos += line_height + 10
    
    # Draw main text overlay in center (gold color)
    if text_overlay:
        overlay_lines = wrap_text(text_overlay, overlay_font, width - 150, draw)
        total_overlay_height = len(overlay_lines) * 50
        y_pos = (height - total_overlay_height) // 2
        
        for line in overlay_lines:
            if overlay_font:
                bbox = draw.textbbox((0, 0), line, font=overlay_font)
                text_width = bbox[2] - bbox[0]
            else:
                text_width = len(line) * 15
            x_pos = (width - text_width) // 2
            draw.text((x_pos, y_pos), line, fill=(255, 215, 0), font=overlay_font)
            y_pos += 50
    
    # Draw narration at bottom
    if narration:
        narration_lines = wrap_text(narration, narration_font, width - 100, draw)
        y_pos = height - 50 - (len(narration_lines) * 30)
        
        for line in narration_lines:
            if narration_font:
                bbox = draw.textbbox((0, 0), line, font=narration_font)
                text_width = bbox[2] - bbox[0]
            else:
                text_width = len(line) * 10
            x_pos = (width - text_width) // 2
            draw.text((x_pos, y_pos), line, fill=(200, 200, 200), font=narration_font)
            y_pos += 30
    
    # Draw topic watermark (top-left)
    topic_text = f"# {topic.upper()}"
    draw.text((30, 25), topic_text, fill=(136, 136, 136), font=small_font)
    
    # Draw progress indicator (top-right)
    progress_text = f"{segment_num + 1}/{total_segments}"
    if small_font:
        try:
            bbox = draw.textbbox((0, 0), progress_text, font=small_font)
            text_width = bbox[2] - bbox[0]
        except:
            text_width = 40
    else:
        text_width = 40
    draw.text((width - text_width - 30, 25), progress_text, fill=(136, 136, 136), font=small_font)
    
    # Convert PIL image to OpenCV format (BGR)
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    return frame


def generate_video(script_data: Dict, filename: str = None) -> str:
    """
    Generate video from script data using PIL and OpenCV.
    
    Args:
        script_data: Script data with segments
        filename: Optional custom filename
        
    Returns:
        Path to the generated video file
    """
    segments = script_data.get('segments', [])
    total_duration = script_data.get('duration', 30)
    topic = script_data.get('topic', 'News')
    
    if not segments:
        raise ValueError("No segments found in script data")
    
    # Generate filename if not provided
    if not filename:
        timestamp = int(time.time())
        topic_slug = topic.replace(' ', '_')[:20]
        filename = f"{topic_slug}_{timestamp}.mp4"
    
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    # Video settings
    width, height = 1280, 720
    fps = 24
    
    # Calculate frames per segment
    segment_duration = total_duration / len(segments)
    frames_per_segment = int(segment_duration * fps)
    
    print(f"Creating video: {len(segments)} segments, {segment_duration:.1f}s each")
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    if not video_writer.isOpened():
        raise RuntimeError(f"Failed to create video writer for {output_path}")
    
    try:
        for i, segment in enumerate(segments):
            print(f"  Creating segment {i+1}/{len(segments)}: {segment.get('title', 'N/A')[:30]}")
            
            # Create the frame for this segment
            frame = create_segment_frame(
                segment=segment,
                topic=topic,
                segment_num=i,
                total_segments=len(segments),
                width=width,
                height=height
            )
            
            # Write the same frame multiple times for the segment duration
            for _ in range(frames_per_segment):
                video_writer.write(frame)
        
        print(f"  Finalizing video...")
        
    finally:
        video_writer.release()
    
    # Verify output
    if os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  Video saved: {size_mb:.2f} MB")
    
    return output_path


if __name__ == "__main__":
    # Test video generation
    test_script = {
        "topic": "AI Technology",
        "duration": 30,
        "segments": [
            {
                "title": "The AI Revolution",
                "narration": "Artificial intelligence is transforming every industry worldwide.",
                "text_overlay": "AI is changing the world"
            },
            {
                "title": "Key Developments",
                "narration": "Major tech companies are investing billions in AI research.",
                "text_overlay": "Billions invested in AI"
            },
            {
                "title": "The Future",
                "narration": "Experts predict AI will revolutionize how we work and live.",
                "text_overlay": "The future is AI-powered"
            }
        ]
    }
    
    result = generate_video(test_script)
    print(f"Video generated: {result}")
