"""
Shared protocols package for Pydantic AI agents.

This package contains the core protocol implementations that enforce
consistent behavior across all worker agents.

Available protocols:
- startup_protocol: Worker initialization and compliance checking
- logging_protocol: Standardized event and debug logging  
- coordination_protocol: Inter-agent communication patterns
- session_management: Session lifecycle and state management
- monitoring_protocol: Progress tracking and health monitoring
- completion_protocol: Task completion and result validation
"""

from .startup_protocol import *
from .logging_protocol import *
from .coordination_protocol import *
from .session_management import *
from .monitoring_protocol import *
from .completion_protocol import *

__all__ = [
    # Startup Protocol
    "initialize_worker",
    "check_protocol_compliance", 
    "load_session_context",
    
    # Logging Protocol
    "log_event",
    "log_debug", 
    "log_error",
    "log_worker_status",
    
    # Coordination Protocol  
    "register_worker",
    "update_worker_status",
    "check_for_blocks",
    "escalate_to_queen",
    
    # Session Management
    "create_session",
    "load_session_state",
    "update_session_state", 
    "save_session_state",
    
    # Monitoring Protocol
    "start_monitoring",
    "check_worker_health",
    "detect_stalled_workers",
    
    # Completion Protocol
    "mark_task_complete",
    "validate_deliverables",
    "archive_results"
]