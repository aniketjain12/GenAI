"""
Stage 4: Pseudocode Generator
Generates pseudocode for core functionalities based on modules and schema.
"""

from typing import Any, Dict
import json
from .base import PipelineStage


class PseudocodeGenerator(PipelineStage):
    """
    Generates pseudocode for major functionalities including:
    - Module methods
    - Business logic
    - Data operations
    - Error handling
    """
    
    SYSTEM_PROMPT = """You are an expert software engineer specializing in algorithm design and pseudocode.
Your task is to write clear, structured pseudocode that can be easily translated to any programming language.
Follow best practices for readability and maintainability.
Always respond with valid JSON format."""

    def get_prompt(self, input_data: Dict[str, Any]) -> str:
        """Generate the pseudocode generation prompt."""
        analysis = input_data.get("analysis", {})
        modules = input_data.get("modules", {})
        schema = input_data.get("schema", {})
        requirement = input_data.get("requirement", "")
        
        actions = analysis.get("actions", [])
        module_list = modules.get("modules", [])
        
        return f"""Based on the system design, generate pseudocode for all major functionalities.

ORIGINAL REQUIREMENT:
"{requirement}"

KEY ACTIONS TO IMPLEMENT:
{json.dumps(actions, indent=2)}

SYSTEM MODULES:
{json.dumps(module_list, indent=2)}

DATABASE SCHEMA:
{json.dumps(schema.get('tables', []), indent=2)}

Generate pseudocode following these guidelines:
1. Use clear, language-agnostic syntax
2. Include input validation
3. Handle errors appropriately
4. Add comments for complex logic
5. Follow single responsibility principle

Provide your pseudocode in the following JSON format:
{{
    "functions": [
        {{
            "module": "ModuleName",
            "name": "functionName",
            "description": "What this function does",
            "parameters": [
                {{
                    "name": "paramName",
                    "type": "DataType",
                    "description": "Parameter purpose"
                }}
            ],
            "returns": {{
                "type": "ReturnType",
                "description": "What is returned"
            }},
            "pseudocode": [
                "// Step-by-step pseudocode",
                "// Each line is an element in this array",
                "FUNCTION functionName(params):",
                "    // Validation",
                "    IF param IS INVALID:",
                "        THROW ValidationError",
                "    END IF",
                "",
                "    // Main logic",
                "    result = PERFORM_OPERATION()",
                "",
                "    // Return result",
                "    RETURN result",
                "END FUNCTION"
            ],
            "error_handling": [
                {{
                    "error_type": "ErrorName",
                    "condition": "When this error occurs",
                    "handling": "How it's handled"
                }}
            ],
            "complexity": {{
                "time": "O(n)",
                "space": "O(1)"
            }}
        }}
    ],
    "data_flows": [
        {{
            "name": "FlowName (e.g., User Registration Flow)",
            "description": "End-to-end flow description",
            "steps": [
                {{
                    "step": 1,
                    "action": "What happens",
                    "function": "Which function is called",
                    "data": "What data is passed/returned"
                }}
            ]
        }}
    ],
    "api_contracts": [
        {{
            "endpoint": "/api/resource",
            "method": "GET/POST/PUT/DELETE",
            "description": "What this endpoint does",
            "request_body": {{}},
            "response": {{}},
            "status_codes": [
                {{"code": 200, "description": "Success"}},
                {{"code": 400, "description": "Bad Request"}}
            ]
        }}
    ]
}}

Respond ONLY with the JSON, no additional text."""

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the design and generate pseudocode.
        
        Args:
            input_data: Dictionary containing analysis, modules, and schema
            
        Returns:
            Complete pseudocode for all major functionalities
        """
        self.log("Generating pseudocode...")
        
        prompt = self.get_prompt(input_data)
        response = self.call_llm(prompt, self.SYSTEM_PROMPT)
        
        pseudocode = self.parse_json_response(response)
        
        self.log(f"Generated {len(pseudocode.get('functions', []))} functions")
        
        return {
            "requirement": input_data.get("requirement"),
            "analysis": input_data.get("analysis"),
            "modules": input_data.get("modules"),
            "schema": input_data.get("schema"),
            "pseudocode": pseudocode
        }
