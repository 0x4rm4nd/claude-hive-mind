# Worker Template System
# =====================
# Centralized template loading for worker prompt generation

from pathlib import Path


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
