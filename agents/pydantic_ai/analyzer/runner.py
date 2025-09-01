"""
Analyzer Worker Runner
======================
Execution runner for the Analyzer Worker - provides security, performance, and code quality analysis.
"""

from typing import Dict, Any
from pathlib import Path

from shared.base_worker import BaseWorker
from analyzer.models import AnalyzerOutput
from analyzer.agent import analyzer_agent, AnalyzerAgentConfig


class AnalyzerWorker(BaseWorker[AnalyzerOutput]):
    """
    Security, performance, and code quality analysis worker.

    Analyzes codebases for vulnerabilities, performance bottlenecks, and quality metrics.
    Provides detailed findings with actionable recommendations and severity ratings.
    """

    def __init__(self):
        super().__init__(
            worker_type="analyzer-worker",
            worker_config=None,
            output_model=AnalyzerOutput,
        )

    def run(self, session_id: str, task_description: str, model: str) -> AnalyzerOutput:
        """Execute analysis with comprehensive security, performance, and quality assessment.

        Args:
            session_id: Session identifier for tracking analysis
            task_description: Specific analysis requirements and focus areas
            model: AI model to use for analysis execution

        Returns:
            AnalyzerOutput: Structured analysis results with findings and recommendations
        """
        # Create worker config at runtime with actual values
        self.worker_config = AnalyzerAgentConfig.create_worker_config(
            session_id, task_description
        )
        return self.run_analysis(session_id, task_description, model)

    def execute_ai_analysis(
        self, session_id: str, task_description: str, model: str
    ) -> Any:
        """Execute AI-powered security, performance, and quality analysis.

        Args:
            session_id: Session identifier for analysis tracking
            task_description: Detailed analysis requirements
            model: AI model for analysis execution

        Returns:
            Analysis results from AI agent processing
        """
        return analyzer_agent.run_sync(
            f"""Analyze the codebase for security vulnerabilities, performance issues, and code quality problems.

Task: {task_description}
Session: {session_id}

Perform comprehensive analysis including:
1. Security vulnerability assessment
2. Performance bottleneck identification  
3. Code quality metrics evaluation
4. Dependency security analysis
5. Technical debt quantification

Provide specific, actionable findings with clear priorities and effort estimates.""",
            model=model,
        )

    def get_file_prefix(self) -> str:
        """Return file prefix for analysis output files.

        Returns:
            File prefix for analyzer output files
        """
        return "analyzer"

    def get_worker_display_name(self) -> str:
        """Return human-readable name for CLI display.

        Returns:
            Display name for the analyzer worker
        """
        return "Analyzer Worker"

    def get_worker_description(self) -> str:
        """Return description for CLI help and documentation.

        Returns:
            Brief description of analyzer capabilities
        """
        return "Security and Performance Analysis"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return event details when analysis starts.

        Args:
            task_description: Analysis task description

        Returns:
            Event details for analysis started logging
        """
        return {
            "task": task_description,
            "analysis_type": "security_performance_quality",
        }

    def get_completion_event_details(self, output: AnalyzerOutput) -> Dict[str, Any]:
        """Return event details when analysis completes.

        Args:
            output: Analysis output with findings and metrics

        Returns:
            Event details for analysis completion logging
        """
        return {
            "duration": "calculated",
            "security_findings_count": len(output.security_findings),
            "performance_issues_count": len(output.performance_issues),
            "quality_metrics_count": len(output.quality_metrics),
            "status": output.status,
        }

    def get_success_message(self, output: AnalyzerOutput) -> str:
        """Return success message with analysis summary.

        Args:
            output: Analysis output with scores and findings

        Returns:
            Success message with key analysis metrics
        """
        return f"Analysis completed successfully. Security score: {output.security_score}, Performance score: {output.performance_score}, Quality score: {output.quality_score}"

    def create_worker_specific_files(
        self, session_id: str, output: AnalyzerOutput, session_path: Path
    ) -> None:
        """Create additional analyzer-specific output files.

        Args:
            session_id: Session identifier
            output: Analysis output data
            session_path: Path to session directory
        """
        # Analyzer worker uses standard file creation - no additional files needed
        pass


def main():
    """CLI entry point for analyzer worker execution.

    Returns:
        Exit code from worker execution
    """
    worker = AnalyzerWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
