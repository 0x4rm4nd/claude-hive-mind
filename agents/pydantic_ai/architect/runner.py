"""
Architect Worker Runner
=======================
Execution runner for the Architect Worker - provides system design and architecture analysis.
"""

import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Minimal path setup to enable shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.base_worker import BaseWorker
from shared.models import WorkerSummary
from shared.tools import iso_now
from shared.protocols.session_management import SessionManagement
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

    def create_setup_output(
        self, session_id: str
    ) -> ArchitectOutput:
        """Create minimal output object for setup phase and initialize template files."""
        # Read the Queen-generated specific task prompt for this session
        worker_prompt = self.read_worker_prompt(session_id)

        # Get session path and create worker output directories
        session_path = Path(SessionManagement.get_session_path(session_id))
        notes_dir = session_path / "workers" / "notes"
        json_dir = session_path / "workers" / "json"
        
        # Ensure directories exist
        notes_dir.mkdir(parents=True, exist_ok=True)
        json_dir.mkdir(parents=True, exist_ok=True)

        # Load templates from architect/templates/
        template_dir = Path(__file__).parent / "templates"
        
        # Read markdown template
        markdown_template_path = template_dir / "architect_notes_template.md"
        with open(markdown_template_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Read JSON template
        json_template_path = template_dir / "architect_output_template.json"
        with open(json_template_path, 'r', encoding='utf-8') as f:
            json_content = f.read()
        
        # Replace template variables
        current_time = datetime.now().isoformat()
        markdown_content = markdown_content.replace('{{TIMESTAMP}}', current_time)
        json_content = json_content.replace('{{SESSION_ID}}', session_id)
        json_content = json_content.replace('{{TIMESTAMP}}', current_time)
        json_content = json_content.replace('{{DURATION}}', 'TBD')

        # Create the actual output files
        notes_file = notes_dir / "architect_notes.md"
        json_file = json_dir / "architect_output.json"
        
        with open(notes_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write(json_content)

        return ArchitectOutput(
            session_id=session_id,
            worker="architect-worker",
            timestamp=iso_now(),
            status="completed",
            summary=WorkerSummary(
                key_findings=[
                    "Setup phase completed successfully", 
                    "Queen-generated prompt loaded",
                    f"Template files created: {notes_file.name} and {json_file.name}"
                ],
                critical_issues=[],
                recommendations=["Proceed to Phase 2: Modify template files with architecture findings and remove unused sections"],
            ),
            current_architecture_assessment="Setup phase - assessment pending",
            architectural_recommendations=[],
            technology_decisions=[],
            notes_markdown=f"# Architect Worker Setup Phase\n\nTemplate files created and ready for Phase 2 modification.\n\n## Files Created\n- Markdown: {notes_file}\n- JSON: {json_file}\n\n## Specific Task Instructions from Queen\n\n{worker_prompt}",
            config={
                "queen_prompt": worker_prompt,
                "template_files_created": {
                    "notes_file": str(notes_file),
                    "json_file": str(json_file)
                }
            },
        )

    def create_output_validation(
        self, session_id: str
    ) -> ArchitectOutput:
        """Create validation output object for output phase."""

        return ArchitectOutput(
            session_id=session_id,
            worker="architect-worker",
            timestamp=iso_now(),
            status="completed",
            summary=WorkerSummary(
                key_findings=["Output validation phase completed"],
                critical_issues=[],
                recommendations=["Architecture analysis workflow completed successfully"],
            ),
            current_architecture_assessment="Validation phase completed",
            architectural_recommendations=[],
            technology_decisions=[],
            notes_markdown=f"# Architect Worker Validation Phase\n\nOutput validation completed.\n\nArchitecture analysis files validated and confirmed complete.",
            config={},
        )

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
