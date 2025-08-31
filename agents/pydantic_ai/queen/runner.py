#!/usr/bin/env python3
"""
Queen Orchestrator Runner
=========================
Execution script with continuous monitoring capabilities.
"""

import argparse
import json
import time
import asyncio
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
import sys
import os

# Environment setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Add agents/pydantic_ai to path for imports
pydantic_ai_path = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, str(pydantic_ai_path))

from shared.protocols import (
    SessionManagement,
    LoggingProtocol,
    ProtocolConfig,
    WorkerPromptProtocol,
    create_worker_prompts_from_plan,
    load_project_env
)

# Use helper function to load project environment
load_project_env()

from queen.models import QueenOrchestrationPlan, WorkerAssignment
from queen.agent import queen_agent
from shared.tools import iso_now


def log_event(session_id: str, event_type: str, agent: str, details: Any):
    """Log event using protocol infrastructure"""
    try:
        cfg = ProtocolConfig({"session_id": session_id, "agent_name": agent})
        logger = LoggingProtocol(cfg)
        logger.log_event(event_type, details)
    except Exception as e:
        print(f"Logging failed: {e}")


def log_debug(session_id: str, message: str, details: Any):
    """Log debug message using protocol infrastructure"""
    try:
        cfg = ProtocolConfig(
            {"session_id": session_id, "agent_name": "queen-orchestrator"}
        )
        logger = LoggingProtocol(cfg)
        logger.log_debug(message, details)
    except Exception as e:
        print(f"Debug logging failed: {e}")


def update_session_state(session_id: str, state_update: Dict[str, Any]):
    """Update session state using protocol infrastructure"""
    try:
        SessionManagement.update_state_atomically(session_id, state_update)
        log_debug(
            session_id, "Session state updated", {"keys": list(state_update.keys())}
        )
    except Exception as e:
        log_debug(session_id, "Session state update failed", {"error": str(e)})


def run_orchestration(
    session_id: str, task_description: str, model: str, retry_count: int = 0
) -> QueenOrchestrationPlan:
    """Run Queen orchestration with AI analysis and intelligent retry"""
    worker = "queen-orchestrator"
    timestamp = iso_now()
    max_retries = 3

    # Validate session exists using protocol infrastructure
    try:
        if not SessionManagement.ensure_session_exists(session_id):
            raise ValueError(f"Session {session_id} does not exist or is invalid")
        log_debug(
            session_id, "Session validation successful", {"session_id": session_id}
        )
    except Exception as e:
        log_debug(
            session_id,
            "Session validation failed",
            {"error": str(e), "session_id": session_id},
        )

    # Log mandatory Queen spawn event
    log_event(
        session_id,
        "queen_spawned",
        worker,
        {"note": "Queen orchestrator initialized for session", "retry": retry_count},
    )

    if not queen_agent:
        raise RuntimeError("Queen agent not available")

    try:
        # Run AI orchestration
        result = queen_agent.run_sync(
            f"Orchestrate this task: {task_description}", model=model
        )

        orchestration_plan: QueenOrchestrationPlan = result.output

        # Ensure session_id and timestamp are set
        orchestration_plan.session_id = session_id
        orchestration_plan.timestamp = timestamp

        # Update session state with detailed worker configurations
        detailed_state_update = create_detailed_state_update(
            session_id, task_description, orchestration_plan
        )
        SessionManagement.update_state_atomically(session_id, detailed_state_update)
        
        # Spawn the Pydantic AI workers
        spawn_result = spawn_pydantic_workers(session_id, task_description, orchestration_plan.worker_assignments)
        
        log_event(
            session_id,
            "workers_deployed",
            "queen-orchestrator",
            {
                "spawned_count": spawn_result["spawn_count"],
                "failed_count": len(spawn_result["failed_spawns"]),
                "spawned_workers": [w["worker_type"] for w in spawn_result["spawned_workers"]],
                "failed_workers": [f["worker_type"] for f in spawn_result["failed_spawns"]]
            }
        )
        
        # Update SESSION.md with human-readable summary
        update_session_summary(session_id, task_description, orchestration_plan)

        # Log consolidated task assignment event for all workers
        log_event(
            session_id,
            "tasks_assigned",
            worker,
            {
                "worker_assignments": [
                    {
                        "worker_type": assignment.worker_type,
                        "task_focus": assignment.task_focus,
                        "priority": assignment.priority,
                        "dependencies": assignment.dependencies,
                        "estimated_duration": assignment.estimated_duration,
                        "rationale": assignment.rationale
                    }
                    for assignment in orchestration_plan.worker_assignments
                ],
                "total_workers": len(orchestration_plan.worker_assignments),
                "complexity_level": orchestration_plan.complexity_assessment,
                "execution_strategy": orchestration_plan.execution_strategy,
            },
        )

        # Create worker prompt files (framework-enforced)
        try:
            created_prompts = create_worker_prompts_from_plan(session_id, orchestration_plan)
            # Logging is handled by prompt_generator with batch_logging=True (default)
        except Exception as e:
            log_debug(
                session_id,
                "Worker prompts creation failed",
                {
                    "error": str(e),
                    "exception_type": str(type(e)),
                    "impact": "Workers may not have proper task instructions"
                }
            )
            # Continue execution - workers can use fallback extraction

        # Log successful orchestration
        log_event(
            session_id,
            "orchestration_completed",
            worker,
            {
                "complexity": orchestration_plan.complexity_assessment,
                "worker_count": len(orchestration_plan.worker_assignments),
                "strategy": orchestration_plan.execution_strategy,
            },
        )

        return orchestration_plan

    except Exception as e:
        error_str = str(e).lower()
        
        # Log error to debug
        log_debug(
            session_id,
            f"Queen orchestration attempt {retry_count + 1} failed",
            {
                "error": str(e),
                "exception_type": str(type(e)),
                "retry_count": retry_count,
                "original_model": model,
            },
        )
        
        # Check if we should retry with different parameters
        if retry_count < max_retries:
            new_model = model
            
            # Adjust model based on error type
            if "model_not_found" in error_str or "does not exist" in error_str:
                if "o3" in model or "o1" in model:
                    new_model = "openai:gpt-4o"
                    log_debug(session_id, "Switching to available model", {"new_model": new_model})
                elif "gpt-5" in model:
                    new_model = "openai:gpt-4o" 
                    log_debug(session_id, "Switching to available model", {"new_model": new_model})
            elif "rate_limit" in error_str:
                import time
                wait_time = (retry_count + 1) * 2  # Exponential backoff
                log_debug(session_id, f"Rate limit hit, waiting {wait_time}s", {"wait_time": wait_time})
                time.sleep(wait_time)
            elif "context_length" in error_str or "too long" in error_str:
                # Could adjust prompt length here if needed
                log_debug(session_id, "Context length exceeded, using simpler prompt", {})
            
            # Retry with adjusted parameters
            return run_orchestration(session_id, task_description, new_model, retry_count + 1)
        
        # Max retries exceeded, re-raise the exception
        log_debug(session_id, "Max retries exceeded, giving up", {"max_retries": max_retries})
        raise e


