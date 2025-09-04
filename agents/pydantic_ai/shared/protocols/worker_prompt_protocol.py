#!/usr/bin/env python3
"""
Worker Prompt Protocol Implementation
=====================================
Handles reading and parsing worker prompt files for task-specific instructions.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from .protocol_loader import BaseProtocol, ProtocolConfig
from .session_management import SessionManagement
from .logging_protocol import LoggingProtocol


class WorkerPromptProtocol(BaseProtocol):
    """Handles worker prompt file reading and parsing"""

    def __init__(self, config: ProtocolConfig):
        super().__init__(config)
        self.prompt_data = None
        self.task_instructions = None
        self.logger = LoggingProtocol(config)

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
                    "agent": self.config.agent_name or worker_type,
                    "details": {
                        "status": "success",
                        "file": prompt_file_path,
                        "worker": worker_type,
                    },
                    "timestamp": self._get_timestamp(),
                },
            )

            return prompt_data

        except FileNotFoundError:
            # Fallback to extracting from main prompt
            return self._extract_from_main_prompt()

        except Exception as e:
            raise

    def _parse_prompt_content(self, file_path: str) -> Dict[str, Any]:
        """
        Parse prompt file content into structured data.

        Expected format:
        - YAML frontmatter with metadata
        - Markdown sections for different instruction types
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split YAML frontmatter and markdown content
            if not content.startswith('---'):
                raise ValueError("Prompt file must start with YAML frontmatter")
            
            # Find the end of frontmatter
            parts = content.split('---', 2)
            if len(parts) < 3:
                raise ValueError("Invalid YAML frontmatter format")
            
            frontmatter_text = parts[1].strip()
            markdown_content = parts[2].strip()
            
            # Parse YAML frontmatter
            frontmatter = yaml.safe_load(frontmatter_text) or {}
            
            # Parse markdown sections
            markdown_sections = self._parse_markdown_sections(markdown_content)
            
            # Combine into structured data
            return {
                # From YAML frontmatter
                "worker_type": frontmatter.get("worker_type", ""),
                "session_id": frontmatter.get("session_id", ""),
                "task_description": frontmatter.get("task_focus", ""),
                "priority": frontmatter.get("priority", "medium"),
                "estimated_duration": frontmatter.get("estimated_duration", "1-2h"),
                "complexity_level": frontmatter.get("complexity_level", 1),
                "target_services": frontmatter.get("target_services", []),
                "primary_target": frontmatter.get("primary_target", "unknown"),
                "dependencies": frontmatter.get("dependencies", []),
                "focus_areas": frontmatter.get("focus_areas", []),
                "created_by": frontmatter.get("created_by", "unknown"),
                
                # From markdown sections
                "worker_expertise": markdown_sections.get("worker_expertise", ""),
                "rationale": markdown_sections.get("strategic_rationale", ""),
                "success_criteria": markdown_sections.get("success_criteria", []),
                "output_requirements": markdown_sections.get("output_requirements", {}),
                "available_tools": markdown_sections.get("available_tools", []),
                "codebase_context": markdown_sections.get("codebase_context", {}),
                "risk_context": markdown_sections.get("risk_context", []),
                "coordination_strategy": markdown_sections.get("coordination_strategy", []),
                
                # Combined metadata
                "timeout": 3600,  # Default timeout
                "full_content": content,
                "parsed_sections": list(markdown_sections.keys()),
            }
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML frontmatter in prompt file: {e}")
        except Exception as e:
            raise RuntimeError(f"Error parsing prompt file {file_path}: {e}")
    
    def _parse_markdown_sections(self, markdown_content: str) -> Dict[str, Any]:
        """Parse markdown sections into structured data"""
        sections = {}
        
        # Split by headers
        lines = markdown_content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            if line.startswith('##'):
                # Save previous section
                if current_section:
                    sections[current_section] = self._process_section_content(
                        current_section, '\n'.join(current_content).strip()
                    )
                
                # Start new section
                current_section = line.replace('##', '').strip().lower().replace(' ', '_')
                current_content = []
            elif line.startswith('#') and not line.startswith('##'):
                # Skip main headers
                continue
            else:
                current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = self._process_section_content(
                current_section, '\n'.join(current_content).strip()
            )
        
        return sections
    
    def _process_section_content(self, section_name: str, content: str) -> Any:
        """Process section content based on section type"""
        if section_name in ['success_criteria', 'available_tools', 'focus_areas_priority_order', 'worker_dependencies']:
            # List-based sections
            items = []
            for line in content.split('\n'):
                line = line.strip()
                if line and (line.startswith('- ') or line.startswith('1. ') or line.startswith('2. ') or line.startswith('3. ')):
                    # Remove list markers
                    item = re.sub(r'^[-\d\.]\s*', '', line).strip()
                    if item:
                        items.append(item)
            return items
        
        elif section_name == 'output_requirements':
            # Extract file requirements
            files = []
            json_format = {}
            
            # Look for file listings
            file_matches = re.findall(r'- `([^`]+)`', content)
            files.extend(file_matches)
            
            # Look for JSON format
            json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                try:
                    import json
                    json_format = json.loads(json_match.group(1))
                except:
                    json_format = {"format": "json", "raw": json_match.group(1)}
            
            return {
                "required_files": files,
                "json_format": json_format,
                "raw_content": content
            }
        
        elif section_name in ['codebase_context', 'critical_risk_context']:
            # Context sections - extract key points
            points = []
            for line in content.split('\n'):
                line = line.strip()
                if line and (line.startswith('- ') or line.startswith('**') or line.startswith('###')):
                    points.append(line)
            
            return {
                "key_points": points,
                "full_content": content
            }
        
        else:
            # Default: return as string
            return content

    def _validate_prompt_data(self, data: Dict[str, Any]) -> None:
        """Validate that prompt data contains required fields"""
        required_fields = ["task_description", "focus_areas", "success_criteria"]

        for field in required_fields:
            if field not in data or not data[field]:
                self.logger.log_debug(
                    "Prompt validation failed - missing required field",
                    details={
                        "missing_field": field,
                        "required_fields": required_fields,
                        "available_fields": list(data.keys()),
                        "validation_failure": True,
                    },
                    level="ERROR"
                )
                raise ValueError(f"Missing required field in prompt: {field}")

    def _extract_from_main_prompt(self) -> Dict[str, Any]:
        """
        Fallback method to extract task info from main prompt
        when prompt file is not available.
        """
        # Parse the original prompt passed to the worker
        prompt = self.config.prompt_text or ""

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
            "timeout": self.config.timeout or 3600,
            "success_criteria": ["Complete assigned analysis"],
            "output_requirements": {
                "notes_file": f"notes/{self.config.agent_name.replace('-worker','')}_notes.md",
                "json_response": f"workers/json/{self.config.agent_name}-response.json",
                "additional_outputs": [],
            },
        }

    def get_task_instructions(self) -> Dict[str, Any]:
        """
        Get parsed task instructions for the worker.
        Reads prompt file if not already loaded.
        """
        if not self.prompt_data:
            self.prompt_data = self.read_prompt_file(self.config.agent_name)

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

    def get_output_paths(self) -> Dict[str, Any]:
        """Get required output file paths and JSON format"""
        if not self.prompt_data:
            self.get_task_instructions()

        return self.prompt_data.get("output_requirements", {})
    
    def get_worker_expertise(self) -> str:
        """Get worker expertise description"""
        if not self.prompt_data:
            self.get_task_instructions()
        
        return self.prompt_data.get("worker_expertise", "")
    
    def get_codebase_context(self) -> Dict[str, Any]:
        """Get codebase context and insights"""
        if not self.prompt_data:
            self.get_task_instructions()
            
        return self.prompt_data.get("codebase_context", {})
    
    def get_risk_context(self) -> List[str]:
        """Get identified risks and concerns"""
        if not self.prompt_data:
            self.get_task_instructions()
            
        return self.prompt_data.get("risk_context", [])
    
    def get_coordination_strategy(self) -> List[str]:
        """Get coordination strategy notes"""
        if not self.prompt_data:
            self.get_task_instructions()
            
        return self.prompt_data.get("coordination_strategy", [])
    
    def get_target_services(self) -> List[str]:
        """Get target services for analysis"""
        if not self.prompt_data:
            self.get_task_instructions()
            
        return self.prompt_data.get("target_services", [])
    
    def get_primary_target(self) -> str:
        """Get primary target service"""
        if not self.prompt_data:
            self.get_task_instructions()
            
        return self.prompt_data.get("primary_target", "unknown")
    
    def get_complexity_level(self) -> int:
        """Get task complexity level (1-10)"""
        if not self.prompt_data:
            self.get_task_instructions()
            
        return self.prompt_data.get("complexity_level", 1)
    
    def get_priority(self) -> str:
        """Get task priority level"""
        if not self.prompt_data:
            self.get_task_instructions()
            
        return self.prompt_data.get("priority", "medium")
    
    def get_estimated_duration(self) -> str:
        """Get estimated duration for task"""
        if not self.prompt_data:
            self.get_task_instructions()
            
        return self.prompt_data.get("estimated_duration", "1-2h")
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tools for this worker"""
        if not self.prompt_data:
            self.get_task_instructions()
            
        return self.prompt_data.get("available_tools", [])
    
    def get_full_prompt_content(self) -> str:
        """Get the full original prompt file content"""
        if not self.prompt_data:
            self.get_task_instructions()
            
        return self.prompt_data.get("full_content", "")
    
    def get_json_response_format(self) -> Dict[str, Any]:
        """Get the expected JSON response format"""
        if not self.prompt_data:
            self.get_task_instructions()
            
        output_reqs = self.prompt_data.get("output_requirements", {})
        return output_reqs.get("json_format", {})

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

        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
