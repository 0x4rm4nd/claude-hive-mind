"""
Shared Tools and Utilities
==========================
Common functionality used across multiple agents.
"""

import sys
import os
from pathlib import Path

# Environment setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from protocols import load_project_env
from datetime import datetime

load_project_env()


def iso_now() -> str:
    """Generate ISO timestamp string"""
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def detect_project_root() -> str:
    """Detect project root directory"""
    current_path = Path.cwd()

    # Search upward for project markers
    for path in [current_path] + list(current_path.parents):
        if (
            (path / "api").exists()
            and (path / "frontend").exists()
            and (path / "crypto-data").exists()
        ):
            return str(path)

    # Fallback - go up from .claude directory
    if ".claude" in str(current_path):
        claude_path = Path(str(current_path).split(".claude")[0]) / ".claude"
        return str(claude_path.parent)

    return str(current_path.parent)
