"""
DevOps Worker Runner
====================
Execution runner for the DevOps Worker - provides infrastructure, deployment, and CI/CD analysis.
"""

import sys
import os
from pathlib import Path

# Minimal path setup to enable shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, Any

from shared.base_worker import BaseWorker
from shared.models import WorkerOutput
from devops.agent import devops_agent, DevOpsAgentConfig


class DevOpsWorker(BaseWorker):
    """
    Infrastructure, deployment, and CI/CD analysis worker.
    
    Provides comprehensive DevOps analysis including infrastructure design,
    deployment strategies, monitoring setup, and CI/CD pipeline optimization.
    """

    def __init__(self):
        super().__init__(
            worker_type="devops-worker", worker_config=None, output_model=WorkerOutput
        )


    def get_file_prefix(self) -> str:
        """Return file prefix for devops output files"""
        return "devops"

    def get_worker_display_name(self) -> str:
        """Return human-readable worker name for CLI and logging"""
        return "DevOps Worker"

    def get_worker_description(self) -> str:
        """Return worker description for CLI help"""
        return "Infrastructure and Deployment Operations"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return worker-specific event details for analysis_started event"""
        return {
            "worker": "devops-worker",
            "task": task_description,
            "focus_areas": ["infrastructure", "deployment", "monitoring", "automation"],
        }

    def get_completion_event_details(self, output: WorkerOutput) -> Dict[str, Any]:
        """Return worker-specific event details for worker_completed event"""
        return {
            "worker": "devops-worker",
            "infrastructure_recommendations": len(
                output.infrastructure_recommendations
            ),
            "automation_score": output.automation_score,
            "reliability_score": output.reliability_score,
        }

    def get_success_message(self, output: WorkerOutput) -> str:
        """Return worker-specific CLI success message"""
        return (
            f"DevOps analysis completed. Infrastructure recommendations: {len(output.infrastructure_recommendations)}, "
            f"Automation score: {output.automation_score}, Reliability score: {output.reliability_score}"
        )

    def create_worker_specific_files(
        self, session_id: str, output: WorkerOutput, session_path: Path
    ) -> None:
        """Create devops-specific output files beyond standard notes/JSON"""
        # DevOps worker uses standard file creation - no additional files needed
        pass


def main():
    """CLI entry point for devops worker"""
    worker = DevOpsWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
