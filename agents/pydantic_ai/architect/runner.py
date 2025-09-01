"""
Architect Worker Runner
=======================
Execution runner for the Architect Worker - provides system design and architecture analysis.
"""

from typing import Dict, Any
from pathlib import Path

from shared.base_worker import BaseWorker
from architect.models import ArchitectOutput
from architect.agent import architect_agent, ArchitectAgentConfig


class ArchitectWorker(BaseWorker[ArchitectOutput]):
    """
    System design and architecture analysis worker.
    
    Evaluates system architecture, provides design recommendations, and assesses
    technology stack decisions with scalability and modernization guidance.
    """

    def __init__(self):
        super().__init__(
            worker_type="architect-worker",
            worker_config=None,
            output_model=ArchitectOutput,
        )

    def run(
        self, session_id: str, task_description: str, model: str
    ) -> ArchitectOutput:
        """Execute architectural analysis with design recommendations and technology guidance.
        
        Args:
            session_id: Session identifier for tracking analysis
            task_description: Specific architectural requirements and focus areas
            model: AI model to use for analysis execution
            
        Returns:
            ArchitectOutput: Structured architecture analysis with recommendations
        """
        # Create worker config at runtime with actual values
        self.worker_config = ArchitectAgentConfig.create_worker_config(
            session_id, task_description
        )
        return self.run_analysis(session_id, task_description, model)

    def execute_ai_analysis(
        self, session_id: str, task_description: str, model: str
    ) -> Any:
        """Execute AI-powered architectural analysis and design recommendations.
        
        Args:
            session_id: Session identifier for analysis tracking
            task_description: Detailed architectural requirements
            model: AI model for analysis execution
            
        Returns:
            Architecture analysis results from AI agent processing
        """
        return architect_agent.run_sync(
            f"""Analyze the system architecture and provide design recommendations.

Task: {task_description}
Session: {session_id}

Perform comprehensive architectural analysis including:
1. Current architecture assessment and maturity evaluation
2. Scalability and performance architecture review
3. Technology stack evaluation and recommendations
4. Design pattern identification and suggestions
5. Migration and modernization strategies

Focus on providing specific, actionable architectural guidance with clear implementation priorities.""",
            model=model,
        )

    def get_file_prefix(self) -> str:
        """Return file prefix for architecture output files.
        
        Returns:
            File prefix for architect output files
        """
        return "architect"

    def get_worker_display_name(self) -> str:
        """Return human-readable name for CLI display.
        
        Returns:
            Display name for the architect worker
        """
        return "Architect Worker"

    def get_worker_description(self) -> str:
        """Return description for CLI help and documentation.
        
        Returns:
            Brief description of architect capabilities
        """
        return "System Design and Architecture Analysis"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return event details when architectural analysis starts.
        
        Args:
            task_description: Architecture analysis task description
            
        Returns:
            Event details for analysis started logging
        """
        return {
            "task": task_description,
            "analysis_type": "architecture_analysis",
        }

    def get_completion_event_details(self, output: ArchitectOutput) -> Dict[str, Any]:
        """Return event details when architectural analysis completes.
        
        Args:
            output: Architecture analysis output with recommendations
            
        Returns:
            Event details for analysis completion logging
        """
        return {
            "duration": "calculated",
            "recommendations_count": len(output.architectural_recommendations),
            "technology_decisions_count": len(output.technology_decisions),
            "status": output.status,
        }

    def get_success_message(self, output: ArchitectOutput) -> str:
        """Return success message with architectural analysis summary.
        
        Args:
            output: Architecture analysis output with scores and recommendations
            
        Returns:
            Success message with key architecture metrics
        """
        return f"Architecture analysis completed successfully. Maturity score: {output.architectural_maturity_score}, Recommendations: {len(output.architectural_recommendations)}, Technology decisions: {len(output.technology_decisions)}"

    def create_worker_specific_files(
        self, session_id: str, output: ArchitectOutput, session_path: Path
    ) -> None:
        """Create additional architect-specific output files.
        
        Args:
            session_id: Session identifier
            output: Architecture analysis output data
            session_path: Path to session directory
        """
        # Architect worker uses standard file creation - no additional files needed
        pass


def main():
    """CLI entry point for architect worker execution.
    
    Returns:
        Exit code from worker execution
    """
    worker = ArchitectWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
