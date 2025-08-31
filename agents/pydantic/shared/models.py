"""
Shared Models for Pydantic AI Agents
====================================

This module contains ONLY models that are truly shared across multiple agents.
Agent-specific models belong in their respective agent directories:
- Queen-specific models: queen/models.py
- Scribe-specific models: scribe/models.py  
- Worker-specific models: [worker]/models.py
"""

from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field


# Shared type definitions
Status = Literal["completed", "blocked", "failed"]


class WorkerSummary(BaseModel):
    """Standard summary format used by all workers"""
    key_findings: List[str] = []
    critical_issues: List[str] = []
    recommendations: List[str] = []


class WorkerMetrics(BaseModel):
    """Standard metrics format used by all workers"""
    items_analyzed: int = 0
    issues_found: int = 0
    severity_breakdown: Dict[str, int] = {}


class WorkerDependencies(BaseModel):
    """Cross-worker dependency tracking used by all workers"""
    requires: List[str] = []
    blocks: List[str] = []
    handoffs: List[str] = []


class WorkerOutput(BaseModel):
    """
    Canonical worker output format aligned with worker-output-protocol.md
    
    This is the base output format that ALL workers must use or extend.
    It provides a consistent structure for cross-worker communication
    and protocol compliance.
    """
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
    notes_markdown: str = Field(
        default="", 
        description="Full notes content for workers/notes/{worker}_notes.md"
    )
