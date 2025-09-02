"""
Max Subscription Provider
========================
Provider that routes Pydantic AI requests through Claude Code's Max subscription
instead of requiring separate API credits.
"""

import asyncio
import os
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
                for part in msg.parts:
                    if hasattr(part, "content"):
                        # Simplified role detection using ternary operators
                        part_type = type(part).__name__
                        role = (
                            "system"
                            if "System" in part_type
                            else "assistant" if "Assistant" in part_type else "user"
                        )

                        simple_messages.append(
                            {"role": role, "content": str(part.content)}
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

    def __init__(self, claude_code_executable: str = "claude"):
        # Override parent __init__ to avoid HTTP client setup
        self.claude_code_executable = claude_code_executable

        self.default_model = "custom:claude-sonnet-4"
        self.claude_code_model_mapping = {
            "custom:claude-opus-4": "opus",
            "custom:claude-sonnet-4": "sonnet",
            "custom:claude-3-7-sonnet": "claude-3-7-sonnet-20250219",
            "custom:claude-3-5-haiku": "haiku",
        }

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
        """Execute request via Claude CLI subprocess with OAuth token authentication"""
        cmd_args = [
            self.claude_code_executable,
            "--print",
            "--model",
            claude_code_model,
            prompt,
        ]

        # Add enhanced environment variables for authentication
        env = os.environ.copy()
        env.update(
            {
                "ANTHROPIC_CLIENT_TYPE": "claude-code",
                "CLAUDE_SESSION_PARENT": str(os.getppid()),
                "CLAUDE_SUBPROCESS": "1",
            }
        )

        # Use async subprocess execution with longer timeout for simple prompts
        process = await asyncio.create_subprocess_exec(
            *cmd_args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )

        try:
            # Longer timeout for simple prompts to see if it's just slow
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=60.0  # Extended timeout
            )

            if process.returncode != 0:
                stdout_str = stdout.decode() if stdout else ""
                stderr_str = stderr.decode() if stderr else ""
                raise Exception(
                    f"Claude CLI subprocess failed (exit code {process.returncode}):\n"
                    f"STDOUT: {stdout_str}\n"
                    f"STDERR: {stderr_str}"
                )

            result = stdout.decode().strip()
            return result

        except asyncio.TimeoutError:
            # Try to terminate the process
            try:
                process.terminate()
                await process.wait()
            except:
                pass

            raise Exception(
                "Claude CLI subprocess timed out after 60 seconds.\n"
                "This suggests the Raw mode issue persists even with OAuth token setup."
            )

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
        return False

    except Exception as e:
        print(f"⚠️  Unexpected error in monkey patch: {e}")
        import traceback

        print(f"Full error: {traceback.format_exc()}")
        return False
