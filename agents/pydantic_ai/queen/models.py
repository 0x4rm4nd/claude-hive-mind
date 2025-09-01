"""
Queen Orchestrator Models

Pydantic models specific to Queen orchestrator functionality.
"""

from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field

from ..shared.models import WorkerOutput


class WorkerAssignment(BaseModel):
    """Individual worker assignment with strategic reasoning"""

    worker_type: str = Field(
        description="Worker type (e.g., 'analyzer-worker', 'architect-worker')"
    )
    priority: Literal["high", "medium", "low"] = Field(
        default="medium", description="Strategic priority for this worker"
    )
    task_focus: str = Field(
        description="Specific focus area and objectives for this worker"
    )
    dependencies: List[str] = Field(
        default_factory=list, description="Other workers this depends on"
    )
    estimated_duration: str = Field(
        default="1-2h", description="Estimated time (e.g., '30min', '1-2h')"
    )
    strategic_value: Literal["critical", "high", "medium", "low"] = Field(
        default="medium", description="Strategic value of this worker's contribution"
    )
    rationale: str = Field(
        default="Required for task completion",
        description="Queen's strategic reasoning for including this worker",
    )


class CodebaseInsight(BaseModel):
    """Codebase exploration insight"""

    service_name: str = Field(description="Service/component name")
    key_files: List[str] = Field(description="Important files found")
    architecture_notes: List[str] = Field(description="Architecture observations")
    potential_issues: List[str] = Field(description="Potential areas of concern")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in assessment")


class QueenOrchestrationPlan(BaseModel):
    """Main orchestration plan output from Queen"""

    session_id: str = Field(default="", description="Session identifier")
    timestamp: str = Field(default="", description="ISO timestamp of plan creation")
    status: Literal["completed", "failed"] = Field(
        default="completed", description="Orchestration status"
    )

    # Strategic task analysis
    strategic_assessment: Dict[str, Any] = Field(
        default_factory=dict, description="Multi-dimensional strategic task assessment"
    )
    complexity_assessment: int = Field(
        ge=1, le=4, description="Overall complexity rating (1-4, guidance only)"
    )
    strategic_rationale: str = Field(
        default="", description="Queen's reasoning for worker selection and approach"
    )
    estimated_total_duration: str = Field(
        default="2-4h", description="Total estimated time for all workers"
    )

    # Worker coordination
    worker_assignments: List[WorkerAssignment] = Field(
        default_factory=list, description="List of workers and their assignments"
    )
    execution_strategy: Literal["parallel", "sequential", "hybrid"] = Field(
        default="parallel", description="How workers should be executed"
    )

    # Coordination details
    coordination_notes: List[str] = Field(
        default_factory=list, description="Important coordination considerations"
    )
    identified_risks: List[str] = Field(
        default_factory=list, description="Potential risks and blockers identified"
    )
    mitigation_strategies: List[str] = Field(
        default_factory=list, description="Risk mitigation approaches"
    )
    success_metrics: List[str] = Field(
        default_factory=list, description="How to measure success"
    )
    quality_gates: List[str] = Field(
        default_factory=list, description="Quality checkpoints before proceeding"
    )

    # Optional codebase insights
    codebase_insights: List[CodebaseInsight] = Field(
        default_factory=list, description="Insights from codebase exploration"
    )

    # Task execution plan for main Claude agent
    task_execution_plan: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Claude Code Task parameters for spawning workers",
    )


class QueenOutput(WorkerOutput):
    """Queen orchestrator unified output extending WorkerOutput"""

    orchestration_plan: QueenOrchestrationPlan = Field(
        description="Generated orchestration plan with strategic analysis"
    )
    workers_spawned: List[str] = Field(
        default_factory=list, description="Workers successfully spawned"
    )
    coordination_status: Literal["planned", "active", "completed", "failed"] = Field(
        description="Overall coordination status"
    )
    monitoring_active: bool = Field(
        default=False, description="Whether monitoring is active"
    )
    session_path: str = Field(
        description="Session directory path for coordination files"
    )
