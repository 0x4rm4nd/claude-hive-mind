"""
Queen Orchestrator Models

Pydantic models specific to Queen orchestrator functionality.
"""

from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field

from shared.models import WorkerOutput


class WorkerAssignment(BaseModel):
    """Individual worker assignment with strategic reasoning"""

    worker_type: str = Field(
        description="Worker type (e.g., 'analyzer-worker', 'architect-worker')"
    )
    priority: Literal["critical", "high", "medium", "low"] = Field(
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
    """Service context for orchestration - factual mapping, no analysis"""

    service_name: str = Field(description="Service/component name")
    key_files: List[str] = Field(description="Files that need engineering attention")
    service_description: str = Field(description="What this service does (high-level)")
    technology_stack: List[str] = Field(
        default_factory=list,
        description="Technologies used (React, FastAPI, Redis, etc.)",
    )
    interaction_points: List[str] = Field(
        default_factory=list, description="How this service interacts with others"
    )


class QueenOrchestrationPlan(BaseModel):
    """Main orchestration plan output from Queen"""

    session_id: str = Field(default="", description="Session identifier")
    timestamp: str = Field(default="", description="ISO timestamp of plan creation")
    status: Literal["completed", "failed", "planning"] = Field(
        default="completed", description="Orchestration status"
    )

    # Orchestration understanding
    task_summary: str = Field(
        default="",
        description="Orchestrator's understanding of what needs to be accomplished",
    )
    coordination_complexity: int = Field(
        ge=1, le=5, description="Coordination complexity (not technical complexity)"
    )
    orchestration_rationale: str = Field(
        default="", description="Why these workers were selected for coordination"
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

    # Coordination details (orchestrator focus)
    coordination_notes: List[str] = Field(
        default_factory=list,
        description="How workers should coordinate and handoff results",
    )
    success_criteria: List[str] = Field(
        default_factory=list, description="High-level criteria for task completion"
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

    # Execution metadata (previously in worker_spawns.json)
    workers_spawned: List[str] = Field(
        default_factory=list, description="List of worker types spawned from this plan"
    )
    coordination_status: str = Field(
        default="planned", description="Current coordination status"
    )
    monitoring_active: bool = Field(
        default=False, description="Whether monitoring is currently active"
    )
    session_path: str = Field(
        default="", description="Full path to the session directory"
    )


class QueenOutput(WorkerOutput):
    """Queen orchestrator unified output extending WorkerOutput"""

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
