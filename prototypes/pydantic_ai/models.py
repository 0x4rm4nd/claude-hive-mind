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
    notes_markdown: str = Field(default="", description="Full notes content for notes/{worker}_notes.md")


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
    synthesis_markdown: str = Field(description="Full content for notes/RESEARCH_SYNTHESIS.md")
    synthesis_overview: SynthesisOverview = SynthesisOverview()
    sources: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional mapping of source filenames to key points used",
    )
