"""
Environment variable loading utilities for the hive-mind system.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


def detect_project_root() -> str:
    """Detect project root - looks for hive-mind directory structure"""
    current_path = Path.cwd()
    
    # Search upward for project markers
    while current_path != current_path.parent:
        # Check for definitive project markers
        if all([
            (current_path / "Docs" / "hive-mind").exists(),
            (current_path / ".claude").exists()
        ]):
            return str(current_path)
        
        current_path = current_path.parent
    
    raise ValueError(f"Could not detect project root with hive-mind structure from {Path.cwd()}")


def load_project_env():
    """Load environment variables from project root .env file"""
    project_root = detect_project_root()
    env_file = Path(project_root) / ".env"

    if env_file.exists():
        load_dotenv(env_file)
    
    return project_root
