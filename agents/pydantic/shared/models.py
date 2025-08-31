from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field


Status = Literal["completed", "blocked", "failed"]


class WorkerSummary(BaseModel):
    key_findings: List[str] = []
    critical_issues: List[str] = []
    recommendations: List[str] = []


class WorkerMetrics(BaseModel):
    items_analyzed: int = 0
    issues_found: int = 0
    severity_breakdown: Dict[str, int] = {}


class WorkerDependencies(BaseModel):
    requires: List[str] = []
    blocks: List[str] = []
    handoffs: List[str] = []


class WorkerOutput(BaseModel):
    """Canonical worker output aligned with worker-output-protocol.md"""

    worker: str
    session_id: str
    timestamp: str
    status: Status
    summary: WorkerSummary
    analysis: Dict[str, Any] = {}
    metrics: WorkerMetrics = WorkerMetrics()
    dependencies: WorkerDependencies = WorkerDependencies()
    files_examined: List[str] = []
    files_modified: List[str] = []
    next_actions: List[str] = []
    # Optional notes content to write deterministically by the host
    notes_markdown: str = Field(default="", description="Full notes content for workers/notes/{worker}_notes.md")


class SynthesisOverview(BaseModel):
    """High-level synthesis facets for scribe output"""

    consensus: List[str] = []
    conflicts: List[str] = []
    themes: List[str] = []


class ScribeSynthesisOutput(BaseModel):
    """Scribe synthesis result (no scribe notes or scribe JSON output).

    The scribe aggregates other workers' outputs and produces a single
    synthesis document written to notes/RESEARCH_SYNTHESIS.md.
    """

    session_id: str
    timestamp: str
    status: Status
    synthesis_markdown: str = Field(description="Full content for workers/notes/RESEARCH_SYNTHESIS.md")
    synthesis_overview: SynthesisOverview = SynthesisOverview()
    sources: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional mapping of source filenames to key points used",
    )


class ScribeSessionCreationOutput(BaseModel):
    """Scribe session creation result - creates new session structure."""
    
    session_id: str = Field(description="Generated session ID in YYYY-MM-DD-HH-mm-shorttaskdescription format")
    timestamp: str
    status: Status  
    task_description: str = Field(description="The task description that was provided")
    complexity_level: int = Field(ge=1, le=4, description="Task complexity assessment (1-4)")
    session_path: str = Field(description="Full path to created session directory")


class TaskSummaryOutput(BaseModel):
    """AI-generated task summary for session ID"""
    short_description: str = Field(
        description="2-4 hyphenated words summarizing the task (e.g., 'crypto-security-audit', 'api-performance-review')"
    )
    complexity_level: int = Field(ge=1, le=4, description="Task complexity assessment (1-4)")
    focus_areas: List[str] = Field(description="Main areas this task will focus on")


class WorkerAssignment(BaseModel):
    """Individual worker assignment"""
    worker_type: str = Field(description="Worker type (e.g., 'analyzer-worker', 'architect-worker')")
    priority: Literal["high", "medium", "low"] = Field(default="medium", description="Task priority for this worker")
    task_focus: str = Field(description="Specific focus area for this worker")
    dependencies: List[str] = Field(default_factory=list, description="Other workers this depends on")
    estimated_duration: str = Field(default="1-2h", description="Estimated time (e.g., '30min', '1-2h')")
    rationale: str = Field(default="Required for comprehensive analysis", description="Why this worker is needed")


class CodebaseInsight(BaseModel):
    """Codebase exploration insight"""
    service_name: str = Field(description="Service/component name")
    key_files: List[str] = Field(description="Important files found")
    architecture_notes: List[str] = Field(description="Architecture observations")
    potential_issues: List[str] = Field(description="Potential areas of concern")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in assessment")


class QueenOrchestrationPlan(BaseModel):
    """Queen's orchestration plan output"""
    session_id: str = Field(default="", description="Session identifier")
    timestamp: str = Field(default="", description="Timestamp when plan was created")
    status: Status = Field(default="completed", description="Plan status")
    
    # Task Analysis
    task_analysis: Dict[str, Any] = Field(default_factory=dict, description="Detailed task breakdown and analysis")
    complexity_assessment: int = Field(default=2, ge=1, le=4, description="Overall complexity (1-4)")
    estimated_total_duration: str = Field(default="2-4h", description="Total estimated time")
    
    # Codebase Insights (if exploration was performed)
    codebase_insights: List[CodebaseInsight] = Field(default_factory=list, description="Codebase analysis results")
    
    # Worker Orchestration  
    worker_assignments: List[WorkerAssignment] = Field(default_factory=list, description="Detailed worker assignments")
    execution_strategy: Literal["parallel", "sequential", "hybrid"] = Field(default="parallel", description="Execution approach")
    coordination_notes: List[str] = Field(default_factory=list, description="Special coordination requirements")
    
    # Risk Assessment
    identified_risks: List[str] = Field(default_factory=list, description="Potential risks and blockers")
    mitigation_strategies: List[str] = Field(default_factory=list, description="Risk mitigation approaches")
    
    # Success Criteria
    success_metrics: List[str] = Field(default_factory=list, description="How to measure success")
    quality_gates: List[str] = Field(default_factory=list, description="Quality checkpoints")
