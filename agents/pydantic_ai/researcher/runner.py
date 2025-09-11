"""
Researcher Worker Runner
========================
Execution runner for the Researcher Worker - provides technical research and industry standards analysis.
"""

import sys
from pathlib import Path
from typing import Dict, Any

# Minimal path setup to enable shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.base_worker import BaseWorker
from shared.models import WorkerOutput


class ResearcherWorker(BaseWorker):
    """
    Technical research and industry standards analysis worker.

    Analyzes codebases for technology evaluation, best practices compliance,
    competitive research, and industry trend assessment. Provides detailed
    findings with actionable recommendations and evidence-based insights.
    """

    def __init__(self):
        super().__init__(
            worker_type="researcher-worker",
            worker_config=None,
        )

    def get_file_prefix(self) -> str:
        """Return file prefix for analysis output files.

        Returns:
            File prefix for researcher output files
        """
        return "researcher"

    def get_worker_display_name(self) -> str:
        """Return human-readable name for CLI display.

        Returns:
            Display name for the researcher worker
        """
        return "Researcher Worker"

    def get_worker_description(self) -> str:
        """Return description for CLI help and documentation.

        Returns:
            Brief description of researcher capabilities
        """
        return "Technical Research and Industry Analysis"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return event details when analysis starts.

        Args:
            task_description: Analysis task description

        Returns:
            Event details for analysis started logging
        """
        return {
            "task": task_description,
            "analysis_type": "research_technology_industry_trends",
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
        return f"Research analysis completed successfully. Research areas analyzed: {output.metrics.items_analyzed}, Issues found: {output.metrics.issues_found}"


def main():
    """CLI entry point for researcher worker execution.

    Returns:
        Exit code from worker execution
    """
    worker = ResearcherWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
