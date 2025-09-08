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
from researcher.agent import researcher_agent, ResearcherAgentConfig


class ResearcherWorker(BaseWorker):
    """
    Technical research and industry standards analysis worker.

    Provides comprehensive research including technology evaluation,
    best practices analysis, competitive research, and trend assessment.
    """

    def __init__(self):
        super().__init__(
            worker_type="researcher-worker",
            worker_config=None,
        )


    def get_file_prefix(self) -> str:
        """Return file prefix for researcher output files"""
        return "researcher"

    def get_worker_display_name(self) -> str:
        """Return human-readable worker name for CLI and logging"""
        return "Researcher Worker"

    def get_worker_description(self) -> str:
        """Return worker description for CLI help"""
        return "Research and Information Gathering"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return worker-specific event details for analysis_started event"""
        return {
            "worker": "researcher-worker",
            "task": task_description,
            "focus_areas": ["research", "analysis", "documentation", "insights"],
        }

    def get_completion_event_details(self, output: WorkerOutput) -> Dict[str, Any]:
        """Return worker-specific event details for worker_completed event"""
        return {
            "worker": "researcher-worker",
            "research_findings": len(output.research_findings),
            "confidence_score": output.confidence_score,
        }

    def get_success_message(self, output: WorkerOutput) -> str:
        """Return worker-specific CLI success message"""
        return (
            f"Research analysis completed. Research findings: {len(output.research_findings)}, "
            f"Confidence score: {output.confidence_score}"
        )

    def create_worker_specific_files(
        self, session_id: str, output: WorkerOutput, session_path: Path
    ) -> None:
        """Create researcher-specific output files beyond standard notes/JSON"""
        # Researcher worker uses standard file creation - no additional files needed
        pass


def main():
    """CLI entry point for researcher worker"""
    worker = ResearcherWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
