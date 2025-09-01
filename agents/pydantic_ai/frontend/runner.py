"""
Frontend Worker Runner
======================
Execution runner for the Frontend Worker - provides UI/UX implementation and component architecture analysis.
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
from frontend.models import FrontendOutput
from frontend.agent import frontend_agent, FrontendAgentConfig


class FrontendWorker(BaseWorker[FrontendOutput]):
    """
    Frontend UI/UX implementation and component architecture worker.
    
    Provides comprehensive frontend analysis including component design,
    state management, performance optimization, and accessibility compliance.
    """

    def __init__(self):
        super().__init__(
            worker_type="frontend-worker",
            worker_config=None,
            output_model=FrontendOutput,
        )

    def run(self, session_id: str, task_description: str, model: str) -> FrontendOutput:
        """Run frontend worker with runtime worker config"""
        # Create worker config at runtime with actual values
        self.worker_config = FrontendAgentConfig.create_worker_config(
            session_id, task_description
        )
        return self.run_analysis(session_id, task_description, model)

    def execute_ai_analysis(
        self, session_id: str, task_description: str, model: str
    ) -> Any:
        """Execute frontend-specific AI analysis"""
        return frontend_agent.run_sync(
            f"""Provide comprehensive frontend development and UI/UX implementation analysis.
Task: {task_description}
Session: {session_id}
Perform thorough frontend analysis including:
1. Component architecture and design system implementation
2. State management patterns and data flow optimization
3. Performance optimization and bundle analysis
4. Accessibility compliance and inclusive design
5. Responsive design and cross-platform compatibility
6. Testing strategies for UI components and user interactions
Focus on modern frontend best practices with specific implementation guidance.""",
            model=model,
        )

    def get_file_prefix(self) -> str:
        """Return file prefix for frontend output files"""
        return "frontend"

    def get_worker_display_name(self) -> str:
        """Return human-readable worker name for CLI and logging"""
        return "Frontend Worker"

    def get_worker_description(self) -> str:
        """Return worker description for CLI help"""
        return "Frontend Development and User Interfaces"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return worker-specific event details for analysis_started event"""
        return {
            "worker": "frontend-worker",
            "task": task_description,
            "focus_areas": [
                "components",
                "state_management",
                "performance",
                "accessibility",
            ],
        }

    def get_completion_event_details(self, output: FrontendOutput) -> Dict[str, Any]:
        """Return worker-specific event details for worker_completed event"""
        return {
            "worker": "frontend-worker",
            "components_count": len(output.component_specifications),
            "performance_score": output.performance_score,
        }

    def get_success_message(self, output: FrontendOutput) -> str:
        """Return worker-specific CLI success message"""
        return (
            f"Frontend analysis completed. Components: {len(output.component_specifications)}, "
            f"Performance score: {output.performance_score}"
        )

    def create_worker_specific_files(
        self, session_id: str, output: FrontendOutput, session_path: Path
    ) -> None:
        """Create frontend-specific output files beyond standard notes/JSON"""
        # Frontend worker uses standard file creation - no additional files needed
        pass


def main():
    """CLI entry point for frontend worker"""
    worker = FrontendWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