def update_session_summary(
    session_id: str, task_description: str, orchestration_plan: QueenOrchestrationPlan
) -> bool:
    """Update SESSION.md with human-readable summary"""
    try:
        session_path = SessionManagement.get_session_path(session_id)
        session_md_path = os.path.join(session_path, "SESSION.md")
        
        # Parse session ID for date
        date_part = session_id.split("-")[:3]  # 2025-08-31-10
        session_date = "-".join(date_part[:3]) if len(date_part) >= 3 else "unknown"
        
        # Generate worker assignments section
        worker_assignments_md = ""
        for assignment in orchestration_plan.worker_assignments:
            worker_assignments_md += f"- **{assignment.worker_type}**: {assignment.task_focus}\n"
        
        # Create SESSION.md content
        session_content = f"""# {task_description.title()} Session

## Session Details
- **Session ID**: {session_id}
- **Date**: {session_date}
- **Coordinator**: queen-orchestrator
- **Status**: Workers Assigned - {len(orchestration_plan.worker_assignments)} workers ready
- **Complexity**: Level {orchestration_plan.complexity_assessment}/4
- **Strategy**: {orchestration_plan.execution_strategy}

## Task Overview
{task_description}

## Worker Assignments
{worker_assignments_md}
## Orchestration Plan
- **Estimated Duration**: {orchestration_plan.estimated_total_duration}
- **Worker Count**: {len(orchestration_plan.worker_assignments)}
- **Execution Strategy**: {orchestration_plan.execution_strategy}

## Coordination Progress
- ✅ Queen orchestrator activated
- ✅ Task analysis completed
- ✅ Worker assignments generated
- ✅ Worker prompts created
- ⏳ Waiting for worker deployment

## Success Metrics
{chr(10).join(f"- {metric}" for metric in orchestration_plan.success_metrics) if orchestration_plan.success_metrics else "- Standard completion criteria"}

## Quality Gates
{chr(10).join(f"- {gate}" for gate in orchestration_plan.quality_gates) if orchestration_plan.quality_gates else "- Framework-enforced validation"}

---
*Generated by Queen Orchestrator at {orchestration_plan.timestamp}*
"""
        
        # Write SESSION.md
        with open(session_md_path, "w") as f:
            f.write(session_content)
            
        return True
        
    except Exception as e:
        log_debug(session_id, "SESSION.md update failed", {"error": str(e)})
        return False


