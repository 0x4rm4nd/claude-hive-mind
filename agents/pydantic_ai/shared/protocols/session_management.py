#!/usr/bin/env python3
"""
Session Management Protocol

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
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
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
            event_data["timestamp"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

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
            debug_data["timestamp"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        try:
            # CRITICAL: Use append mode, never write mode
            with open(debug_file, "a") as f:
                f.write(json.dumps(debug_data, separators=(",", ":")) + "\n")
            return True
        except Exception as e:
            print(f"Failed to append to DEBUG.jsonl: {e}")
            return False

    @staticmethod
    def derive_session_state_from_events(session_id: str) -> Dict[str, Any]:
        """
        Derive current session state from EVENTS.jsonl event stream.
        This replaces STATE.json with event sourcing approach.

        Args:
            session_id: Session identifier

        Returns:
            Derived state dictionary
        """
        session_path = SessionManagement.get_session_path(session_id)
        events_file = os.path.join(session_path, "EVENTS.jsonl")

        state = {
            "session_id": session_id,
            "workers": {},
            "coordination": {
                "status": "unknown",
                "workers_spawned": [],
                "workers_completed": [],
                "workers_failed": []
            },
            "last_event_time": None,
            "event_count": 0
        }

        try:
            with open(events_file, "r") as f:
                for line in f:
                    if line.strip():
                        event = json.loads(line.strip())
                        state["event_count"] += 1
                        state["last_event_time"] = event.get("timestamp")
                        
                        # Process different event types
                        event_type = event.get("type", "")
                        agent = event.get("agent", "")
                        details = event.get("details", {})
                        
                        if event_type == "worker_spawned":
                            if agent not in state["coordination"]["workers_spawned"]:
                                state["coordination"]["workers_spawned"].append(agent)
                                state["workers"][agent] = {
                                    "status": "spawned",
                                    "spawn_time": event.get("timestamp"),
                                    "task": details.get("task", ""),
                                    "capabilities": details.get("capabilities", [])
                                }
                        
                        elif event_type == "worker_completed":
                            if agent not in state["coordination"]["workers_completed"]:
                                state["coordination"]["workers_completed"].append(agent)
                                if agent in state["workers"]:
                                    state["workers"][agent]["status"] = "completed"
                                    state["workers"][agent]["completion_time"] = event.get("timestamp")
                        
                        elif event_type == "analysis_started":
                            if agent in state["workers"]:
                                state["workers"][agent]["status"] = "in_progress"
                                state["workers"][agent]["analysis_start"] = event.get("timestamp")

            # Determine overall coordination status
            total_workers = len(state["coordination"]["workers_spawned"])
            completed_workers = len(state["coordination"]["workers_completed"])
            
            if total_workers == 0:
                state["coordination"]["status"] = "no_workers"
            elif completed_workers == total_workers:
                state["coordination"]["status"] = "completed"
            elif completed_workers > 0:
                state["coordination"]["status"] = "in_progress"
            else:
                state["coordination"]["status"] = "starting"

            return state

        except Exception as e:
            print(f"Failed to derive state from events: {e}")
            return state

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
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
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
            worker_clean = worker_type.replace("-worker", "")
            file_path = os.path.join(session_path, "notes", f"{worker_clean}_notes.md")
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
    def update_session_progress(
        session_id: str, progress_update: str, worker_type: str = "system"
    ) -> bool:
        """
        Update SESSION.md with progress information.
        Appends progress updates to the Coordination Progress section.
        Args:
            session_id: Session identifier
            progress_update: Progress update to add (markdown format)
            worker_type: Worker reporting the progress
        Returns:
            True if update successful
        """
        try:
            session_path = SessionManagement.get_session_path(session_id)
            session_md_path = os.path.join(session_path, "SESSION.md")
            # Read current SESSION.md
            if os.path.exists(session_md_path):
                with open(session_md_path, "r") as f:
                    content = f.read()

                # Find the Coordination Progress section
                import re

                progress_pattern = r"(## Coordination Progress\n)(.*?)(\n## |\n---|\Z)"

                def update_progress(match):
                    header = match.group(1)
                    current_progress = match.group(2)
                    footer = match.group(3)

                    # Add timestamp to progress update
                    timestamp = datetime.utcnow().strftime("%H:%M")
                    new_entry = f"- ✅ [{timestamp}] {progress_update}\n"

                    return header + current_progress + new_entry + footer

                # Update the content
                updated_content = re.sub(
                    progress_pattern, update_progress, content, flags=re.DOTALL
                )

                # Write back
                with open(session_md_path, "w") as f:
                    f.write(updated_content)

                return True
            else:
                # SESSION.md doesn't exist, log debug
                SessionManagement.append_to_debug(
                    session_id,
                    {
                        "level": "DEBUG",
                        "agent": worker_type,
                        "message": "SESSION.md not found for progress update",
                        "details": {"progress_update": progress_update},
                    },
                )
                return False

        except Exception as e:
            SessionManagement.append_to_debug(
                session_id,
                {
                    "level": "ERROR",
                    "agent": worker_type,
                    "message": "Failed to update SESSION.md progress",
                    "details": {"error": str(e), "progress_update": progress_update},
                },
            )
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
            backlog_item["timestamp"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        try:
            # CRITICAL: Use append mode
            with open(backlog_file, "a") as f:
                f.write(json.dumps(backlog_item, separators=(",", ":")) + "\n")
            return True
        except Exception as e:
            print(f"Failed to append to BACKLOG.jsonl: {e}")
            return False
