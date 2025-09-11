"""
Test Worker Runner
==================
Execution runner for the Test Worker - provides testing strategy and quality assurance analysis.
"""

import sys
from pathlib import Path
from typing import Dict, Any

# Minimal path setup to enable shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.base_worker import BaseWorker
from shared.models import WorkerOutput


class TestWorker(BaseWorker):
    """
    Testing strategy and quality assurance analysis worker.

    Analyzes codebases for test coverage, automation frameworks, and quality metrics.
    Provides detailed findings with actionable recommendations and coverage ratings.
    """

    def __init__(self):
        super().__init__(
            worker_type="test-worker",
            worker_config=None,
        )

    def get_file_prefix(self) -> str:
        """Return file prefix for testing output files.

        Returns:
            File prefix for test output files
        """
        return "test"

    def get_worker_display_name(self) -> str:
        """Return human-readable name for CLI display.

        Returns:
            Display name for the test worker
        """
        return "Test Worker"

    def get_worker_description(self) -> str:
        """Return description for CLI help and documentation.

        Returns:
            Brief description of test worker capabilities
        """
        return "Testing and Quality Assurance"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return event details when testing analysis starts.

        Args:
            task_description: Testing analysis task description

        Returns:
            Event details for analysis started logging
        """
        return {
            "task": task_description,
            "analysis_type": "testing_coverage_quality",
        }

    def get_completion_event_details(self, output: WorkerOutput) -> Dict[str, Any]:
        """Return event details when testing analysis completes.

        Args:
            output: Testing analysis output with findings and metrics

        Returns:
            Event details for analysis completion logging
        """
        return {
            "duration": "calculated",
            "metrics": output.metrics.model_dump(),
            "status": output.status,
        }

    def get_success_message(self, output: WorkerOutput) -> str:
        """Return success message with testing analysis summary.

        Args:
            output: Testing analysis output with scores and findings

        Returns:
            Success message with key testing analysis metrics
        """
        return f"Testing analysis completed successfully. Files analyzed: {output.metrics.items_analyzed}, Issues found: {output.metrics.issues_found}"


def main():
    """CLI entry point for test worker execution.

    Returns:
        Exit code from worker execution
    """
    worker = TestWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
