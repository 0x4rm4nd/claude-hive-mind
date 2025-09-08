"""
Designer Worker Runner
======================
Execution runner for the Designer Worker - provides user experience and visual design analysis.
"""

import sys
import os
from pathlib import Path

# Minimal path setup to enable shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, Any

from shared.base_worker import BaseWorker
from shared.models import WorkerOutput
from designer.agent import designer_agent, DesignerAgentConfig


class DesignerWorker(BaseWorker):
    """
    User experience and visual design analysis worker.
    
    Provides comprehensive UX/UI analysis, design system recommendations,
    accessibility compliance, and visual design guidance.
    """

    def __init__(self):
        super().__init__(
            worker_type="designer-worker",
            worker_config=None,
        )


    def get_file_prefix(self) -> str:
        """Return file prefix for designer output files"""
        return "designer"

    def get_worker_display_name(self) -> str:
        """Return human-readable worker name for CLI and logging"""
        return "Designer Worker"

    def get_worker_description(self) -> str:
        """Return worker description for CLI help"""
        return "UX/UI Design and Accessibility"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return worker-specific event details for analysis_started event"""
        return {
            "worker": "designer-worker",
            "task": task_description,
            "focus_areas": [
                "ux_design",
                "ui_design",
                "accessibility",
                "responsive_design",
            ],
        }

    def get_completion_event_details(self, output: WorkerOutput) -> Dict[str, Any]:
        """Return worker-specific event details for worker_completed event"""
        return {
            "worker": "designer-worker",
            "ux_recommendations": len(output.ux_recommendations),
            "ui_improvements": len(output.ui_improvements),
            "accessibility_score": output.accessibility_score,
        }

    def get_success_message(self, output: WorkerOutput) -> str:
        """Return worker-specific CLI success message"""
        return (
            f"Design analysis completed. UX recommendations: {len(output.ux_recommendations)}, "
            f"UI improvements: {len(output.ui_improvements)}, "
            f"Accessibility score: {output.accessibility_score}"
        )

    def create_worker_specific_files(
        self, session_id: str, output: WorkerOutput, session_path: Path
    ) -> None:
        """Create designer-specific output files beyond standard notes/JSON"""
        # Designer worker uses standard file creation - no additional files needed
        pass


def main():
    """CLI entry point for designer worker"""
    worker = DesignerWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
