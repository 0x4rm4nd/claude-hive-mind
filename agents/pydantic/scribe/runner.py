#!/usr/bin/env python3
"""
Scribe Agent Runner

Handles session creation and task summarization.
"""

import argparse
import json
import os
import re
from datetime import datetime
import sys

# Critical: Ensure the real pydantic library is imported correctly
# Manipulate sys.path to avoid the naming conflict with our 'pydantic' directory

script_dir = os.path.dirname(os.path.abspath(__file__))
pydantic_agents_dir = os.path.dirname(script_dir)  # The 'pydantic' directory
agents_dir = os.path.dirname(pydantic_agents_dir)  # The 'agents' directory  
project_root = os.path.dirname(os.path.dirname(agents_dir))  # The project root

# CRITICAL: Remove the agents directory from sys.path to prevent the naming conflict
sys.path = [p for p in sys.path if not (agents_dir in p or pydantic_agents_dir in p)]

# Add project root for general imports
sys.path.insert(0, project_root)

# Now we can safely import the real pydantic library
from pydantic import BaseModel, Field
from pydantic_ai import Agent

# Import our modules using full paths to avoid the naming conflict
# Import shared modules by dynamically loading them
import importlib.util

def load_module_from_file(module_name: str, file_path: str):
    """Load a module directly from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module {module_name} from {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load shared modules
session_mgmt_path = os.path.join(pydantic_agents_dir, 'shared', 'protocols', 'session_management.py')
session_mgmt_module = load_module_from_file('session_management', session_mgmt_path)
SessionManagement = session_mgmt_module.SessionManagement

tools_path = os.path.join(pydantic_agents_dir, 'shared', 'tools.py')

# Tools.py has its own relative import issue, so let's load what we need directly
# For now, implement the functions we need inline
def iso_now() -> str:
    """Return current timestamp in ISO format"""
    return datetime.utcnow().isoformat() + "Z"

def detect_project_root() -> str:
    """Detect the project root directory"""
    current = os.path.abspath(os.getcwd())
    
    # Look for key project indicators
    while current != os.path.dirname(current):  # Not at filesystem root
        if any(os.path.exists(os.path.join(current, indicator)) for indicator in [
            '.git', 'pyproject.toml', 'package.json', 'Cargo.toml', 'go.mod'
        ]):
            return current
        if os.path.basename(current) == 'SmartWalletFX':
            return current
        current = os.path.dirname(current)
    
    # Fallback - go up from .claude directory
    current = script_dir
    while current and not current.endswith('SmartWalletFX'):
        current = os.path.dirname(current)
        if os.path.basename(current) == 'SmartWalletFX':
            return current
    
    return os.getcwd()

# Load local modules
models_path = os.path.join(script_dir, 'models.py')
scribe_models = load_module_from_file('scribe_models', models_path)
ScribeSynthesisOutput = scribe_models.ScribeSynthesisOutput
ScribeSessionCreationOutput = scribe_models.ScribeSessionCreationOutput
TaskSummaryOutput = scribe_models.TaskSummaryOutput

# For the agent, we'll need to be more careful because it imports the problematic modules
# Let's implement the functionality inline for now

# Simple task summarization using direct pydantic_ai usage
class TaskSummary(BaseModel):
    summary: str
    key_requirements: list[str]
    complexity_estimate: int  # 1-4 scale
    suggested_approach: str

task_summary_agent = Agent(
    model='openai:gpt-4o-mini',
    result_type=TaskSummary,
    system_prompt="""You are a task analysis specialist. Analyze tasks and provide:

    1. A clear, concise summary of what needs to be done
    2. Key requirements and constraints 
    3. Complexity estimate (1=simple, 2=moderate, 3=complex, 4=very complex)
    4. Suggested implementation approach

    Focus on technical accuracy and actionable insights."""
)


def generate_ai_session_id(task_description: str, model: str) -> tuple[str, int]:
    """Generate session ID using AI to create better short description"""
    timestamp = datetime.utcnow().strftime('%Y-%m-%d-%H-%M')
    
    # Use AI to generate a concise description
    class SessionDescription(BaseModel):
        short_name: str  # 1-3 words, lowercase, hyphens for spaces
    
    desc_agent = Agent(model, result_type=SessionDescription)
    
    prompt = f"""Create a very short description (1-3 words) for this task: {task_description}
    
    Requirements:
    - Maximum 3 words
    - Use lowercase
    - Use hyphens instead of spaces
    - Be descriptive but concise
    
    Examples:
    - "add user authentication" -> "user-auth"
    - "fix database connection issues" -> "db-fix"  
    - "implement payment processing" -> "payment-proc"
    """
    
    try:
        result = desc_agent.run_sync(prompt)
        short_desc = result.data.short_name
        # Clean and validate the description
        short_desc = re.sub(r'[^a-z0-9\-]', '', short_desc.lower())
        short_desc = re.sub(r'-+', '-', short_desc).strip('-')
        
        if len(short_desc) > 20:  # Fallback if too long
            short_desc = short_desc[:20]
        
        session_id = f"{timestamp}-{short_desc}"
        return session_id, len(short_desc)
        
    except Exception as e:
        # Fallback to simple approach
        print(f"AI description failed: {e}")
        # Extract first few meaningful words
        words = re.findall(r'\b[a-z]+\b', task_description.lower())[:3]
        short_desc = '-'.join(words) if words else 'task'
        session_id = f"{timestamp}-{short_desc}"
        return session_id, len(short_desc)


def create_session(task_description: str, model: str) -> ScribeSessionCreationOutput:
    """Create a new session with proper directory structure"""
    
    # Generate session ID
    session_id, desc_length = generate_ai_session_id(task_description, model)
    
    # Set up paths
    project_root = detect_project_root()
    sessions_dir = os.path.join(project_root, "Docs", "hive-mind", "sessions")
    session_path = os.path.join(sessions_dir, session_id)
    
    # Create session directories
    os.makedirs(session_path, exist_ok=True)
    os.makedirs(os.path.join(session_path, "prompts"), exist_ok=True)
    os.makedirs(os.path.join(session_path, "workers", "notes"), exist_ok=True)
    
    # Initialize session management
    session_mgmt = SessionManagement(session_id, session_path)
    
    # Log session creation
    session_mgmt.log_event("session_created", "scribe", {
        "timestamp": iso_now(),
        "task_description": task_description,
        "model": model,
        "session_path": session_path,
        "generated_by": "scribe",
        "description_length": desc_length
    })
    
    # Log scribe spawn
    session_mgmt.log_event("worker_spawned", "scribe", {
        "timestamp": iso_now(),
        "worker_type": "scribe",
        "mode": "create",
        "model": model,
        "purpose": "session_creation"
    })
    
    # Create initial STATE.json
    initial_state = {
        "session_id": session_id,
        "created": iso_now(),
        "task_description": task_description,
        "model": model,
        "status": "created",
        "phase": "initialization",
        "workers": {
            "scribe": {
                "status": "active",
                "spawned_at": iso_now(),
                "mode": "create"
            }
        }
    }
    
    with open(os.path.join(session_path, "STATE.json"), "w") as f:
        json.dump(initial_state, f, indent=2)
    
    return ScribeSessionCreationOutput(
        session_id=session_id,
        session_path=session_path,
        task_description=task_description,
        model=model,
        status="created",
        created_at=iso_now()
    )


def summarize_task(session_id: str, task: str, model: str) -> TaskSummaryOutput:
    """Generate task summary using the AI agent"""
    result = task_summary_agent.run_sync(
        f"Analyze and summarize this task: {task}",
        model=model
    )
    
    return TaskSummaryOutput(
        session_id=session_id,
        original_task=task,
        summary=result.data.summary,
        key_requirements=result.data.key_requirements,
        complexity_estimate=result.data.complexity_estimate,
        suggested_approach=result.data.suggested_approach,
        model_used=model
    )


def main():
    parser = argparse.ArgumentParser(description="Scribe Agent - Session creation and task summarization")
    parser.add_argument("mode", choices=["create", "summarize"], help="Operation mode")
    parser.add_argument("--session", help="Session ID (for summarize mode)")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--model", default="openai:gpt-4o-mini", help="Model to use")
    
    args = parser.parse_args()
    
    try:
        if args.mode == "create":
            result = create_session(args.task, args.model)
            print(json.dumps(result.model_dump(), indent=2))
            
        elif args.mode == "summarize":
            if not args.session:
                raise ValueError("--session is required for summarize mode")
            result = summarize_task(args.session, args.task, args.model) 
            print(json.dumps(result.model_dump(), indent=2))
            
    except Exception as e:
        error_response = {
            "error": str(e),
            "mode": args.mode,
            "task": args.task,
            "model": args.model
        }
        print(json.dumps(error_response, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()