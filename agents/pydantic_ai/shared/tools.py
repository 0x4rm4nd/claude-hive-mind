"""
Shared Tools and Utilities
==========================
Common functionality used across multiple agents.
"""

import os
from pathlib import Path
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


