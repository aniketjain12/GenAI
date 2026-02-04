"""
Blog Publisher Module

Handles publishing generated blog posts to various platforms:
- Local file system (Markdown/HTML)
- Medium (via API)
- WordPress (via REST API)
- Dev.to (via API)

Note: API keys for publishing platforms must be configured separately.
"""

import os
import json
import requests
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
from abc import ABC, abstractmethod

from models import BlogPost, ExportedContent
from config import DEFAULT_CONFIG

# Configure logging
logger = logging.getLogger(__name__)


class BlogPublisher(ABC):
    """Abstract base class for blog publishers."""
    
    @abstractmethod
    def publish(self, blog: BlogPost) -> Dict[str, Any]:
        """
        Publish a blog post.
        
        Args:
            blog: BlogPost to publish
            
        Returns:
            Dict with publication details (url, id, status)
        """
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """Check if the publisher is properly configured."""
        pass


class LocalPublisher(BlogPublisher):
    """Publishes blogs to local file system."""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def is_configured(self) -> bool:
        return True
    
    def publish(self, blog: BlogPost, format: str = "markdown") -> Dict[str, Any]:
        """Save blog to local file."""
        from exporter import ContentExporter, ExporterConfig
        
        config = ExporterConfig(output_dir=self.output_dir, format=format)
        exporter = ContentExporter(config)
        result = exporter.export(blog, format)
        
        return {
            "platform": "local",
            "status": "success",
            "filepath": result.filepath,
            "url": f"file://{os.path.abspath(result.filepath)}"
        }


