"""
Researcher Worker Runner
========================
Execution runner for the Researcher Worker - provides technical research and industry standards analysis.
"""

import sys
import os
from pathlib import Path

# Ensure imports work when run directly or from CLI
current_dir = Path(__file__).parent
pydantic_ai_root = current_dir.parent
if str(pydantic_ai_root) not in sys.path:
    sys.path.insert(0, str(pydantic_ai_root))

from typing import Dict, Any

from shared.base_worker import BaseWorker
from researcher.models import ResearcherOutput
from researcher.agent import researcher_agent, ResearcherAgentConfig


class ResearcherWorker(BaseWorker[ResearcherOutput]):
    """
    Technical research and industry standards analysis worker.
    
    Provides comprehensive research including technology evaluation,
    best practices analysis, competitive research, and trend assessment.
    """

    def __init__(self):
        super().__init__(
            worker_type="researcher-worker",
            worker_config=None,
            output_model=ResearcherOutput,
        )

    def run(
        self, session_id: str, task_description: str, model: str
    ) -> ResearcherOutput:
        """Run researcher worker with runtime worker config"""
        # Create worker config at runtime with actual values
        self.worker_config = ResearcherAgentConfig.create_worker_config(
            session_id, task_description
        )
        return self.run_analysis(session_id, task_description, model)

    def execute_ai_analysis(
        self, session_id: str, task_description: str, model: str
    ) -> Any:
        """Execute researcher-specific AI analysis"""
        return researcher_agent.run_sync(
            f"""Conduct comprehensive technical research and analysis.
Task: {task_description}
Session: {session_id}
Perform thorough research analysis including:
1. Technology evaluation and comparison
2. Industry best practices and standards research
3. Security and compliance requirements analysis
4. Performance optimization insights and benchmarks
5. Emerging technology trends and adoption considerations
6. Competitive analysis and market intelligence
Focus on evidence-based findings with credible sources and actionable recommendations.""",
            model=model,
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

    def get_completion_event_details(self, output: ResearcherOutput) -> Dict[str, Any]:
        """Return worker-specific event details for worker_completed event"""
        return {
            "worker": "researcher-worker",
            "research_findings": len(output.research_findings),
            "confidence_score": output.confidence_score,
        }

    def get_success_message(self, output: ResearcherOutput) -> str:
        """Return worker-specific CLI success message"""
        return (
            f"Research analysis completed. Research findings: {len(output.research_findings)}, "
            f"Confidence score: {output.confidence_score}"
        )

    def create_worker_specific_files(
        self, session_id: str, output: ResearcherOutput, session_path: Path
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
