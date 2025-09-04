"""
Environment variable loading utilities for the hive-mind system.
"""

from pathlib import Path
from dotenv import load_dotenv
from shared.protocols.session_management import SessionManagement


def load_project_env():
    """Load environment variables from project root .env file"""
    # Use absolute import to avoid circular import issues during package loading
    project_root = SessionManagement.detect_project_root()
    env_file = Path(project_root) / ".env"

    if env_file.exists():
        load_dotenv(env_file)

    return project_root