class MediumPublisher(BlogPublisher):
    """
    Publishes blogs to Medium.
    
    Requires:
        - MEDIUM_ACCESS_TOKEN environment variable
        - Integration token from Medium settings
    """
    
    API_BASE = "https://api.medium.com/v1"
    
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or os.getenv("MEDIUM_ACCESS_TOKEN")
        self._user_id = None
    
    def is_configured(self) -> bool:
        return bool(self.access_token)
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _get_user_id(self) -> str:
        """Get the authenticated user's ID."""
        if self._user_id:
            return self._user_id
        
        response = requests.get(
            f"{self.API_BASE}/me",
            headers=self._get_headers()
        )
        response.raise_for_status()
        self._user_id = response.json()["data"]["id"]
        return self._user_id
    
    def publish(self, blog: BlogPost, publish_status: str = "draft") -> Dict[str, Any]:
        """
        Publish blog to Medium.
        
        Args:
            blog: BlogPost to publish
            publish_status: "public", "draft", or "unlisted"
            
        Returns:
            Publication details
        """
        if not self.is_configured():
            return {
                "platform": "medium",
                "status": "error",
                "error": "Medium access token not configured"
            }
        
        try:
            user_id = self._get_user_id()
            
            # Prepare content with HTML formatting
            content = f"""
<h1>{blog.title}</h1>
<p><strong>Category:</strong> {blog.book.category} | 
<strong>Rating:</strong> {'⭐' * blog.book.rating} | 
<strong>Price:</strong> £{blog.book.price:.2f}</p>

{blog.content.replace(chr(10), '<br>')}

<hr>
<p><strong>Related Searches:</strong> {' • '.join(blog.keywords.selected_keywords)}</p>
<p><a href="{blog.book.url}">View Book Details</a></p>
"""
            
            payload = {
                "title": blog.title,
                "contentFormat": "html",
                "content": content,
                "tags": blog.keywords.selected_keywords[:5],  # Medium allows max 5 tags
                "publishStatus": publish_status
            }
            
            response = requests.post(
                f"{self.API_BASE}/users/{user_id}/posts",
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            data = response.json()["data"]
            
            return {
                "platform": "medium",
                "status": "success",
                "url": data["url"],
                "id": data["id"],
                "publish_status": data["publishStatus"]
            }
            
        except Exception as e:
            logger.error(f"Medium publish error: {e}")
            return {
                "platform": "medium",
                "status": "error",
                "error": str(e)
            }


class WordPressPublisher(BlogPublisher):
    """
    Publishes blogs to WordPress.
    
    Requires:
        - WORDPRESS_URL: Your WordPress site URL
        - WORDPRESS_USERNAME: WordPress username
        - WORDPRESS_APP_PASSWORD: Application password (not regular password)
    """
    
    def __init__(
        self,
        site_url: Optional[str] = None,
        username: Optional[str] = None,
        app_password: Optional[str] = None
    ):
        self.site_url = site_url or os.getenv("WORDPRESS_URL", "").rstrip('/')
        self.username = username or os.getenv("WORDPRESS_USERNAME")
        self.app_password = app_password or os.getenv("WORDPRESS_APP_PASSWORD")
    
    def is_configured(self) -> bool:
        return bool(self.site_url and self.username and self.app_password)
    
    def publish(self, blog: BlogPost, status: str = "draft") -> Dict[str, Any]:
        """
        Publish blog to WordPress.
        
        Args:
            blog: BlogPost to publish
            status: "publish", "draft", "pending", or "private"
            
        Returns:
            Publication details
        """
        if not self.is_configured():
            return {
                "platform": "wordpress",
                "status": "error",
                "error": "WordPress credentials not configured"
            }
        
        try:
            # Prepare content
            content = f"""
<p><strong>Category:</strong> {blog.book.category} | 
<strong>Rating:</strong> {'⭐' * blog.book.rating} | 
<strong>Price:</strong> £{blog.book.price:.2f}</p>

{blog.content.replace(chr(10), '</p><p>')}

<hr>
<p><strong>Related Searches:</strong> {' • '.join(blog.keywords.selected_keywords)}</p>
<p><a href="{blog.book.url}" target="_blank">View Book Details</a></p>
"""
            
            payload = {
                "title": blog.title,
                "content": content,
                "status": status,
                "tags": [],  # Would need to create/get tag IDs
                "meta": {
                    "keywords": ", ".join(blog.keywords.selected_keywords)
                }
            }
            
            response = requests.post(
                f"{self.site_url}/wp-json/wp/v2/posts",
                auth=(self.username, self.app_password),
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "platform": "wordpress",
                "status": "success",
                "url": data["link"],
                "id": data["id"],
                "publish_status": data["status"]
            }
            
        except Exception as e:
            logger.error(f"WordPress publish error: {e}")
            return {
                "platform": "wordpress",
                "status": "error",
                "error": str(e)
            }


class DevToPublisher(BlogPublisher):
    """
    Publishes blogs to Dev.to.
    
    Requires:
        - DEVTO_API_KEY environment variable
    """
    
    API_BASE = "https://dev.to/api"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DEVTO_API_KEY")
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    def publish(self, blog: BlogPost, published: bool = False) -> Dict[str, Any]:
        """
        Publish blog to Dev.to.
        
        Args:
            blog: BlogPost to publish
            published: True to publish immediately, False for draft
            
        Returns:
            Publication details
        """
        if not self.is_configured():
            return {
                "platform": "devto",
                "status": "error",
                "error": "Dev.to API key not configured"
            }
        
        try:
            # Prepare markdown content
            content = f"""
**Category:** {blog.book.category} | **Rating:** {'⭐' * blog.book.rating} | **Price:** £{blog.book.price:.2f}

{blog.content}

---

**Related Searches:** {' • '.join(blog.keywords.selected_keywords)}

[View Book Details]({blog.book.url})
"""
            
            payload = {
                "article": {
                    "title": blog.title,
                    "body_markdown": content,
                    "published": published,
                    "tags": blog.keywords.selected_keywords[:4]  # Dev.to allows max 4 tags
                }
            }
            
            response = requests.post(
                f"{self.API_BASE}/articles",
                headers={
                    "api-key": self.api_key,
                    "Content-Type": "application/json"
                },
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "platform": "devto",
                "status": "success",
                "url": data["url"],
                "id": data["id"],
                "published": data["published"]
            }
            
        except Exception as e:
            logger.error(f"Dev.to publish error: {e}")
            return {
                "platform": "devto",
                "status": "error",
                "error": str(e)
            }


class MultiPublisher:
    """
    Publishes blogs to multiple platforms simultaneously.
    """
    
    def __init__(self):
        self.publishers: Dict[str, BlogPublisher] = {
            "local": LocalPublisher(),
            "medium": MediumPublisher(),
            "wordpress": WordPressPublisher(),
            "devto": DevToPublisher()
        }
    
    def get_available_publishers(self) -> List[str]:
        """Get list of configured publishers."""
        return [name for name, pub in self.publishers.items() if pub.is_configured()]
    
    def publish(
        self,
        blog: BlogPost,
        platforms: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Publish blog to specified platforms.
        
        Args:
            blog: BlogPost to publish
            platforms: List of platform names. If None, publishes to all configured.
            
        Returns:
            Dict mapping platform names to publication results
        """
        if platforms is None:
            platforms = self.get_available_publishers()
        
        results = {}
        for platform in platforms:
            if platform in self.publishers:
                if self.publishers[platform].is_configured():
                    results[platform] = self.publishers[platform].publish(blog)
                else:
                    results[platform] = {
                        "platform": platform,
                        "status": "skipped",
                        "reason": "Not configured"
                    }
            else:
                results[platform] = {
                    "platform": platform,
                    "status": "error",
                    "error": f"Unknown platform: {platform}"
                }
        
        return results
    
    def publish_all(
        self,
        blogs: List[BlogPost],
        platforms: Optional[List[str]] = None
    ) -> List[Dict[str, Dict[str, Any]]]:
        """Publish multiple blogs to specified platforms."""
        return [self.publish(blog, platforms) for blog in blogs]


# Convenience functions
def publish_to_medium(blog: BlogPost, access_token: Optional[str] = None) -> Dict[str, Any]:
    """Quick publish to Medium."""
    publisher = MediumPublisher(access_token)
    return publisher.publish(blog)


def publish_to_wordpress(
    blog: BlogPost,
    site_url: Optional[str] = None,
    username: Optional[str] = None,
    app_password: Optional[str] = None
) -> Dict[str, Any]:
    """Quick publish to WordPress."""
    publisher = WordPressPublisher(site_url, username, app_password)
    return publisher.publish(blog)


def publish_to_devto(blog: BlogPost, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Quick publish to Dev.to."""
    publisher = DevToPublisher(api_key)
    return publisher.publish(blog)


if __name__ == "__main__":
    print("Blog Publisher Module")
    print("=" * 40)
    
    # Check available publishers
    multi = MultiPublisher()
    available = multi.get_available_publishers()
    
    print(f"Available publishers: {available}")
    print("\nTo enable additional publishers, set environment variables:")
    print("  - Medium: MEDIUM_ACCESS_TOKEN")
    print("  - WordPress: WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD")
    print("  - Dev.to: DEVTO_API_KEY")
