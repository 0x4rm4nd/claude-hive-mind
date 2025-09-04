"""
Environment variable loading utilities for the hive-mind system.
"""

import os
from pathlib import Path
from dotenv import load_dotenv



def load_project_env():
    """Load environment variables from project root .env file"""
    # Use absolute import to avoid circular import issues during package loading
    try:
        from shared.protocols.session_management import SessionManagement
        project_root = SessionManagement.detect_project_root()
    except ImportError:
        # Fallback: duplicate the minimal detection logic
        current_path = Path.cwd()
        while current_path != current_path.parent:
            if all([
                (current_path / "Docs" / "hive-mind").exists(),
                (current_path / ".claude").exists()
            ]):
                project_root = str(current_path)
                break
            current_path = current_path.parent
        else:
            raise ValueError(f"Could not detect project root with hive-mind structure from {Path.cwd()}")
    env_file = Path(project_root) / ".env"

    if env_file.exists():
        load_dotenv(env_file)
    
    return project_root
