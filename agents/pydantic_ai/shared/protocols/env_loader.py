"""
Environment variable loading utilities for the hive-mind system.
"""

from pathlib import Path
from dotenv import load_dotenv


def load_project_env():
    """Load environment variables from project root .env file"""
    # Start from any package location and find project root
    current_file = Path(__file__)

    # Look for project root markers - search up from .claude directory
    search_path = current_file.parent.parent  # Start from .claude

    for path in [search_path] + list(search_path.parents):
        env_file = path / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            return str(path)

    # Fallback - look for common project structure markers
    for path in [search_path] + list(search_path.parents):
        # Check for common project indicators
        if (
            (path / "package.json").exists()
            or (path / "requirements.txt").exists()
            or (path / "pyproject.toml").exists()
        ):
            env_file = path / ".env"
            if env_file.exists():
                load_dotenv(env_file)
                return str(path)

    # Last resort - try to load from search_path
    env_file = search_path / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        return str(search_path)

    return str(search_path)
