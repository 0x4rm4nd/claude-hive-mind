#!/usr/bin/env python3
"""
Agent Runner Wrapper

This wrapper avoids naming conflicts by creating a temporary symlink 
with a different name than 'pydantic' to avoid conflicts with the pydantic library.
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

def run_agent_with_clean_imports(agent_name: str, args_list: list):
    """
    Run an agent with clean imports by creating a temporary symlink with a different name.
    
    Args:
        agent_name: Name of the agent (scribe, queen, etc.)
        args_list: List of command line arguments to pass to the runner
    """
    # Get paths
    current_dir = Path(__file__).parent
    agents_dir = current_dir.parent
    
    # Create temporary directory for the symlink
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_agents_dir = Path(temp_dir) / "agents"
        temp_agents_dir.mkdir()
        
        # Create symlink with a different name to avoid pydantic library conflict
        pydantic_agents_link = temp_agents_dir / "pydantic_agents"
        pydantic_agents_link.symlink_to(current_dir, target_is_directory=True)
        
        # Set up the Python command with the temporary path
        runner_script = pydantic_agents_link / agent_name / "runner.py"
        
        cmd = [
            sys.executable,
            str(runner_script)
        ] + args_list
        
        # Set up environment with the temporary agents directory in Python path
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{temp_agents_dir}:{env.get('PYTHONPATH', '')}"
        
        # Run the command
        return subprocess.run(cmd, env=env)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_agent.py <agent_name> [args...]")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    agent_args = sys.argv[2:]
    
    result = run_agent_with_clean_imports(agent_name, agent_args)
    sys.exit(result.returncode)