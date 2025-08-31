#!/usr/bin/env python3
"""
Conflict-Free Agent Runner

This script runs agent runners by temporarily creating a directory structure 
that avoids the pydantic naming conflict.
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path


def run_agent_without_conflict(agent_name: str, args: list[str]) -> int:
    """
    Run an agent by creating a temporary structure without naming conflicts.
    
    Args:
        agent_name: Name of the agent ('scribe', 'queen', etc.)
        args: Command line arguments to pass to the runner
        
    Returns:
        Exit code from the runner
    """
    current_dir = Path(__file__).parent  # /path/to/.claude/agents/pydantic
    agents_dir = current_dir.parent      # /path/to/.claude/agents
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        
        # Create the temporary structure
        temp_agents = temp_dir / "agents"
        temp_agents.mkdir()
        
        # Copy the entire pydantic directory with a different name
        temp_pydantic = temp_agents / "pydantic_ai_agents"
        shutil.copytree(current_dir, temp_pydantic, symlinks=True)
        
        # Set up the environment
        env = os.environ.copy()
        # Add temp_agents to Python path so 'import pydantic_ai_agents.shared.protocols' works
        env['PYTHONPATH'] = f"{temp_agents}:{env.get('PYTHONPATH', '')}"
        
        # Run the runner script
        runner_path = temp_pydantic / agent_name / "runner.py"
        
        cmd = [sys.executable, str(runner_path)] + args
        
        # Execute with modified environment
        result = subprocess.run(cmd, env=env)
        return result.returncode


def main():
    """Main entry point - parse args and run the appropriate agent."""
    if len(sys.argv) < 3:
        print("Usage: python run_without_conflict.py <agent_name> <runner_args...>")
        print("Example: python run_without_conflict.py scribe create --task 'test' --model 'openai:gpt-4o-mini'")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    runner_args = sys.argv[2:]
    
    exit_code = run_agent_without_conflict(agent_name, runner_args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()