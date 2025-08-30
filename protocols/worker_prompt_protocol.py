#!/usr/bin/env python3
"""
Worker Prompt Protocol Implementation
=====================================
Handles reading and parsing worker prompt files for task-specific instructions.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, Optional, List
from .protocol_loader import BaseProtocol, ProtocolConfig
from .session_management import SessionManagement

class WorkerPromptProtocol(BaseProtocol):
    """Handles worker prompt file reading and parsing"""
    
    def __init__(self, config: ProtocolConfig):
        super().__init__(config)
        self.prompt_data = None
        self.task_instructions = None
    
    def read_prompt_file(self, worker_type: str) -> Dict[str, Any]:
        """
        Read and parse worker-specific prompt file.
        
        Args:
            worker_type: The type of worker (e.g., 'analyzer-worker')
            
        Returns:
            Dict containing parsed prompt data including:
            - task_description: Primary task to complete
            - focus_areas: Specific areas to prioritize
            - dependencies: Other workers this depends on
            - timeout: Maximum execution time
            - success_criteria: How to measure success
            - output_requirements: Expected outputs and file paths
        """
        try:
            # Get session path using unified session management
            session_path = SessionManagement.get_session_path(self.config.session_id)
            prompt_file_path = f"{session_path}/workers/prompts/{worker_type}.prompt"
            
            # Note: In production, use Read tool to read the file
            # prompt_content = Read(prompt_file_path)
            
            # For now, parse standard format
            prompt_data = self._parse_prompt_content(prompt_file_path)
            
            # Validate required fields
            self._validate_prompt_data(prompt_data)
            
            # Store for later reference
            self.prompt_data = prompt_data
            
            # Log successful prompt reading
            SessionManagement.append_to_events(
                self.config.session_id,
                {
                    "type": "prompt_file_read",
                    "worker": worker_type,
                    "status": "success",
                    "file": prompt_file_path,
                    "timestamp": self._get_timestamp()
                }
            )
            
            self.log_execution("read_prompt_file", "success", prompt_data)
            return prompt_data
            
        except FileNotFoundError:
            # Fallback to extracting from main prompt
            return self._extract_from_main_prompt()
            
        except Exception as e:
            self.log_execution("read_prompt_file", "failed", {"error": str(e)})
            raise
    
    def _parse_prompt_content(self, file_path: str) -> Dict[str, Any]:
        """
        Parse prompt file content into structured data.
        
        Expected format:
        - YAML frontmatter with metadata
        - Markdown sections for different instruction types
        """
        # This would be implemented to actually parse the file
        # For now, return a template structure
        return {
            "task_description": "",
            "focus_areas": [],
            "dependencies": [],
            "timeout": 3600,
            "success_criteria": [],
            "output_requirements": {
                "notes_file": None,
                "json_response": None,
                "additional_outputs": []
            }
        }
    
    def _validate_prompt_data(self, data: Dict[str, Any]) -> None:
        """Validate that prompt data contains required fields"""
        required_fields = ["task_description", "focus_areas", "success_criteria"]
        
        for field in required_fields:
            if field not in data or not data[field]:
                self.log_debug(
                    "Prompt validation failed - missing required field",
                    "ERROR",
                    details={
                        "missing_field": field,
                        "required_fields": required_fields,
                        "available_fields": list(data.keys()),
                        "validation_failure": True
                    }
                )
                raise ValueError(f"Missing required field in prompt: {field}")
    
    def _extract_from_main_prompt(self) -> Dict[str, Any]:
        """
        Fallback method to extract task info from main prompt
        when prompt file is not available.
        """
        # Parse the original prompt passed to the worker
        prompt = self.config.initial_prompt or ""
        
        # Extract task description
        task_match = re.search(r"Task:\s*(.+?)(?:\n|$)", prompt, re.MULTILINE)
        task_description = task_match.group(1) if task_match else "Analysis task"
        
        # Extract focus areas
        focus_match = re.search(r"Focus:\s*(.+?)(?:\n|$)", prompt, re.MULTILINE)
        focus_areas = [focus_match.group(1)] if focus_match else ["General analysis"]
        
        # Extract dependencies
        dep_match = re.search(r"Dependencies:\s*(.+?)(?:\n|$)", prompt, re.MULTILINE)
        dependencies = dep_match.group(1).split(",") if dep_match else []
        
        return {
            "task_description": task_description,
            "focus_areas": focus_areas,
            "dependencies": [d.strip() for d in dependencies],
            "timeout": self.config.escalation_timeout or 3600,
            "success_criteria": ["Complete assigned analysis"],
            "output_requirements": {
                "notes_file": f"workers/{self.config.worker_type}-notes.md",
                "json_response": f"workers/json/{self.config.worker_type}-response.json",
                "additional_outputs": []
            }
        }
    
    def get_task_instructions(self) -> Dict[str, Any]:
        """
        Get parsed task instructions for the worker.
        Reads prompt file if not already loaded.
        """
        if not self.prompt_data:
            self.prompt_data = self.read_prompt_file(self.config.worker_type)
        
        return self.prompt_data
    
    def get_focus_areas(self) -> List[str]:
        """Get specific focus areas for this worker's task"""
        if not self.prompt_data:
            self.get_task_instructions()
        
        return self.prompt_data.get("focus_areas", [])
    
    def get_dependencies(self) -> List[str]:
        """Get list of other workers this task depends on"""
        if not self.prompt_data:
            self.get_task_instructions()
        
        return self.prompt_data.get("dependencies", [])
    
    def get_success_criteria(self) -> List[str]:
        """Get success criteria for task completion"""
        if not self.prompt_data:
            self.get_task_instructions()
        
        return self.prompt_data.get("success_criteria", [])
    
    def get_output_paths(self) -> Dict[str, str]:
        """Get required output file paths"""
        if not self.prompt_data:
            self.get_task_instructions()
        
        return self.prompt_data.get("output_requirements", {})
    
    def validate_task_completion(self, outputs: Dict[str, Any]) -> bool:
        """
        Validate that task completion meets success criteria.
        
        Args:
            outputs: Dictionary of produced outputs
            
        Returns:
            Boolean indicating if success criteria are met
        """
        criteria = self.get_success_criteria()
        output_paths = self.get_output_paths()
        
        # Check required outputs exist
        if output_paths.get("notes_file") and "notes" not in outputs:
            return False
        
        if output_paths.get("json_response") and "json_response" not in outputs:
            return False
        
        # Additional validation logic would go here
        return True
    
    def _get_timestamp(self) -> str:
        """Get current ISO-8601 timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()