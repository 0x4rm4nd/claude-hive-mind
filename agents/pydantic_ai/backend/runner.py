"""
Backend Worker Runner
=====================
Execution runner for the Backend Worker - provides API development and database design analysis.
"""

from typing import Dict, Any
from pathlib import Path

from shared.base_worker import BaseWorker
from backend.models import BackendOutput
from backend.agent import backend_agent, BackendAgentConfig


class BackendWorker(BaseWorker[BackendOutput]):
    """
    Backend API development and database design worker.
    
    Provides comprehensive analysis for API design, database schema, business logic,
    security implementation, and performance optimization guidance.
    """

    def __init__(self):
        super().__init__(
            worker_type="backend-worker",
            worker_config=None,
            output_model=BackendOutput,
        )

    def run(self, session_id: str, task_description: str, model: str) -> BackendOutput:
        """Execute backend analysis with API design and database architecture guidance.
        
        Args:
            session_id: Session identifier for tracking analysis
            task_description: Specific backend requirements and focus areas
            model: AI model to use for analysis execution
            
        Returns:
            BackendOutput: Structured backend analysis with API and database recommendations
        """
        # Create worker config at runtime with actual values
        self.worker_config = BackendAgentConfig.create_worker_config(
            session_id, task_description
        )
        return self.run_analysis(session_id, task_description, model)

    def execute_ai_analysis(
        self, session_id: str, task_description: str, model: str
    ) -> Any:
        """Execute AI-powered backend development and architecture analysis.
        
        Args:
            session_id: Session identifier for analysis tracking
            task_description: Detailed backend requirements
            model: AI model for analysis execution
            
        Returns:
            Backend analysis results from AI agent processing
        """
        return backend_agent.run_sync(
            f"""Provide comprehensive backend development and API design analysis.
Task: {task_description}
Session: {session_id}
Perform thorough backend analysis including:
1. API design and endpoint specifications
2. Database schema design and optimization strategies
3. Business logic implementation and service architecture
4. Security implementation and compliance measures
5. Performance optimization and scalability planning
6. Integration patterns and third-party service connections
Focus on production-ready backend solutions with specific implementation guidance.""",
            model=model,
        )

    def get_file_prefix(self) -> str:
        """Return file prefix for backend output files.
        
        Returns:
            File prefix for backend output files
        """
        return "backend"

    def get_worker_display_name(self) -> str:
        """Return human-readable name for CLI display.
        
        Returns:
            Display name for the backend worker
        """
        return "Backend Worker"

    def get_worker_description(self) -> str:
        """Return description for CLI help and documentation.
        
        Returns:
            Brief description of backend capabilities
        """
        return "API Development and Database Design"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return event details when backend analysis starts.
        
        Args:
            task_description: Backend analysis task description
            
        Returns:
            Event details for analysis started logging
        """
        return {
            "worker": "backend-worker",
            "task": task_description,
            "focus_areas": ["api_design", "database_schema", "security", "performance"],
        }

    def get_completion_event_details(self, output: BackendOutput) -> Dict[str, Any]:
        """Return event details when backend analysis completes.
        
        Args:
            output: Backend analysis output with API and database designs
            
        Returns:
            Event details for analysis completion logging
        """
        return {
            "worker": "backend-worker",
            "api_specifications": len(output.api_specifications),
            "database_designs": len(output.database_designs),
            "performance_score": output.performance_score,
            "security_score": output.security_score,
        }

    def get_success_message(self, output: BackendOutput) -> str:
        """Return success message with backend analysis summary.
        
        Args:
            output: Backend analysis output with API and database metrics
            
        Returns:
            Success message with key backend analysis results
        """
        return (
            f"Backend analysis completed. API specifications: {len(output.api_specifications)}, "
            f"Database designs: {len(output.database_designs)}, "
            f"Performance score: {output.performance_score}"
        )

    def create_worker_specific_files(
        self, session_id: str, output: BackendOutput, session_path: Path
    ) -> None:
        """Create additional backend-specific output files.
        
        Args:
            session_id: Session identifier
            output: Backend analysis output data
            session_path: Path to session directory
        """
        # Backend worker uses standard file creation - no additional files needed
        pass


def main():
    """CLI entry point for backend worker execution.
    
    Returns:
        Exit code from worker execution
    """
    worker = BackendWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
