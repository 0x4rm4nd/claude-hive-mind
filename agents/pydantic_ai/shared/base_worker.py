"""
Base Worker Class
=================
Abstract base class for all Pydantic AI workers providing standardized execution framework
with protocol compliance, session management, and extensible worker-specific behavior.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import TypeVar, Generic, Dict, Any, Optional, Type, Union
from abc import ABC, abstractmethod

from .protocols import (
    SessionManagement,
    ProtocolConfig,
    WorkerManager,
    BaseProtocol,
)

from .worker_config import WorkerConfig
from .tools import iso_now
from pydantic import BaseModel

# Type variable for worker-specific output models
T = TypeVar("T", bound=BaseModel)


class BaseWorker(BaseProtocol, ABC, Generic[T]):
    """
    Base class for all Pydantic AI workers.

    Provides framework-enforced functionality while allowing worker-specific
    customization through abstract methods and configuration.
    """

    def __init__(
        self,
        worker_type: str,
        worker_config: Optional[WorkerConfig],
        output_model: Type[T],
    ):
        """
        Initialize base worker.

        Args:
            worker_type: Worker identifier (e.g., "analyzer-worker")
            worker_config: Worker configuration instance (can be None, set at runtime)
            output_model: Pydantic model class for worker output validation
        """
        # Initialize BaseProtocol with dummy config (session_id will be set at runtime)
        super().__init__({"session_id": "temp", "agent_name": worker_type})
        
        self.worker_type = worker_type
        self.worker_config = worker_config
        self.output_model = output_model
        self._prompt_protocol: Optional[WorkerManager] = None
        self._prompt_data: Optional[Dict[str, Any]] = None

    def update_session_config(self, session_id: str) -> None:
        """Update the protocol configuration with actual session ID"""
        self.config = ProtocolConfig({
            "session_id": session_id, 
            "agent_name": self.worker_type
        })

    def log_worker_debug(
        self, session_id: str, message: str, details: Any = {}, level: str = "DEBUG"
    ) -> None:
        """Framework-enforced debug logging with session update"""
        self.update_session_config(session_id)
        self.log_debug(message, details, level)

    def read_worker_prompt(self, session_id: str) -> Dict[str, Any]:
        """
        Read and parse worker-specific prompt file with rich contextual information.
        
        Returns structured data including:
        - YAML frontmatter (task_focus, dependencies, priority, complexity_level, etc.)
        - Parsed markdown sections (success_criteria, available_tools, etc.)
        - Codebase context and strategic insights from Queen orchestration
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dictionary containing structured prompt data
        """
        if not self._prompt_data:
            try:
                cfg = ProtocolConfig({
                    "session_id": session_id, 
                    "agent_name": self.worker_type
                })
                
                self._prompt_protocol = WorkerManager(cfg.to_dict())
                self._prompt_data = self._prompt_protocol.read_prompt_file(self.worker_type)
                
                self.log_worker_debug(
                    session_id, 
                    f"Successfully loaded prompt data for {self.worker_type}",
                    {
                        "focus_areas": self._prompt_data.get("focus_areas", []),
                        "complexity_level": self._prompt_data.get("complexity_level", 1),
                        "priority": self._prompt_data.get("priority", "medium"),
                        "dependencies": self._prompt_data.get("dependencies", [])
                    }
                )
                
            except Exception as e:
                self.log_worker_debug(
                    session_id,
                    f"Failed to read prompt file for {self.worker_type}",
                    {"error": str(e)},
                    "WARNING"
                )
                # Fallback to basic task description
                self._prompt_data = {
                    "task_description": f"Analyze and provide insights for {self.worker_type}",
                    "focus_areas": [],
                    "dependencies": [],
                    "priority": "medium",
                    "complexity_level": 1,
                    "success_criteria": [],
                    "available_tools": [],
                    "output_requirements": {}
                }
        
        return self._prompt_data
    
    def get_task_context(self, session_id: str) -> Dict[str, Any]:
        """
        Get rich task context from parsed prompt data.
        Convenience method that returns key contextual information.
        """
        prompt_data = self.read_worker_prompt(session_id)
        
        return {
            "task_description": prompt_data.get("task_description", ""),
            "focus_areas": prompt_data.get("focus_areas", []),
            "priority": prompt_data.get("priority", "medium"),
            "complexity_level": prompt_data.get("complexity_level", 1),
            "dependencies": prompt_data.get("dependencies", []),
            "success_criteria": prompt_data.get("success_criteria", []),
            "target_services": prompt_data.get("target_services", []),
            "primary_target": prompt_data.get("primary_target", "unknown"),
            "estimated_duration": prompt_data.get("estimated_duration", "1-2h"),
        }

    def validate_session(self, session_id: str) -> None:
        """Framework-enforced session validation"""
        try:
            if not SessionManagement.ensure_session_exists(session_id):
                raise ValueError(f"Session {session_id} does not exist or is invalid")
            self.log_worker_debug(session_id, "Session validation successful")
        except Exception as e:
            self.log_worker_debug(
                session_id, "Session validation failed", {"error": str(e)}, "ERROR"
            )
            raise

    def validate_and_enrich_output(
        self, output: T, session_id: str, task_description: str
    ) -> T:
        """Framework-enforced output validation and enrichment"""
        timestamp = iso_now()

        # Standard enrichment for all workers
        if hasattr(output, "worker") and not output.worker:
            output.worker = self.worker_type
        if hasattr(output, "session_id") and not output.session_id:
            output.session_id = session_id
        if hasattr(output, "timestamp") and not output.timestamp:
            output.timestamp = timestamp

        # Add worker configuration to output
        if hasattr(output, "config") and self.worker_config is not None:
            worker_config = self.worker_config.model_copy(
                update={"session_id": session_id, "task_description": task_description}
            )
            output.config = worker_config.model_dump()

        return output

    def create_output_files_base(
        self, session_id: str, output: T, file_prefix: str
    ) -> None:
        """Framework-enforced base file creation with worker-specific prefix"""
        try:
            session_path = Path(SessionManagement.get_session_path(session_id))
            notes_dir = session_path / "workers" / "notes"
            json_dir = session_path / "workers" / "json"
            notes_dir.mkdir(parents=True, exist_ok=True)
            json_dir.mkdir(parents=True, exist_ok=True)

            # Get project root for relative paths
            project_root = Path(SessionManagement.detect_project_root())

            # Create notes file if content provided
            if hasattr(output, "notes_markdown") and output.notes_markdown:
                notes_file = notes_dir / f"{file_prefix}_notes.md"
                notes_file.write_text(output.notes_markdown)
                try:
                    relative_path = notes_file.relative_to(project_root)
                    path_str = str(relative_path)
                except ValueError:
                    # File is outside project root, use absolute path
                    path_str = str(notes_file)
                self.log_worker_debug(
                    session_id,
                    f"Created {file_prefix} notes file",
                    {"path": path_str},
                )

            # Create structured output JSON
            output_file = json_dir / f"{file_prefix}_output.json"
            output_file.write_text(output.model_dump_json(indent=2))
            try:
                relative_path = output_file.relative_to(project_root)
                path_str = str(relative_path)
            except ValueError:
                # File is outside project root, use absolute path
                path_str = str(output_file)
            self.log_worker_debug(
                session_id,
                f"Created {file_prefix} output JSON",
                {"path": path_str},
            )

            # Allow worker-specific file creation
            self.create_worker_specific_files(session_id, output, session_path)

        except Exception as e:
            self.log_worker_debug(
                session_id, "File creation failed", {"error": str(e)}, "ERROR"
            )
            raise

    def run_analysis(self, session_id: str, task_description: str, model: str) -> T:
        """
        Framework-enforced main execution flow.

        This method orchestrates the entire worker execution with protocol compliance
        while delegating worker-specific logic to abstract methods.
        """

        # Framework-enforced session validation
        self.validate_session(session_id)

        try:
            # Execute worker-specific AI logic
            result = self.execute_ai_analysis(session_id, task_description, model)
            output: T = result.output

            # Framework-enforced output validation and enrichment
            output = self.validate_and_enrich_output(
                output, session_id, task_description
            )

            # Create output files
            file_prefix = self.get_file_prefix()
            self.create_output_files_base(session_id, output, file_prefix)

            # Update session config and log completion with worker-specific details
            self.update_session_config(session_id)
            completion_details = self.get_completion_event_details(output)
            self.log_event("analysis_completed", completion_details)

            return output

        except Exception as e:
            self.log_worker_debug(
                session_id,
                f"{self.worker_type} analysis failed",
                {"error": str(e), "task": task_description},
                "ERROR",
            )
            raise

    def create_cli_parser(self) -> argparse.ArgumentParser:
        """Framework-enforced CLI argument parsing with worker-specific description"""
        parser = argparse.ArgumentParser(
            description=f"{self.get_worker_display_name()} - {self.get_worker_description()}"
        )
        parser.add_argument("--session", required=True, help="Session ID")
        parser.add_argument("--task", required=True, help="Analysis task description")
        parser.add_argument(
            "--model", default="custom:max-subscription", help="AI model to use"
        )
        return parser

    def run_cli_main(self) -> int:
        """Framework-enforced CLI main function"""
        parser = self.create_cli_parser()
        args = parser.parse_args()

        try:
            output = self.run_analysis(args.session, args.task, args.model)
            success_message = self.get_success_message(output)
            print(success_message)
            return 0
        except Exception as e:
            print(f"{self.get_worker_display_name()} failed: {e}")
            return 1

    # Abstract methods for worker-specific behavior

    @abstractmethod
    def execute_ai_analysis(
        self, session_id: str, task_description: str, model: str
    ) -> Any:
        """
        Execute worker-specific AI analysis.

        Must return a result object with an .output attribute containing the worker's output model.
        This is where the worker calls its specific agent with custom prompts and logic.
        """
        pass

    @abstractmethod
    def get_file_prefix(self) -> str:
        """Return file prefix for output files (e.g., 'analyzer', 'architect')"""
        pass

    @abstractmethod
    def get_worker_display_name(self) -> str:
        """Return human-readable worker name for CLI and logging"""
        pass

    @abstractmethod
    def get_worker_description(self) -> str:
        """Return worker description for CLI help"""
        pass

    @abstractmethod
    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return worker-specific event details for analysis_started event"""
        pass

    @abstractmethod
    def get_completion_event_details(self, output: T) -> Dict[str, Any]:
        """Return worker-specific event details for worker_completed event"""
        pass

    @abstractmethod
    def get_success_message(self, output: T) -> str:
        """Return worker-specific CLI success message"""
        pass

    def create_worker_specific_files(
        self, session_id: str, output: T, session_path: Path
    ) -> None:
        """
        Optional hook for worker-specific file creation beyond standard notes/JSON.

        Override this method if the worker needs to create additional files.
        Default implementation does nothing.
        """
        pass
