"""
Designer Worker Runner
======================
Execution runner for the Designer Worker - provides user experience and visual design analysis.
"""

import sys
from pathlib import Path
from typing import Dict, Any

# Minimal path setup to enable shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.base_worker import BaseWorker
from shared.models import WorkerOutput


class DesignerWorker(BaseWorker):
    """
    User experience and visual design analysis worker.

    Analyzes interfaces for UX/UI design patterns, accessibility compliance, and usability.
    Provides detailed design findings with actionable recommendations and design metrics.
    """

    def __init__(self):
        super().__init__(
            worker_type="designer-worker",
            worker_config=None,
        )

    def get_file_prefix(self) -> str:
        """Return file prefix for design analysis output files.

        Returns:
            File prefix for designer output files
        """
        return "designer"

    def get_worker_display_name(self) -> str:
        """Return human-readable name for CLI display.

        Returns:
            Display name for the designer worker
        """
        return "Designer Worker"

    def get_worker_description(self) -> str:
        """Return description for CLI help and documentation.

        Returns:
            Brief description of designer capabilities
        """
        return "UX/UI Design and Accessibility"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return event details when design analysis starts.

        Args:
            task_description: Design analysis task description

        Returns:
            Event details for analysis started logging
        """
        return {
            "task": task_description,
            "analysis_type": "ux_ui_accessibility_design",
        }

    def get_completion_event_details(self, output: WorkerOutput) -> Dict[str, Any]:
        """Return event details when design analysis completes.

        Args:
            output: Design analysis output with findings and metrics

        Returns:
            Event details for analysis completion logging
        """
        return {
            "duration": "calculated",
            "metrics": output.metrics.model_dump(),
            "status": output.status,
        }

    def get_success_message(self, output: WorkerOutput) -> str:
        """Return success message with design analysis summary.

        Args:
            output: Design analysis output with scores and findings

        Returns:
            Success message with key design analysis metrics
        """
        return f"Design analysis completed successfully. Files analyzed: {output.metrics.items_analyzed}, Issues found: {output.metrics.issues_found}"


def main():
    """CLI entry point for designer worker execution.

    Returns:
        Exit code from worker execution
    """
    worker = DesignerWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
