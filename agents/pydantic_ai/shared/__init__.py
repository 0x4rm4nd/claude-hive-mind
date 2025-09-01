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

# Import and enable Max subscription provider automatically
from .max_subscription_provider import (
    MaxSubscriptionProvider, 
    enable_max_subscription_globally
)

# Enable Max subscription support on import
enable_max_subscription_globally()

__all__ = [
    # Models
    'WorkerOutput',
    'WorkerSummary', 
    'WorkerMetrics',
    'WorkerDependencies',
    
    # Configuration
    'WorkerConfig',
    'WorkerTagMapping',
    
    # Base Classes
    'BaseWorker',
    'BaseAgentConfig',
    
    # Max Subscription Support
    'MaxSubscriptionProvider',
    
    # Utilities
    'iso_now'
]