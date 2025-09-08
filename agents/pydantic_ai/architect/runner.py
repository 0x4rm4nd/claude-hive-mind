"""
Architect Worker Runner
=======================
Execution runner for the Architect Worker - provides system design and architecture analysis.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Minimal path setup to enable shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.base_worker import BaseWorker
from shared.models import WorkerSummary, WorkerOutput
from shared.tools import iso_now
from shared.protocols.session_management import SessionManagement


class ArchitectWorker(BaseWorker):
    """
    System design and architecture analysis worker.

    Evaluates system architecture, provides design recommendations, and assesses
    technology stack decisions with scalability and modernization guidance.
    """

    def __init__(self):
        super().__init__(
            worker_type="architect-worker",
            worker_config=None,
        )


    def get_file_prefix(self) -> str:
        """Return file prefix for architecture output files.

        Returns:
            File prefix for architect output files
        """
        return "architect"

    def get_worker_display_name(self) -> str:
        """Return human-readable name for CLI display.

        Returns:
            Display name for the architect worker
        """
        return "Architect Worker"

    def get_worker_description(self) -> str:
        """Return description for CLI help and documentation.

        Returns:
            Brief description of architect capabilities
        """
        return "System Design and Architecture Analysis"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return event details when architectural analysis starts.

        Args:
            task_description: Architecture analysis task description

        Returns:
            Event details for analysis started logging
        """
        return {
            "task": task_description,
            "analysis_type": "architecture_analysis",
        }

    def get_completion_event_details(self, output: WorkerOutput) -> Dict[str, Any]:
        """Return event details when architectural analysis completes.

        Args:
            output: Architecture analysis output with recommendations

        Returns:
            Event details for analysis completion logging
        """
        return {
            "duration": "calculated",
            "recommendations_count": len(output.architectural_recommendations),
            "technology_decisions_count": len(output.technology_decisions),
            "status": output.status,
        }

    def get_success_message(self, output: WorkerOutput) -> str:
        """Return success message with architectural analysis summary.

        Args:
            output: Architecture analysis output with scores and recommendations

        Returns:
            Success message with key architecture metrics
        """
        return f"Architecture analysis completed successfully. Maturity score: {output.architectural_maturity_score}, Recommendations: {len(output.architectural_recommendations)}, Technology decisions: {len(output.technology_decisions)}"


    def create_output_validation(self, session_id: str) -> WorkerOutput:
        """Create validation output object for output phase."""

        return WorkerOutput(
            session_id=session_id,
            worker="architect-worker",
            timestamp=iso_now(),
            status="completed",
            summary=WorkerSummary(
                key_findings=["Output validation phase completed"],
                critical_issues=[],
                recommendations=[
                    "Architecture analysis workflow completed successfully"
                ],
            ),
            current_architecture_assessment="Validation phase completed",
            architectural_recommendations=[],
            technology_decisions=[],
            notes_markdown="# Architect Worker Validation Phase\n\nOutput validation completed.\n\nArchitecture analysis files validated and confirmed complete.",
            config={},
        )

    def create_worker_specific_files(
        self, session_id: str, output: WorkerOutput, session_path: Path
    ) -> None:
        """Create additional architect-specific output files.

        Args:
            session_id: Session identifier
            output: Architecture analysis output data
            session_path: Path to session directory
        """
        # Architect worker uses standard file creation - no additional files needed
        pass

    def get_setup_output_fields(self) -> Dict[str, Any]:
        """Return architect-specific fields for setup output."""
        return {
            'current_architecture_assessment': "Setup phase - assessment pending",
            'architectural_recommendations': [],
            'technology_decisions': [],
        }


def main():
    """CLI entry point for architect worker execution.

    Returns:
        Exit code from worker execution
    """
    worker = ArchitectWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
