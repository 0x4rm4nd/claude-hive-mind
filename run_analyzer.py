#!/usr/bin/env python3
"""
Temporary analyzer runner script to bypass import issues.
"""

import sys
import os
import argparse

# Add the correct path for imports
pydantic_ai_path = os.path.join(os.path.dirname(__file__), "agents", "pydantic_ai")
sys.path.insert(0, pydantic_ai_path)

# Now import with absolute imports
from shared.protocols import (
    SessionManagement,
    LoggingProtocol,
    ProtocolConfig,
    WorkerPromptProtocol,
    load_project_env,
)

# Load project environment
load_project_env()

from analyzer.models import AnalyzerOutput
from analyzer.agent import analyzer_agent
from shared.tools import iso_now

def main():
    parser = argparse.ArgumentParser(description="Security Analyzer Worker")
    parser.add_argument("--session", required=True, help="Session ID")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--model", default="openai:gpt-4", help="AI model to use")
    
    args = parser.parse_args()
    
    # Initialize logging protocol
    log_event = LoggingProtocol.log_event
    log_debug = LoggingProtocol.log_debug
    worker = "analyzer-worker"
    
    # Log startup
    log_event(
        args.session,
        "worker_spawned",
        worker,
        {
            "task": args.task,
            "model": args.model,
            "timestamp": iso_now(),
            "capabilities": [
                "security_analysis",
                "performance_optimization", 
                "code_quality_assessment",
                "dependency_analysis",
                "static_analysis"
            ]
        }
    )
    
    log_event(
        args.session,
        "analysis_started",
        worker,
        {
            "task": args.task,
            "analysis_type": "security_performance_quality",
            "timestamp": iso_now()
        }
    )
    
    # Get task-specific prompt
    try:
        task_prompt = WorkerPromptProtocol.get_prompt(args.session, "analyzer-worker")
        if task_prompt:
            log_debug(args.session, "Using session-specific task prompt", {"prompt_source": "session_prompt_file"})
        else:
            task_prompt = args.task
            log_debug(args.session, "Using fallback task description", {"task": args.task})
    except Exception as e:
        task_prompt = args.task
        log_debug(args.session, "Task prompt extraction failed, using fallback", {"error": str(e), "fallback": args.task})
    
    try:
        # Run the analyzer
        log_debug(args.session, "Starting analyzer agent execution", {"task": task_prompt, "model": args.model})
        
        result = analyzer_agent.run(
            task_prompt,
            model=args.model
        )
        
        log_debug(args.session, "Analyzer agent completed successfully", {"result_type": str(type(result))})
        
        # Save analysis results
        session_path = SessionManagement.get_session_path(args.session)
        workers_dir = os.path.join(session_path, "workers", "notes")
        os.makedirs(workers_dir, exist_ok=True)
        
        analysis_file = os.path.join(workers_dir, "analyzer_analysis.md")
        
        if hasattr(result, 'analysis_report'):
            with open(analysis_file, "w") as f:
                f.write(result.analysis_report)
        else:
            with open(analysis_file, "w") as f:
                f.write(str(result))
        
        log_event(
            args.session,
            "analysis_completed",
            worker,
            {
                "analysis_file": analysis_file,
                "timestamp": iso_now(),
                "status": "completed"
            }
        )
        
        print(f"Analysis completed successfully. Results saved to: {analysis_file}")
        
    except Exception as e:
        log_event(
            args.session,
            "analysis_failed",
            worker,
            {
                "error": str(e),
                "timestamp": iso_now(),
                "status": "failed"
            }
        )
        print(f"Analysis failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()