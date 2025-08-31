"""
Queen Orchestrator Agent
========================
Lightweight Pydantic AI agent for efficient task orchestration.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any

# Environment setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
# Add the pydantic_ai directory to path for direct imports
pydantic_ai_path = Path(__file__).parent.parent
sys.path.insert(0, str(pydantic_ai_path))

from shared.protocols import load_project_env

load_project_env()

from pydantic_ai import Agent, RunContext

from .models import QueenOrchestrationPlan


# Lightweight Queen orchestrator agent - keyword-based assignment
queen_agent = Agent(
    model="openai:gpt-4o",
    output_type=QueenOrchestrationPlan,
    system_prompt="""You are the Queen Orchestrator - a lean, efficient task coordinator that assigns workers based on task keywords.

IMPORTANT: Return a valid QueenOrchestrationPlan JSON structure. All fields are required.

## Available Workers
- **analyzer-worker**: Security, performance, code quality assessment  
- **architect-worker**: System design, technical architecture, scalability
- **backend-worker**: API development, service implementation, database design
- **frontend-worker**: UI/UX implementation, component architecture
- **designer-worker**: Visual design, user experience, accessibility
- **devops-worker**: Infrastructure, deployment, monitoring, CI/CD
- **researcher-worker**: Technical research, best practices, standards
- **test-worker**: Testing strategy, quality assurance, coverage

## Assignment Rules by Task Keywords
- **"security"/"vulnerability"** → analyzer-worker + architect-worker (+ backend-worker if Level 4)
- **"performance"/"optimization"** → analyzer-worker + backend-worker (+ architect-worker if Level 4)  
- **"architecture"/"design"** → architect-worker + backend-worker (+ analyzer-worker if Level 4)
- **"comprehensive"/"detailed"** → 4-5 workers for full coverage

## Complexity Levels (based on task keywords)
- **Level 1**: Single focus (1-2 workers) - "fix", "simple", specific issue
- **Level 2**: Moderate scope (2-3 workers) - "analyze", "review", "assess"
- **Level 3**: Complex task (3-4 workers) - "improve", "optimize", multiple areas
- **Level 4**: Comprehensive (4-5 workers) - "comprehensive", "detailed", "architecture", "security", "performance", "scalability" together

## Response Requirements
- complexity_assessment: Integer 1-4 based on keyword analysis
- worker_assignments: Follow complexity rules (Level 4 = 4-5 workers)
- execution_strategy: "parallel" for most tasks
- estimated_total_duration: Based on complexity and worker count

## Worker Assignment Strategy
1. Use analyze_task_keywords() to understand task complexity
2. Use suggest_workers() to get worker recommendations  
3. Create comprehensive WorkerAssignment objects in the orchestration plan

The Queen creates the orchestration plan with worker assignments. The runner will handle spawning the actual Pydantic AI agents.

