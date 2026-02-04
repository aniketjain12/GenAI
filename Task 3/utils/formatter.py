"""
Output Formatter
Converts pipeline output to various formats (Markdown, JSON).
"""

from typing import Any, Dict
import json
from datetime import datetime


class OutputFormatter:
    """
    Formats pipeline output to Markdown or JSON.
    """
    
    @staticmethod
    def to_json(data: Dict[str, Any], indent: int = 2) -> str:
        """Convert output to formatted JSON string."""
        return json.dumps(data, indent=indent, default=str)
    
    @staticmethod
    def to_markdown(data: Dict[str, Any]) -> str:
        """Convert output to Markdown format."""
        md = []
        
        # Header
        md.append("# 🏗️ Technical Specification Document")
        md.append("")
        md.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md.append("")
        
        # Original Requirement
        md.append("---")
        md.append("## 📝 Original Requirement")
        md.append("")
        md.append(f"> {data.get('requirement', 'N/A')}")
        md.append("")
        
        # Requirement Analysis
        analysis = data.get("analysis", {})
        if analysis:
            md.append("---")
            md.append("## 🔍 1. Requirement Analysis")
            md.append("")
            
            # Summary
            if analysis.get("requirement_summary"):
                md.append("### Summary")
                md.append(analysis["requirement_summary"])
                md.append("")
            
            # Actors
            actors = analysis.get("actors", [])
            if actors:
                md.append("### 👥 Actors")
                md.append("")
                md.append("| Name | Type | Description |")
                md.append("|------|------|-------------|")
                for actor in actors:
                    md.append(f"| {actor.get('name', 'N/A')} | {actor.get('type', 'N/A')} | {actor.get('description', 'N/A')} |")
                md.append("")
            
            # Actions
            actions = analysis.get("actions", [])
            if actions:
                md.append("### ⚡ Key Actions")
                md.append("")
                md.append("| Action | Actor | Priority | Description |")
                md.append("|--------|-------|----------|-------------|")
                for action in actions:
                    md.append(f"| {action.get('name', 'N/A')} | {action.get('actor', 'N/A')} | {action.get('priority', 'N/A')} | {action.get('description', 'N/A')} |")
                md.append("")
            
            # Entities
            entities = analysis.get("entities", [])
            if entities:
                md.append("### 📦 Core Entities")
                md.append("")
                for entity in entities:
                    md.append(f"**{entity.get('name', 'N/A')}**")
                    md.append(f"- Description: {entity.get('description', 'N/A')}")
                    attrs = entity.get('attributes', [])
                    if attrs:
                        md.append(f"- Attributes: `{'`, `'.join(attrs)}`")
                    md.append("")
            
            # Relationships
            relationships = analysis.get("relationships", [])
            if relationships:
                md.append("### 🔗 Relationships")
                md.append("")
                md.append("| From | To | Type | Description |")
                md.append("|------|----|----|-------------|")
                for rel in relationships:
                    md.append(f"| {rel.get('from_entity', 'N/A')} | {rel.get('to_entity', 'N/A')} | {rel.get('relationship_type', 'N/A')} | {rel.get('description', 'N/A')} |")
                md.append("")
            
            # Business Rules
            rules = analysis.get("business_rules", [])
            if rules:
                md.append("### 📋 Business Rules")
                md.append("")
                for i, rule in enumerate(rules, 1):
                    md.append(f"{i}. {rule}")
                md.append("")
        
        # Module Design
        modules = data.get("modules", {})
        if modules:
            md.append("---")
            md.append("## 🧩 2. Module Design")
            md.append("")
            
            if modules.get("system_overview"):
                md.append("### System Overview")
                md.append(modules["system_overview"])
                md.append("")
            
            if modules.get("architecture_pattern"):
                md.append(f"**Architecture Pattern:** {modules['architecture_pattern']}")
                md.append("")
            
            module_list = modules.get("modules", [])
            if module_list:
                md.append("### Modules")
                md.append("")
                
                for module in module_list:
                    md.append(f"#### 📦 {module.get('name', 'N/A')}")
                    md.append("")
                    md.append(f"**Type:** {module.get('type', 'N/A')}")
                    md.append("")
                    md.append(f"**Purpose:** {module.get('purpose', 'N/A')}")
                    md.append("")
                    
                    responsibilities = module.get("responsibilities", [])
                    if responsibilities:
                        md.append("**Responsibilities:**")
                        for resp in responsibilities:
                            md.append(f"- {resp}")
                        md.append("")
                    
                    interfaces = module.get("interfaces", [])
                    if interfaces:
                        md.append("**Interfaces:**")
                        md.append("")
                        md.append("| Method | Inputs | Outputs | Description |")
                        md.append("|--------|--------|---------|-------------|")
                        for iface in interfaces:
                            inputs = ", ".join(iface.get("inputs", []))
                            md.append(f"| `{iface.get('name', 'N/A')}` | {inputs} | {iface.get('outputs', 'N/A')} | {iface.get('description', 'N/A')} |")
                        md.append("")
                    
                    deps = module.get("dependencies", [])
                    if deps:
                        md.append(f"**Dependencies:** `{'`, `'.join(deps)}`")
                        md.append("")
            
            # Module Interactions
            interactions = modules.get("module_interactions", [])
            if interactions:
                md.append("### Module Interactions")
                md.append("")
                md.append("```")
                for inter in interactions:
                    md.append(f"{inter.get('from_module', 'N/A')} --[{inter.get('interaction_type', 'calls')}]--> {inter.get('to_module', 'N/A')}")
                md.append("```")
                md.append("")
            
            # Cross-cutting Concerns
            concerns = modules.get("cross_cutting_concerns", [])
            if concerns:
                md.append("### Cross-cutting Concerns")
                md.append("")
                for concern in concerns:
                    md.append(f"- **{concern.get('name', 'N/A')}**: {concern.get('description', 'N/A')}")
                md.append("")
        
        # Schema Design
        schema = data.get("schema", {})
        if schema:
            md.append("---")
            md.append("## 🗄️ 3. Database Schema")
            md.append("")
            
            if schema.get("database_type"):
                md.append(f"**Database Type:** {schema['database_type']}")
                md.append("")
            
            tables = schema.get("tables", [])
            if tables:
                md.append("### Tables")
                md.append("")
                
                for table in tables:
                    md.append(f"#### 📊 {table.get('name', 'N/A')}")
                    md.append("")
                    
                    if table.get("description"):
                        md.append(f"*{table['description']}*")
                        md.append("")
                    
                    fields = table.get("fields", [])
                    if fields:
                        md.append("| Field | Type | Nullable | Key | Description |")
                        md.append("|-------|------|----------|-----|-------------|")
                        for field in fields:
                            key = "🔑 PK" if field.get("primary_key") else ("🔗 FK" if field.get("foreign_key") else "")
                            nullable = "Yes" if field.get("nullable") else "No"
                            md.append(f"| `{field.get('name', 'N/A')}` | {field.get('data_type', 'N/A')} | {nullable} | {key} | {field.get('description', '')} |")
                        md.append("")
                    
                    indexes = table.get("indexes", [])
                    if indexes:
                        md.append("**Indexes:**")
                        for idx in indexes:
                            unique = "UNIQUE" if idx.get("unique") else ""
                            fields_str = ", ".join(idx.get("fields", []))
                            md.append(f"- `{idx.get('name', 'N/A')}` ({unique} {idx.get('type', 'btree')}) on ({fields_str})")
                        md.append("")
            
            # Enums
            enums = schema.get("enums", [])
            if enums:
                md.append("### Enums")
                md.append("")
                for enum in enums:
                    values = ", ".join(enum.get("values", []))
                    md.append(f"- **{enum.get('name', 'N/A')}**: {values}")
                    if enum.get("description"):
                        md.append(f"  - *{enum['description']}*")
                md.append("")
            
            # Schema Relationships
            relationships = schema.get("relationships", [])
            if relationships:
                md.append("### Schema Relationships")
                md.append("")
                md.append("```")
                for rel in relationships:
                    md.append(f"{rel.get('from_table', 'N/A')} --[{rel.get('type', 'N/A')}]--> {rel.get('to_table', 'N/A')}")
                md.append("```")
                md.append("")
        
        # Pseudocode
        pseudocode = data.get("pseudocode", {})
        if pseudocode:
            md.append("---")
            md.append("## 💻 4. Pseudocode")
            md.append("")
            
            functions = pseudocode.get("functions", [])
            if functions:
                md.append("### Functions")
                md.append("")
                
                for func in functions:
                    md.append(f"#### `{func.get('module', '')}.{func.get('name', 'N/A')}`")
                    md.append("")
                    md.append(f"**Description:** {func.get('description', 'N/A')}")
                    md.append("")
                    
                    params = func.get("parameters", [])
                    if params:
                        md.append("**Parameters:**")
                        for param in params:
                            md.append(f"- `{param.get('name', 'N/A')}` ({param.get('type', 'Any')}): {param.get('description', '')}")
                        md.append("")
                    
                    returns = func.get("returns", {})
                    if returns:
                        md.append(f"**Returns:** `{returns.get('type', 'void')}` - {returns.get('description', '')}")
                        md.append("")
                    
                    code = func.get("pseudocode", [])
                    if code:
                        md.append("```")
                        for line in code:
                            md.append(line)
                        md.append("```")
                        md.append("")
                    
                    complexity = func.get("complexity", {})
                    if complexity:
                        md.append(f"**Complexity:** Time: {complexity.get('time', 'N/A')}, Space: {complexity.get('space', 'N/A')}")
                        md.append("")
            
            # Data Flows
            flows = pseudocode.get("data_flows", [])
            if flows:
                md.append("### Data Flows")
                md.append("")
                
                for flow in flows:
                    md.append(f"#### {flow.get('name', 'N/A')}")
                    md.append("")
                    md.append(f"*{flow.get('description', '')}*")
                    md.append("")
                    
                    steps = flow.get("steps", [])
                    if steps:
                        md.append("| Step | Action | Function | Data |")
                        md.append("|------|--------|----------|------|")
                        for step in steps:
                            md.append(f"| {step.get('step', '')} | {step.get('action', '')} | `{step.get('function', '')}` | {step.get('data', '')} |")
                        md.append("")
            
            # API Contracts
            apis = pseudocode.get("api_contracts", [])
            if apis:
                md.append("### API Contracts")
                md.append("")
                
                for api in apis:
                    md.append(f"#### `{api.get('method', 'GET')} {api.get('endpoint', '/api')}`")
                    md.append("")
                    md.append(f"*{api.get('description', '')}*")
                    md.append("")
                    
                    if api.get("request_body"):
                        md.append("**Request Body:**")
                        md.append("```json")
                        md.append(json.dumps(api["request_body"], indent=2))
                        md.append("```")
                        md.append("")
                    
                    if api.get("response"):
                        md.append("**Response:**")
                        md.append("```json")
                        md.append(json.dumps(api["response"], indent=2))
                        md.append("```")
                        md.append("")
                    
                    status_codes = api.get("status_codes", [])
                    if status_codes:
                        md.append("**Status Codes:**")
                        for sc in status_codes:
                            md.append(f"- `{sc.get('code', '')}`: {sc.get('description', '')}")
                        md.append("")
        
        # Metadata
        metadata = data.get("metadata", {})
        if metadata:
            md.append("---")
            md.append("## 📊 Execution Summary")
            md.append("")
            md.append(f"- **Generated At:** {metadata.get('generated_at', 'N/A')}")
            md.append(f"- **Total Duration:** {metadata.get('total_duration_seconds', 0):.2f} seconds")
            md.append("")
            
            log = metadata.get("execution_log", [])
            if log:
                md.append("### Pipeline Execution Log")
                md.append("")
                md.append("| Stage | Status | Duration |")
                md.append("|-------|--------|----------|")
                for entry in log:
                    status_icon = "✅" if entry.get("status") == "success" else "❌"
                    duration = f"{entry.get('duration_seconds', 0):.2f}s" if entry.get('duration_seconds') else "N/A"
                    md.append(f"| {entry.get('stage', 'N/A')} | {status_icon} {entry.get('status', 'N/A')} | {duration} |")
                md.append("")
        
        return "\n".join(md)
    
    @staticmethod
    def save_to_file(content: str, filepath: str):
        """Save formatted content to a file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📄 Output saved to: {filepath}")
