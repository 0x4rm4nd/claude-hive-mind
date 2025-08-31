"""
Queen Orchestrator Agent
========================
Pydantic AI agent for intelligent task orchestration.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any

# Environment setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
from ..shared.protocols import load_project_env
load_project_env()

from pydantic_ai import Agent, RunContext

from .models import QueenOrchestrationPlan
from .tools import QueenTools


# Queen orchestrator agent with creative assessment capabilities
queen_agent = Agent(
    model="openai:gpt-5",
    output_type=QueenOrchestrationPlan,
    system_prompt="""You are the Queen Orchestrator, an elite task coordinator specializing in complex multi-agent workflow orchestration.

IMPORTANT: You must return a valid QueenOrchestrationPlan JSON structure. All fields are required unless marked optional.

## Core Responsibilities
1. **Strategic Analysis**: Deep analysis of complex tasks to understand requirements, scope, and challenges
2. **Worker Selection**: Intelligent matching of task requirements to optimal worker expertise profiles  
3. **Risk Assessment**: Identify potential blockers, dependencies, and mitigation strategies
4. **Quality Orchestration**: Design execution strategies with proper coordination and quality gates

## Available Workers (choose 2-5 appropriate ones for the task)
- **analyzer-worker**: Security, performance, code quality assessment, vulnerability analysis
- **architect-worker**: System design, technical architecture, scalability patterns, design principles  
- **backend-worker**: API development, service implementation, database design, business logic
- **frontend-worker**: UI/UX implementation, component architecture, state management, user experience
- **designer-worker**: Visual design, user experience, accessibility, design systems
- **devops-worker**: Infrastructure, deployment, monitoring, CI/CD pipelines, containerization
- **researcher-worker**: Technical research, best practices, industry standards, technology evaluation
- **test-worker**: Testing strategy, quality assurance, test coverage, automated testing

## Response Requirements
- complexity_assessment: Must be integer 1-4 based on task scope
- worker_assignments: List of 2-5 workers with specific task_focus for each
- execution_strategy: Must be "parallel", "sequential", or "hybrid"
- All list fields can be empty [] but must exist as arrays
- estimated_total_duration: Format like "2-4h" or "30min-1h"

Be strategic, thorough, and precise in your orchestration planning.""",
)


# Tool functions for the AI agent
@queen_agent.tool
async def explore_codebase(ctx: RunContext[None]) -> Dict[str, Any]:
    """Explore the overall project structure to understand the codebase"""
    return QueenTools.analyze_project_structure()


@queen_agent.tool
async def explore_service(
    ctx: RunContext[None], service_name: str
) -> Dict[str, Any]:
    """Explore a specific service's structure and key files"""
    # Detect project root and explore specific service
    current_path = Path.cwd()
    for path in [current_path] + list(current_path.parents):
        if (path / "api").exists() and (path / "frontend").exists():
            service_path = path / service_name
            if service_path.exists():
                structure = QueenTools.explore_service_structure(str(service_path))
                key_files = QueenTools.find_key_files(str(service_path))
                return {
                    "structure": structure,
                    "key_files": key_files,
                    "service_path": str(service_path),
                }
    return {"error": f"Service {service_name} not found"}


@queen_agent.tool
async def search_security_patterns(
    ctx: RunContext[None], service_name: str
) -> Dict[str, Any]:
    """Search for security-related patterns in a service"""
    current_path = Path.cwd()
    for path in [current_path] + list(current_path.parents):
        if (path / "api").exists():
            service_path = path / service_name
            if service_path.exists():
                patterns = [
                    "auth",
                    "password",
                    "token",
                    "jwt",
                    "encrypt",
                    "decrypt",
                    "hash",
                    "security",
                ]
                return QueenTools.search_for_patterns(str(service_path), patterns)
    return {"error": f"Could not search {service_name}"}


@queen_agent.tool
async def search_performance_patterns(
    ctx: RunContext[None], service_name: str
) -> Dict[str, Any]:
    """Search for performance-related patterns in a service"""
    current_path = Path.cwd()
    for path in [current_path] + list(current_path.parents):
        if (path / "api").exists():
            service_path = path / service_name
            if service_path.exists():
                patterns = [
                    "cache",
                    "redis",
                    "database",
                    "query",
                    "async",
                    "await",
                    "performance",
                    "optimization",
                ]
                return QueenTools.search_for_patterns(str(service_path), patterns)
    return {"error": f"Could not search {service_name}"}
