"""
DevOps Worker Runner
====================
Execution runner for the DevOps Worker - provides infrastructure, deployment, and CI/CD analysis.
"""

import sys
from pathlib import Path
from typing import Dict, Any

# Minimal path setup to enable shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.base_worker import BaseWorker
from shared.models import WorkerOutput


class DevOpsWorker(BaseWorker):
    """
    Infrastructure, deployment, and CI/CD analysis worker.

    Provides comprehensive DevOps analysis including infrastructure design,
    deployment strategies, monitoring setup, and CI/CD pipeline optimization.
    """

    def __init__(self):
        super().__init__(
            worker_type="devops-worker",
            worker_config=None,
        )

    def get_file_prefix(self) -> str:
        """Return file prefix for devops output files.

        Returns:
            File prefix for devops output files
        """
        return "devops"

    def get_worker_display_name(self) -> str:
        """Return human-readable name for CLI display.

        Returns:
            Display name for the devops worker
        """
        return "DevOps Worker"

    def get_worker_description(self) -> str:
        """Return description for CLI help and documentation.

        Returns:
            Brief description of devops capabilities
        """
        return "Infrastructure and Deployment Operations"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return event details when devops analysis starts.

        Args:
            task_description: DevOps analysis task description

        Returns:
            Event details for analysis started logging
        """
        return {
            "worker": "devops-worker",
            "task": task_description,
            "focus_areas": ["infrastructure", "deployment", "monitoring", "automation"],
        }

    def get_completion_event_details(self, output: WorkerOutput) -> Dict[str, Any]:
        """Return event details when devops analysis completes.

        Args:
            output: DevOps analysis output with infrastructure and automation metrics

        Returns:
            Event details for analysis completion logging
        """
        return {
            "worker": "devops-worker",
            "status": output.status,
        }

    def get_success_message(self, output: WorkerOutput) -> str:
        """Return success message with devops analysis summary.

        Args:
            output: DevOps analysis output with infrastructure and automation metrics

        Returns:
            Success message with key devops analysis results
        """
        return f"DevOps analysis completed successfully. Status: {output.status}"


def main():
    """CLI entry point for devops worker execution.

    Returns:
        Exit code from worker execution
    """
    worker = DevOpsWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
