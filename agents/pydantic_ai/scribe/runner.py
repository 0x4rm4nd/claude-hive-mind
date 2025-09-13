"""
Scribe Worker Runner
====================
Execution runner for the Scribe Worker - provides session lifecycle management and synthesis.
"""

import sys
from pathlib import Path

from datetime import datetime
from typing import Dict, Any
from pydantic_ai import Agent
from pydantic_ai.models import ModelSettings
from typing import List
from scribe.models import TaskSummaryOutput
from shared.base_worker import BaseWorker
from shared.tools import iso_now
from shared.protocols import SessionManagement
from scribe.models import ScribeOutput, SynthesisOverview
from scribe.agent import ScribeAgentConfig

from shared.protocols.worker_prompt_templates import format_scribe_prompt

# Ensure imports work when run directly or from CLI
current_dir = Path(__file__).parent
pydantic_ai_root = current_dir.parent
if str(pydantic_ai_root) not in sys.path:
    sys.path.insert(0, str(pydantic_ai_root))


class ScribeWorker(BaseWorker):
    """
    Scribe session lifecycle manager and synthesis coordinator.

    Provides comprehensive session management including creation, tracking,
    and synthesis of multi-worker coordination results.
    """

    def __init__(self):
        super().__init__(
            worker_type="scribe",
            worker_config=None,
        )

        # Initialize path attributes
        self.project_root_path = Path(SessionManagement.detect_project_root())
        self.sessions_dir = self.project_root_path / "Docs" / "hive-mind" / "sessions"

    def run_creation(
        self, session_id: str, task_description: str, model: str
    ) -> ScribeOutput:
        """Execute session creation (called only by CLI --create mode)."""
        actual_session_id, complexity_level = self._generate_ai_session_id(
            task_description, model
        )
        self.worker_config = ScribeAgentConfig.create_worker_config(
            actual_session_id, task_description
        )
        self._create_session_directory(actual_session_id)
        self._create_session_markdown(
            actual_session_id, self.worker_config.task_description, model
        )

        return self._create_session_completion_result(
            actual_session_id, self.worker_config.task_description, complexity_level
        )

    def _create_session_completion_result(
        self, session_id: str, task_description: str, complexity_level: int
    ) -> ScribeOutput:
        """Create completion result for session creation"""
        self.update_session_config(session_id)
        self.log_event(
            "worker_spawned",
            {
                "worker_type": "scribe",
                "mode": "create",
                "purpose": "session_creation",
            },
            "INFO",
        )

        session_full_path = Path(SessionManagement.get_session_path(session_id))
        relative_session_path = str(
            session_full_path.relative_to(self.project_root_path)
        )

        # Log session creation event
        self.log_event(
            "session_created",
            {
                "session_id": session_id,
                "task_description": task_description,
                "session_path": relative_session_path,
                "generated_by": "scribe",
            },
            "INFO",
        )

        return ScribeOutput(
            mode="create",
            session_id=session_id,
            timestamp=iso_now(),
            status="completed",
            task_description=task_description,
            complexity_level=complexity_level,
            session_path=relative_session_path,
        )

    def run_setup_phase(self, session_id: str, model: str) -> ScribeOutput:
        """Phase 1: Setup & Data Collection for creative synthesis"""
        self.update_session_config(session_id)

        # Validate session exists
        project_root_path = Path(__file__).parent.parent.parent.parent.parent
        sessions_dir = project_root_path / "Docs" / "hive-mind" / "sessions"
        session_path = sessions_dir / session_id

        if not session_path.exists():
            raise FileNotFoundError(f"Session {session_id} not found")

        # Collect worker file paths for Claude Code
        worker_inventory = self._collect_worker_file_inventory(session_path)

        self._create_synthesis_prompt_file(session_id, session_path, worker_inventory)
        self._create_synthesis_template_file(session_id, session_path, worker_inventory)

        # Return setup output with file paths
        return ScribeOutput(
            mode="synthesis_setup",
            session_id=session_id,
            session_path=str(session_path),
            timestamp=iso_now(),
            status="setup_completed",
            worker_file_paths=worker_inventory["file_paths"],
            sources=worker_inventory["sources"],
        )

    def run_output_phase(self, session_id: str, model: str) -> ScribeOutput:
        """Phase 3: Validation & File Creation after Claude Code creative synthesis"""
        self.update_session_config(session_id)

        # Validate that synthesis files exist (created by Claude Code in Phase 2)
        session_path = self.sessions_dir / session_id
        synthesis_file = session_path / "SYNTHESIS.md"

        if not synthesis_file.exists():
            raise FileNotFoundError(
                f"Creative synthesis file not found: {synthesis_file}"
            )

        # Read the synthesis content created by Claude Code
        synthesis_content = synthesis_file.read_text()
        validation_result = self._validate_synthesis_completeness(synthesis_content)

        if not validation_result["valid"]:
            raise ValueError(
                f"Synthesis validation failed: {validation_result['errors']}"
            )

        # Create final synthesis overview
        synthesis_overview = SynthesisOverview(
            consensus=["Creative synthesis completed by Claude Code"],
            conflicts=validation_result.get("conflicts", []),
            themes=validation_result.get("themes", ["Creative architectural analysis"]),
        )

        # Create output files for synthesis mode
        try:
            self.create_output_files_base(
                session_id,
                ScribeOutput(
                    mode="synthesis",
                    session_id=session_id,
                    timestamp=iso_now(),
                    status="completed",
                    synthesis_markdown=synthesis_content,
                    synthesis_overview=synthesis_overview,
                    sources={
                        "synthesis_file": str(
                            synthesis_file.relative_to(self.project_root_path)
                        )
                    },
                ),
                self.get_file_prefix(),
            )
        except Exception as e:
            self.log_debug(
                f"File creation failed during output phase: {e}", level="ERROR"
            )

        # Return completed synthesis output
        return ScribeOutput(
            mode="synthesis",
            session_id=session_id,
            timestamp=iso_now(),
            status="completed",
            synthesis_markdown=synthesis_content,
            synthesis_overview=synthesis_overview,
            sources={
                "synthesis_file": str(
                    synthesis_file.relative_to(self.project_root_path)
                )
            },
        )

    def _collect_worker_file_inventory(self, session_path: Path) -> Dict[str, Any]:
        """Collect file paths for Claude Code creative analysis"""

        workers_dir = session_path / "workers"
        notes_dir = workers_dir / "notes"
        json_dir = workers_dir / "json"

        print(notes_dir, json_dir)

        file_paths = []
        sources = {}
        worker_count = 0

        # Collect notes files
        if notes_dir.exists():
            for notes_file in notes_dir.glob("*_notes.md"):
                worker_type = notes_file.stem.replace("_notes", "")
                file_paths.append(str(notes_file))
                sources[f"{worker_type}_notes"] = str(notes_file)
                worker_count += 1

        # Collect JSON files
        if json_dir.exists():
            for json_file in json_dir.glob("*_output.json"):
                worker_type = json_file.stem.replace("_output", "")
                file_paths.append(str(json_file))
                sources[f"{worker_type}_json"] = str(json_file)

        return {
            "file_paths": file_paths,
            "sources": sources,
            "worker_count": worker_count,
            "session_path": str(session_path),
        }

    def _validate_synthesis_completeness(
        self, synthesis_content: str
    ) -> Dict[str, Any]:
        """Validate that Claude Code synthesis is complete and has no placeholders"""

        errors = []

        # Validate placeholder patterns
        placeholder_errors = self._check_placeholder_patterns(synthesis_content)
        errors.extend(placeholder_errors)

        # Validate content completeness
        completeness_errors = self._check_content_completeness(synthesis_content)
        errors.extend(completeness_errors)

        # Extract content analysis
        themes = self._extract_content_themes(synthesis_content)
        conflicts = self._extract_content_conflicts(synthesis_content)

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "themes": themes,
            "conflicts": conflicts,
        }

    def _check_placeholder_patterns(self, content: str) -> List[str]:
        """Check for remaining placeholder patterns"""
        errors = []
        content_lower = content.lower()

        # Template variable patterns
        if "{" in content and "}" in content:
            errors.append("Found template variable placeholders")

        # Common placeholder keywords
        placeholder_keywords = [
            "todo",
            "fixme",
            "placeholder",
            "analysis needed",
            "content here",
        ]
        for keyword in placeholder_keywords:
            if keyword in content_lower:
                errors.append(f"Found placeholder keyword: {keyword}")

        # Markdown placeholder sections
        placeholder_sections = ["## [", "### ["]
        for section in placeholder_sections:
            if section in content:
                errors.append("Found incomplete markdown sections")

        return errors

    def _check_content_completeness(self, content: str) -> List[str]:
        """Check content completeness and quality"""
        errors = []

        # Minimum length check
        min_length = 1000
        if len(content) < min_length:
            errors.append(
                f"Content too short ({len(content)} chars, minimum {min_length})"
            )

        # Section completeness check
        required_sections = ["executive summary", "critical issues", "recommendations"]
        content_lower = content.lower()

        missing_sections = [
            section for section in required_sections if section not in content_lower
        ]

        if missing_sections:
            errors.append(f"Missing required sections: {', '.join(missing_sections)}")

        return errors

    def _extract_content_themes(self, content: str) -> List[str]:
        """Extract themes based on content analysis"""
        content_lower = content.lower()
        themes = []

        theme_mapping = {
            "security": "Security Analysis",
            "performance": "Performance Optimization",
            "architecture": "Architecture Assessment",
            "devops": "Infrastructure & DevOps",
            "infrastructure": "Infrastructure & DevOps",
        }

        for keyword, theme in theme_mapping.items():
            if keyword in content_lower and theme not in themes:
                themes.append(theme)

        return themes if themes else ["Comprehensive Analysis"]

    def _extract_content_conflicts(self, content: str) -> List[str]:
        """Extract conflicts and priority indicators"""
        content_lower = content.lower()
        conflicts = []

        conflict_indicators = {
            "conflict": "Cross-domain conflicts identified",
            "priority": "Prioritization required",
            "tradeoff": "Technical tradeoffs identified",
            "dependency": "Implementation dependencies mapped",
        }

        for indicator, description in conflict_indicators.items():
            if indicator in content_lower and description not in conflicts:
                conflicts.append(description)

        return conflicts if conflicts else ["No major conflicts"]

    def _generate_ai_session_id(
        self, task_description: str, model: str
    ) -> tuple[str, int]:
        """Generate session ID and complexity using AI assessment"""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H-%M")

        try:
            if model.startswith("custom:"):
                scribe_prompt = f"""Using the Scribe Agent, generate a session ID and complexity assessment for this task: "{task_description}" """

                # Use ModelSettings to pass outputStyle settings
                model_settings = ModelSettings(
                    extra_headers={"X-Settings": r'{"outputStyle": "scribe-json"}'}
                )

                temp_agent = Agent(
                    model=model,
                    output_type=TaskSummaryOutput,
                    model_settings=model_settings,
                    # NO system prompt for custom models - let Docker agent handle it
                )

                complexity_data = temp_agent.run_sync(scribe_prompt)
            else:
                temp_agent = Agent(
                    model=model,
                    output_type=TaskSummaryOutput,
                    system_prompt=ScribeAgentConfig.get_system_prompt(),
                )

                complexity_data = temp_agent.run_sync(task_description)

            session_id = f"{timestamp}-{complexity_data.output.short_description}"
            complexity_level = complexity_data.output.complexity_level

            return session_id, complexity_level

        except Exception as e:
            raise RuntimeError(
                f"CRITICAL: AI model '{model}' failed for session generation.\n"
                f"\n"
                f"For custom:* models, ensure Claude API service is running:\n"
                f"cd .claude/claude-api-service && docker-compose up -d\n"
                f"\n"
                f"For custom models (custom:max-subscription, custom:claude-opus-4), ensure Docker service is running.\n"
                f"\n"
                f"Original error: {e}"
            )

    def _create_session_directory(self, session_id: str):
        """Create session directory structure"""
        session_path = self.sessions_dir / session_id

        session_path.mkdir(parents=True, exist_ok=True)
        (session_path / "workers").mkdir(exist_ok=True)
        (session_path / "workers" / "notes").mkdir(exist_ok=True)
        (session_path / "workers" / "prompts").mkdir(exist_ok=True)
        (session_path / "workers" / "json").mkdir(exist_ok=True)

        # Create session files - only EVENTS.jsonl, DEBUG.jsonl, BACKLOG.jsonl (no STATE.json)
        events_file = session_path / "EVENTS.jsonl"
        events_file.touch()
        debug_file = session_path / "DEBUG.jsonl"
        debug_file.touch()
        backlog_file = session_path / "BACKLOG.jsonl"
        backlog_file.touch()

    def _create_session_markdown(
        self, session_id: str, task_description: str, model: str
    ):
        """Create SESSION.md file"""
        session_path = self.sessions_dir / session_id

        session_md_content = self._load_template(
            "session.md",
            {
                "session_id": session_id,
                "timestamp": iso_now(),
                "task_description": task_description,
                "model": model,
            },
        )

        with open(session_path / "SESSION.md", "w") as f:
            f.write(session_md_content)

    def _create_synthesis_prompt_file(
        self, session_id: str, session_path: Path, worker_inventory: Dict[str, Any]
    ) -> None:
        """Create synthesis prompt file for Claude Code Phase 2 analysis"""

        # Generate the synthesis prompt
        synthesis_prompt = format_scribe_prompt(session_id, worker_inventory)

        # Write prompt to session's workers/prompts directory
        prompts_dir = session_path / "workers" / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)

        prompt_file = prompts_dir / "scribe-synthesis.prompt"
        with open(prompt_file, "w") as f:
            f.write(synthesis_prompt)

        # Log prompt file creation
        project_root = Path(SessionManagement.detect_project_root())
        relative_path = prompt_file.relative_to(project_root)
        log_path = str(relative_path)

        self.log_debug(
            "Created synthesis prompt file for Claude Code",
            {
                "path": log_path,
                "worker_files_count": len(worker_inventory["file_paths"]),
            },
        )

    def _create_synthesis_template_file(
        self, session_id: str, session_path: Path, worker_inventory: Dict[str, Any]
    ) -> None:
        """Create SYNTHESIS.md template file for Claude Code to fill in during Phase 2"""

        template_variables = {
            "session_id": session_id,
            "timestamp": iso_now(),
            "workers_count": str(worker_inventory["worker_count"]),
        }

        # Load and populate template using proper template engine
        synthesis_content = self._load_template(
            "synthesis_report.md", template_variables
        )

        # Write template to session directory
        synthesis_file = session_path / "SYNTHESIS.md"
        with open(synthesis_file, "w") as f:
            f.write(synthesis_content)

        # Log template creation
        try:
            from shared.protocols import SessionManagement

            project_root = Path(SessionManagement.detect_project_root())
            relative_path = synthesis_file.relative_to(project_root)
            log_path = str(relative_path)
        except Exception:
            log_path = str(synthesis_file)

        self.log_debug(
            "Created synthesis template file for Claude Code",
            {
                "path": log_path,
                "ready_for_creative_analysis": True,
            },
        )

    def _load_template(self, template_name: str, variables: Dict[str, str]) -> str:
        """Load template file and substitute variables.

        Args:
            template_name: Name of template file in templates directory
            variables: Dictionary of variables to substitute in template

        Returns:
            Template content with variables substituted
        """
        template_path = Path(__file__).parent / "templates" / template_name
        try:
            with open(template_path, "r") as f:
                template_content = f.read()
            return template_content.format(**variables)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Template file {template_name} not found in templates directory"
            )
        except KeyError as e:
            raise ValueError(f"Missing variable {e} for template {template_name}")

    def get_file_prefix(self) -> str:
        """Return file prefix for scribe output files.

        Returns:
            File prefix for scribe output files
        """
        return "scribe"

    def get_worker_display_name(self) -> str:
        """Return human-readable name for CLI display.

        Returns:
            Display name for the scribe worker
        """
        return "Scribe Worker"

    def get_worker_description(self) -> str:
        """Return description for CLI help and documentation.

        Returns:
            Brief description of scribe capabilities
        """
        return "Session Lifecycle Management and Synthesis"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return event details when scribe analysis starts.

        Args:
            task_description: Scribe analysis task description

        Returns:
            Event details for analysis started logging
        """
        mode = "synthesis" if "synthesis" in task_description.lower() else "create"
        return {
            "worker": "scribe",
            "mode": mode,
            "task": task_description,
            "focus_areas": ["session_management", "coordination", "synthesis"],
        }

    def get_completion_event_details(self, output: ScribeOutput) -> Dict[str, Any]:
        """Return event details when scribe analysis completes.

        Args:
            output: Scribe analysis output with session or synthesis info

        Returns:
            Event details for analysis completion logging
        """
        details = {
            "worker": "scribe",
            "mode": output.mode,
            "session_id": output.session_id,
            "status": output.status,
        }

        if output.mode == "create":
            details.update(
                {
                    "complexity_level": output.complexity_level,
                    "session_path": output.session_path,
                }
            )
        elif output.mode == "synthesis":
            details.update(
                {
                    "sources_count": len(output.sources),
                    "synthesis_length": len(output.synthesis_markdown or ""),
                }
            )

        return details

    def get_success_message(self, output: ScribeOutput) -> str:
        """Return success message with scribe analysis summary.

        Args:
            output: Scribe analysis output with session or synthesis metrics

        Returns:
            Success message with key scribe analysis results
        """
        if output.mode == "create":
            return (
                f"Session created successfully. Session ID: {output.session_id}, "
                f"Complexity: {output.complexity_level}, Path: {output.session_path}"
            )
        elif output.mode == "synthesis_setup":
            return (
                f"Phase 1 setup completed for session {output.session_id}. "
                f"Worker files: {len(output.worker_file_paths or [])}, "
                f"Ready for Claude Code creative synthesis"
            )
        elif output.mode == "synthesis":
            return (
                f"Synthesis completed for session {output.session_id}. "
                f"Content length: {len(output.synthesis_markdown or '')}, "
                f"Sources: {len(output.sources)}"
            )
        else:
            return f"Scribe analysis completed for session {output.session_id}"

    def create_output_files_base(
        self, session_id: str, output: ScribeOutput, file_prefix: str
    ) -> None:
        """Override to skip file creation for session creation mode"""
        if output.mode == "create":
            # Only create worker-specific files (SESSION.md, etc.) but no JSON/notes output
            session_path = Path(SessionManagement.get_session_path(session_id))
            self.create_worker_specific_files(session_id, output, session_path)
            return

        # For synthesis mode, create full output files
        try:
            session_path = Path(SessionManagement.get_session_path(session_id))
            notes_dir = session_path / "workers" / "notes"
            json_dir = session_path / "workers" / "json"
            notes_dir.mkdir(parents=True, exist_ok=True)
            json_dir.mkdir(parents=True, exist_ok=True)

            # Create notes file if content provided
            if hasattr(output, "notes_markdown") and output.notes_markdown:
                notes_file = notes_dir / f"{file_prefix}_notes.md"
                notes_file.write_text(output.notes_markdown)
                relative_path = notes_file.relative_to(self.project_root_path)
                self.log_debug(
                    f"Created {file_prefix} notes file",
                    {"path": str(relative_path)},
                )

            # Create structured output JSON
            output_file = json_dir / f"{file_prefix}_output.json"
            output_file.write_text(output.model_dump_json(indent=2))
            relative_path = output_file.relative_to(self.project_root_path)
            self.log_debug(
                f"Created {file_prefix} output JSON",
                {"path": str(relative_path)},
            )

            # Allow worker-specific file creation
            self.create_worker_specific_files(session_id, output, session_path)

        except Exception as e:
            self.log_debug(
                "File creation failed",
                {"error": str(e)},
                "ERROR",
            )
            raise

    def create_worker_specific_files(
        self, session_id: str, output: ScribeOutput, session_path: Path
    ) -> None:
        """Create additional scribe-specific output files.

        Args:
            session_id: Session identifier
            output: Scribe analysis output data
            session_path: Path to session directory
        """
        # For synthesis mode, create the synthesis markdown file
        if output.mode == "synthesis" and output.synthesis_markdown:
            synthesis_file = session_path / "SYNTHESIS.md"
            with open(synthesis_file, "w") as f:
                f.write(output.synthesis_markdown)

            relative_path = synthesis_file.relative_to(self.project_root_path)

            self.log_debug(
                "Created synthesis markdown file",
                {
                    "path": str(relative_path),
                },
            )


def main():
    """CLI entry point for scribe worker execution.

    Returns:
        Exit code from worker execution
    """
    worker = ScribeWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
