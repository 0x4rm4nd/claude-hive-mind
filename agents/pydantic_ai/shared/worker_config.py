"""
Worker Configuration Models
==========================
Pydantic models for worker configuration, replacing STATE.json configuration.
"""

from typing import List, Dict, Any, Literal, Optional, ClassVar
from pydantic import BaseModel, Field


class WorkerConfig(BaseModel):
    """Configuration for a Pydantic AI worker"""

    # Core Identity
    worker_type: str = Field(description="Worker type identifier")
    session_id: str = Field(description="Session this worker belongs to")

    # Memory Bank Access
    tag_access: List[str] = Field(
        default_factory=list, description="Memory bank tags this worker can access"
    )

    # Escalation Configuration
    escalation_timeout: int = Field(
        default=300, description="Timeout in seconds before escalation"
    )
    escalation_chain: List[str] = Field(
        default_factory=lambda: ["queen-orchestrator"],
        description="Escalation chain for blocked/failed workers",
    )

    # Task Configuration
    complexity_level: Literal[1, 2, 3, 4] = Field(
        default=2, description="Task complexity level (1=simple, 4=complex)"
    )
    task_description: str = Field(description="Specific task for this worker")

    # Coordination
    dependencies: List[str] = Field(
        default_factory=list, description="Other workers this one depends on"
    )
    priority: Literal["critical", "high", "medium", "low"] = Field(
        default="medium", description="Worker execution priority"
    )


class WorkerTagMapping(BaseModel):
    """Standard tag access patterns for different worker types"""

    WORKER_TAGS: ClassVar[Dict[str, List[str]]] = {
        "architect-worker": ["architecture", "patterns", "design"],
        "analyzer-worker": ["security", "performance", "quality"],
        "devops-worker": ["infrastructure", "deployment", "monitoring"],
        "researcher-worker": ["research", "patterns", "standards"],
        "test-worker": ["testing", "quality", "coverage"],
        "frontend-worker": ["frontend", "ui", "components"],
        "designer-worker": ["design", "ux", "accessibility"],
        "backend-worker": ["backend", "api", "architecture"],
    }

    @classmethod
    def get_tags_for_worker(cls, worker_type: str) -> List[str]:
        """Get standard tag access for a worker type"""
        return cls.WORKER_TAGS.get(worker_type, [])
