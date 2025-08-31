"""
Shared Tools and Utilities
==========================
Common functionality used across multiple agents.
"""

import sys
import os
from pathlib import Path

# Environment setup - protocols now imported via relative imports

# Import protocols using direct file loading to avoid relative import issues
import os
import importlib.util

# Load load_project_env directly
protocols_init_path = os.path.join(os.path.dirname(__file__), 'protocols', '__init__.py')
spec = importlib.util.spec_from_file_location('protocols_module', protocols_init_path)
protocols_module = importlib.util.module_from_spec(spec)

# Load the env_loader module which contains load_project_env
env_loader_path = os.path.join(os.path.dirname(__file__), 'protocols', 'env_loader.py')
spec = importlib.util.spec_from_file_location('env_loader', env_loader_path)
env_loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(env_loader)
load_project_env = env_loader.load_project_env
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
