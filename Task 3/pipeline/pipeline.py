"""
Main Pipeline Orchestrator
Coordinates all stages of the architecture pipeline.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import json

from .analyzer import RequirementAnalyzer
from .module_identifier import ModuleIdentifier
from .schema_generator import SchemaGenerator
from .pseudocode_generator import PseudocodeGenerator
from .base import PipelineStage


class ArchitecturePipeline:
    """
    Orchestrates the complete pipeline for converting business requirements
    to technical specifications.
    
    Pipeline Stages:
    1. Requirement Analysis
    2. Module Identification
    3. Schema Generation
    4. Pseudocode Generation
    """
    
    def __init__(self, llm_client: Any, config: Any):
        """
        Initialize the pipeline with all stages.
        
        Args:
            llm_client: OpenAI client for LLM operations
            config: Pipeline configuration
        """
        self.llm_client = llm_client
        self.config = config
        
        # Initialize all stages
        self.stages: List[PipelineStage] = [
            RequirementAnalyzer(llm_client, config),
            ModuleIdentifier(llm_client, config),
            SchemaGenerator(llm_client, config),
            PseudocodeGenerator(llm_client, config)
        ]
        
        self.execution_log: List[Dict[str, Any]] = []
    
    def run(self, requirement: str) -> Dict[str, Any]:
        """
        Execute the complete pipeline.
        
        Args:
            requirement: High-level business requirement text
            
        Returns:
            Complete technical specification
        """
        print("\n" + "="*60)
        print("[START] AI Architecture Pipeline Started")
        print("="*60)
        
        start_time = datetime.now()
        
        # Initial input
        data = {"requirement": requirement}
        
        # Execute each stage
        for i, stage in enumerate(self.stages, 1):
            stage_start = datetime.now()
            print(f"\n[STAGE] Stage {i}/{len(self.stages)}: {stage.stage_name}")
            print("-" * 40)
            
            try:
                data = stage.process(data)
                
                stage_duration = (datetime.now() - stage_start).total_seconds()
                
                self.execution_log.append({
                    "stage": stage.stage_name,
                    "status": "success",
                    "duration_seconds": stage_duration
                })
                
                print(f"[OK] {stage.stage_name} completed in {stage_duration:.2f}s")
                
            except Exception as e:
                self.execution_log.append({
                    "stage": stage.stage_name,
                    "status": "failed",
                    "error": str(e)
                })
                print(f"[FAIL] {stage.stage_name} failed: {str(e)}")
                raise
        
        total_duration = (datetime.now() - start_time).total_seconds()
        
        print("\n" + "="*60)
        print(f"[DONE] Pipeline completed successfully in {total_duration:.2f}s")
        print("="*60)
        
        # Add metadata
        data["metadata"] = {
            "generated_at": datetime.now().isoformat(),
            "total_duration_seconds": total_duration,
            "execution_log": self.execution_log
        }
        
        return data
    
    def run_stage(self, stage_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a specific stage of the pipeline.
        
        Args:
            stage_name: Name of the stage to run
            input_data: Input data for the stage
            
        Returns:
            Stage output
        """
        for stage in self.stages:
            if stage.stage_name == stage_name:
                return stage.process(input_data)
        
        raise ValueError(f"Stage '{stage_name}' not found")
    
    def get_stage_names(self) -> List[str]:
        """Get list of all stage names."""
        return [stage.stage_name for stage in self.stages]
