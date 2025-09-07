"""
Shared Pydantic AI Infrastructure
======================================

This package contains shared utilities, protocols, and configurations
used across all Pydantic AI agents in the hive-mind system.
"""

import sys
from pathlib import Path

# Ensure pydantic_ai root is in sys.path for all workers
pydantic_ai_root = Path(__file__).parent.parent
if str(pydantic_ai_root) not in sys.path:
    sys.path.insert(0, str(pydantic_ai_root))

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
