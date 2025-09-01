#!/usr/bin/env python3
"""
Queen Orchestrator Runner
=========================
BaseWorker implementation for strategic multi-worker orchestration.
"""

from typing import Dict, Any
from pathlib import Path

from shared.base_worker import BaseWorker
from queen.models import QueenOutput
from queen.agent import queen_agent, QueenAgentConfig
from shared.protocols import SessionManagement
from shared.tools import iso_now


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
        monitoring_mode = "--monitor" in task_description
        clean_task = task_description.replace(" --monitor", "").strip()
        
        # Use AI agent directly - no legacy functions
        orchestration_result = queen_agent.run_sync(
            f"Analyze task and create orchestration plan.\nTask: {clean_task}\nSession: {session_id}",
            model=model
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

        # Create worker spawn logs
        import json
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
