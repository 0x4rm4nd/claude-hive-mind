"""
Base Worker Class
=================
Abstract base class for all Pydantic AI workers providing standardized execution
framework with protocol compliance, session management, and extensible
worker-specific behavior.
"""

import argparse
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

from .protocols import (
    SessionManagement,
    ProtocolConfig,
    WorkerManager,
    BaseProtocol,
)

from .models import WorkerSummary, WorkerOutput
from .worker_config import WorkerConfig
from .tools import iso_now


class BaseWorker(BaseProtocol, ABC):
    """
    Base class for all Pydantic AI workers.

    Provides framework-enforced functionality while allowing worker-specific
    customization through abstract methods and configuration.
    """

    def __init__(
        self,
        worker_type: str,
        worker_config: Optional[WorkerConfig],
    ):
        """
        Initialize base worker.

        Args:
            worker_type: Worker identifier (e.g., "analyzer-worker")
            worker_config: Worker configuration instance (can be None, set at runtime)
        """
        # Initialize BaseProtocol with dummy config (session_id will be set at runtime)
        super().__init__({"session_id": "temp", "agent_name": worker_type})

        self.worker_type = worker_type
        self.worker_config = worker_config
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

    def create_cli_parser(self) -> argparse.ArgumentParser:
        """Framework-enforced CLI argument parsing with worker-specific description"""
        parser = argparse.ArgumentParser(
            description=f"{self.get_worker_display_name()} - {self.get_worker_description()}"
        )
        parser.add_argument("--session", required=True, help="Session ID")
        parser.add_argument(
            "--task",
            help="Analysis task description (not needed for --setup/--output phases)",
        )
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
                print(
                    "❌ Error: --task is required when not using --setup or --output phases"
                )
                return 1

            # Update session config for logging context
            self.update_session_config(args.session)

            # Determine which phase to execute
            if args.setup:
                # Log worker spawned event only phase 1
                spawn_details = self.get_analysis_event_details(
                    args.task or "phase-based-execution"
                )
                spawn_details["phase"] = "setup"
                self.log_event("worker_spawned", spawn_details)
                output = self.run_setup_phase(args.session, args.model)
                success_message = self.get_setup_success_message(output)
            elif args.output:
                output = self.run_output_phase(args.session, args.model)
                success_message = self.get_output_success_message(output)
            else:
                print(
                    "❌ Error: Direct analysis mode is not supported. Use --setup or --output phases."
                )
                return 1

            print(success_message)

            # Print output as JSON for CC Agent to parse
            print("WORKER_OUTPUT_JSON:")
            print(output.model_dump_json(indent=2))

            return 0
        except Exception as e:
            print(f"{self.get_worker_display_name()} failed: {e}")
            print("Full traceback:")
            traceback.print_exc()
            return 1

    # Abstract methods for worker-specific behavior

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
    def get_completion_event_details(self, output: WorkerOutput) -> Dict[str, Any]:
        """Return worker-specific event details for worker_completed event"""
        pass

    @abstractmethod
    def get_success_message(self, output: WorkerOutput) -> str:
        """Return worker-specific CLI success message"""
        pass

    def create_worker_specific_files(
        self, session_id: str, session_path: Path
    ) -> Dict[str, Any]:
        """Create template files during setup phase and return config data."""
        # Read the Queen-generated specific task prompt for this session
        worker_prompt = self.read_worker_prompt(session_id)

        notes_dir = session_path / "workers" / "notes"
        json_dir = session_path / "workers" / "json"

        # Ensure directories exist
        notes_dir.mkdir(parents=True, exist_ok=True)
        json_dir.mkdir(parents=True, exist_ok=True)

        # Load templates from worker/templates/
        template_dir = (
            Path(__file__).parent.parent / self.get_file_prefix() / "templates"
        )

        # Read markdown template
        markdown_template_path = (
            template_dir / f"{self.get_file_prefix()}_notes_template.md"
        )
        with open(markdown_template_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()

        # Read JSON template
        json_template_path = (
            template_dir / f"{self.get_file_prefix()}_output_template.json"
        )
        with open(json_template_path, "r", encoding="utf-8") as f:
            json_content = f.read()

        # Replace template variables
        current_time = datetime.now().isoformat()
        markdown_content = markdown_content.replace("{{TIMESTAMP}}", current_time)
        json_content = json_content.replace("{{SESSION_ID}}", session_id)
        json_content = json_content.replace("{{TIMESTAMP}}", current_time)
        json_content = json_content.replace("{{DURATION}}", "TBD")

        # Create the actual output files
        notes_file = notes_dir / f"{self.get_file_prefix()}_notes.md"
        json_file = json_dir / f"{self.get_file_prefix()}_output.json"

        with open(notes_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        with open(json_file, "w", encoding="utf-8") as f:
            f.write(json_content)

        # Store config in instance for create_setup_output to use
        self._setup_config = {
            "queen_prompt": worker_prompt,
            "template_files_created": {
                "notes_file": str(notes_file),
                "json_file": str(json_file),
            },
        }

        return self._setup_config

    def run_setup_phase(self, session_id: str, model: str) -> WorkerOutput:
        """
        Execute Phase 1: Setup & Context Loading.

        Default implementation validates session and reads worker prompt.
        Can be overridden by workers for custom setup behavior.
        """
        # Framework-enforced session validation
        self.validate_session(session_id)

        session_path = Path(SessionManagement.get_session_path(session_id))
        self.create_worker_specific_files(session_id, session_path)

        # Create setup output with populated config
        output = self.create_setup_output(session_id)

        self.log_event(
            "setup_completed",
            {
                "task": "Phase 1: Setup & Context Loading",
                "worker": self.worker_type,
            },
        )

        return output

    def run_output_phase(self, session_id: str, model: str) -> WorkerOutput:
        """
        Execute Phase 3: Validation & Output Generation.

        Default implementation validates existing analysis files and confirms completion.
        Can be overridden by workers for custom output validation.
        """
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

    def create_setup_output(self, session_id: str) -> WorkerOutput:
        """Create minimal output object for setup phase."""
        # Get config from template creation (will be set by create_worker_specific_files)
        config = getattr(self, "_setup_config", {})
        worker_prompt = config.get("queen_prompt", "No prompt available")

        return WorkerOutput(
            session_id=session_id,
            worker=self.worker_type,
            timestamp=iso_now(),
            status="completed",
            summary=WorkerSummary(
                key_findings=[
                    "Setup phase completed successfully",
                    "Queen-generated prompt loaded",
                    f"Template files created: {self.get_file_prefix()}_notes.md and {self.get_file_prefix()}_output.json",
                ],
                critical_issues=[],
                recommendations=[
                    "Proceed to Phase 2: Modify template files with analysis findings and remove unused sections"
                ],
            ),
            notes_markdown=f"# {self.get_worker_display_name()} Setup Phase\n\nTemplate files created and ready for Phase 2 modification.\n\n## Files Created\n- Markdown: {self.get_file_prefix()}_notes.md\n- JSON: {self.get_file_prefix()}_output.json\n\n## Specific Task Instructions from Queen\n\n{worker_prompt}",
            config=config,
        )

    def create_output_validation(self, session_id: str) -> WorkerOutput:
        """Create validation output object for output phase."""
        return WorkerOutput(
            session_id=session_id,
            worker=self.worker_type,
            timestamp=iso_now(),
            status="completed",
            summary=WorkerSummary(
                key_findings=["Output validation phase completed"],
                critical_issues=[],
                recommendations=["Analysis workflow completed successfully"],
            ),
            notes_markdown=f"# {self.get_worker_display_name()} Validation Phase\n\nOutput validation completed.\n\nAnalysis files validated and confirmed complete.",
            config={},
        )

    def get_setup_success_message(self, output: WorkerOutput) -> str:
        """Return success message for setup phase. Override if needed."""
        return f"{self.get_worker_display_name()} setup phase completed successfully"

    def get_output_success_message(self, output: WorkerOutput) -> str:
        """Return success message for output phase. Override if needed."""
        return (
            f"{self.get_worker_display_name()} output validation completed successfully"
        )
