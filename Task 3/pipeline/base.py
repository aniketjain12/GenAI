"""
Base class for pipeline stages.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import json
import re


class PipelineStage(ABC):
    """Abstract base class for all pipeline stages."""
    
    def __init__(self, llm_client: Any, config: Any):
        """
        Initialize the pipeline stage.
        
        Args:
            llm_client: The LLM client for AI operations
            config: Pipeline configuration
        """
        self.llm_client = llm_client
        self.config = config
        self.stage_name = self.__class__.__name__
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input data and return the output.
        
        Args:
            input_data: Input dictionary from previous stage
            
        Returns:
            Output dictionary to pass to next stage
        """
        pass
    
    @abstractmethod
    def get_prompt(self, input_data: Dict[str, Any]) -> str:
        """
        Generate the prompt for this stage.
        
        Args:
            input_data: Input data for prompt generation
            
        Returns:
            Formatted prompt string
        """
        pass
    
    def call_llm(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Call the LLM with the given prompt using Cohere API.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            
        Returns:
            LLM response text
        """
        # Build messages list for Cohere V2 API
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.llm_client.chat(
            model=self.config.model_name,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        return response.message.content[0].text
    
    def parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Parse JSON from LLM response.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Parsed JSON dictionary
        """
        # Clean up the response
        cleaned = response.strip()
        
        # Try to extract JSON from markdown code blocks
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', cleaned)
        
        if json_match:
            json_str = json_match.group(1).strip()
        else:
            # Try to find JSON object or array in the response
            # Look for content between first { and last }
            start_brace = cleaned.find('{')
            end_brace = cleaned.rfind('}')
            
            if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
                json_str = cleaned[start_brace:end_brace + 1]
            else:
                json_str = cleaned
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            self.log(f"JSON parsing failed: {e}")
            self.log(f"Raw response (first 500 chars): {response[:500]}")
            # Return as raw text if parsing fails
            return {"raw_response": response, "parse_error": str(e)}
    
    def log(self, message: str):
        """Log a message if verbose mode is enabled."""
        if self.config.verbose:
            print(f"[{self.stage_name}] {message}")
