"""
Shared Pydantic AI Infrastructure
======================================

This package contains shared utilities, protocols, and configurations
used across all Pydantic AI agents in the hive-mind system.
"""

from .models import WorkerOutput, WorkerSummary, WorkerMetrics, WorkerDependencies
from .worker_config import WorkerConfig, WorkerTagMapping
from .tools import iso_now
from .base_worker import BaseWorker
from .base_agent import BaseAgentConfig

# Import and enable Max subscription integration automatically
from .custom_provider.claude_max import (
    ClaudeMaxSubscriptionModel,
    ClaudeAPIServiceClient,
    enable_max_subscription_integration,
)

# Integration is auto-enabled in claude_integration module

__all__ = [
    # Models
    "WorkerOutput",
    "WorkerSummary",
    "WorkerMetrics",
    "WorkerDependencies",
    # Configuration
    "WorkerConfig",
    "WorkerTagMapping",
    # Base Classes
    "BaseWorker",
    "BaseAgentConfig",
    # Max Subscription Support
    "MaxSubscriptionModel",
    "ClaudeAPISubscriptionProvider",
    # Utilities
    "iso_now",
]
