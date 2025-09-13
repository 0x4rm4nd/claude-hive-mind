"""
Worker Prompt Templates
======================
Centralized prompt templates for worker coordination and synthesis.
"""

from pathlib import Path
from typing import Dict, Any


def load_scribe_template() -> str:
    """Load the scribe worker creative synthesis prompt template."""
    template_path = Path(__file__).parent / "scribe-worker.txt"

    try:
        with open(template_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Scribe worker template not found: {template_path}")


def format_scribe_prompt(session_id: str, worker_inventory: Dict[str, Any]) -> str:
    """Format the scribe worker template with session-specific data."""
    template = load_scribe_template()

    # Prepare template variables
    file_paths_str = "\n".join([f"- {path}" for path in worker_inventory["file_paths"]])

    # Format template with variables
    return template.format(
        session_id=session_id,
        file_paths_str=file_paths_str,
        worker_count=worker_inventory["worker_count"],
        session_path=worker_inventory["session_path"],
    )


def load_template(worker_type: str) -> str:
    """
    Load worker template from external file.

    Args:
        worker_type: Worker type (e.g., 'analyzer-worker', 'backend-worker')

    Returns:
        Template content as string

    Raises:
        FileNotFoundError: If template file doesn't exist (fail-hard behavior)
    """
    template_path = Path(__file__).parent / f"{worker_type}.txt"

    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    return template_path.read_text(encoding="utf-8")


def format_template(template_content: str, task_focus: str, context: str) -> str:
    """
    Format template with task-specific content.

    Args:
        template_content: Raw template content
        task_focus: Task description to inject
        context: Context information to inject

    Returns:
        Formatted prompt string
    """
    return template_content.format(task_focus=task_focus, context=context)
