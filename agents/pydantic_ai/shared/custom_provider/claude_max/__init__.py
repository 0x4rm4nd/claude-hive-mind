"""
Claude Max Subscription Provider

Provides Pydantic AI integration with Claude Max subscription through API service.

Key Components:
- ClaudeAPIServiceClient: HTTP client for Docker API service  
- ClaudeMaxSubscriptionModel: Pydantic AI model adapter
- Integration functions: Enable Agent('custom:max-subscription') syntax

Eliminates nested subprocess issues while maintaining full compatibility.
"""

from .api_service_client import ClaudeAPIServiceClient
from .pydantic_model_adapter import (
    ClaudeMaxSubscriptionModel,
    enable_max_subscription_integration,
)

# Auto-enable integration when module is imported
enable_max_subscription_integration()

__all__ = [
    "ClaudeAPIServiceClient",
    "ClaudeMaxSubscriptionModel",
    "enable_max_subscription_integration",
]
