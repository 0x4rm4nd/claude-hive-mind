"""
Test Worker Runner
==================
Execution runner for the Test Worker - provides testing strategy and quality assurance analysis.
"""

import sys
import os
from pathlib import Path

# Minimal path setup to enable shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, Any

from shared.base_worker import BaseWorker
from shared.models import WorkerOutput
from test.agent import test_agent, TestAgentConfig


class TestWorker(BaseWorker):
    """
    Testing strategy and quality assurance analysis worker.
    
    Provides comprehensive testing analysis including test strategy design,
    coverage assessment, automation recommendations, and quality metrics evaluation.
    """

    def __init__(self):
        super().__init__(
            worker_type="test-worker", worker_config=None, output_model=WorkerOutput
        )


    def get_file_prefix(self) -> str:
        """Return file prefix for test output files"""
        return "test"

    def get_worker_display_name(self) -> str:
        """Return human-readable worker name for CLI and logging"""
        return "Test Worker"

    def get_worker_description(self) -> str:
        """Return worker description for CLI help"""
        return "Testing and Quality Assurance"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return worker-specific event details for analysis_started event"""
        return {
            "worker": "test-worker",
            "task": task_description,
            "focus_areas": [
                "unit_testing",
                "integration_testing",
                "test_coverage",
                "quality_assurance",
            ],
        }

    def get_completion_event_details(self, output: WorkerOutput) -> Dict[str, Any]:
        """Return worker-specific event details for worker_completed event"""
        return {
            "worker": "test-worker",
            "test_strategies": len(output.test_strategies),
            "coverage_score": output.coverage_score,
            "quality_score": output.quality_score,
        }

    def get_success_message(self, output: WorkerOutput) -> str:
        """Return worker-specific CLI success message"""
        return (
            f"Test analysis completed. Test strategies: {len(output.test_strategies)}, "
            f"Coverage score: {output.coverage_score}, Quality score: {output.quality_score}"
        )

    def create_worker_specific_files(
        self, session_id: str, output: WorkerOutput, session_path: Path
    ) -> None:
        """Create test-specific output files beyond standard notes/JSON"""
        # Test worker uses standard file creation - no additional files needed
        pass


def main():
    """CLI entry point for test worker"""
    worker = TestWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
