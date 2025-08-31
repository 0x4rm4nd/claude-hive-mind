#!/usr/bin/env python3
"""
Session Management Protocol
==========================================
Unified session path detection and append-safe file operations.
Ensures all agents use consistent paths and never overwrite session data.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class SessionManagement:
    """Core session management with guaranteed path consistency and atomic operations"""

    @staticmethod
    def detect_project_root() -> str:
        """
        Detect SmartWalletFX project root with guaranteed consistency.
        All agents MUST use this function for path detection.

        Returns absolute path to SmartWalletFX project root.
        """
        # Start from current working directory
        current_path = Path.cwd()

        # Search upward for SmartWalletFX project markers
        while current_path != current_path.parent:
            # Check if this is the SmartWalletFX root
            if current_path.name == "SmartWalletFX":
                # Verify it has the expected structure
                if (current_path / "Docs" / "hive-mind").exists():
                    return str(current_path)

            # Check for definitive project markers even if not named SmartWalletFX
            if all(
                [
                    (current_path / "Docs" / "hive-mind").exists(),
                    (current_path / ".claude").exists(),
                    any(
                        [
                            (current_path / svc).exists()
                            for svc in ["api", "frontend", "crypto-data"]
                        ]
                    ),
                ]
            ):
                return str(current_path)

            current_path = current_path.parent

        # Final fallback: look for SmartWalletFX in path
        cwd_str = str(Path.cwd())
        if "SmartWalletFX" in cwd_str:
            # Extract path up to and including SmartWalletFX
            parts = cwd_str.split("SmartWalletFX")
            if len(parts) >= 2:
                base_path = parts[0] + "SmartWalletFX"
                # Verify it's valid
                if (
                    Path(base_path).exists()
                    and (Path(base_path) / "Docs" / "hive-mind").exists()
                ):
                    return base_path

        # Log debug info before raising exception - attempt to write to temp location
        try:
            import tempfile

            temp_debug = {
                "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "level": "ERROR",
                "agent": "session_management",
                "message": "Failed to detect SmartWalletFX project root",
                "details": {
                    "current_working_dir": str(Path.cwd()),
                    "search_paths_checked": str(current_path),
                    "error": "Could not detect SmartWalletFX project root",
                },
            }
            # Try to write to a temp file for debugging
            temp_file = Path(tempfile.gettempdir()) / "smartwalletfx_debug.jsonl"
            with open(temp_file, "a") as f:
                f.write(json.dumps(temp_debug, separators=(",", ":")) + "\n")
        except Exception:
            pass  # Fail silently if debug logging fails

        raise ValueError(
            f"Could not detect SmartWalletFX project root from {Path.cwd()}. "
            "Ensure you're running from within the SmartWalletFX project."
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
        Verify session directory and files exist.

        Args:
            session_id: Session identifier

        Returns:
            True if session exists and is valid
        """
        session_path = SessionManagement.get_session_path(session_id)

        required_files = ["STATE.json", "EVENTS.jsonl", "BACKLOG.jsonl", "DEBUG.jsonl", "SESSION.md"]

        required_dirs = [
            "",  # Session root
            "workers",
            "workers/json",
            "workers/prompts",
            "notes",
        ]

        # Check directories
        for dir_name in required_dirs:
            dir_path = (
                os.path.join(session_path, dir_name) if dir_name else session_path
            )
            if not os.path.isdir(dir_path):
                return False

        # Check files
        for file_name in required_files:
            file_path = os.path.join(session_path, file_name)
            if not os.path.isfile(file_path):
                return False

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
            event_data["timestamp"] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        try:
            # CRITICAL: Use append mode, never write mode
            with open(events_file, "a") as f:
                f.write(json.dumps(event_data, separators=(",", ":")) + "\n")
            return True
        except Exception as e:
            print(f"Failed to append to EVENTS.jsonl: {e}")
            return False

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
            debug_data["timestamp"] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        try:
            # CRITICAL: Use append mode, never write mode
            with open(debug_file, "a") as f:
                f.write(json.dumps(debug_data, separators=(",", ":")) + "\n")
            return True
        except Exception as e:
            print(f"Failed to append to DEBUG.jsonl: {e}")
            return False

    @staticmethod
    def update_state_atomically(session_id: str, updates: Dict[str, Any]) -> bool:
        """
        Atomically update STATE.json by reading, merging, and writing back.
        Preserves existing data and only updates specified fields.

        Args:
            session_id: Session identifier
            updates: Dictionary of updates to merge into state

        Returns:
            True if update successful
        """
        session_path = SessionManagement.get_session_path(session_id)
        state_file = os.path.join(session_path, "STATE.json")

        try:
            # Step 1: Read existing state
            with open(state_file, "r") as f:
                current_state = json.load(f)

            # Step 2: Deep merge updates into current state
            merged_state = SessionManagement._deep_merge(current_state, updates)

            # Step 3: Add update metadata
            merged_state["last_updated"] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            if "update_count" in merged_state:
                merged_state["update_count"] += 1
            else:
                merged_state["update_count"] = 1

            # Step 4: Write back atomically (using temp file + rename for atomicity)
            temp_file = state_file + ".tmp"
            with open(temp_file, "w") as f:
                json.dump(merged_state, f, indent=2)

            # Atomic rename
            os.replace(temp_file, state_file)
            return True

        except Exception as e:
            print(f"Failed to update STATE.json atomically: {e}")
            # Clean up temp file if exists
            temp_file = state_file + ".tmp"
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False

    @staticmethod
    def _deep_merge(base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge updates into base dictionary.

        Args:
            base: Base dictionary
            updates: Updates to merge

        Returns:
            Merged dictionary
        """
        result = base.copy()

        for key, value in updates.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                # Recursive merge for nested dicts
                result[key] = SessionManagement._deep_merge(result[key], value)
            else:
                # Direct update for non-dict values
                result[key] = value

        return result

    @staticmethod
    def read_state(session_id: str) -> Optional[Dict[str, Any]]:
        """
        Read current session state.

        Args:
            session_id: Session identifier

        Returns:
            State dictionary or None if error
        """
        session_path = SessionManagement.get_session_path(session_id)
        state_file = os.path.join(session_path, "STATE.json")

        try:
            with open(state_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to read STATE.json: {e}")
            return None

    @staticmethod
    def validate_session_path(
        session_id: str, expected_path: Optional[str] = None
    ) -> bool:
        """
        Validate that session path matches expected location.

        Args:
            session_id: Session identifier
            expected_path: Optional expected path to compare against

        Returns:
            True if path is valid and matches expectation
        """
        actual_path = SessionManagement.get_session_path(session_id)

        # Check path exists
        if not os.path.exists(actual_path):
            print(f"Session path does not exist: {actual_path}")
            return False

        # If expected path provided, verify match
        if expected_path:
            expected_abs = os.path.abspath(expected_path)
            if actual_path != expected_abs:
                print(f"Path mismatch! Expected: {expected_abs}, Got: {actual_path}")
                return False

        return True

    @staticmethod
    def log_worker_activity(
        session_id: str,
        worker_type: str,
        activity: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Log worker activity with guaranteed append behavior.

        Args:
            session_id: Session identifier
            worker_type: Type of worker logging activity
            activity: Activity description
            details: Optional additional details

        Returns:
            True if logging successful
        """
        event = {
            "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "type": "worker_activity",
            "agent": worker_type,
            "activity": activity,
            "details": details or {},
        }

        return SessionManagement.append_to_events(session_id, event)

    @staticmethod
    def create_worker_file(
        session_id: str, worker_type: str, file_type: str, content: Any
    ) -> bool:
        """
        Create a worker-specific file in the correct location.

        Args:
            session_id: Session identifier
            worker_type: Type of worker
            file_type: Type of file (json, prompt, decision)
            content: Content to write

        Returns:
            True if file created successfully
        """
        session_path = SessionManagement.get_session_path(session_id)

        # Determine file path based on type
        if file_type == "json":
            file_path = os.path.join(
                session_path, "workers", "json", f"{worker_type}.json"
            )
            content_str = (
                json.dumps(content, indent=2)
                if not isinstance(content, str)
                else content
            )
        elif file_type == "prompt":
            file_path = os.path.join(
                session_path, "workers", "prompts", f"{worker_type}.md"
            )
            content_str = content if isinstance(content, str) else str(content)
        elif file_type == "notes":
            worker_clean = worker_type.replace('-worker', '')
            file_path = os.path.join(
                session_path, "notes", f"{worker_clean}_notes.md"
            )
            content_str = content if isinstance(content, str) else str(content)
        else:
            print(f"Unknown file type: {file_type}")
            return False

        try:
            with open(file_path, "w") as f:
                f.write(content_str)
            return True
        except Exception as e:
            print(f"Failed to create worker file: {e}")
            return False

    @staticmethod
    def append_to_backlog(session_id: str, backlog_item: Dict[str, Any]) -> bool:
        """
        Append item to BACKLOG.jsonl for future processing.

        Args:
            session_id: Session identifier
            backlog_item: Item to add to backlog

        Returns:
            True if append successful
        """
        session_path = SessionManagement.get_session_path(session_id)
        backlog_file = os.path.join(session_path, "BACKLOG.jsonl")

        # Ensure item has timestamp
        if "timestamp" not in backlog_item:
            backlog_item["timestamp"] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        try:
            # CRITICAL: Use append mode
            with open(backlog_file, "a") as f:
                f.write(json.dumps(backlog_item, separators=(",", ":")) + "\n")
            return True
        except Exception as e:
            print(f"Failed to append to BACKLOG.jsonl: {e}")
            return False