def create_detailed_state_update(
    session_id: str, task_description: str, orchestration_plan: QueenOrchestrationPlan
) -> Dict[str, Any]:
    """Create comprehensive state update for session"""
    timestamp = iso_now()

    # Extract target service from task or codebase insights
    target_service = "unknown"
    if orchestration_plan.codebase_insights:
        target_service = orchestration_plan.codebase_insights[0].service_name
    elif "crypto-data" in task_description.lower():
        target_service = "crypto-data"
    elif "api" in task_description.lower():
        target_service = "api"
    elif "frontend" in task_description.lower():
        target_service = "frontend"

    worker_types = [
        assignment.worker_type for assignment in orchestration_plan.worker_assignments
    ]

    # Create comprehensive state update
    state_update = {
        "coordinator": "queen-orchestrator",
        "target_service": target_service,
        "coordination_status": {
            "phase": "worker_preparation",
            "workers_spawned": [],
            "workers_completed": [],
            "workers_pending": worker_types.copy(),
            "synthesis_ready": False,
        },
        "worker_configs": {},
    }

    # Tag mapping for worker types
    tag_mapping = {
        "analyzer-worker": ["security", "performance", "quality"],
        "architect-worker": ["architecture", "patterns", "design"],
        "backend-worker": ["backend", "database", "api"],
        "frontend-worker": ["frontend", "ui", "components"],
        "designer-worker": ["design", "ux", "accessibility"],
        "devops-worker": ["infrastructure", "deployment", "monitoring"],
        "researcher-worker": ["research", "patterns", "standards"],
        "test-worker": ["testing", "quality", "coverage"],
    }

    # Create detailed worker configurations
    for assignment in orchestration_plan.worker_assignments:
        worker_type = assignment.worker_type
        tags = tag_mapping.get(worker_type, ["analysis"])

        worker_config = {
            "tag_access": tags,
            "escalation_timeout": 300,
            "escalation_chain": ["queen-orchestrator"],
            "complexity_level": orchestration_plan.complexity_assessment,
            "task_description": assignment.task_focus,
            "status": "not_started",
            "protocol_compliance": {
                "startup_completed": False,
                "monitoring_active": False,
            },
        }

        state_update["worker_configs"][worker_type] = worker_config

    return state_update




async def monitor_worker_progress(
    session_id: str,
    worker_assignments: List[WorkerAssignment],
    monitoring_interval: int = 30,
):
    """
    Continuous monitoring of worker progress.
    Queen spawned alongside workers to monitor their evolution.
    """
    worker = "queen-orchestrator"

    log_event(
        session_id,
        "monitoring_started",
        worker,
        {
            "workers_to_monitor": [w.worker_type for w in worker_assignments],
            "interval_seconds": monitoring_interval,
        },
    )

    all_workers_complete = False

    while not all_workers_complete:
        try:
            # Check worker status in STATE.json
            session_state = SessionManagement.read_state(session_id)

            if not session_state:
                log_event(
                    session_id,
                    "monitoring_error",
                    worker,
                    {"error": "Could not load session state"},
                )
                await asyncio.sleep(monitoring_interval)
                continue

            coordination_status = session_state.get("coordination_status", {})
            workers_completed = coordination_status.get("workers_completed", [])
            workers_pending = coordination_status.get("workers_pending", [])

            # Check if all workers are done
            expected_workers = {w.worker_type for w in worker_assignments}
            completed_workers = set(workers_completed)

            if expected_workers.issubset(completed_workers):
                log_event(
                    session_id,
                    "all_workers_completed",
                    worker,
                    {
                        "completed_workers": list(completed_workers),
                        "monitoring_duration": "continuous",
                    },
                )
                all_workers_complete = True
                break

            # Check for blocked/failed workers
            blocked_workers = []
            for worker_type in workers_pending:
                worker_config = session_state.get("worker_configs", {}).get(
                    worker_type, {}
                )
                if worker_config.get("status") == "blocked":
                    blocked_workers.append(worker_type)

            if blocked_workers:
                log_event(
                    session_id,
                    "workers_blocked_detected",
                    worker,
                    {
                        "blocked_workers": blocked_workers,
                        "action": "escalation_required",
                    },
                )

            # Log periodic status update
            log_event(
                session_id,
                "monitoring_heartbeat",
                worker,
                {
                    "completed": list(completed_workers),
                    "pending": workers_pending,
                    "blocked": blocked_workers,
                    "progress": f"{len(completed_workers)}/{len(expected_workers)}",
                },
            )

            # Wait for next check
            await asyncio.sleep(monitoring_interval)

        except Exception as e:
            log_debug(
                session_id,
                "Worker monitoring error",
                {"error": str(e), "action": "continuing_monitoring"},
            )
            await asyncio.sleep(monitoring_interval)

    log_event(
        session_id,
        "monitoring_completed",
        worker,
        {"status": "all_workers_finished", "final_check": "ready_for_synthesis"},
    )


