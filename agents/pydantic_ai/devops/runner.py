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
from devops.models import DevOpsOutput
from devops.agent import devops_agent, DevOpsAgentConfig


class DevOpsWorker(BaseWorker[DevOpsOutput]):
    """
    Infrastructure, deployment, and CI/CD analysis worker.
    
    Provides comprehensive DevOps analysis including infrastructure design,
    deployment strategies, monitoring setup, and CI/CD pipeline optimization.
    """

    def __init__(self):
        super().__init__(
            worker_type="devops-worker", worker_config=None, output_model=DevOpsOutput
        )

    def run(self, session_id: str, task_description: str, model: str) -> DevOpsOutput:
        """Run devops worker with runtime worker config"""
        # Create worker config at runtime with actual values
        self.worker_config = DevOpsAgentConfig.create_worker_config(
            session_id, task_description
        )
        return self.run_analysis(session_id, task_description, model)

    def execute_ai_analysis(
        self, session_id: str, task_description: str, model: str
    ) -> Any:
        """Execute devops-specific AI analysis"""
        return devops_agent.run_sync(
            f"""Provide comprehensive DevOps infrastructure and deployment analysis.
Task: {task_description}
Session: {session_id}
Perform thorough DevOps analysis including:
1. Infrastructure architecture and deployment strategy
2. CI/CD pipeline design and optimization
3. Monitoring and observability implementation
4. Security hardening and compliance requirements
5. Scalability planning and reliability engineering
6. Operational procedures and incident response
Focus on production-ready solutions with specific implementation details.""",
            model=model,
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

    def get_completion_event_details(self, output: DevOpsOutput) -> Dict[str, Any]:
        """Return worker-specific event details for worker_completed event"""
        return {
            "worker": "devops-worker",
            "infrastructure_recommendations": len(
                output.infrastructure_recommendations
            ),
            "automation_score": output.automation_score,
            "reliability_score": output.reliability_score,
        }

    def get_success_message(self, output: DevOpsOutput) -> str:
        """Return worker-specific CLI success message"""
        return (
            f"DevOps analysis completed. Infrastructure recommendations: {len(output.infrastructure_recommendations)}, "
            f"Automation score: {output.automation_score}, Reliability score: {output.reliability_score}"
        )

    def create_worker_specific_files(
        self, session_id: str, output: DevOpsOutput, session_path: Path
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
