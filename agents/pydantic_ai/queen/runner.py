#!/usr/bin/env python3
"""
Queen Orchestrator Runner
=========================
BaseWorker implementation for strategic multi-worker orchestration.
"""

import sys
from pathlib import Path
import json

from typing import Dict, Any
from pydantic_ai import Agent
from pydantic_ai.models import ModelSettings
from .models import QueenOrchestrationPlan
from shared.base_worker import BaseWorker
from queen.models import QueenOutput
from queen.agent import queen_agent, QueenAgentConfig
from shared.protocols import SessionManagement
from shared.protocols import create_worker_prompts_from_plan
from shared.tools import iso_now

# Ensure imports work when run directly or from CLI
current_dir = Path(__file__).parent
pydantic_ai_root = current_dir.parent
if str(pydantic_ai_root) not in sys.path:
    sys.path.insert(0, str(pydantic_ai_root))


class QueenWorker(BaseWorker):
    """
    Strategic multi-worker orchestrator and coordination manager.

    Analyzes complex tasks to determine optimal worker assignments and provides
    continuous monitoring of worker progress and coordination.
    """

    def __init__(self):
        super().__init__(
            worker_type="queen-orchestrator",
            worker_config=None,
        )

    def run(self, session_id: str, task_description: str, model: str) -> QueenOutput:
        """Run queen orchestrator with runtime worker config"""
        # Create worker config at runtime with actual values
        self.worker_config = QueenAgentConfig.create_worker_config(
            session_id, task_description
        )
        # Update session config before any logging
        self.update_session_config(session_id)

        # Log queen spawned event
        self.log_event(
            "queen_spawned",
            {
                "worker_type": "queen-orchestrator",
                "mode": "orchestration",
                "purpose": "Task AI Analysis",
            },
            "INFO",
        )

        self.validate_session(session_id)
        return self.execute_queen_analysis(session_id, task_description, model)

    def execute_queen_analysis(
        self, session_id: str, task_description: str, model: str
    ) -> Any:
        """Execute orchestration analysis using Pydantic AI agent"""
        # Log analysis started event after queen spawned
        self.log_event(
            "analysis_started",
            self.get_analysis_event_details(task_description),
            "INFO",
        )

        queen_prompt = f"Using the Queen Agent, analyze task and create orchestration plan.\nTask: {task_description}\nSession: {session_id}"

        # Handle custom models with system prompt override
        if model.startswith("custom:"):
            system_prompt = (
                "You are a Queen Orchestrator - a JSON generator that delegates work to engineering teams. "
                "Your ONLY job is to output valid JSON for orchestration. "
                "NEVER write explanatory text. "
                "NEVER write 'The Queen Agent has completed...' "
                "NEVER use ```json blocks. "
                "DO NOT explain what you are doing. "
                "OUTPUT FORMAT: Start immediately with { and end with } "
                "REQUIRED FIELDS: session_id, timestamp, status (completed/failed/planning), task_summary (string), coordination_complexity (number 1-5), orchestration_rationale (string), estimated_total_duration (string), worker_assignments (array), execution_strategy (parallel/sequential/hybrid), coordination_notes (string array), success_criteria (string array), codebase_insights (array of objects with service_name string, key_files string array, service_description string, technology_stack string array, interaction_points string array). "
                "worker_assignments items need: worker_type (analyzer-worker/architect-worker/backend-worker/frontend-worker/designer-worker/devops-worker/researcher-worker/test-worker), priority (critical/high/medium/low), task_focus (string), dependencies (string array), estimated_duration (string), strategic_value (critical/high/medium/low), rationale (string). "
                'RESPOND ONLY WITH: {"session_id": "2025-09-03-11-10-queen-orchestration-test", "timestamp": "2025-09-03T11:10:00Z", "status": "completed", "task_summary": "Orchestration task understanding", "coordination_complexity": 3, "orchestration_rationale": "Selected teams for optimal coordination", "estimated_total_duration": "2h", "worker_assignments": [{"worker_type": "test-worker", "priority": "high", "task_focus": "test focus", "dependencies": [], "estimated_duration": "1h", "strategic_value": "high", "rationale": "test rationale"}], "execution_strategy": "parallel", "coordination_notes": ["team coordination note"], "success_criteria": ["completion criteria"], "codebase_insights": [{"service_name": "test-service", "key_files": ["test.py"], "service_description": "Test service for example", "technology_stack": ["Python"], "interaction_points": ["connects to API"]}]}'
            )

            model_settings = ModelSettings(
                extra_headers={"X-System-Prompt-Override": system_prompt}
            )

            temp_agent = Agent(
                model=model,
                output_type=QueenOrchestrationPlan,
                model_settings=model_settings,
                # NO system prompt for custom models - let Docker agent handle it
            )

            orchestration_result = temp_agent.run_sync(queen_prompt)
        else:
            orchestration_result = queen_agent.run_sync(
                queen_prompt,
                model=model,
            )

        orchestration_plan = orchestration_result.output
        session_path = SessionManagement.get_session_path(session_id)

        project_root = Path(SessionManagement.detect_project_root())
        relative_session_path = str(Path(session_path).relative_to(project_root))

        # Generate worker-specific prompts from orchestration plan
        try:
            create_worker_prompts_from_plan(session_id, orchestration_plan)
        except Exception as e:
            self.log_debug(
                "worker_prompts_generation_failed",
                {
                    "exception_type": str(type(e)),
                    "error": str(e),
                    "worker_count": len(orchestration_plan.worker_assignments),
                },
                "WARNING",
            )

        queen_output = QueenOutput(
            worker="queen-orchestrator",
            session_id=session_id,
            timestamp=iso_now(),
            status="completed",
            summary={
                "key_findings": [
                    f"Orchestration plan generated with {len(orchestration_plan.worker_assignments)} workers",
                    f"Worker-specific prompts created for {len(orchestration_plan.worker_assignments)} specialists",
                    f"Coordination strategy: {orchestration_plan.execution_strategy}",
                ],
                "critical_issues": [],
                "recommendations": [
                    assignment.rationale
                    for assignment in orchestration_plan.worker_assignments
                ],
            },
            workers_spawned=[
                assignment.worker_type
                for assignment in orchestration_plan.worker_assignments
            ],
            coordination_status="planned",
            monitoring_active=False,
            session_path=relative_session_path,
        )

        # Store orchestration_plan temporarily for file creation
        queen_output._orchestration_plan = orchestration_plan

        session_path = Path(SessionManagement.get_session_path(session_id))
        self.create_worker_specific_files(session_id, queen_output, session_path)

        completion_details = self.get_completion_event_details(queen_output)
        self.log_event("analysis_completed", completion_details)

        return queen_output

    def get_file_prefix(self) -> str:
        return "queen"

    def get_worker_display_name(self) -> str:
        return "Queen Orchestrator"

    def get_worker_description(self) -> str:
        return "Multi-Worker Coordination and Orchestration"

    def get_analysis_event_details(self, task_description: str) -> Dict[str, Any]:
        return {
            "worker": "queen-orchestrator",
            "task": task_description,
            "focus_areas": ["orchestration", "coordination", "strategic_planning"],
        }

    def get_completion_event_details(self, output: QueenOutput) -> Dict[str, Any]:
        return {
            "worker": "queen-orchestrator",
            "workers_spawned": len(output.workers_spawned),
            "coordination_status": output.coordination_status,
            "monitoring_active": output.monitoring_active,
        }

    def get_success_message(self, output: QueenOutput) -> str:
        return (
            f"Queen orchestration completed. Workers spawned: {len(output.workers_spawned)}, "
            f"Coordination status: {output.coordination_status}"
        )

    def create_worker_specific_files(
        self, session_id: str, output: QueenOutput, session_path: Path
    ) -> None:
        """Create queen-specific output files"""
        # Create orchestration plan file
        orchestration_dir = session_path / "workers" / "orchestration"
        orchestration_dir.mkdir(parents=True, exist_ok=True)

        # Create enhanced orchestration plan with execution metadata
        orchestration_data = output._orchestration_plan.model_dump()

        # Add execution metadata that was previously in worker_spawns.json
        orchestration_data["execution_metadata"] = {
            "workers_spawned": output.workers_spawned,
            "coordination_status": output.coordination_status,
            "monitoring_active": output.monitoring_active,
            "session_path": output.session_path,
            "execution_timestamp": output.timestamp,
        }

        orchestration_file = orchestration_dir / "orchestration_plan.json"
        orchestration_file.write_text(json.dumps(orchestration_data, indent=2))

        # Update SESSION.md with orchestration summary
        self._update_session_md(session_path, output._orchestration_plan, output)

    def _update_session_md(
        self, session_path: Path, orchestration_plan, output: QueenOutput
    ) -> None:
        """Update SESSION.md with Queen orchestration details"""
        session_md_path = session_path / "SESSION.md"

        if not session_md_path.exists():
            return

        try:
            content = session_md_path.read_text()
            lines = content.split("\n")

            # Look for Progress section to update
            progress_idx = -1
            notes_idx = -1

            for i, line in enumerate(lines):
                if line.startswith("## Progress"):
                    progress_idx = i
                elif line.startswith("## Notes"):
                    notes_idx = i
                    break

            if progress_idx == -1:
                return  # No Progress section found

            # Update progress section
            progress_section = [
                "## Progress",
                "- [x] Session initialization",
                "- [x] Queen orchestration completed",
                f"- [x] {len(orchestration_plan.worker_assignments)} workers planned",
                f"- [x] Execution strategy: {orchestration_plan.execution_strategy}",
                "- [ ] Worker deployment",
                "- [ ] Synthesis",
            ]

            # Create orchestration summary section
            orchestration_section = [
                "",
                "## Queen Orchestration Summary",
                f"**Coordination Complexity:** {orchestration_plan.coordination_complexity}/5",
                f"**Execution Strategy:** {orchestration_plan.execution_strategy}",
                f"**Estimated Duration:** {orchestration_plan.estimated_total_duration}",
                f"**Workers Deployed:** {len(orchestration_plan.worker_assignments)}",
                "",
                "### Strategic Assessment",
                orchestration_plan.orchestration_rationale,
                "",
                "### Worker Assignments",
            ]

            # Add worker assignments with priorities
            for assignment in orchestration_plan.worker_assignments:
                orchestration_section.append(
                    f"- **{assignment.worker_type}** ({assignment.priority}) - {assignment.task_focus}"
                )

            # Add coordination notes
            if orchestration_plan.coordination_notes:
                orchestration_section.extend(
                    [
                        "",
                        "### Coordination Strategy",
                    ]
                )
                for note in orchestration_plan.coordination_notes:
                    orchestration_section.append(f"- {note}")

            # Reconstruct content
            if notes_idx != -1:
                # Insert orchestration section before Notes
                new_lines = (
                    lines[:progress_idx]
                    + progress_section
                    + orchestration_section
                    + [""]
                    + lines[notes_idx:]
                )
            else:
                # Append orchestration section at the end
                new_lines = (
                    lines[:progress_idx] + progress_section + orchestration_section
                )

            # Write updated content
            session_md_path.write_text("\n".join(new_lines))

        except Exception as e:
            # Log error but don't fail the operation
            self.log_debug(
                "session_md_update_failed",
                {"error": str(e), "session_path": str(session_md_path)},
                "ERROR",
            )


def main():
    """Standard BaseWorker CLI entry point"""
    worker = QueenWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
