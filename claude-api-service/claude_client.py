"""
Claude CLI client wrapper for the API service.
This runs in a clean Docker environment, avoiding nested subprocess issues.
"""

import asyncio
import os
from pathlib import Path
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class ClaudeClient:
    """Claude CLI client that runs in clean Docker environment"""

    def __init__(self):
        self.claude_executable = "claude"
        self.workspace_root = Path(os.environ.get("WORKSPACE_ROOT", "/app"))

    async def _call_claude(
        self,
        prompt: str,
        model: str = "sonnet",
        timeout: int = 180,
        settings: str = None,
    ) -> Dict[str, any]:
        """
        Call Claude CLI with the given prompt.

        Returns:
            Dict with 'success', 'response', 'error' keys
        """
        cmd = [
            self.claude_executable,
            "--print",
            "--model",
            model,
        ]

        if settings:
            # Wrap JSON settings in single quotes for proper shell escaping
            cmd.extend(["--settings", f"{settings}"])
            logger.info("Settings applied")

        cmd.extend(
            [
                prompt,
                "--dangerously-skip-permissions",
            ]
        )

        logger.info(f"Executing Claude CLI: {' '.join(cmd[:-2])} [{prompt}]")

        try:
            # Run in async subprocess
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.workspace_root,
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )

            result = {
                "success": process.returncode == 0,
                "response": stdout.decode().strip() if stdout else "",
                "error": stderr.decode().strip() if stderr else "",
                "return_code": process.returncode,
            }

            if not result["success"]:
                logger.error(f"Claude CLI failed:\n{result}")

            return result

        except asyncio.TimeoutError:
            logger.error(f"Claude CLI timeout after {timeout}s")
            return {
                "success": False,
                "response": "",
                "error": f"Claude CLI call timed out after {timeout} seconds",
                "return_code": -1,
            }
        except Exception as e:
            logger.error(f"Claude CLI exception: {e}")
            return {
                "success": False,
                "response": "",
                "error": str(e),
                "return_code": -1,
            }

    async def run_claude_command(
        self,
        prompt: str,
        model: str = "sonnet",
        timeout: int = 180,
        settings: str = None,
    ) -> str:
        """
        Simple Claude CLI execution for generic proxy use.
        Just passes the prompt through to Claude and returns the response.
        """
        result = await self._call_claude(prompt, model, timeout, settings)

        if result["success"]:
            return result["response"]
        else:
            raise Exception(f"Claude CLI failed: {result['error']}")

    async def health_check(self) -> bool:
        """Check if Claude CLI is accessible"""
        try:
            result = await self._call_claude(
                "Health check - respond with 'OK'", timeout=20
            )
            return result["success"] and "OK" in result.get("response", "")
        except Exception:
            return False
