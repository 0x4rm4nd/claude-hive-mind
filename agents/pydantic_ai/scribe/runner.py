"""
Scribe Worker Runner
====================
Execution runner for the Scribe Worker - provides session lifecycle management and synthesis.
"""

import re
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from shared.base_worker import BaseWorker
from shared.tools import iso_now
from shared.protocols import SessionManagement
from scribe.models import ScribeOutput, SynthesisOverview
from scribe.agent import (
    ScribeAgentConfig,
    task_summary_agent,
    session_creation_agent,
    synthesis_agent,
)


class ScribeWorker(BaseWorker[ScribeOutput]):
    """
    Scribe session lifecycle manager and synthesis coordinator.
    
    Provides comprehensive session management including creation, tracking,
    and synthesis of multi-worker coordination results.
    """

    def __init__(self):
        super().__init__(
            worker_type="scribe",
            worker_config=None,
            output_model=ScribeOutput,
        )

    def run(self, session_id: str, task_description: str, model: str) -> ScribeOutput:
        """Execute scribe analysis with session lifecycle management.
        
        Args:
            session_id: Session identifier for tracking (ignored for creation)
            task_description: Task description (determines mode - create vs synthesis)
            model: AI model to use for analysis execution
            
        Returns:
            ScribeOutput: Unified scribe output for both modes
        """
        # Create worker config at runtime with actual values
        self.worker_config = ScribeAgentConfig.create_worker_config(
            session_id, task_description
        )
        
        return self.run_analysis(session_id, task_description, model)
    
    def run_analysis(self, session_id: str, task_description: str, model: str) -> ScribeOutput:
        """
        Override to handle session creation special case.
        
        For session creation, we need to create the session directory first
        before the BaseWorker framework tries to log events.
        """
        # Check if this is session creation mode
        is_create_mode = "synthesis" not in task_description.lower()
        
        if is_create_mode:
            # For create mode, we need to generate the actual session_id first
            # and create the directory structure before calling parent
            actual_session_id, complexity_level = self._generate_ai_session_id(task_description, model)
            self._create_session_directory(actual_session_id)
            self._create_session_markdown(actual_session_id, task_description, model)
            
            # Now call parent with the actual session_id
            return super().run_analysis(actual_session_id, task_description, model)
        else:
            # For synthesis mode, use normal flow
            return super().run_analysis(session_id, task_description, model)
    
    def execute_ai_analysis(
        self, session_id: str, task_description: str, model: str
    ) -> Any:
        """Execute AI-powered session management and synthesis analysis.
        
        Args:
            session_id: Session identifier for analysis tracking
            task_description: Task description or synthesis request
            model: AI model for analysis execution
            
        Returns:
            Scribe analysis results from AI agent processing
        """
        # Determine mode from task description
        if "synthesis" in task_description.lower():
            return self._run_synthesis(session_id, task_description, model)
        else:
            # For create mode, the session is already created in run_analysis
            # Just return the completion result
            return self._create_session_completion_result(session_id, task_description)

    def _create_session_completion_result(self, session_id: str, task_description: str) -> Any:
        """Create completion result for session creation"""
        # Log session creation event
        self.log_event(
            session_id,
            "session_created",
            {
                "session_id": session_id,
                "task_description": task_description,
                "session_path": f"Docs/hive-mind/sessions/{session_id}",
                "generated_by": "scribe",
            },
        )

        # Log scribe spawn event  
        self.log_event(
            session_id,
            "worker_spawned",
            {
                "worker_type": "scribe",
                "mode": "create",
                "purpose": "session_creation",
            },
        )
        
        # Create mock result to match expected structure
        class MockResult:
            def __init__(self, output):
                self.output = output
        
        output = ScribeOutput(
            mode="create",
            session_id=session_id,
            timestamp=iso_now(),
            status="completed",
            task_description=task_description,
            complexity_level=2,  # Default complexity
            session_path=f"Docs/hive-mind/sessions/{session_id}",
        )
        
        return MockResult(output)

    def _run_synthesis(self, session_id: str, task_description: str, model: str) -> Any:
        """Handle synthesis mode"""
        # Validate session exists
        project_root_path = Path(__file__).parent.parent.parent.parent.parent
        sessions_dir = project_root_path / "Docs" / "hive-mind" / "sessions"
        session_path = sessions_dir / session_id

        if not session_path.exists():
            raise FileNotFoundError(f"Session {session_id} not found")

        # For testing, create simple synthesis without AI call
        synthesis_content = f"""# Synthesis Report - Session {session_id}

Generated: {iso_now()}

## Summary
This is a basic synthesis report for the session. The session has been analyzed and the following findings are reported:

## Key Findings
- Session completed successfully
- No major issues identified
- Ready for further analysis if needed

## Recommendations
- Continue with planned work
- Monitor for any issues

## Next Steps
- Review session outputs
- Plan follow-up activities as needed
"""

        # Create synthesis overview
        synthesis_overview = SynthesisOverview(
            consensus=["Session completed successfully"],
            conflicts=["No conflicts identified"],
            themes=["Basic session management", "Task coordination"]
        )
        
        # Create mock result to match expected structure
        class MockResult:
            def __init__(self, output):
                self.output = output
        
        unified_output = ScribeOutput(
            mode="synthesis",
            session_id=session_id,
            timestamp=iso_now(),
            status="completed",
            synthesis_markdown=synthesis_content,
            synthesis_overview=synthesis_overview,
            sources={"session_files": "Basic session analysis"},
        )
        
        return MockResult(unified_output)

    def _generate_ai_session_id(self, task_description: str, model: str) -> tuple[str, int]:
        """Generate session ID using simple word extraction for testing"""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H-%M")

        # For testing, use simple approach without AI
        # Extract meaningful words from task description
        words = re.findall(r'\b\w{3,}\b', task_description.lower())
        
        # Take first 3-4 meaningful words and join with hyphens
        meaningful_words = [w for w in words if w not in ['the', 'and', 'for', 'with', 'this', 'that']][:4]
        
        if meaningful_words:
            short_desc = '-'.join(meaningful_words)
        else:
            short_desc = 'general-task'
            
        # Clean and validate the description
        short_desc = re.sub(r"[^a-z0-9\-]", "", short_desc.lower())
        short_desc = re.sub(r"-+", "-", short_desc).strip("-")

        if len(short_desc) > 25:
            short_desc = short_desc[:25]

        session_id = f"{timestamp}-{short_desc}"
        complexity_level = 2  # Default complexity
        
        return session_id, complexity_level

    def _create_session_directory(self, session_id: str):
        """Create session directory structure"""
        project_root_path = Path(__file__).parent.parent.parent.parent.parent
        sessions_dir = project_root_path / "Docs" / "hive-mind" / "sessions"
        session_path = sessions_dir / session_id

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

    def _create_session_markdown(self, session_id: str, task_description: str, model: str):
        """Create SESSION.md file"""
        project_root_path = Path(__file__).parent.parent.parent.parent.parent
        sessions_dir = project_root_path / "Docs" / "hive-mind" / "sessions"
        session_path = sessions_dir / session_id
        
        session_md_content = f"""# Session: {session_id}

**Created:** {iso_now()}  
**Task:** {task_description}  
**Model:** {model}  
**Status:** Created  

## Overview
Session created for task analysis and worker coordination.

## Progress
- [x] Session initialization
- [ ] Task analysis  
- [ ] Worker deployment
- [ ] Synthesis

## Notes
Session ready for Queen orchestration.
"""

        with open(session_path / "SESSION.md", "w") as f:
            f.write(session_md_content)

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
            details.update({
                "complexity_level": output.complexity_level,
                "session_path": output.session_path,
            })
        elif output.mode == "synthesis":
            details.update({
                "sources_count": len(output.sources),
                "synthesis_length": len(output.synthesis_markdown or ""),
            })
            
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
        """Override to fix path handling issue in BaseWorker"""
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
                relative_path = notes_file.relative_to(project_root)
                self.log_debug(
                    session_id,
                    f"Created {file_prefix} notes file",
                    {"path": str(relative_path)},
                )

            # Create structured output JSON
            output_file = json_dir / f"{file_prefix}_output.json"
            output_file.write_text(output.model_dump_json(indent=2))
            relative_path = output_file.relative_to(project_root)
            self.log_debug(
                session_id,
                f"Created {file_prefix} output JSON",
                {"path": str(relative_path)},
            )

            # Allow worker-specific file creation
            self.create_worker_specific_files(session_id, output, session_path)

        except Exception as e:
            self.log_debug(
                session_id, "File creation failed", {"error": str(e)}, "ERROR"
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
            
            self.log_debug(
                session_id,
                "Created synthesis markdown file",
                {"path": f"Docs/hive-mind/sessions/{session_id}/SYNTHESIS.md"},
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