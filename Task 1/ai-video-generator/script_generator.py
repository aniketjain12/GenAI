"""
Script Generator Module
Uses Cohere API to generate video scripts from news content.
"""
import time
import re
import cohere
from config import COHERE_API_KEY

# Initialize the Cohere client
client = None

def initialize_cohere():
    """Initialize Cohere API with the configured API key."""
    global client
    if not COHERE_API_KEY:
        raise ValueError("COHERE_API_KEY not set. Please set it in .env file.")
    client = cohere.ClientV2(api_key=COHERE_API_KEY)


def generate_script(topic: str, news_content: str, duration: int = 30) -> dict:
    """
    Generate a video script using Cohere API.
    
    Args:
        topic: The main topic/keyword
        news_content: Formatted news content for context
        duration: Target video duration in seconds (30-60)
        
    Returns:
        Dictionary containing script segments and metadata
    """
    initialize_cohere()
    
    # Calculate approximate word count for duration
    # Average speaking rate: ~150 words per minute = 2.5 words per second
    target_words = int(duration * 2.5)
    
    prompt = f"""You are a professional news video script writer. Create a short, engaging video script about "{topic}" based on the following recent news:

{news_content}

Requirements:
1. Script should be approximately {target_words} words (for a {duration}-second video)
2. Write in a news/explainer style - simple and informational
3. Break the script into exactly 4-6 segments (scenes)
4. Each segment should have:
   - A short title (2-4 words)
   - Narration text (for voice-over)
   - Text overlay suggestion (key phrase to display on screen, max 10 words)

Format your response EXACTLY like this:
SEGMENT 1:
TITLE: [short title]
NARRATION: [what the narrator says]
TEXT_OVERLAY: [key phrase for screen]

SEGMENT 2:
TITLE: [short title]
NARRATION: [what the narrator says]
TEXT_OVERLAY: [key phrase for screen]

(continue for all segments)

Make it engaging, factual, and suitable for social media. Start with a hook and end with a conclusion."""

    max_retries = 3
    # Updated model name - command-r-plus was deprecated
    models_to_try = ["command-a-03-2025", "command-r-plus-08-2024", "command-r-08-2024"]
    
    for model_name in models_to_try:
        for attempt in range(max_retries):
            try:
                print(f"    Using Cohere model: {model_name}")
                response = client.chat(
                    model=model_name,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                
                # Parse the response into segments
                script_text = response.message.content[0].text
                segments = parse_script(script_text)
                
                return {
                    "topic": topic,
                    "duration": duration,
                    "raw_script": script_text,
                    "segments": segments
                }
                
            except Exception as e:
                error_str = str(e)
                # Check if model not found, try next model
                if "404" in error_str or "removed" in error_str.lower() or "not found" in error_str.lower():
                    print(f"    Model {model_name} not available, trying next...")
                    break
                if attempt < max_retries - 1:
                    print(f"    Retry {attempt + 1}/{max_retries} after error...")
                    time.sleep(5)
                    continue
                print(f"Error generating script: {e}")
                raise
    
    raise Exception("All Cohere models failed. Please check your API key and try again.")


def parse_script(script_text: str) -> list:
    """
    Parse the generated script text into structured segments.
    
    Args:
        script_text: Raw script text from Cohere
        
    Returns:
        List of segment dictionaries
    """
    segments = []
    current_segment = {}
    
    lines = script_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        line_upper = line.upper()
        
        # Check for segment start (various formats)
        if line_upper.startswith('SEGMENT') or line_upper.startswith('**SEGMENT'):
            if current_segment and ('title' in current_segment or 'narration' in current_segment):
                segments.append(current_segment)
            current_segment = {}
        elif 'TITLE:' in line_upper or line_upper.startswith('TITLE'):
            # Handle "TITLE:" or "**TITLE:**" formats
            parts = line.split(':', 1)
            if len(parts) > 1:
                current_segment['title'] = parts[1].strip().strip('*').strip()
        elif 'NARRATION:' in line_upper or line_upper.startswith('NARRATION'):
            parts = line.split(':', 1)
            if len(parts) > 1:
                current_segment['narration'] = parts[1].strip().strip('*').strip()
        elif 'TEXT_OVERLAY:' in line_upper or 'TEXT OVERLAY:' in line_upper or line_upper.startswith('TEXT'):
            parts = line.split(':', 1)
            if len(parts) > 1:
                current_segment['text_overlay'] = parts[1].strip().strip('*').strip()
    
    # Add the last segment
    if current_segment and ('title' in current_segment or 'narration' in current_segment):
        segments.append(current_segment)
    
    # If no segments parsed, create default segments from the text
    if not segments:
        # Try to create segments from any text available
        paragraphs = [p.strip() for p in script_text.split('\n\n') if p.strip()]
        for i, para in enumerate(paragraphs[:5]):
            if len(para) > 20:
                segments.append({
                    'title': f'Scene {i+1}',
                    'narration': para[:200],
                    'text_overlay': para[:50]
                })
    
    # Ensure we have at least one segment
    if not segments:
        segments.append({
            'title': 'AI News Update',
            'narration': 'Artificial Intelligence continues to transform our world.',
            'text_overlay': 'AI Transforms Everything'
        })
    
    return segments


if __name__ == "__main__":
    # Test script generation
    test_news = """
    1. AI Revolution in Healthcare
       Summary: New AI models are transforming medical diagnosis...
    2. Tech Giants Invest in AI
       Summary: Major companies announce billion-dollar AI investments...
    """
    
    result = generate_script("artificial intelligence", test_news, 30)
    print(result)
