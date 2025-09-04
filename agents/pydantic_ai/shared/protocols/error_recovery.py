#!/usr/bin/env python3
"""
Error Recovery System - Advanced error handling and recovery mechanisms
======================================================================
Provides comprehensive error recovery strategies for protocol operations.
"""

from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import traceback
import time
import json


class RecoveryStrategy(Enum):
    """Types of recovery strategies"""

    RETRY = "retry"
    FALLBACK = "fallback"
    RESET = "reset"
    SKIP = "skip"
    ESCALATE = "escalate"
    CUSTOM = "custom"


class ErrorSeverity(Enum):
    """Error severity levels"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RecoveryAction:
    """Individual recovery action definition"""

    strategy: RecoveryStrategy
    max_attempts: int = 3
    delay_seconds: float = 1.0
    exponential_backoff: bool = True
    fallback_function: Optional[Callable] = None
    custom_recovery: Optional[Callable] = None
    escalation_threshold: int = 3
    recovery_timeout: float = 30.0

    def should_attempt_recovery(self, attempt_count: int, error: Exception) -> bool:
        """Determine if recovery should be attempted"""
        if attempt_count >= self.max_attempts:
            return False

        # Check for non-recoverable errors
        non_recoverable = [
            PermissionError,
            SecurityError,
            SystemExit,
            KeyboardInterrupt,
        ]

        for error_type in non_recoverable:
            if isinstance(error, error_type):
                return False

        return True

    def calculate_delay(self, attempt_count: int) -> float:
        """Calculate delay before next recovery attempt"""
        if self.exponential_backoff:
            return self.delay_seconds * (2**attempt_count)
        return self.delay_seconds


@dataclass
class ErrorContext:
    """Context information about an error occurrence"""

    error: Exception
    operation: str
    protocol_name: str
    session_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    context_data: Dict[str, Any] = field(default_factory=dict)
    stack_trace: str = field(default_factory=lambda: traceback.format_exc())
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    is_recoverable: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert error context to dictionary"""
        return {
            "error_type": str(type(self.error)),
            "error_message": str(self.error),
            "operation": self.operation,
            "protocol_name": self.protocol_name,
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "context_data": self.context_data,
            "stack_trace": self.stack_trace,
            "severity": self.severity.value,
            "is_recoverable": self.is_recoverable,
        }


