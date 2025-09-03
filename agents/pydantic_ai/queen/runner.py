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
from shared.tools import iso_now

# Ensure imports work when run directly or from CLI
current_dir = Path(__file__).parent
pydantic_ai_root = current_dir.parent
if str(pydantic_ai_root) not in sys.path:
    sys.path.insert(0, str(pydantic_ai_root))


class QueenWorker(BaseWorker[QueenOutput]):
    """
    Strategic multi-worker orchestrator and coordination manager.

    Analyzes complex tasks to determine optimal worker assignments and provides
    continuous monitoring of worker progress and coordination.
    """

    def __init__(self):
        super().__init__(
            worker_type="queen-orchestrator",
            worker_config=None,
            output_model=QueenOutput,
        )

    def run(self, session_id: str, task_description: str, model: str) -> QueenOutput:
        """Run queen orchestrator with runtime worker config"""
        # Create worker config at runtime with actual values
        self.worker_config = QueenAgentConfig.create_worker_config(
            session_id, task_description
        )
        return self.run_analysis(session_id, task_description, model)

    def execute_ai_analysis(
        self, session_id: str, task_description: str, model: str
    ) -> Any:
        """Execute orchestration analysis using Pydantic AI agent"""
        # Log queen spawned event
        self.log_event(
            session_id,
            "queen_spawned",
            {
                "worker_type": "queen-orchestrator",
                "mode": "orchestration",
                "purpose": "Task AI Analysis",
            },
        )

        # Log analysis started event after queen spawned
        self.log_event(
            session_id,
            "analysis_started",
            self.get_analysis_event_details(task_description),
        )

        monitoring_mode = "--monitor" in task_description
        clean_task = task_description.replace(" --monitor", "").strip()

        queen_prompt = f"Using the Queen Agent, analyze task and create orchestration plan.\nTask: {clean_task}\nSession: {session_id}"

        # Handle custom models with system prompt override
        if model.startswith("custom:"):
            system_prompt = (
                "You are a JSON generator. "
                "Your ONLY job is to output valid JSON. "
                "NEVER write explanatory text. "
                "NEVER write 'The Queen Agent has completed...' "
                "NEVER use ```json blocks. "
                "DO NOT explain what you are doing. "
                "OUTPUT FORMAT: Start immediately with { and end with } "
                "REQUIRED FIELDS: session_id, timestamp, status (completed/failed/planning), strategic_assessment (object), complexity_assessment (number), strategic_rationale (string), estimated_total_duration (string), worker_assignments (array), execution_strategy (parallel/sequential/hybrid), coordination_notes (string array), identified_risks (string array), mitigation_strategies (string array), success_metrics (string array), quality_gates (string array), codebase_insights (array of objects with service_name string, key_files string array, architecture_notes string array, potential_issues string array, confidence float). "
                "worker_assignments items need: worker_type (analyzer-worker/architect-worker/backend-worker/frontend-worker/designer-worker/devops-worker/researcher-worker/test-worker), priority (critical/high/medium/low), task_focus (string), dependencies (string array), estimated_duration (string), strategic_value (critical/high/medium/low), rationale (string). "
                'RESPOND ONLY WITH: {"session_id": "2025-09-03-11-10-queen-orchestration-test", "timestamp": "2025-09-03T11:10:00Z", "status": "completed", "strategic_assessment": {}, "complexity_assessment": 3, "strategic_rationale": "Analysis complete", "estimated_total_duration": "2h", "worker_assignments": [{"worker_type": "test-worker", "priority": "high", "task_focus": "test focus", "dependencies": [], "estimated_duration": "1h", "strategic_value": "high", "rationale": "test rationale"}], "execution_strategy": "sequential", "coordination_notes": ["test note"], "identified_risks": ["test risk"], "mitigation_strategies": ["test strategy"], "success_metrics": ["test metric"], "quality_gates": ["test gate"], "codebase_insights": [{"service_name": "test-service", "key_files": ["test.py"], "architecture_notes": ["note"], "potential_issues": ["issue"], "confidence": 0.8}]}'
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

        queen_output = QueenOutput(
            worker="queen-orchestrator",
            session_id=session_id,
            timestamp=iso_now(),
            status="completed",
            summary={
                "key_findings": [
                    f"Orchestration plan generated with {len(orchestration_plan.worker_assignments)} workers"
                ],
                "critical_issues": [],
                "recommendations": [
                    assignment.rationale
                    for assignment in orchestration_plan.worker_assignments
                ],
            },
            orchestration_plan=orchestration_plan,
            workers_spawned=[
                assignment.worker_type
                for assignment in orchestration_plan.worker_assignments
            ],
            coordination_status="planned",
            monitoring_active=monitoring_mode,
            session_path=str(session_path),
        )

        # Return mock result object with output attribute for BaseWorker compatibility
        class MockResult:
            def __init__(self, output):
                self.output = output

        return MockResult(queen_output)

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

        orchestration_file = orchestration_dir / "orchestration_plan.json"
        orchestration_file.write_text(
            output.orchestration_plan.model_dump_json(indent=2)
        )

        spawn_log_file = orchestration_dir / "worker_spawns.json"
        spawn_log = {
            "workers_spawned": output.workers_spawned,
            "coordination_status": output.coordination_status,
            "monitoring_active": output.monitoring_active,
            "session_path": output.session_path,
            "timestamp": output.timestamp,
        }
        spawn_log_file.write_text(json.dumps(spawn_log, indent=2))


def main():
    """Standard BaseWorker CLI entry point"""
    worker = QueenWorker()
    return worker.run_cli_main()


if __name__ == "__main__":
    exit(main())
