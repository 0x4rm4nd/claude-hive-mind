"""
Max Subscription Provider
========================
Provider that routes Pydantic AI requests through Claude Code's Max subscription
instead of requiring separate API credits.
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Any, Dict, List

from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart
from pydantic_ai.models import Model, ModelRequestParameters
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.settings import ModelSettings
from pydantic_ai.usage import RequestUsage


class MaxSubscriptionModel(Model):
    """Custom model class that properly inherits from Pydantic AI's Model base class"""

    def __init__(self, model_name: str = "custom:max-subscription", **kwargs):
        # Initialize parent class properly
        super().__init__(settings=kwargs.get("settings"), profile=kwargs.get("profile"))
        self._model_name = model_name
        self._provider = MaxSubscriptionProvider()

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def system(self) -> str:
        return "max-subscription"

    async def request(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> ModelResponse:
        """Route requests through MaxSubscriptionProvider"""
        # Convert pydantic_ai messages to simple format for our provider
        simple_messages = []
        for msg in messages:
            if hasattr(msg, "parts"):
                # Extract text from message parts
                text_parts = [part.text for part in msg.parts if hasattr(part, "text")]
                content = " ".join(text_parts)
                simple_messages.append(
                    {"role": getattr(msg, "role", "user"), "content": content}
                )
            elif hasattr(msg, "content"):
                simple_messages.append(
                    {"role": getattr(msg, "role", "user"), "content": str(msg.content)}
                )

        # Get response from our provider
        anthropic_response = await self._provider.request_structured_response(
            simple_messages, self._model_name
        )

        # Convert back to Pydantic AI format
        return ModelResponse(
            parts=[TextPart(text=anthropic_response["content"][0]["text"])],
            model_name=self._model_name,
            timestamp=datetime.now(),
            usage=RequestUsage(
                input_tokens=anthropic_response["usage"]["input_tokens"],
                output_tokens=anthropic_response["usage"]["output_tokens"],
            ),
        )

    async def count_tokens(
        self,
        messages: list[ModelMessage],
        model_settings: ModelSettings | None,
        model_request_parameters: ModelRequestParameters,
    ) -> RequestUsage:
        """Estimate token count"""
        total_chars = sum(len(str(msg)) for msg in messages)
        return RequestUsage(input_tokens=total_chars // 4, output_tokens=0)

    def __str__(self) -> str:
        return self._model_name

    def __repr__(self) -> str:
        return f"MaxSubscriptionModel('{self._model_name}')"


class MaxSubscriptionProvider(AnthropicProvider):
    """Provider that routes Anthropic requests through Claude Code's Max subscription"""

    def __init__(self, claude_code_executable: str = "claude-code"):
        # Override parent __init__ to avoid HTTP client setup
        self.claude_code_executable = claude_code_executable

        self.default_model = "custom:claude-sonnet-4"
        self.claude_code_model_mapping = {
            "custom:claude-opus-4": "opus",
            "custom:claude-sonnet-4": "sonnet",
            "custom:claude-3-7-sonnet": "claude-3-7-sonnet-20250219",
            "custom:claude-3-5-haiku": "haiku",
        }
        self.fallback_model = "claude-3-7-sonnet-20250219"

    async def request_structured_response(self, messages, model_name, **kwargs):
        """Route request through Claude Code instead of Anthropic API"""

        if model_name == "custom:max-subscription":
            actual_model = self.default_model
        elif model_name in self.claude_code_model_mapping:
            actual_model = model_name
        else:
            actual_model = self.default_model

        claude_code_model = self.claude_code_model_mapping.get(actual_model, "sonnet")
        prompt = self._format_messages_for_claude_code(messages)
        claude_response = await self._execute_claude_code_task(
            prompt, claude_code_model
        )
        return self._format_as_anthropic_response(claude_response, actual_model)

    def _format_messages_for_claude_code(self, messages: List[Dict[str, Any]]) -> str:
        """Convert Anthropic API messages to simple text prompt (KISS principle)"""
        formatted = []

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if isinstance(content, list):
                text_parts = [
                    part.get("text", "")
                    for part in content
                    if part.get("type") == "text"
                ]
                content = " ".join(text_parts)
            if role == "system":
                formatted.append(f"System: {content}")
            elif role == "user":
                formatted.append(f"User: {content}")
            elif role == "assistant":
                formatted.append(f"Assistant: {content}")

        return "\n\n".join(formatted)

    async def _execute_claude_code_task(
        self, prompt: str, claude_code_model: str
    ) -> str:
        """Execute request via Claude Code Task tool with no timeout"""

        task_config = {
            "subagent_type": "general-purpose",
            "description": "Max subscription proxy request",
            "prompt": f"""You are proxying a request from Pydantic AI.

{prompt}

Respond with ONLY the AI model's response content. No additional formatting or explanations.""",
        }

        cmd_args = [
            self.claude_code_executable,
            "task",
            "--model",
            claude_code_model,
            "--fallback-model",
            self.fallback_model,
            "--config",
            json.dumps(task_config),
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd_args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise Exception(
                f"Claude Code task failed (exit code {process.returncode}):\n"
                f"STDOUT: {stdout.decode()}\n"
                f"STDERR: {stderr.decode()}"
            )

        return stdout.decode().strip()

    def _format_as_anthropic_response(
        self, claude_response: str, original_model: str
    ) -> Dict[str, Any]:
        """Convert Claude Code response to Anthropic API format"""

        return {
            "id": f"msg_{uuid.uuid4()}",
            "type": "message",
            "role": "assistant",
            "content": [{"type": "text", "text": claude_response}],
            "model": original_model,
            "usage": {
                "input_tokens": 0,
                "output_tokens": len(claude_response.split()),
            },
            "stop_reason": "end_turn",
        }


# Monkey patch for global integration
def enable_max_subscription_globally():
    """Enable custom:* model support by patching model resolution"""
    try:
        # Directly patch the infer_model function
        import pydantic_ai.models as models_module

        # Store original infer_model function
        original_infer_model = models_module.infer_model

        def patched_infer_model(model):
            """Intercept custom: models before original infer_model logic"""
            if isinstance(model, str) and model.startswith("custom:"):
                # Check if it's a known custom model
                known_custom_models = [
                    "custom:max-subscription",
                    "custom:claude-opus-4",
                    "custom:claude-sonnet-4",
                    "custom:claude-3-7-sonnet",
                    "custom:claude-3-5-haiku",
                ]

                if model in known_custom_models:
                    return MaxSubscriptionModel(model)
                else:
                    # Unknown custom model, use default
                    return MaxSubscriptionModel()

            # Let Pydantic AI handle all other models normally
            return original_infer_model(model)

        # Replace the infer_model function
        models_module.infer_model = patched_infer_model

        print("✅ Max subscription globally enabled - Agent('custom:*') now works!")
        return True

    except (ImportError, AttributeError) as e:
        print(f"⚠️  Could not enable global monkey patch: {e}")

        # Fallback to the old approach (patch AnthropicModel directly)
        try:
            import pydantic_ai.models.anthropic as anthropic_module

            OriginalAnthropicModel = anthropic_module.AnthropicModel

            class MaxSubscriptionAnthropicModel(OriginalAnthropicModel):
                def __init__(self, model_name, *, provider=None, **kwargs):
                    if isinstance(model_name, str) and model_name.startswith("custom:"):
                        if provider is None:
                            provider = MaxSubscriptionProvider()

                        self.name = model_name
                        self.provider = provider
                        self.profile = kwargs.get("profile", None)
                        self.settings = kwargs.get("settings", None)

                    else:
                        super().__init__(model_name, provider=provider, **kwargs)

            anthropic_module.AnthropicModel = MaxSubscriptionAnthropicModel
            print(
                "✅ Max subscription enabled via fallback method - limited compatibility"
            )
            return True

        except Exception as fallback_error:
            print(f"⚠️  Fallback monkey patch also failed: {fallback_error}")
            print("💡 Use helper functions instead: create_max_subscription_agent()")
            return False

    except Exception as e:
        print(f"⚠️  Unexpected error in monkey patch: {e}")
        import traceback

        print(f"Full error: {traceback.format_exc()}")
        return False
