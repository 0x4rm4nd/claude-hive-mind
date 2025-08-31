"""
Pydantic AI Agents Module
=========================
Bridge module for backward compatibility with expected import paths.
Maps agents.pydantic.* to agents.pydantic_ai.*
"""

# Re-export main modules for backward compatibility
from ..pydantic_ai import *
from ..pydantic_ai.cli import run_scribe, run_queen

__all__ = ['run_scribe', 'run_queen']