"""
Stage 3: Schema Generator
Generates database schemas based on entities and modules.
"""

from typing import Any, Dict
import json
from .base import PipelineStage


class SchemaGenerator(PipelineStage):
    """
    Generates database schema designs including:
    - Tables/Collections
    - Fields with data types
    - Relationships and constraints
    - Indexes
    """
    
    SYSTEM_PROMPT = """You are an expert database architect specializing in schema design.
Your task is to design efficient and normalized database schemas based on the given entities.
Follow database normalization principles and best practices.
You MUST respond with valid JSON format only. No markdown, no explanations, just pure JSON."""

    def get_prompt(self, input_data: Dict[str, Any]) -> str:
        """Generate the schema design prompt."""
        analysis = input_data.get("analysis", {})
        modules = input_data.get("modules", {})
        requirement = input_data.get("requirement", "")
        
        entities = analysis.get("entities", [])
        relationships = analysis.get("relationships", [])
        
        # Create a simpler, more direct prompt
        return f"""Create a database schema for the following system.

REQUIREMENT: "{requirement}"

ENTITIES TO CREATE TABLES FOR:
{json.dumps(entities, indent=2)}

RELATIONSHIPS BETWEEN ENTITIES:
{json.dumps(relationships, indent=2)}

IMPORTANT: You MUST create at least one table for each entity listed above.
Convert each entity into a database table with appropriate fields.

Return a JSON object with this EXACT structure:
{{
    "database_type": "relational",
    "tables": [
        {{
            "name": "table_name",
            "description": "What this table stores",
            "fields": [
                {{
                    "name": "id",
                    "data_type": "UUID",
                    "nullable": false,
                    "primary_key": true,
                    "foreign_key": null,
                    "description": "Primary key"
                }},
                {{
                    "name": "field_name",
                    "data_type": "VARCHAR(255)",
                    "nullable": true,
                    "primary_key": false,
                    "foreign_key": null,
                    "description": "Field description"
                }}
            ],
            "indexes": []
        }}
    ],
    "relationships": [
        {{
            "from_table": "Table1",
            "to_table": "Table2",
            "type": "one-to-many"
        }}
    ],
    "enums": []
}}

Return ONLY valid JSON. No markdown code blocks. No explanations. Just the JSON object."""

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the analysis and modules to generate database schema.
        
        Args:
            input_data: Dictionary containing analysis and modules
            
        Returns:
            Database schema design
        """
        self.log("Generating database schema...")
        
        prompt = self.get_prompt(input_data)
        response = self.call_llm(prompt, self.SYSTEM_PROMPT)
        
        schema = self.parse_json_response(response)
        
        self.log(f"Generated schema with {len(schema.get('tables', []))} tables")
        
        return {
            "requirement": input_data.get("requirement"),
            "analysis": input_data.get("analysis"),
            "modules": input_data.get("modules"),
            "schema": schema
        }
