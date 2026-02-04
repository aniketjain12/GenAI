"""
Configuration settings for the AI Architecture Pipeline.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class PipelineConfig:
    """Configuration for the pipeline."""
    
    # Cohere API Configuration
    cohere_api_key: Optional[str] = None
    model_name: str = "command-a-03-2025"  # Cohere's latest model
    temperature: float = 0.7
    max_tokens: int = 2000
    
    # Output Configuration
    output_format: str = "markdown"  # 'markdown' or 'json'
    
    # Pipeline Settings
    verbose: bool = True
    
    def __post_init__(self):
        """Load API key from environment if not provided."""
        if self.cohere_api_key is None:
            self.cohere_api_key = os.getenv("COHERE_API_KEY")


# Default configuration instance
default_config = PipelineConfig()
