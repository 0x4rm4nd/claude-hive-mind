"""
Base Agent Configuration
========================
Abstract base class for standardized Pydantic AI agent configuration and setup
with extensible worker-specific customization patterns.
"""

from pathlib import Path
from typing import Dict, Any, Type
from abc import ABC, abstractmethod

from .protocols import load_project_env
from .worker_config import WorkerConfig, WorkerTagMapping
from pydantic_ai import Agent
from pydantic import BaseModel

# Ensure project environment is loaded
load_project_env()


class BaseAgentConfig(ABC):
    """
    Base class for agent configuration and setup.

    Provides standardized environment setup and configuration patterns
    while allowing worker-specific customization.
    """

    @classmethod
    def setup_environment(cls) -> None:
        """Standardized environment setup for all agents"""
        # Environment is already set up in module imports above
        pass

    @classmethod
    @abstractmethod
    def get_worker_type(cls) -> str:
        """Return worker type identifier (e.g., 'analyzer-worker')"""
        pass

    @classmethod
    @abstractmethod
    def get_output_model(cls) -> Type[BaseModel]:
        """Return the Pydantic output model for this worker"""
        pass

    @classmethod
    @abstractmethod
    def get_system_prompt(cls) -> str:
        """Return worker-specific system prompt for the AI agent"""
        pass

    @classmethod
    def get_default_model(cls) -> str:
        """Return default AI model (can be overridden by workers)"""
        return "google-gla:gemini-2.5-flash"

    @classmethod
    def get_worker_config(cls) -> WorkerConfig:
        """Create standardized worker configuration"""
        return WorkerConfig(
            worker_type=cls.get_worker_type(),
            session_id="",  # Set at runtime
            task_description="",  # Set at runtime
            tag_access=WorkerTagMapping.get_tags_for_worker(cls.get_worker_type()),
            escalation_timeout=300,
            escalation_chain=["queen-orchestrator"],
            complexity_level=2,
            dependencies=[],
            priority="medium",
        )

    @classmethod
    def create_worker_config(cls, session_id: str, task_description: str) -> WorkerConfig:
        """Create worker configuration with runtime values"""
        return WorkerConfig(
            worker_type=cls.get_worker_type(),
            session_id=session_id,
            task_description=task_description,
            tag_access=WorkerTagMapping.get_tags_for_worker(cls.get_worker_type()),
            escalation_timeout=300,
            escalation_chain=["queen-orchestrator"],
            complexity_level=2,
            dependencies=[],
            priority="medium",
        )

    @classmethod
    def create_agent(cls) -> Agent:
        """Create standardized Pydantic AI agent with worker-specific configuration"""
        cls.setup_environment()

        return Agent(
            model=cls.get_default_model(),
            output_type=cls.get_output_model(),
            system_prompt=cls.get_system_prompt(),
        )

    @classmethod
    def create_worker_exports(cls) -> tuple:
        """
        Create standard exports for worker agent modules.

        Returns:
            tuple: (agent_instance, worker_config) - standard exports for agent.py files
        """
        agent = cls.create_agent()
        config = cls.get_worker_config()
        return agent, config
