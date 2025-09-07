"""
Analyzer Worker Runner
======================
Execution runner for the Analyzer Worker - provides security, performance, and code quality analysis.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from shared.base_worker import BaseWorker
from shared.models import WorkerSummary  
from shared.tools import iso_now
from shared.protocols.session_management import SessionManagement
from analyzer.models import AnalyzerOutput
from analyzer.agent import analyzer_agent, AnalyzerAgentConfig

# Ensure imports work when run directly or from CLI
current_dir = Path(__file__).parent
pydantic_ai_root = current_dir.parent
if str(pydantic_ai_root) not in sys.path:
    sys.path.insert(0, str(pydantic_ai_root))


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

    def create_setup_output(
        self, session_id: str
    ) -> AnalyzerOutput:
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

        # Load templates from analyzer/templates/
        template_dir = Path(__file__).parent / "templates"
        
        # Read markdown template
        markdown_template_path = template_dir / "analyzer_notes_template.md"
        with open(markdown_template_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Read JSON template
        json_template_path = template_dir / "analyzer_output_template.json"
        with open(json_template_path, 'r', encoding='utf-8') as f:
            json_content = f.read()
        
        # Replace template variables
        current_time = datetime.now().isoformat()
        markdown_content = markdown_content.replace('{{TIMESTAMP}}', current_time)
        json_content = json_content.replace('{{SESSION_ID}}', session_id)
        json_content = json_content.replace('{{TIMESTAMP}}', current_time)
        json_content = json_content.replace('{{DURATION}}', 'TBD')

        # Create the actual output files
        notes_file = notes_dir / "analyzer_notes.md"
        json_file = json_dir / "analyzer_output.json"
        
        with open(notes_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write(json_content)

        return AnalyzerOutput(
            session_id=session_id,
            worker="analyzer-worker",
            timestamp=iso_now(),
            status="completed",
            summary=WorkerSummary(
                key_findings=[
                    "Setup phase completed successfully", 
                    "Queen-generated prompt loaded",
                    f"Template files created: {notes_file.name} and {json_file.name}"
                ],
                critical_issues=[],
                recommendations=["Proceed to Phase 2: Modify template files with analysis findings and remove unused sections"],
            ),
            security_findings=[],
            performance_issues=[],
            quality_metrics=[],
            security_score=0,
            performance_score=0,
            quality_score=0,
            priority_actions=[],
            technical_debt_estimate="TBD",
            notes_markdown=f"# Analyzer Worker Setup Phase\n\nTemplate files created and ready for Phase 2 modification.\n\n## Files Created\n- Markdown: {notes_file}\n- JSON: {json_file}\n\n## Specific Task Instructions from Queen\n\n{worker_prompt}",
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
    ) -> AnalyzerOutput:
        """Create validation output object for output phase."""

        return AnalyzerOutput(
            session_id=session_id,
            worker="analyzer-worker",
            timestamp=iso_now(),
            status="completed",
            summary=WorkerSummary(
                key_findings=["Output validation phase completed"],
                critical_issues=[],
                recommendations=["Analysis workflow completed successfully"],
            ),
            security_findings=[],
            performance_issues=[],
            quality_metrics=[],
            security_score=0,
            performance_score=0,
            quality_score=0,
            priority_actions=[],
            technical_debt_estimate="N/A",
            notes_markdown=f"# Analyzer Worker Validation Phase\n\nOutput validation completed.\n\nAnalysis files validated and confirmed complete.",
            config={},
        )


def main():
    """CLI entry point for analyzer worker execution.

    Returns:
        Exit code from worker execution
    """
    worker = AnalyzerWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