Analyze task keywords, determine complexity level, assign appropriate number of workers. DO NOT perform deep code exploration.""",
)


@queen_agent.tool
async def analyze_task_keywords(ctx: RunContext[None], task_description: str) -> Dict[str, Any]:
    """Simple keyword-based task analysis"""
    
    task_lower = task_description.lower()
    
    # Complexity indicators
    high_complexity_keywords = [
        "comprehensive", "architecture", "security", "performance", "scalability",
        "detailed", "full", "complete", "thorough"
    ]
    
    medium_complexity_keywords = [
        "analyze", "review", "audit", "assess", "evaluate", "improve"
    ]
    
    # Count matches
    high_matches = sum(1 for keyword in high_complexity_keywords if keyword in task_lower)
    medium_matches = sum(1 for keyword in medium_complexity_keywords if keyword in task_lower)
    
    # Determine complexity
    if high_matches >= 3 or ("comprehensive" in task_lower and any(word in task_lower for word in ["architecture", "security", "performance"])):
        complexity = 4
    elif high_matches >= 2:
        complexity = 3  
    elif high_matches >= 1 or medium_matches >= 2:
        complexity = 2
    else:
        complexity = 1
    
    # Extract service hints
    service_hints = []
    if "crypto-data" in task_lower or "market" in task_lower:
        service_hints.append("crypto-data")
    if "api" in task_lower or "backend" in task_lower:
        service_hints.append("api")
    if "frontend" in task_lower or "ui" in task_lower:
        service_hints.append("frontend")
    
    return {
        "complexity": complexity,
        "high_complexity_matches": high_matches,
        "medium_complexity_matches": medium_matches,
        "service_hints": service_hints,
        "task_keywords": [word for word in ["security", "performance", "architecture", "comprehensive"] if word in task_lower]
    }


@queen_agent.tool 
async def suggest_workers(ctx: RunContext[None], task_description: str, complexity: int) -> Dict[str, Any]:
    """Suggest optimal workers based on task analysis"""
    
    task_lower = task_description.lower()
    suggested_workers = []
    
    # Core workers based on keywords
    if any(word in task_lower for word in ["security", "vulnerability", "performance", "quality"]):
        suggested_workers.append({
            "type": "analyzer-worker",
            "rationale": "Security and performance analysis required",
            "priority": "high"
        })
    
    if any(word in task_lower for word in ["architecture", "design", "scalability", "patterns"]):
        suggested_workers.append({
            "type": "architect-worker", 
            "rationale": "System architecture and design analysis needed",
            "priority": "high"
        })
    
    if any(word in task_lower for word in ["api", "database", "backend", "service", "endpoint"]):
        suggested_workers.append({
            "type": "backend-worker",
            "rationale": "Backend system analysis required", 
            "priority": "medium"
        })
    
    if any(word in task_lower for word in ["test", "testing", "quality", "coverage"]):
        suggested_workers.append({
            "type": "test-worker",
            "rationale": "Testing and quality analysis needed",
            "priority": "low"
        })
    
    if any(word in task_lower for word in ["research", "best", "practices", "standards"]):
        suggested_workers.append({
            "type": "researcher-worker",
            "rationale": "Research and best practices analysis required",
            "priority": "low"
        })
    
    # Ensure we have appropriate number based on complexity
    if complexity == 4 and len(suggested_workers) < 4:
        # Add missing workers for comprehensive tasks
        if not any(w["type"] == "analyzer-worker" for w in suggested_workers):
            suggested_workers.append({
                "type": "analyzer-worker",
                "rationale": "Comprehensive analysis requires security and performance review",
                "priority": "high"
            })
        if not any(w["type"] == "architect-worker" for w in suggested_workers):
            suggested_workers.append({
                "type": "architect-worker",
                "rationale": "Architecture analysis essential for comprehensive review",
                "priority": "high"
            })
        if not any(w["type"] == "backend-worker" for w in suggested_workers):
            suggested_workers.append({
                "type": "backend-worker",
                "rationale": "Backend implementation analysis needed",
                "priority": "medium"
            })
        if len(suggested_workers) < 4:
            suggested_workers.append({
                "type": "researcher-worker",
                "rationale": "Best practices research for comprehensive analysis",
                "priority": "medium"
            })
    
    # Ensure proper count based on complexity
    if complexity == 4:
        target_workers = min(5, max(4, len(suggested_workers)))
    elif complexity == 3:
        target_workers = min(4, max(3, len(suggested_workers)))
    elif complexity == 2:
        target_workers = min(3, max(2, len(suggested_workers)))
    else:
        target_workers = min(2, max(1, len(suggested_workers)))
    
    suggested_workers = suggested_workers[:target_workers]
    
    return {
        "suggested_workers": suggested_workers,
        "target_workers": target_workers,
        "task_keywords_found": [word for word in ["security", "performance", "architecture", "api", "comprehensive"] if word in task_lower]
    }


