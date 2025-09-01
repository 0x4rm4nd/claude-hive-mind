"""
Scribe Agent Models
==================
Pydantic models specific to Scribe agent functionality.
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field


class TaskSummaryOutput(BaseModel):
    """AI-generated task summary for session ID"""

    short_description: str = Field(
        description="2-4 hyphenated words summarizing the task (e.g., 'crypto-security-audit', 'api-performance-review')"
    )
    complexity_level: int = Field(
        ge=1, le=4, description="Task complexity assessment (1-4)"
    )
    focus_areas: List[str] = Field(description="Main areas this task will focus on")


class ScribeSessionCreationOutput(BaseModel):
    """Output from session creation"""

    session_id: str = Field(description="Generated session identifier")
    timestamp: str = Field(description="ISO timestamp of creation")
    status: str = Field(description="Creation status")
    task_description: str = Field(description="Original task description")
    complexity_level: int = Field(description="Assessed complexity level")
    session_path: str = Field(description="Full path to session directory")


class SynthesisOverview(BaseModel):
    """High-level synthesis facets for scribe output"""

    consensus: List[str] = []
    conflicts: List[str] = []
    themes: List[str] = []


class ScribeSynthesisOutput(BaseModel):
    """Output from synthesis process"""

    session_id: str = Field(description="Session identifier")
    timestamp: str = Field(description="ISO timestamp of synthesis")
    status: str = Field(description="Synthesis status")
    synthesis_markdown: str = Field(description="Generated synthesis content")
    synthesis_overview: SynthesisOverview = SynthesisOverview()
    sources: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional mapping of source filenames to key points used",
    )


class ScribeOutput(BaseModel):
    """Unified Scribe worker output for both create and synthesis modes"""
    
    mode: Literal["create", "synthesis"] = Field(description="Scribe operation mode")
    session_id: str = Field(description="Session identifier")
    timestamp: str = Field(description="ISO timestamp")
    status: str = Field(description="Operation status")
    
    # Session creation fields
    task_description: Optional[str] = Field(default=None, description="Original task")
    complexity_level: Optional[int] = Field(default=None, description="Task complexity")
    session_path: Optional[str] = Field(default=None, description="Session directory path")
    
    # Synthesis fields  
    synthesis_markdown: Optional[str] = Field(default=None, description="Synthesis content")
    synthesis_overview: Optional[SynthesisOverview] = Field(default=None, description="Synthesis overview")
    sources: Dict[str, Any] = Field(default_factory=dict, description="Synthesis sources")
    
    # Standard worker fields
    worker: Optional[str] = Field(default=None, description="Worker type")
    config: Optional[Dict[str, Any]] = Field(default=None, description="Worker configuration")
    notes_markdown: Optional[str] = Field(default=None, description="Additional notes")
