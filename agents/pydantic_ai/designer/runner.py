"""
Designer Worker Runner
======================
Execution runner for the Designer Worker - provides user experience and visual design analysis.
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
from designer.models import DesignerOutput
from designer.agent import designer_agent, DesignerAgentConfig


class DesignerWorker(BaseWorker[DesignerOutput]):
    """
    User experience and visual design analysis worker.
    
    Provides comprehensive UX/UI analysis, design system recommendations,
    accessibility compliance, and visual design guidance.
    """

    def __init__(self):
        super().__init__(
            worker_type="designer-worker",
            worker_config=None,
            output_model=DesignerOutput,
        )

    def run(self, session_id: str, task_description: str, model: str) -> DesignerOutput:
        """Run designer worker with runtime worker config"""
        # Create worker config at runtime with actual values
        self.worker_config = DesignerAgentConfig.create_worker_config(
            session_id, task_description
        )
        return self.run_analysis(session_id, task_description, model)

    def execute_ai_analysis(
        self, session_id: str, task_description: str, model: str
    ) -> Any:
        """Execute designer-specific AI analysis"""
        return designer_agent.run_sync(
            f"""Provide comprehensive UX/UI design and accessibility analysis.
Task: {task_description}
Session: {session_id}
Perform thorough design analysis including:
1. User experience design and journey optimization
2. Visual design system and component specifications
3. Accessibility compliance and inclusive design practices
4. Responsive design patterns and mobile optimization
5. Design system consistency and scalability
6. Usability improvements and conversion optimization
Focus on user-centered design with specific implementation guidance.""",
            model=model,
        )

    def get_file_prefix(self) -> str:
        """Return file prefix for designer output files"""
        return "designer"

    def get_worker_display_name(self) -> str:
        """Return human-readable worker name for CLI and logging"""
        return "Designer Worker"

    def get_worker_description(self) -> str:
        """Return worker description for CLI help"""
        return "UX/UI Design and Accessibility"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        """Return worker-specific event details for analysis_started event"""
        return {
            "worker": "designer-worker",
            "task": task_description,
            "focus_areas": [
                "ux_design",
                "ui_design",
                "accessibility",
                "responsive_design",
            ],
        }

    def get_completion_event_details(self, output: DesignerOutput) -> Dict[str, Any]:
        """Return worker-specific event details for worker_completed event"""
        return {
            "worker": "designer-worker",
            "ux_recommendations": len(output.ux_recommendations),
            "ui_improvements": len(output.ui_improvements),
            "accessibility_score": output.accessibility_score,
        }

    def get_success_message(self, output: DesignerOutput) -> str:
        """Return worker-specific CLI success message"""
        return (
            f"Design analysis completed. UX recommendations: {len(output.ux_recommendations)}, "
            f"UI improvements: {len(output.ui_improvements)}, "
            f"Accessibility score: {output.accessibility_score}"
        )

    def create_worker_specific_files(
        self, session_id: str, output: DesignerOutput, session_path: Path
    ) -> None:
        """Create designer-specific output files beyond standard notes/JSON"""
        # Designer worker uses standard file creation - no additional files needed
        pass


def main():
    """CLI entry point for designer worker"""
    worker = DesignerWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
