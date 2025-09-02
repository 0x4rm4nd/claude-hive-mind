"""
Claude API Service Client

Client for communicating with the Claude API service to eliminate nested subprocess issues.
Routes Pydantic AI requests through Docker-based Claude CLI service.
"""

from typing import Any, Dict

import aiohttp


class ClaudeAPIServiceClient:
    """
    Client for communicating with Claude API service.

    Handles HTTP communication with Docker-based Claude API service to eliminate
    nested subprocess authentication issues while maintaining Max subscription access.
    """

    def __init__(
        self,
        api_base_url: str = "http://localhost:47291",
        auto_start_service: bool = False,
        default_model: str = "sonnet",
    ):
        self.api_base_url = api_base_url
        self.auto_start_service = auto_start_service
        self.default_model = default_model
        self.service_started = False

        # Model mapping for compatibility
        self.model_mapping = {
            "custom:max-subscription": "sonnet",
            "custom:claude-opus-4": "opus",
            "custom:claude-sonnet-4": "sonnet",
            "custom:claude-3-7-sonnet": "claude-3-7-sonnet-20250219",
            "custom:claude-3-5-haiku": "haiku",
        }

    async def send_prompt(self, prompt: str, model_name: str) -> str:
        """
        Send a prompt directly to Claude API service.
        
        Simplified method that takes a prompt string and returns response.
        """
        # Check if API service is running
        if not self.service_started:
            if not await self._check_service_health():
                raise Exception(
                    f"Claude API service is not running at {self.api_base_url}\n"
                    f"Start the service with: cd .claude/claude-api-service && docker-compose up -d"
                )
            self.service_started = True

        # Map custom model name to Claude model
        claude_model = self.model_mapping.get(model_name, self.default_model)

        # Call Claude API service
        try:
            return await self._call_claude_api_service(prompt, claude_model)
        except Exception as e:
            # If API service fails, provide clear error
            raise Exception(
                f"Claude API Service failed: {str(e)}\n"
                f"Ensure the Claude API service is running:\n"
                f"cd .claude/claude-api-service && docker-compose up -d\n"
                f"Or check service health at: {self.api_base_url}/health"
            )

    async def _check_service_health(self) -> bool:
        """Check if the Claude API service is healthy"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_base_url}/health",
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as response:
                    if response.status == 200:
                        health_data = await response.json()
                        return health_data.get("status") == "healthy"
        except Exception:
            pass
        return False

    async def _call_claude_api_service(self, prompt: str, model: str) -> str:
        """Call the Claude API service"""
        request_data = {"prompt": prompt, "model": model, "timeout": 120}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_base_url}/claude",
                json=request_data,
                timeout=aiohttp.ClientTimeout(
                    total=150
                ),  # Longer timeout for Claude calls
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(
                        f"API service returned {response.status}: {error_text}"
                    )

                result = await response.json()
                return result["response"]


    def get_service_status(self) -> Dict[str, Any]:
        """Get status information about the Claude API service"""
        return {
            "api_base_url": self.api_base_url,
            "service_started": self.service_started,
            "auto_start_service": self.auto_start_service,
            "default_model": self.default_model,
            "available_models": list(self.model_mapping.keys()),
        }
