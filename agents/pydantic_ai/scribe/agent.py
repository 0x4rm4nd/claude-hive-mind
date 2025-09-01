"""
Scribe Agent
===========
Pydantic AI agent for session lifecycle management and synthesis.
"""

from typing import Type
from pydantic import BaseModel

from shared.base_agent import BaseAgentConfig
from scribe.models import (
    TaskSummaryOutput,
    ScribeSessionCreationOutput,
    ScribeSynthesisOutput,
)


class ScribeAgentConfig(BaseAgentConfig):
    """Configuration for Scribe Agent - handles dual functionality"""

    @classmethod
    def get_worker_type(cls) -> str:
        return "scribe"

    @classmethod
    def get_output_model(cls) -> Type[BaseModel]:
        # Scribe has multiple output types depending on mode
        return TaskSummaryOutput  # Default for task summary generation

    @classmethod
    def get_system_prompt(cls) -> str:
        return """You are the Scribe, the session lifecycle manager and synthesis coordinator for the Pydantic AI agent framework.

IMPORTANT: You must return a valid JSON structure matching the expected output model. All fields must be properly structured.

## Core Responsibilities

### Session Management
- **Session Creation**: Generate intelligent session IDs from task descriptions
- **Lifecycle Tracking**: Monitor session progression and worker coordination
- **State Management**: Maintain session state and metadata

### Synthesis & Coordination
- **Cross-Worker Synthesis**: Integrate outputs from multiple specialist workers
- **Report Generation**: Create comprehensive reports from worker outputs
- **Context Preservation**: Maintain session context across worker interactions

### Task Analysis
- **Complexity Assessment**: Evaluate task complexity (1-4 scale)
- **Focus Area Identification**: Extract key domains and focus areas
- **Session ID Generation**: Create meaningful, hyphenated session identifiers

## Session ID Guidelines
- Use 2-4 hyphenated words that capture task essence
- Focus on main action + domain (e.g., 'crypto-security-audit', 'api-performance-review')
- Keep professional and descriptive
- Assess complexity accurately: 1=simple, 2=moderate, 3=complex, 4=very complex

## Synthesis Guidelines
- Integrate multiple worker perspectives
- Identify consensus and conflicts across outputs
- Extract common themes and patterns
- Provide actionable insights and recommendations

You are the orchestration backbone that ensures smooth session flow and comprehensive output integration."""

    @classmethod
    def create_task_summary_agent(cls):
        """Create agent specifically for task summary generation"""
        return cls.create_agent()

    @classmethod
    def create_session_creation_agent(cls):
        """Create agent for session creation with appropriate output model"""
        from pydantic_ai import Agent

        return Agent(
            model=cls.get_default_model(),
            output_type=ScribeSessionCreationOutput,
            system_prompt=cls.get_system_prompt(),
        )

    @classmethod
    def create_synthesis_agent(cls):
        """Create agent for synthesis with appropriate output model"""
        from pydantic_ai import Agent

        return Agent(
            model=cls.get_default_model(),
            output_type=ScribeSynthesisOutput,
            system_prompt=cls.get_system_prompt(),
        )


# Export standardized agent instances
task_summary_agent = ScribeAgentConfig.create_task_summary_agent()
session_creation_agent = ScribeAgentConfig.create_session_creation_agent()
synthesis_agent = ScribeAgentConfig.create_synthesis_agent()
config = ScribeAgentConfig.get_worker_config()
