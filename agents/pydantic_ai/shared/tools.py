"""
Shared Tools and Utilities
==========================
Common functionality used across multiple agents.
"""

from datetime import datetime
from .protocols import load_project_env

# Load project environment on import
load_project_env()


def iso_now() -> str:
    """Generate ISO timestamp string"""
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
