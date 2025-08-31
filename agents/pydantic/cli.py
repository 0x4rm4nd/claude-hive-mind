#!/usr/bin/env python3
"""
Pydantic AI Agents CLI
=====================
Main CLI entry point that routes to different agents.
"""

import argparse
import sys
import subprocess
import os
from pathlib import Path

def run_queen(args):
    """Run Queen orchestrator"""
    queen_runner = Path(__file__).parent / "queen" / "runner.py"
    cmd = [
        sys.executable, str(queen_runner),
        "--session", args.session,
        "--task", args.task,
        "--model", args.model or "openai:gpt-4o-mini"
    ]
    
    if args.monitor:
        cmd.append("--monitor")
    if args.monitor_interval:
        cmd.extend(["--monitor-interval", str(args.monitor_interval)])
        
    return subprocess.run(cmd)

def run_scribe(args):
    """Run Scribe agent"""
    scribe_runner = Path(__file__).parent / "scribe" / "runner.py"
    cmd = [
        sys.executable, str(scribe_runner),
        args.mode,
        "--model", args.model or "openai:gpt-4o-mini"
    ]
    
    if args.session:
        cmd.extend(["--session", args.session])
    if args.task:
        cmd.extend(["--task", args.task])
        
    return subprocess.run(cmd)

def run_worker(worker_name: str, args):
    """Run a specific worker agent"""
    worker_runner = Path(__file__).parent / worker_name / "runner.py"
    cmd = [
        sys.executable, str(worker_runner),
        "--session", args.session,
        "--task", args.task,
        "--model", args.model or "openai:gpt-4o-mini"
    ]
    
    return subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(
        description="Pydantic AI Agents CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create new session
  python cli.py scribe create --task "Analyze crypto-data security"
  
  # Run Queen orchestrator with monitoring
  python cli.py queen --session 2024-01-15-14-30-crypto-security-audit --task "..." --monitor
  
  # Run synthesis
  python cli.py scribe synthesis --session 2024-01-15-14-30-crypto-security-audit
  
  # Run individual workers
  python cli.py analyzer --session SESSION_ID --task "Security analysis"
  python cli.py backend --session SESSION_ID --task "API implementation"
  python cli.py frontend --session SESSION_ID --task "UI component development"
        """
    )
    
    subparsers = parser.add_subparsers(dest='agent', help='Agent to run')
    
    # Queen orchestrator
    queen_parser = subparsers.add_parser('queen', help='Queen orchestrator')
    queen_parser.add_argument('--session', required=True, help='Session ID')
    queen_parser.add_argument('--task', required=True, help='Task description')
    queen_parser.add_argument('--model', help='AI model to use')
    queen_parser.add_argument('--monitor', action='store_true', help='Enable continuous monitoring')
    queen_parser.add_argument('--monitor-interval', type=int, default=30, help='Monitoring interval in seconds')
    
    # Scribe agent  
    scribe_parser = subparsers.add_parser('scribe', help='Scribe agent')
    scribe_parser.add_argument('mode', choices=['create', 'synthesis'], help='Scribe mode')
    scribe_parser.add_argument('--session', help='Session ID (required for synthesis)')
    scribe_parser.add_argument('--task', help='Task description (required for create)')
    scribe_parser.add_argument('--model', help='AI model to use')
    
    # Worker agents - all follow same pattern
    workers = [
        ('analyzer', 'Security analysis, performance optimization, and code quality assessment'),
        ('architect', 'System design, scalability patterns, and technical architecture'),
        ('backend', 'API development, database design, and service implementation'),
        ('designer', 'User experience design, visual design, and accessibility'),
        ('devops', 'Infrastructure, deployment, monitoring, and CI/CD pipelines'),
        ('frontend', 'UI/UX implementation, component architecture, and state management'),
        ('researcher', 'Technical research, best practices, and industry standards analysis'),
        ('test', 'Testing strategy, quality assurance, and test coverage analysis')
    ]
    
    for worker_name, worker_description in workers:
        worker_parser = subparsers.add_parser(worker_name, help=worker_description)
        worker_parser.add_argument('--session', required=True, help='Session ID')
        worker_parser.add_argument('--task', required=True, help='Task description')
        worker_parser.add_argument('--model', help='AI model to use')
    
    args = parser.parse_args()
    
    if not args.agent:
        parser.print_help()
        return 1
    
    # Route to appropriate agent
    if args.agent == 'queen':
        return run_queen(args).returncode
    elif args.agent == 'scribe':
        return run_scribe(args).returncode
    elif args.agent in ['analyzer', 'architect', 'backend', 'designer', 'devops', 'frontend', 'researcher', 'test']:
        return run_worker(args.agent, args).returncode
    else:
        print(f"Unknown agent: {args.agent}")
        return 1

if __name__ == "__main__":
    sys.exit(main())