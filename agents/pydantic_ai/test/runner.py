"""
Test Worker Runner
==================
Execution runner for the Test Worker - provides testing strategy and quality assurance analysis.
"""

from typing import Dict, Any
from pathlib import Path

from shared.base_worker import BaseWorker
from test.models import TestOutput
from test.agent import test_agent, TestAgentConfig


class TestWorker(BaseWorker[TestOutput]):
    """
    Testing strategy and quality assurance analysis worker.
    
    Provides comprehensive testing analysis including test strategy design,
    coverage assessment, automation recommendations, and quality metrics evaluation.
    """

    def __init__(self):
        super().__init__(
            worker_type="test-worker", worker_config=None, output_model=TestOutput
        )

    def run(self, session_id: str, task_description: str, model: str) -> TestOutput:
        """Run test worker with runtime worker config"""
        # Create worker config at runtime with actual values
        self.worker_config = TestAgentConfig.create_worker_config(
            session_id, task_description
        )
        return self.run_analysis(session_id, task_description, model)

    def execute_ai_analysis(
        self, session_id: str, task_description: str, model: str
    ) -> Any:
        """Execute test-specific AI analysis"""
        return test_agent.run_sync(
            f"""Provide comprehensive testing strategy and quality assurance analysis.
Task: {task_description}
Session: {session_id}
Perform thorough testing analysis including:
1. Testing strategy design and test coverage planning
2. Test automation framework recommendations
3. Quality assurance process optimization
4. Performance and security testing approaches
5. CI/CD testing integration strategies
6. Test metrics and quality validation procedures
Focus on comprehensive testing solutions with specific implementation guidance.""",
            model=model,
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

    def get_completion_event_details(self, output: TestOutput) -> Dict[str, Any]:
        """Return worker-specific event details for worker_completed event"""
        return {
            "worker": "test-worker",
            "test_strategies": len(output.test_strategies),
            "coverage_score": output.coverage_score,
            "quality_score": output.quality_score,
        }

    def get_success_message(self, output: TestOutput) -> str:
        """Return worker-specific CLI success message"""
        return (
            f"Test analysis completed. Test strategies: {len(output.test_strategies)}, "
            f"Coverage score: {output.coverage_score}, Quality score: {output.quality_score}"
        )

    def create_worker_specific_files(
        self, session_id: str, output: TestOutput, session_path: Path
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
