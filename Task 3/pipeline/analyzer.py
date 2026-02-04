"""
Stage 1: Requirement Analyzer
Analyzes business requirements to identify actors, actions, and entities.
"""

from typing import Any, Dict
from .base import PipelineStage


class RequirementAnalyzer(PipelineStage):
    """
    Analyzes high-level business requirements and extracts:
    - Actors (users, systems, roles)
    - Key Actions (verbs, operations)
    - Core Entities (nouns, data objects)
    """
    
    SYSTEM_PROMPT = """You are an expert software architect specializing in requirement analysis.
Your task is to analyze business requirements and extract structured information.
Always respond with valid JSON format."""

    def get_prompt(self, input_data: Dict[str, Any]) -> str:
        """Generate the analysis prompt."""
        requirement = input_data.get("requirement", "")
        
        return f"""Analyze the following business requirement and extract key components.

BUSINESS REQUIREMENT:
"{requirement}"

Provide your analysis in the following JSON format:
{{
    "requirement_summary": "Brief summary of the requirement",
    "actors": [
        {{
            "name": "Actor name",
            "type": "user/system/external",
            "description": "What this actor does"
        }}
    ],
    "actions": [
        {{
            "name": "Action name (verb)",
            "actor": "Who performs this action",
            "description": "What this action does",
            "priority": "high/medium/low"
        }}
    ],
    "entities": [
        {{
            "name": "Entity name",
            "description": "What this entity represents",
            "attributes": ["list", "of", "potential", "attributes"]
        }}
    ],
    "relationships": [
        {{
            "from_entity": "Entity 1",
            "to_entity": "Entity 2", 
            "relationship_type": "one-to-one/one-to-many/many-to-many",
            "description": "How they relate"
        }}
    ],
    "business_rules": [
        "List of implied business rules"
    ]
}}

Respond ONLY with the JSON, no additional text."""

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the business requirement and extract components.
        
        Args:
            input_data: Dictionary containing 'requirement' key
            
        Returns:
            Analysis results with actors, actions, entities
        """
        self.log("Starting requirement analysis...")
        
        prompt = self.get_prompt(input_data)
        response = self.call_llm(prompt, self.SYSTEM_PROMPT)
        
        analysis = self.parse_json_response(response)
        
        self.log(f"Identified {len(analysis.get('actors', []))} actors, "
                f"{len(analysis.get('actions', []))} actions, "
                f"{len(analysis.get('entities', []))} entities")
        
        return {
            "requirement": input_data.get("requirement"),
            "analysis": analysis
        }
