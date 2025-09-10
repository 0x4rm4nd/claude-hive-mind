"""
Pydantic AI Model Adapter for Claude Max Subscription

Custom Pydantic AI Model that bridges Agent() calls to Claude API service.
Maintains standard Pydantic AI interface while using Claude Max subscription.
"""

from datetime import datetime

from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart, ToolCallPart
from pydantic_ai.models import Model, ModelRequestParameters
from pydantic_ai.settings import ModelSettings
from pydantic_ai.usage import RequestUsage
import json

from .api_service_client import ClaudeAPIServiceClient


class ClaudeMaxSubscriptionModel(Model):
    """
    Pydantic AI Model adapter for Claude Max subscription.

    Bridges standard Pydantic AI Agent interface to Claude API service,
    maintaining full compatibility while using Claude Max subscription.
    """

    def __init__(self, model_name: str = "custom:max-subscription", **kwargs):
        super().__init__(settings=kwargs.get("settings"), profile=kwargs.get("profile"))
        self._model_name = model_name
        self._client = ClaudeAPIServiceClient()

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def system(self) -> str:
        return "claude-api-service"

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> ModelResponse:
        """Route requests through ClaudeAPISubscriptionProvider"""

        # Convert Pydantic AI messages to prompt string
        prompt = self._convert_pydantic_messages(messages)

        # Extract extra headers from model settings (ModelSettings is a dict, not object)
        extra_headers = model_settings.get("extra_headers") if model_settings else None
        response_text = await self._client.send_prompt(
            prompt, self._model_name, extra_headers
        )

        # Try to parse as JSON first - if it works, return as ToolCallPart
        try:
            json_data = json.loads(response_text.strip())
            return ModelResponse(
                parts=[
                    ToolCallPart(
                        tool_name="final_result",  # Use the correct tool name from Pydantic AI
                        args=json_data,  # Pass JSON fields directly, not wrapped
                        tool_call_id="custom_model_response",
                    )
                ],
                model_name=self._model_name,
                timestamp=datetime.now(),
                usage=RequestUsage(
                    input_tokens=self._estimate_tokens(messages),
                    output_tokens=len(response_text.split()),
                ),
            )
        except (json.JSONDecodeError, AttributeError) as e:
            return ModelResponse(
                parts=[TextPart(content=response_text)],
                model_name=self._model_name,
                timestamp=datetime.now(),
                usage=RequestUsage(
                    input_tokens=self._estimate_tokens(messages),
                    output_tokens=len(response_text.split()),
                ),
            )

    async def count_tokens(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> RequestUsage:
        """Estimate token count for messages"""
        total_chars = sum(len(str(msg)) for msg in messages)
        return RequestUsage(input_tokens=total_chars // 4, output_tokens=0)

    def _convert_pydantic_messages(self, messages: list[ModelMessage]) -> str:
        """Convert Pydantic AI messages directly to prompt string"""
        formatted = []

        for msg in messages:
            if hasattr(msg, "parts"):
                for part in msg.parts:
                    if hasattr(part, "content"):
                        role = self._determine_role_from_part(part)
                        content = str(part.content)
                        formatted.append(f"{role}: {content}")
            elif hasattr(msg, "content"):
                role = getattr(msg, "role", "user").title()
                content = str(msg.content)
                formatted.append(f"{role}: {content}")

        return "\n\n".join(formatted)

    def _determine_role_from_part(self, part) -> str:
        """Determine message role from part type"""
        part_type = type(part).__name__
        if "System" in part_type:
            return "System"
        elif "Assistant" in part_type:
            return "Assistant"
        else:
            return "User"

    def _estimate_tokens(self, messages: list[ModelMessage]) -> int:
        """Rough token estimation"""
        total_chars = sum(len(str(msg)) for msg in messages)
        return total_chars // 4  # Rough approximation

    def __str__(self) -> str:
        return self._model_name

    def __repr__(self) -> str:
        return f"ClaudeMaxSubscriptionModel('{self._model_name}')"


def enable_max_subscription_integration():
    """
    Enable custom:max-subscription model support in Pydantic AI.

    This function patches Pydantic AI's model resolution to recognize
    custom:* models and route them through the Claude API service.
    """
    try:
        import pydantic_ai.models as models_module

        # Store original infer_model function
        original_infer_model = getattr(
            models_module, "_original_infer_model", models_module.infer_model
        )
        models_module._original_infer_model = original_infer_model

        def patched_infer_model(model):
            """Intercept custom: models and route to MaxSubscriptionModel"""
            if isinstance(model, str) and model.startswith("custom:"):
                supported_models = [
                    "custom:max-subscription",
                    "custom:claude-opus-4",
                    "custom:claude-sonnet-4",
                    "custom:claude-3-7-sonnet",
                    "custom:claude-3-5-haiku",
                ]

                if model in supported_models:
                    return ClaudeMaxSubscriptionModel(model)
                else:
                    # Unknown custom model, use default max subscription
                    return ClaudeMaxSubscriptionModel("custom:max-subscription")

            # Let Pydantic AI handle all other models normally
            return original_infer_model(model)

        # Apply the patch
        models_module.infer_model = patched_infer_model

        print(
            "✅ Max subscription integration enabled - Agent('custom:max-subscription') now works!"
        )
        return True

    except Exception as e:
        print(f"⚠️  Failed to enable max subscription integration: {e}")
        import traceback

        print(f"Full error: {traceback.format_exc()}")
        return False