@dataclass
class RecoveryResult:
    """Result of a recovery attempt"""

    success: bool
    strategy_used: RecoveryStrategy
    attempts_made: int
    total_recovery_time: float
    final_error: Optional[Exception] = None
    recovery_log: List[Dict[str, Any]] = field(default_factory=list)
    fallback_used: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert recovery result to dictionary"""
        return {
            "success": self.success,
            "strategy_used": self.strategy_used.value,
            "attempts_made": self.attempts_made,
            "total_recovery_time": self.total_recovery_time,
            "final_error": str(self.final_error) if self.final_error else None,
            "recovery_log": self.recovery_log,
            "fallback_used": self.fallback_used,
        }


class ErrorRecoveryManager:
    """Manager for error recovery strategies and execution"""

    def __init__(self):
        self.recovery_strategies: Dict[type, RecoveryAction] = {}
        self.recovery_history: List[Dict[str, Any]] = []
        self.error_patterns: Dict[str, RecoveryAction] = {}
        self._setup_default_strategies()

    def _setup_default_strategies(self):
        """Setup default recovery strategies for common error types"""

        # File operation errors - retry with exponential backoff
        self.recovery_strategies[FileNotFoundError] = RecoveryAction(
            strategy=RecoveryStrategy.RETRY,
            max_attempts=3,
            delay_seconds=0.5,
            exponential_backoff=True,
        )

        self.recovery_strategies[OSError] = RecoveryAction(
            strategy=RecoveryStrategy.RETRY,
            max_attempts=2,
            delay_seconds=1.0,
            exponential_backoff=True,
        )

        # Configuration errors - try reset/fallback
        self.recovery_strategies[ValueError] = RecoveryAction(
            strategy=RecoveryStrategy.FALLBACK,
            max_attempts=2,
            delay_seconds=0.1,
            exponential_backoff=False,
        )

        # Connection/timeout errors - retry with longer delays
        self.recovery_strategies[TimeoutError] = RecoveryAction(
            strategy=RecoveryStrategy.RETRY,
            max_attempts=5,
            delay_seconds=2.0,
            exponential_backoff=True,
        )

        # Memory errors - escalate immediately
        self.recovery_strategies[MemoryError] = RecoveryAction(
            strategy=RecoveryStrategy.ESCALATE, max_attempts=1, delay_seconds=0.0
        )

    def register_recovery_strategy(self, error_type: type, action: RecoveryAction):
        """Register a recovery strategy for a specific error type"""
        self.recovery_strategies[error_type] = action

    def register_pattern_strategy(self, error_pattern: str, action: RecoveryAction):
        """Register a recovery strategy for errors matching a pattern"""
        self.error_patterns[error_pattern] = action

    def attempt_recovery(
        self, error_context: ErrorContext, operation_function: Callable, *args, **kwargs
    ) -> RecoveryResult:
        """
        Attempt to recover from an error using appropriate strategy.

        Args:
            error_context: Context about the error
            operation_function: Function to retry after recovery
            *args, **kwargs: Arguments for the operation function

        Returns:
            RecoveryResult indicating success/failure and details
        """
        start_time = time.time()
        recovery_action = self._get_recovery_action(error_context)

        recovery_result = RecoveryResult(
            success=False,
            strategy_used=recovery_action.strategy,
            attempts_made=0,
            total_recovery_time=0.0,
        )

        try:
            if recovery_action.strategy == RecoveryStrategy.RETRY:
                recovery_result = self._attempt_retry_recovery(
                    error_context, recovery_action, operation_function, *args, **kwargs
                )

            elif recovery_action.strategy == RecoveryStrategy.FALLBACK:
                recovery_result = self._attempt_fallback_recovery(
                    error_context, recovery_action, operation_function, *args, **kwargs
                )

            elif recovery_action.strategy == RecoveryStrategy.RESET:
                recovery_result = self._attempt_reset_recovery(
                    error_context, recovery_action, operation_function, *args, **kwargs
                )

            elif recovery_action.strategy == RecoveryStrategy.SKIP:
                recovery_result = self._attempt_skip_recovery(error_context)

            elif recovery_action.strategy == RecoveryStrategy.CUSTOM:
                recovery_result = self._attempt_custom_recovery(
                    error_context, recovery_action, operation_function, *args, **kwargs
                )

            elif recovery_action.strategy == RecoveryStrategy.ESCALATE:
                recovery_result = self._escalate_error(error_context)

        except Exception as recovery_error:
            recovery_result.final_error = recovery_error
            recovery_result.recovery_log.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "event": "recovery_failed",
                    "error": str(recovery_error),
                }
            )

        recovery_result.total_recovery_time = time.time() - start_time

        # Log recovery attempt
        self._log_recovery_attempt(error_context, recovery_result)

        return recovery_result

    def _get_recovery_action(self, error_context: ErrorContext) -> RecoveryAction:
        """Determine appropriate recovery action for error"""
        error_type = type(error_context.error)

        # Check for exact type match
        if error_type in self.recovery_strategies:
            return self.recovery_strategies[error_type]

        # Check parent types
        for registered_type, action in self.recovery_strategies.items():
            if issubclass(error_type, registered_type):
                return action

        # Check error message patterns
        error_message = str(error_context.error).lower()
        for pattern, action in self.error_patterns.items():
            if pattern.lower() in error_message:
                return action

        # Default fallback strategy
        return RecoveryAction(
            strategy=RecoveryStrategy.RETRY, max_attempts=2, delay_seconds=1.0
        )

    def _attempt_retry_recovery(
        self,
        error_context: ErrorContext,
        recovery_action: RecoveryAction,
        operation_function: Callable,
        *args,
        **kwargs
    ) -> RecoveryResult:
        """Attempt recovery using retry strategy"""
        recovery_result = RecoveryResult(
            success=False,
            strategy_used=RecoveryStrategy.RETRY,
            attempts_made=0,
            total_recovery_time=0.0,
        )

        for attempt in range(recovery_action.max_attempts):
            recovery_result.attempts_made = attempt + 1

            if attempt > 0:  # Skip delay on first attempt
                delay = recovery_action.calculate_delay(attempt - 1)
                recovery_result.recovery_log.append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "event": "retry_delay",
                        "delay_seconds": delay,
                        "attempt": attempt + 1,
                    }
                )
                time.sleep(delay)

            try:
                result = operation_function(*args, **kwargs)
                recovery_result.success = True
                recovery_result.recovery_log.append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "event": "retry_success",
                        "attempt": attempt + 1,
                    }
                )
                return recovery_result

            except Exception as retry_error:
                recovery_result.final_error = retry_error
                recovery_result.recovery_log.append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "event": "retry_failed",
                        "attempt": attempt + 1,
                        "error": str(retry_error),
                    }
                )

                if not recovery_action.should_attempt_recovery(
                    attempt + 1, retry_error
                ):
                    break

        return recovery_result

    def _attempt_fallback_recovery(
        self,
        error_context: ErrorContext,
        recovery_action: RecoveryAction,
        operation_function: Callable,
        *args,
        **kwargs
    ) -> RecoveryResult:
        """Attempt recovery using fallback strategy"""
        recovery_result = RecoveryResult(
            success=False,
            strategy_used=RecoveryStrategy.FALLBACK,
            attempts_made=1,
            total_recovery_time=0.0,
        )

        if recovery_action.fallback_function:
            try:
                result = recovery_action.fallback_function(*args, **kwargs)
                recovery_result.success = True
                recovery_result.fallback_used = True
                recovery_result.recovery_log.append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "event": "fallback_success",
                    }
                )
                return recovery_result

            except Exception as fallback_error:
                recovery_result.final_error = fallback_error
                recovery_result.recovery_log.append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "event": "fallback_failed",
                        "error": str(fallback_error),
                    }
                )

        # Try original operation once more with modified parameters
        try:
            # Try with minimal/default parameters
            if "config" in kwargs:
                minimal_config = {
                    "session_id": kwargs["config"].get("session_id", "recovery"),
                    "agent_name": kwargs["config"].get("agent_name", "system"),
                }
                kwargs["config"] = minimal_config

            result = operation_function(*args, **kwargs)
            recovery_result.success = True
            recovery_result.recovery_log.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "event": "fallback_with_minimal_params_success",
                }
            )

        except Exception as final_error:
            recovery_result.final_error = final_error
            recovery_result.recovery_log.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "event": "fallback_final_attempt_failed",
                    "error": str(final_error),
                }
            )

        return recovery_result

    def _attempt_reset_recovery(
        self,
        error_context: ErrorContext,
        recovery_action: RecoveryAction,
        operation_function: Callable,
        *args,
        **kwargs
    ) -> RecoveryResult:
        """Attempt recovery using reset strategy"""
        recovery_result = RecoveryResult(
            success=False,
            strategy_used=RecoveryStrategy.RESET,
            attempts_made=1,
            total_recovery_time=0.0,
        )

        try:
            # Try to reset protocol state if possible
            if hasattr(operation_function, "__self__"):
                protocol_instance = operation_function.__self__
                if hasattr(protocol_instance, "_reset_state"):
                    protocol_instance._reset_state()
                elif hasattr(protocol_instance, "cleanup"):
                    protocol_instance.cleanup()
                    protocol_instance.initialize(protocol_instance.config.to_dict())

            result = operation_function(*args, **kwargs)
            recovery_result.success = True
            recovery_result.recovery_log.append(
                {"timestamp": datetime.now().isoformat(), "event": "reset_success"}
            )

        except Exception as reset_error:
            recovery_result.final_error = reset_error
            recovery_result.recovery_log.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "event": "reset_failed",
                    "error": str(reset_error),
                }
            )

        return recovery_result

    def _attempt_skip_recovery(self, error_context: ErrorContext) -> RecoveryResult:
        """Attempt recovery using skip strategy"""
        return RecoveryResult(
            success=True,  # Skipping is considered "successful"
            strategy_used=RecoveryStrategy.SKIP,
            attempts_made=1,
            total_recovery_time=0.0,
            recovery_log=[
                {
                    "timestamp": datetime.now().isoformat(),
                    "event": "operation_skipped",
                    "reason": "skip_strategy_applied",
                }
            ],
        )

    def _attempt_custom_recovery(
        self,
        error_context: ErrorContext,
        recovery_action: RecoveryAction,
        operation_function: Callable,
        *args,
        **kwargs
    ) -> RecoveryResult:
        """Attempt recovery using custom strategy"""
        recovery_result = RecoveryResult(
            success=False,
            strategy_used=RecoveryStrategy.CUSTOM,
            attempts_made=1,
            total_recovery_time=0.0,
        )

        if recovery_action.custom_recovery:
            try:
                result = recovery_action.custom_recovery(
                    error_context, operation_function, *args, **kwargs
                )
                recovery_result.success = True
                recovery_result.recovery_log.append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "event": "custom_recovery_success",
                    }
                )

            except Exception as custom_error:
                recovery_result.final_error = custom_error
                recovery_result.recovery_log.append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "event": "custom_recovery_failed",
                        "error": str(custom_error),
                    }
                )

        return recovery_result

    def _escalate_error(self, error_context: ErrorContext) -> RecoveryResult:
        """Escalate error without recovery attempt"""
        recovery_result = RecoveryResult(
            success=False,
            strategy_used=RecoveryStrategy.ESCALATE,
            attempts_made=0,
            total_recovery_time=0.0,
            final_error=error_context.error,
        )

        recovery_result.recovery_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "event": "error_escalated",
                "reason": "critical_error_requires_intervention",
            }
        )

        return recovery_result

    def _log_recovery_attempt(
        self, error_context: ErrorContext, recovery_result: RecoveryResult
    ):
        """Log recovery attempt to history"""
        recovery_record = {
            "timestamp": datetime.now().isoformat(),
            "error_context": error_context.to_dict(),
            "recovery_result": recovery_result.to_dict(),
        }

        self.recovery_history.append(recovery_record)

        # Keep only last 100 recovery attempts
        if len(self.recovery_history) > 100:
            self.recovery_history = self.recovery_history[-100:]

    def get_recovery_statistics(self) -> Dict[str, Any]:
        """Get statistics about recovery attempts"""
        if not self.recovery_history:
            return {"total_attempts": 0, "success_rate": 0.0}

        total_attempts = len(self.recovery_history)
        successful_recoveries = sum(
            1
            for record in self.recovery_history
            if record["recovery_result"]["success"]
        )

        success_rate = successful_recoveries / total_attempts

        # Strategy breakdown
        strategy_stats = {}
        for record in self.recovery_history:
            strategy = record["recovery_result"]["strategy_used"]
            if strategy not in strategy_stats:
                strategy_stats[strategy] = {"attempts": 0, "successes": 0}
            strategy_stats[strategy]["attempts"] += 1
            if record["recovery_result"]["success"]:
                strategy_stats[strategy]["successes"] += 1

        return {
            "total_attempts": total_attempts,
            "successful_recoveries": successful_recoveries,
            "success_rate": success_rate,
            "strategy_breakdown": strategy_stats,
            "avg_recovery_time": sum(
                record["recovery_result"]["total_recovery_time"]
                for record in self.recovery_history
            )
            / total_attempts,
        }


# Global error recovery manager
error_recovery_manager = ErrorRecoveryManager()
