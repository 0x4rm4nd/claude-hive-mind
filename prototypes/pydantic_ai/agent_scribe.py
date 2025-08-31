from typing import List

from pydantic_ai import Agent, RunContext

from .deps import HiveDeps
from .models import ScribeSynthesisOutput


def system_prompt_from_agent_spec() -> str:
    """Compose a concise, strict system prompt for the scribe worker.

    Mirrors agents/scribe-worker.md in spirit: scribe manages synthesis and logging,
    does not analyze the task, and must follow protocols.
    """
    return (
        "You are the scribe-worker.\n"
        "- You do NOT analyze the task itself; you aggregate outputs.\n"
        "- Follow mandatory protocols: startup/logging/completion/synthesis.\n"
        "- Produce a ScribeOutput JSON that strictly validates.\n"
        "- Include full synthesis_markdown for notes/RESEARCH_SYNTHESIS.md.\n"
        "- Be concise and neutral; accurately represent all workers' findings.\n"
    )


scribe_agent = Agent(
    # Set default model; can be overridden in run() via kwargs
    model="openai:gpt-4o-mini",
    deps_type=HiveDeps,
    output_type=ScribeSynthesisOutput,
    system_prompt=system_prompt_from_agent_spec(),
)


@scribe_agent.system_prompt
async def add_run_context(ctx: RunContext[HiveDeps]) -> str:
    return (
        f"Session: {ctx.deps.session_id}\n"
        f"Worker: {ctx.deps.worker}\n"
        "Return valid ScribeOutput. If validation fails, fix and retry.\n"
    )


@scribe_agent.tool
async def log_event(ctx: RunContext[HiveDeps], event_type: str, note: str) -> bool:
    """Append an event to EVENTS.jsonl with a short note."""
    ctx.deps.logger.log_event(event_type, {"note": note})
    return True
