"""
Stage 2: Module Identifier
Identifies logical system modules/services based on requirement analysis.
"""

from typing import Any, Dict
import json
from .base import PipelineStage


class ModuleIdentifier(PipelineStage):
    """
    Identifies system modules and services based on analyzed requirements.
    Groups related functionality into cohesive modules.
    """
    
    SYSTEM_PROMPT = """You are an expert software architect specializing in system design and modular architecture.
Your task is to design a modular system architecture based on requirement analysis.
Follow SOLID principles and separation of concerns.
Always respond with valid JSON format."""

    def get_prompt(self, input_data: Dict[str, Any]) -> str:
        """Generate the module identification prompt."""
        analysis = input_data.get("analysis", {})
        requirement = input_data.get("requirement", "")
        
        return f"""Based on the requirement analysis below, design a modular system architecture.

ORIGINAL REQUIREMENT:
"{requirement}"

REQUIREMENT ANALYSIS:
{json.dumps(analysis, indent=2)}

Design system modules following these principles:
1. Single Responsibility - Each module has one clear purpose
2. High Cohesion - Related functionality grouped together
3. Low Coupling - Modules are independent
4. Reusability - Common functionality abstracted

Provide your module design in the following JSON format:
{{
    "system_overview": "High-level description of the system",
    "architecture_pattern": "Pattern used (e.g., layered, microservices, MVC)",
    "modules": [
        {{
            "name": "ModuleName",
            "type": "service/controller/repository/utility",
            "purpose": "What this module does",
            "responsibilities": [
                "List of specific responsibilities"
            ],
            "interfaces": [
                {{
                    "name": "MethodName",
                    "description": "What it does",
                    "inputs": ["input1", "input2"],
                    "outputs": "Return type/value"
                }}
            ],
            "dependencies": ["List of other modules it depends on"],
            "related_entities": ["Entities this module manages"]
        }}
    ],
    "module_interactions": [
        {{
            "from_module": "Module1",
            "to_module": "Module2",
            "interaction_type": "calls/subscribes/publishes",
            "description": "How they interact"
        }}
    ],
    "cross_cutting_concerns": [
        {{
            "name": "Concern name (e.g., Authentication, Logging)",
            "description": "How it's handled",
            "affected_modules": ["List of affected modules"]
        }}
    ]
}}

Respond ONLY with the JSON, no additional text."""

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the analysis and identify system modules.
        
        Args:
            input_data: Dictionary containing analysis from Stage 1
            
        Returns:
            Module design with interfaces and interactions
        """
        self.log("Identifying system modules...")
        
        prompt = self.get_prompt(input_data)
        response = self.call_llm(prompt, self.SYSTEM_PROMPT)
        
        modules = self.parse_json_response(response)
        
        self.log(f"Identified {len(modules.get('modules', []))} modules")
        
        return {
            "requirement": input_data.get("requirement"),
            "analysis": input_data.get("analysis"),
            "modules": modules
        }
