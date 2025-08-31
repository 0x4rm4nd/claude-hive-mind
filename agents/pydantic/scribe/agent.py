"""
Scribe Agent
===========
AI agent for session creation and synthesis.
"""

import sys
import os

# Environment setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
from protocols import load_project_env
load_project_env()

from pydantic_ai import Agent

from .models import TaskSummaryOutput

# AI agent for generating task summaries
task_summary_agent = Agent(
    model="openai:gpt-4o-mini",
    output_type=TaskSummaryOutput,
    system_prompt=(
        "You analyze task descriptions and create concise session identifiers.\\n"
        "Generate a short 2-4 word hyphenated description that captures the essence.\\n" 
        "Focus on the main action and domain (e.g., 'crypto-security-audit', 'api-performance-review').\\n"
        "Assess complexity: 1=simple, 2=moderate, 3=complex, 4=very complex.\\n"
        "Be precise and professional."
    )
)