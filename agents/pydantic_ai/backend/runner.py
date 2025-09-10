"""
Backend Worker Runner
=====================
Execution runner for the Backend Worker - provides API development and database design analysis.
"""

import sys
from pathlib import Path
from typing import Dict, Any

# Minimal path setup to enable shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.base_worker import BaseWorker
from shared.models import WorkerOutput


class BackendWorker(BaseWorker):
    """
    Backend API development and database design worker.

    Provides comprehensive analysis for API design, database schema, business logic,
    security implementation, and performance optimization guidance.
    """

    def __init__(self):
        super().__init__(
            worker_type="backend-worker",
            worker_config=None,
        )

    def get_file_prefix(self) -> str:
        """Return file prefix for backend output files.

        Returns:
            File prefix for backend output files
        """
        return "backend"

    def get_worker_display_name(self) -> str:
        """Return human-readable name for CLI display.

        Returns:
            Display name for the backend worker
        """
        return "Backend Worker"

    def get_worker_description(self) -> str:
        """Return description for CLI help and documentation.

        Returns:
            Brief description of backend capabilities
        """
        return "API Development and Database Design"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return event details when backend analysis starts.

        Args:
            task_description: Backend analysis task description

        Returns:
            Event details for analysis started logging
        """
        return {
            "worker": "backend-worker",
            "task": task_description,
            "focus_areas": ["api_design", "database_schema", "security", "performance"],
        }

    def get_completion_event_details(self, output: WorkerOutput) -> Dict[str, Any]:
        """Return event details when backend analysis completes.

        Args:
            output: Backend analysis output with API and database metrics

        Returns:
            Event details for analysis completion logging
        """
        return {
            "worker": "backend-worker",
            "status": output.status,
        }

    def get_success_message(self, output: WorkerOutput) -> str:
        """Return success message with backend analysis summary.

        Args:
            output: Backend analysis output with API and database metrics

        Returns:
            Success message with key backend analysis results
        """
        return f"Backend analysis completed successfully. Status: {output.status}"


def main():
    """CLI entry point for backend worker execution.

    Returns:
        Exit code from worker execution
    """
    worker = BackendWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
