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
        self.config = ProtocolConfig(
            {"session_id": session_id, "agent_name": self.worker_type}
        )

    def read_worker_prompt(self, session_id: str) -> str:
        """
        Read worker-specific prompt file for Pydantic AI agent.

        Returns the raw prompt content that will be used by the Pydantic AI agent.
        Claude Code agents handle the actual prompt file reading and processing.

        Args:
            session_id: Session identifier

        Returns:
            String containing the prompt content for the Pydantic AI agent
        """
        try:
            cfg = ProtocolConfig(
                {"session_id": session_id, "agent_name": self.worker_type}
            )

            self._prompt_protocol = WorkerManager(cfg.to_dict())
            prompt_content = self._prompt_protocol.read_prompt_file(self.worker_type)

            # Return the actual prompt content as string
            if isinstance(prompt_content, dict) and "prompt" in prompt_content:
                return prompt_content["prompt"]
            elif isinstance(prompt_content, str):
                return prompt_content
            else:
                return f"Perform {self.worker_type} analysis for the given task."

        except Exception as e:
            self.log_debug(
                f"Failed to read prompt file for {self.worker_type}",
                {"error": str(e)},
                "WARNING",
            )
            # Simple fallback prompt
            return f"Perform {self.worker_type} analysis for the given task."

    def validate_session(self, session_id: str) -> None:
        """Framework-enforced session validation"""
        try:
            if not SessionManagement.ensure_session_exists(session_id):
                raise ValueError(f"Session {session_id} does not exist or is invalid")
            self.log_debug("Session validation successful")
        except Exception as e:
            self.log_debug("Session validation failed", {"error": str(e)}, "ERROR")
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
                self.log_debug(
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
            self.log_debug(
                f"Created {file_prefix} output JSON",
                {"path": path_str},
            )

            # Allow worker-specific file creation
            self.create_worker_specific_files(session_id, output, session_path)

        except Exception as e:
            self.log_debug("File creation failed", {"error": str(e)}, "ERROR")
            raise

    def run_analysis(self, session_id: str, task_description: str, model: str) -> T:
        """
        Framework-enforced main execution flow.

        This method orchestrates the entire worker execution with protocol compliance
        while delegating worker-specific logic to abstract methods.
        """

        # Update session config IMMEDIATELY before validation so all logging uses correct session_id
        self.update_session_config(session_id)

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

            # Log completion with worker-specific details (session config already updated early)
            completion_details = self.get_completion_event_details(output)
            self.log_event("analysis_completed", completion_details)

            return output

        except Exception as e:
            self.log_debug(
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
        parser.add_argument("--task", help="Analysis task description (not needed for --setup/--output phases)")
        parser.add_argument(
            "--model", default="custom:max-subscription", help="AI model to use"
        )

        # Add mutually exclusive phase flags
        phase_group = parser.add_mutually_exclusive_group()
        phase_group.add_argument(
            "--setup",
            action="store_true",
            help="Execute Phase 1: Setup & Context Loading",
        )
        phase_group.add_argument(
            "--output",
            action="store_true",
            help="Execute Phase 3: Validation & Output Generation",
        )

        return parser

    def run_cli_main(self) -> int:
        """Framework-enforced CLI main function"""
        parser = self.create_cli_parser()
        args = parser.parse_args()

        try:
            # Validate task parameter based on execution mode
            if not (args.setup or args.output) and not args.task:
                print("❌ Error: --task is required when not using --setup or --output phases")
                return 1

            # Update session config for logging context
            self.update_session_config(args.session)

            # Log worker spawned event (single entry point for all phases)
            spawn_details = self.get_analysis_event_details(args.task or "phase-based-execution")

            # Determine which phase to execute and add phase info
            if args.setup:
                spawn_details["phase"] = "setup"
                self.log_event("worker_spawned", spawn_details)
                output = self.run_setup_phase(args.session, args.model)
                success_message = self.get_setup_success_message(output)
            elif args.output:
                spawn_details["phase"] = "output"
                self.log_event("worker_spawned", spawn_details)
                output = self.run_output_phase(args.session, args.model)
                success_message = self.get_output_success_message(output)
            else:
                # Default behavior - requires task
                spawn_details["phase"] = "analysis"
                self.log_event("worker_spawned", spawn_details)
                output = self.run_analysis(args.session, args.task, args.model)
                success_message = self.get_success_message(output)

            print(success_message)
            
            # Print output as JSON for CC Agent to parse
            print("WORKER_OUTPUT_JSON:")
            print(output.model_dump_json(indent=2))
            
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

    def run_setup_phase(self, session_id: str, model: str) -> T:
        """
        Execute Phase 1: Setup & Context Loading.

        Default implementation validates session and reads worker prompt.
        Can be overridden by workers for custom setup behavior.
        """
        # Update session config
        self.update_session_config(session_id)

        # Framework-enforced session validation
        self.validate_session(session_id)

        self.log_event(
            "setup_completed",
            {
                "task": task_description,
                "worker": self.worker_type,
            },
        )

        return self.create_setup_output(session_id)

    def run_output_phase(self, session_id: str, model: str) -> T:
        """
        Execute Phase 3: Validation & Output Generation.

        Default implementation validates existing analysis files and confirms completion.
        Can be overridden by workers for custom output validation.
        """
        # Update session config
        self.update_session_config(session_id)

        # Validate session exists
        self.validate_session(session_id)

        # Validate that analysis files exist
        self.validate_analysis_files(session_id)

        # Log completion
        self.log_event(
            "outputs_completed",
            {"validation_status": "completed"},
        )

        # Create a validation output
        return self.create_output_validation(session_id)

    def validate_analysis_files(self, session_id: str) -> None:
        """Validate that required analysis files exist from previous phases"""
        try:
            session_path = Path(SessionManagement.get_session_path(session_id))
            file_prefix = self.get_file_prefix()

            # Check for notes file
            notes_file = session_path / "workers" / "notes" / f"{file_prefix}_notes.md"
            if not notes_file.exists():
                self.log_debug(f"Notes file not found: {notes_file}", {}, "WARNING")

            # Check for JSON output file
            json_file = session_path / "workers" / "json" / f"{file_prefix}_output.json"
            if not json_file.exists():
                self.log_debug(
                    f"JSON output file not found: {json_file}", {}, "WARNING"
                )

            self.log_debug("Analysis file validation completed")

        except Exception as e:
            self.log_debug(
                "Analysis file validation failed", {"error": str(e)}, "WARNING"
            )

    @abstractmethod
    def create_setup_output(self, session_id: str) -> T:
        """Create minimal output object for setup phase with worker-specific output model."""
        pass

    @abstractmethod
    def create_output_validation(self, session_id: str) -> T:
        """Create validation output object for output phase with worker-specific output model."""
        pass

    def get_setup_success_message(self, output: T) -> str:
        """Return success message for setup phase. Override if needed."""
        return f"{self.get_worker_display_name()} setup phase completed successfully"

    def get_output_success_message(self, output: T) -> str:
        """Return success message for output phase. Override if needed."""
        return (
            f"{self.get_worker_display_name()} output validation completed successfully"
        )
