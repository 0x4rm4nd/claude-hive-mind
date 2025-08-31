"""
Import Helper for Pydantic AI Agents

This module provides clean import functionality to avoid naming conflicts
with the pydantic library when running agents as standalone scripts.
"""

import os
import sys
import importlib.util
from typing import Any


def setup_agent_imports(runner_file_path: str):
    """
    Set up the Python environment for an agent runner to avoid naming conflicts.
    
    Args:
        runner_file_path: The __file__ path of the calling runner
    """
    # Remove current directory and parent directories to avoid pydantic naming conflicts
    runner_dir = os.path.dirname(runner_file_path)
    pydantic_dir = os.path.dirname(runner_dir)
    agents_dir = os.path.dirname(pydantic_dir)
    
    # Clean up sys.path to avoid conflicts
    paths_to_remove = [runner_dir, pydantic_dir, agents_dir]
    for path in paths_to_remove:
        if path in sys.path:
            sys.path.remove(path)
    
    # Add the project root for other imports (not pydantic-related ones)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(agents_dir)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


def import_shared_module(module_name: str, runner_file_path: str):
    """
    Import a module from the shared directory using direct file loading.
    
    Args:
        module_name: Name of the module (e.g., 'session_management', 'tools')
        runner_file_path: The __file__ path of the calling runner
        
    Returns:
        The loaded module
    """
    runner_dir = os.path.dirname(runner_file_path)
    
    # Handle case where we're calling from within shared/ directory
    if runner_dir.endswith('/shared'):
        shared_dir = runner_dir
    else:
        shared_dir = os.path.join(runner_dir, '..', 'shared')
    
    if module_name == 'session_management':
        module_path = os.path.join(shared_dir, 'protocols', 'session_management.py')
    elif module_name == 'tools':
        module_path = os.path.join(shared_dir, 'tools.py')
    else:
        # For other shared modules, assume they're directly in shared/
        module_path = os.path.join(shared_dir, f'{module_name}.py')
    
    if not os.path.exists(module_path):
        raise ImportError(f"Could not find shared module: {module_name} at {module_path}")
    
    spec = importlib.util.spec_from_file_location(f'shared_{module_name}', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def import_local_module(module_name: str, runner_file_path: str):
    """
    Import a module from the same directory as the runner.
    
    Args:
        module_name: Name of the module (e.g., 'models', 'agent')
        runner_file_path: The __file__ path of the calling runner
        
    Returns:
        The loaded module
    """
    runner_dir = os.path.dirname(runner_file_path)
    module_path = os.path.join(runner_dir, f'{module_name}.py')
    
    if not os.path.exists(module_path):
        raise ImportError(f"Could not find local module: {module_name} at {module_path}")
    
    spec = importlib.util.spec_from_file_location(f'local_{module_name}', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_from_module(module: Any, attr_name: str):
    """
    Get an attribute from a module with error handling.
    
    Args:
        module: The module to get the attribute from
        attr_name: Name of the attribute to get
        
    Returns:
        The requested attribute
    """
    if not hasattr(module, attr_name):
        raise ImportError(f"Module {module.__name__} has no attribute '{attr_name}'")
    
    return getattr(module, attr_name)