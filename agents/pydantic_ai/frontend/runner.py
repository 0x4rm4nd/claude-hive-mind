"""
Frontend Worker Runner
======================
Execution runner for the Frontend Worker - provides UI/UX implementation and component architecture analysis.
"""

import sys
from pathlib import Path
from typing import Dict, Any

# Minimal path setup to enable shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.base_worker import BaseWorker
from shared.models import WorkerOutput


class FrontendWorker(BaseWorker):
    """
    Frontend UI/UX implementation and component architecture worker.

    Analyzes codebases for component architecture, performance optimization,
    accessibility compliance, and user experience patterns. Provides detailed
    findings with actionable recommendations and implementation guidance.
    """

    def __init__(self):
        super().__init__(
            worker_type="frontend-worker",
            worker_config=None,
        )


    def get_file_prefix(self) -> str:
        """Return file prefix for analysis output files.

        Returns:
            File prefix for frontend output files
        """
        return "frontend"

    def get_worker_display_name(self) -> str:
        """Return human-readable name for CLI display.

        Returns:
            Display name for the frontend worker
        """
        return "Frontend Worker"

    def get_worker_description(self) -> str:
        """Return description for CLI help and documentation.

        Returns:
            Brief description of frontend capabilities
        """
        return "Frontend Development and User Experience Analysis"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return event details when analysis starts.

        Args:
            task_description: Analysis task description

        Returns:
            Event details for analysis started logging
        """
        return {
            "task": task_description,
            "analysis_type": "frontend_component_performance_ux",
        }

    def get_completion_event_details(self, output: WorkerOutput) -> Dict[str, Any]:
        """Return event details when analysis completes.

        Args:
            output: Analysis output with findings and metrics

        Returns:
            Event details for analysis completion logging
        """
        return {
            "duration": "calculated",
            "metrics": output.metrics.model_dump(),
            "status": output.status,
        }

    def get_success_message(self, output: WorkerOutput) -> str:
        """Return success message with analysis summary.

        Args:
            output: Analysis output with scores and findings

        Returns:
            Success message with key analysis metrics
        """
        return f"Frontend analysis completed successfully. Components analyzed: {output.metrics.items_analyzed}, Issues found: {output.metrics.issues_found}"


def main():
    """CLI entry point for frontend worker"""
    worker = FrontendWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
