"""
Scribe Agent Models
==================
Pydantic models specific to Scribe agent functionality.
"""

from typing import List
from pydantic import BaseModel, Field


class TaskSummaryOutput(BaseModel):
    """AI-generated task summary for session ID"""
    short_description: str = Field(
        description="2-4 hyphenated words summarizing the task (e.g., 'crypto-security-audit', 'api-performance-review')"
    )
    complexity_level: int = Field(ge=1, le=4, description="Task complexity assessment (1-4)")
    focus_areas: List[str] = Field(description="Main areas this task will focus on")


class ScribeSessionCreationOutput(BaseModel):
    """Output from session creation"""
    session_id: str = Field(description="Generated session identifier")
    timestamp: str = Field(description="ISO timestamp of creation")
    status: str = Field(description="Creation status")
    task_description: str = Field(description="Original task description")
    complexity_level: int = Field(description="Assessed complexity level")
    session_path: str = Field(description="Full path to session directory")


class ScribeSynthesisOutput(BaseModel):
    """Output from synthesis process"""
    session_id: str = Field(description="Session identifier")
    timestamp: str = Field(description="ISO timestamp of synthesis")
    status: str = Field(description="Synthesis status")
    synthesis_markdown: str = Field(description="Generated synthesis content")