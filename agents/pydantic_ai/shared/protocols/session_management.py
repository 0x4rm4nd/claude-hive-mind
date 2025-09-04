#!/usr/bin/env python3
"""
Session Management Protocol

Unified session path detection and append-safe file operations.
Ensures all agents use consistent paths and never overwrite session data.
Includes environment variable loading utilities.
"""

import os
import json
import tempfile
import re
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv


class SessionManagement:
    """Core session management with guaranteed path consistency and atomic operations"""

    @staticmethod
    def detect_project_root() -> str:
        """
        Detect project root with guaranteed consistency.
        All agents MUST use this function for path detection.

        Returns absolute path to project root.
        """
        # Start from current working directory
        current_path = Path.cwd()

        # Search upward for project markers
        while current_path != current_path.parent:
            # Check for definitive project markers
            if all(
                [
                    (current_path / "Docs" / "hive-mind").exists(),
                    (current_path / ".claude").exists(),
                ]
            ):
                return str(current_path)

            current_path = current_path.parent

        # Log debug info before raising exception - attempt to write to temp location
        try:

            temp_debug = {
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "level": "ERROR",
                "agent": "session_management",
                "message": "Failed to detect SmartWalletFX project root",
                "details": {
                    "current_working_dir": str(Path.cwd()),
                    "search_paths_checked": str(current_path),
                    "error": "Could not detect project root with hive-mind structure",
                },
            }
            # Try to write to a temp file for debugging
            temp_file = Path(tempfile.gettempdir()) / "protocol_debug.jsonl"
            with open(temp_file, "a") as f:
                f.write(json.dumps(temp_debug, separators=(",", ":")) + "\n")
        except Exception:
            # Debug logging failure should not prevent the main error from being raised
            pass

        raise ValueError(
            f"Could not detect project root from {Path.cwd()}. "
            "Ensure you're running from within a project with hive-mind structure."
        )

    @staticmethod
    def get_session_path(session_id: str) -> str:
        """
        Get absolute path to session directory.
        Ensures all agents use the same session path.

        Args:
            session_id: Session identifier

        Returns:
            Absolute path to session directory
        """
        project_root = SessionManagement.detect_project_root()
        return os.path.join(project_root, "Docs", "hive-mind", "sessions", session_id)

    @staticmethod
    def ensure_session_exists(session_id: str) -> bool:
        """
        Verify session directory and files exist - fail hard if invalid.

        Args:
            session_id: Session identifier

        Returns:
            True if session exists and is valid

        Raises:
            FileNotFoundError: If session directory or required files don't exist
            ValueError: If session structure is invalid
        """
        session_path = SessionManagement.get_session_path(session_id)

        required_files = [
            "EVENTS.jsonl",
            "BACKLOG.jsonl",
            "DEBUG.jsonl",
            "SESSION.md",
        ]

        required_dirs = [
            "",  # Session root
            "workers",
            "workers/json",
            "workers/prompts",
            "workers/notes",
        ]

        # Check directories - fail hard if missing
        for dir_name in required_dirs:
            dir_path = (
                os.path.join(session_path, dir_name) if dir_name else session_path
            )
            if not os.path.isdir(dir_path):
                raise FileNotFoundError(f"Required session directory missing: {dir_path}")

        # Check files - fail hard if missing
        for file_name in required_files:
            file_path = os.path.join(session_path, file_name)
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"Required session file missing: {file_path}")

        return True

    @staticmethod
    def append_to_events(session_id: str, event_data: Dict[str, Any]) -> bool:
        """
        Append event to EVENTS.jsonl - NEVER overwrites.

        Args:
            session_id: Session identifier
            event_data: Event dictionary to append

        Returns:
            True if append successful
        """
        session_path = SessionManagement.get_session_path(session_id)
        events_file = os.path.join(session_path, "EVENTS.jsonl")

        # Ensure event has required fields
        if "timestamp" not in event_data:
            event_data["timestamp"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        # CRITICAL: Use append mode, never write mode - fail hard if this fails
        with open(events_file, "a") as f:
            f.write(json.dumps(event_data, separators=(",", ":")) + "\n")
        return True

    @staticmethod
    def append_to_debug(session_id: str, debug_data: Dict[str, Any]) -> bool:
        """
        Append debug info to DEBUG.jsonl - NEVER overwrites.

        Args:
            session_id: Session identifier
            debug_data: Debug dictionary to append

        Returns:
            True if append successful
        """
        session_path = SessionManagement.get_session_path(session_id)
        debug_file = os.path.join(session_path, "DEBUG.jsonl")

        # Ensure debug has timestamp
        if "timestamp" not in debug_data:
            debug_data["timestamp"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        # CRITICAL: Use append mode, never write mode - fail hard if this fails
        with open(debug_file, "a") as f:
            f.write(json.dumps(debug_data, separators=(",", ":")) + "\n")
        return True


# Environment Variable Loading Utilities
# ======================================
# Merged from env_loader.py for consolidation

def load_project_env():
    """Load environment variables from project root .env file"""
    # Use SessionManagement to avoid duplication of project detection logic
    project_root = SessionManagement.detect_project_root()
    env_file = Path(project_root) / ".env"

    if env_file.exists():
        load_dotenv(env_file)

    return project_root





