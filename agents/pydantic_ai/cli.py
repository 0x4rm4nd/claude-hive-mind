#!/usr/bin/env python3
"""
Pydantic AI Agents CLI
======================
Main command-line interface for the Pydantic AI agent framework.

Provides unified access to all agents and workers through a single entry point
with standardized argument handling and execution routing.
"""

import argparse
import sys
import subprocess
import os

# Get the directory of this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def run_queen(args):
    """Execute Queen orchestrator using BaseWorker pattern.

    Args:
        args: Parsed command line arguments containing session, task, and model parameters

    Returns:
        Exit code from Queen orchestrator execution
    """
    from queen.runner import QueenWorker

    task_description = args.task

    # Use BaseWorker pattern consistently
    worker = QueenWorker()
    try:
        output = worker.run(
            args.session, task_description, args.model or "custom:claude-opus-4"
        )
        print(f"✅ Queen orchestration completed: {worker.get_success_message(output)}")
        return 0
    except Exception as e:
        print(f"❌ Queen orchestration failed: {e}")
        return 1


def run_scribe(args):
    """Run Scribe agent with proper argument handling"""
    from scribe.runner import ScribeWorker

    worker = ScribeWorker()

    try:
        # Handle session creation mode
        if hasattr(args, "create") and args.create:
            if not args.task:
                print("❌ Error: --task required for session creation")
                return 1
            if args.session:
                print("❌ Error: --session should not be provided for create mode")
                return 1
            output = worker.run_creation(
                "", args.task, args.model or "custom:max-subscription"
            )
            success_message = worker.get_success_message(output)

        # Handle synthesis setup phase
        elif hasattr(args, "setup") and args.setup:
            if not args.session:
                print("❌ Error: --session required for synthesis setup")
                return 1
            output = worker.run_setup_phase(
                args.session, args.model or "custom:max-subscription"
            )
            success_message = worker.get_success_message(output)

        # Handle synthesis output phase
        elif hasattr(args, "output") and args.output:
            if not args.session:
                print("❌ Error: --session required for synthesis output")
                return 1
            output = worker.run_output_phase(
                args.session, args.model or "custom:max-subscription"
            )
            success_message = worker.get_success_message(output)

        else:
            print("❌ Error: Must specify --create, --setup, or --output")
            return 1

        print(f"✅ Scribe operation completed: {success_message}")

        # Print output as JSON for CC Agent to parse (like other workers)
        print("WORKER_OUTPUT_JSON:")
        print(output.model_dump_json(indent=2))

        return 0
    except Exception as e:
        print(f"❌ Scribe failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


def run_worker(worker_name: str, args):
    """Run a specific worker agent"""
    worker_runner = os.path.join(SCRIPT_DIR, worker_name, "runner.py")
    cmd = [
        sys.executable,
        worker_runner,
        "--session",
        args.session,
        "--model",
        args.model or "custom:max-subscription",
    ]

    # Add task only if provided
    if args.task is not None:
        cmd.extend(["--task", args.task])

    # Add phase flags if specified
    if hasattr(args, "setup") and args.setup:
        cmd.append("--setup")
    if hasattr(args, "output") and args.output:
        cmd.append("--output")

    return subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(
        description="Pydantic AI Agents CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create new session
  python cli.py scribe create --task "Analyze crypto-data security"
  
  # Run Queen orchestrator  
  python cli.py queen --session 2024-01-15-14-30-crypto-security-audit --task "..."
  
  # Run synthesis
  python cli.py scribe synthesis --session 2024-01-15-14-30-crypto-security-audit
  
  # Run individual workers
  python cli.py analyzer --session SESSION_ID --task "Security analysis"
  python cli.py backend --session SESSION_ID --task "API implementation"
  python cli.py frontend --session SESSION_ID --task "UI component development"
        """,
    )

    subparsers = parser.add_subparsers(dest="agent", help="Agent to run")

    # Queen orchestrator
    queen_parser = subparsers.add_parser("queen", help="Queen orchestrator")
    queen_parser.add_argument("--session", required=True, help="Session ID")
    queen_parser.add_argument("--task", required=True, help="Task description")
    queen_parser.add_argument("--model", help="AI model to use")

    # Scribe agent - follows BaseWorker pattern
    scribe_parser = subparsers.add_parser(
        "scribe", help="Session lifecycle management and creative synthesis"
    )
    scribe_parser.add_argument("--session", help="Session ID")
    scribe_parser.add_argument("--task", help="Task description")
    scribe_parser.add_argument("--model", help="AI model to use")

    # Add mutually exclusive mode flags for scribe operations
    scribe_mode_group = scribe_parser.add_mutually_exclusive_group(required=True)
    scribe_mode_group.add_argument(
        "--create",
        action="store_true",
        help="Create new session (requires --task)",
    )
    scribe_mode_group.add_argument(
        "--setup",
        action="store_true",
        help="Execute Phase 1: Creative Synthesis Setup & Data Collection",
    )
    scribe_mode_group.add_argument(
        "--output",
        action="store_true",
        help="Execute Phase 3: Synthesis Validation & File Creation",
    )

    # Worker agents - all follow same pattern
    workers = [
        (
            "analyzer",
            "Security analysis, performance optimization, and code quality assessment",
        ),
        (
            "architect",
            "System design, scalability patterns, and technical architecture",
        ),
        ("backend", "API development, database design, and service implementation"),
        ("designer", "User experience design, visual design, and accessibility"),
        ("devops", "Infrastructure, deployment, monitoring, and CI/CD pipelines"),
        (
            "frontend",
            "UI/UX implementation, component architecture, and state management",
        ),
        (
            "researcher",
            "Technical research, best practices, and industry standards analysis",
        ),
        ("test", "Testing strategy, quality assurance, and test coverage analysis"),
    ]

    for worker_name, worker_description in workers:
        worker_parser = subparsers.add_parser(worker_name, help=worker_description)
        worker_parser.add_argument("--session", required=True, help="Session ID")
        worker_parser.add_argument("--task", help="Task description")
        worker_parser.add_argument("--model", help="AI model to use")

        # Add mutually exclusive phase flags
        phase_group = worker_parser.add_mutually_exclusive_group()
        phase_group.add_argument(
            "--setup",
            action="store_true",
            help="Execute Phase 1: Setup & Context Loading",
        )
        phase_group.add_argument(
            "--output",
            action="store_true",
            help="Execute Phase 3: Validation & Output Generation",
        )

    args = parser.parse_args()

    if not args.agent:
        parser.print_help()
        return 1

    # Route to appropriate agent
    if args.agent == "queen":
        return run_queen(args)
    elif args.agent == "scribe":
        return run_scribe(args)
    elif args.agent in [
        "analyzer",
        "architect",
        "backend",
        "designer",
        "devops",
        "frontend",
        "researcher",
        "test",
    ]:
        return run_worker(args.agent, args).returncode
    else:
        print(f"Unknown agent: {args.agent}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
