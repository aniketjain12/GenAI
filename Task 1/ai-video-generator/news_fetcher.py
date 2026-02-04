"""
News Fetcher Module
Fetches trending news articles using RSS feeds (legal, structured source).
"""
import feedparser
from typing import List, Dict
from config import NEWS_RSS_FEEDS


def fetch_news(topic: str, max_articles: int = 5) -> List[Dict]:
    """
    Fetch news articles related to a topic using Google News RSS feed.
    
    Args:
        topic: The topic/keyword to search for
        max_articles: Maximum number of articles to fetch
        
    Returns:
        List of dictionaries containing article info
    """
    articles = []
    
    # Use Google News RSS for topic-specific search
    rss_url = NEWS_RSS_FEEDS["general"].format(topic=topic.replace(" ", "+"))
    
    try:
        feed = feedparser.parse(rss_url)
        
        for entry in feed.entries[:max_articles]:
            article = {
                "title": entry.get("title", ""),
                "summary": entry.get("summary", entry.get("description", "")),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
            }
            articles.append(article)
            
    except Exception as e:
        print(f"Error fetching news: {e}")
    
    return articles


def format_news_for_script(articles: List[Dict]) -> str:
    """
    Format fetched news articles into a summary for script generation.
    
    Args:
        articles: List of article dictionaries
        
    Returns:
        Formatted string with news content
    """
    if not articles:
        return "No recent news found on this topic."
    
    formatted = []
    for i, article in enumerate(articles, 1):
        formatted.append(f"{i}. {article['title']}")
        if article['summary']:
            # Clean up summary (remove HTML tags)
            summary = article['summary'].replace("<b>", "").replace("</b>", "")
            summary = summary.replace("&nbsp;", " ").strip()
            formatted.append(f"   Summary: {summary[:200]}...")
    
    return "\n".join(formatted)


if __name__ == "__main__":
    # Test the news fetcher
    articles = fetch_news("artificial intelligence")
    print(f"Found {len(articles)} articles")
    print(format_news_for_script(articles))