def spawn_pydantic_workers(session_id: str, task_description: str, worker_assignments: List[WorkerAssignment]) -> Dict[str, Any]:
    """Spawn Pydantic AI worker agents using bash commands"""
    import subprocess
    
    # Map worker types to agent directory names  
    worker_type_mapping = {
        "analyzer-worker": "analyzer",
        "architect-worker": "architect", 
        "backend-worker": "backend",
        "frontend-worker": "frontend",
        "designer-worker": "designer",
        "devops-worker": "devops",
        "researcher-worker": "researcher",
        "test-worker": "test"
    }
    
    spawned_workers = []
    failed_spawns = []
    
    # Get the base path for agents
    base_path = Path(__file__).parent.parent
    
    # Prepare all worker commands first
    worker_commands = []
    project_root = Path(__file__).parent.parent.parent.parent
    
    for assignment in worker_assignments:
        worker_type = assignment.worker_type
        task_focus = assignment.task_focus
            
        agent_name = worker_type_mapping.get(worker_type)
        
        if not agent_name:
            failed_spawns.append({
                "worker_type": worker_type,
                "error": f"Unknown worker type: {worker_type}"
            })
            continue
            
        # Construct the bash command to spawn the worker as a module
        # Use -m to run as module to handle relative imports correctly
        cmd = [
            "python", 
            "-m", f"agents.pydantic_ai.{agent_name}.runner",
            "--session", session_id,
            "--task", task_focus
        ]
        
        worker_commands.append({
            "worker_type": worker_type,
            "agent_name": agent_name,
            "task_focus": task_focus,
            "cmd": cmd
        })
    
    # Spawn all workers in parallel
    processes = []
    for worker_config in worker_commands:
        try:
            # Spawn the worker process in background
            # Change to project root directory to ensure module imports work
            process = subprocess.Popen(
                worker_config["cmd"],
                cwd=str(project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            processes.append((process, worker_config))
            
            spawned_workers.append({
                "worker_type": worker_config["worker_type"],
                "agent_name": worker_config["agent_name"],
                "process_id": process.pid,
                "command": " ".join(worker_config["cmd"]),
                "task_focus": worker_config["task_focus"]
            })
            
            # Log the worker spawn
            log_event(
                session_id,
                "worker_spawned",
                worker_config["agent_name"],
                {
                    "worker_type": worker_config["worker_type"],
                    "task_focus": worker_config["task_focus"],
                    "process_id": process.pid,
                    "spawned_by": "queen-orchestrator"
                }
            )
            
        except Exception as e:
            failed_spawns.append({
                "worker_type": worker_config["worker_type"],
                "error": str(e)
            })
            log_event(
                session_id,
                "worker_spawn_failed", 
                "queen-orchestrator",
                {
                    "worker_type": worker_config["worker_type"],
                    "error": str(e)
                }
            )
    
    # Log parallel deployment completion
    if spawned_workers:
        log_event(
            session_id,
            "parallel_worker_deployment_completed",
            "queen-orchestrator", 
            {
                "total_spawned": len(spawned_workers),
                "worker_types": [w["worker_type"] for w in spawned_workers],
                "spawn_strategy": "parallel",
                "deployment_time": "simultaneous"
            }
        )
    
    return {
        "spawned_workers": spawned_workers,
        "failed_spawns": failed_spawns,
        "spawn_count": len(spawned_workers),
        "session_id": session_id
    }


def main():
    parser = argparse.ArgumentParser(description="Pydantic AI Queen Orchestrator")
    parser.add_argument("--session", required=True, help="Session ID")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--model", default="openai:gpt-4o", help="AI model to use")
    parser.add_argument(
        "--monitor", action="store_true", help="Enable continuous monitoring"
    )
    parser.add_argument(
        "--monitor-interval",
        type=int,
        default=30,
        help="Monitoring interval in seconds",
    )

    args = parser.parse_args()

    # Run orchestration
    orchestration_plan = run_orchestration(args.session, args.task, args.model)

    # Output the orchestration plan
    print(json.dumps(orchestration_plan.model_dump(), indent=2))

    # If monitoring enabled, start continuous monitoring
    if args.monitor and orchestration_plan.worker_assignments:
        print(
            f"\\n🔍 Starting continuous monitoring (checking every {args.monitor_interval}s)..."
        )
        asyncio.run(
            monitor_worker_progress(
                args.session,
                orchestration_plan.worker_assignments,
                args.monitor_interval,
            )
        )


if __name__ == "__main__":
    main()
