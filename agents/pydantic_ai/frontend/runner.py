"""
Frontend Worker Runner
======================
Execution runner for the Frontend Worker - provides UI/UX implementation and component architecture analysis.
"""

import sys
import os
from pathlib import Path

# Minimal path setup to enable shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, Any

from shared.base_worker import BaseWorker
from shared.models import WorkerOutput
from frontend.agent import frontend_agent, FrontendAgentConfig


class FrontendWorker(BaseWorker):
    """
    Frontend UI/UX implementation and component architecture worker.
    
    Provides comprehensive frontend analysis including component design,
    state management, performance optimization, and accessibility compliance.
    """

    def __init__(self):
        super().__init__(
            worker_type="frontend-worker",
            worker_config=None,
        )


    def get_file_prefix(self) -> str:
        """Return file prefix for frontend output files"""
        return "frontend"

    def get_worker_display_name(self) -> str:
        """Return human-readable worker name for CLI and logging"""
        return "Frontend Worker"

    def get_worker_description(self) -> str:
        """Return worker description for CLI help"""
        return "Frontend Development and User Interfaces"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return worker-specific event details for analysis_started event"""
        return {
            "worker": "frontend-worker",
            "task": task_description,
            "focus_areas": [
                "components",
                "state_management",
                "performance",
                "accessibility",
            ],
        }

    def get_completion_event_details(self, output: WorkerOutput) -> Dict[str, Any]:
        """Return worker-specific event details for worker_completed event"""
        return {
            "worker": "frontend-worker",
            "components_count": len(output.component_specifications),
            "performance_score": output.performance_score,
        }

    def get_success_message(self, output: WorkerOutput) -> str:
        """Return worker-specific CLI success message"""
        return (
            f"Frontend analysis completed. Components: {len(output.component_specifications)}, "
            f"Performance score: {output.performance_score}"
        )

    def create_worker_specific_files(
        self, session_id: str, output: WorkerOutput, session_path: Path
    ) -> None:
        """Create frontend-specific output files beyond standard notes/JSON"""
        # Frontend worker uses standard file creation - no additional files needed
        pass


def main():
    """CLI entry point for frontend worker"""
    worker = FrontendWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
