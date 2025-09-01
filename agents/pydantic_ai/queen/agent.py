"""
Queen Orchestrator Agent
========================
Pydantic AI agent for intelligent multi-worker coordination and task orchestration.
"""

from typing import Dict, Any

from shared.base_agent import BaseAgentConfig
from .models import QueenOutput

from pydantic_ai import RunContext


class QueenAgentConfig(BaseAgentConfig):
    """Configuration for Queen Orchestrator Agent"""

    @classmethod
    def get_worker_type(cls) -> str:
        return "queen-orchestrator"

    @classmethod
    def get_output_model(cls):
        return QueenOutput

    @classmethod
    def get_system_prompt(cls) -> str:
        return """You are the Queen Orchestrator - an intelligent strategic coordinator with full autonomy to make optimal worker assignments.

IMPORTANT: Return a valid QueenOutput JSON structure. All fields are required.

## Your Role & Authority
You have COMPLETE DECISION-MAKING AUTONOMY. You are not bound by rigid rules or worker count limits. Make strategic decisions based on:
- Task complexity and scope
- Risk assessment and implications  
- Resource optimization needs
- Strategic value and business impact
- Your professional judgment as an expert coordinator

## Available Workers (Choose Any Combination)
- **analyzer-worker**: Security, performance, code quality assessment  
- **architect-worker**: System design, technical architecture, scalability
- **backend-worker**: API development, service implementation, database design
- **frontend-worker**: UI/UX implementation, component architecture
- **designer-worker**: Visual design, user experience, accessibility
- **devops-worker**: Infrastructure, deployment, monitoring, CI/CD
- **researcher-worker**: Technical research, best practices, standards
- **test-worker**: Testing strategy, quality assurance, coverage

## Strategic Decision Framework
**Assess the task holistically and decide:**
1. **What expertise domains are truly needed?** (not just keywords)
2. **What are the risks if we miss something?** (security, performance, UX)
3. **Where could coordination issues arise?** (between services, teams, systems)
4. **What's the business impact of getting this wrong?** (user experience, system stability)
5. **How much analysis vs implementation is needed?** (research-heavy vs execution-heavy)

## Examples of Your Autonomy
- **Simple bug fix in API**: Maybe just backend-worker (1 worker)
- **New feature touching UI/API/DB**: Maybe backend-worker + frontend-worker + test-worker (3 workers)
- **Security audit**: Maybe analyzer-worker + architect-worker + devops-worker (3 workers)  
- **Complete system redesign**: Maybe ALL workers if the impact is massive (8 workers)
- **Research task**: Maybe just researcher-worker (1 worker)

## Your Strategic Tools
1. Use assess_task_strategically() to understand implications beyond keywords
2. Use evaluate_worker_needs() to determine optimal expertise mix
3. Apply your intelligence to create the best orchestration plan

## Response Requirements
- orchestration_plan: Complete QueenOrchestrationPlan with all strategic details
- workers_spawned: List of worker types that will be spawned
- coordination_status: Overall coordination status (planned, active, completed, failed)
- monitoring_active: Whether monitoring mode is requested
- session_path: Session directory path for coordination files

You are the strategic mastermind. Make the best decisions for success."""

    @classmethod
    def get_default_model(cls) -> str:
        return "openai:o3-mini"  # Override default model


# Create agent using class methods
queen_agent = QueenAgentConfig.create_agent()


@queen_agent.tool
async def assess_task_strategically(
    ctx: RunContext[None], task_description: str
) -> Dict[str, Any]:
    """Strategic multi-dimensional task assessment beyond simple keywords"""

    task_lower = task_description.lower()

    # Multi-dimensional risk assessment
    security_implications = any(
        word in task_lower
        for word in [
            "auth",
            "security",
            "vulnerability",
            "encrypt",
            "token",
            "permission",
            "access",
            "login",
            "user",
        ]
    )

    performance_implications = any(
        word in task_lower
        for word in [
            "performance",
            "speed",
            "optimize",
            "scale",
            "load",
            "cache",
            "database",
            "query",
            "latency",
        ]
    )

    architectural_implications = any(
        word in task_lower
        for word in [
            "architecture",
            "design",
            "pattern",
            "structure",
            "refactor",
            "migrate",
            "integration",
            "service",
        ]
    )

    user_experience_implications = any(
        word in task_lower
        for word in [
            "ui",
            "ux",
            "frontend",
            "interface",
            "user",
            "design",
            "accessibility",
            "responsive",
            "mobile",
        ]
    )

    infrastructure_implications = any(
        word in task_lower
        for word in [
            "deploy",
            "devops",
            "infrastructure",
            "docker",
            "ci",
            "cd",
            "monitoring",
            "logging",
            "environment",
        ]
    )

    data_implications = any(
        word in task_lower
        for word in [
            "database",
            "data",
            "migration",
            "schema",
            "model",
            "sql",
            "api",
            "endpoint",
            "crud",
        ]
    )

    testing_implications = any(
        word in task_lower
        for word in [
            "test",
            "testing",
            "quality",
            "bug",
            "coverage",
            "integration",
            "unit",
            "e2e",
            "validation",
        ]
    )

    research_implications = any(
        word in task_lower
        for word in [
            "research",
            "best",
            "practice",
            "standard",
            "pattern",
            "library",
            "framework",
            "documentation",
        ]
    )

    # Business impact assessment
    business_critical = any(
        word in task_lower
        for word in [
            "critical",
            "production",
            "urgent",
            "blocking",
            "outage",
            "down",
            "broken",
            "failing",
        ]
    )

    scope_indicators = {
        "isolated_change": any(
            word in task_lower for word in ["fix", "bug", "small", "simple", "specific"]
        ),
        "feature_addition": any(
            word in task_lower
            for word in ["add", "new", "feature", "implement", "create"]
        ),
        "system_improvement": any(
            word in task_lower for word in ["improve", "optimize", "enhance", "upgrade"]
        ),
        "major_overhaul": any(
            word in task_lower
            for word in ["comprehensive", "complete", "overhaul", "redesign", "rewrite"]
        ),
    }

    # Service scope analysis
    service_scope = []
    if any(
        word in task_lower for word in ["crypto-data", "market", "price", "trading"]
    ):
        service_scope.append("crypto-data")
    if any(
        word in task_lower
        for word in ["api", "backend", "server", "endpoint", "service"]
    ):
        service_scope.append("api")
    if any(
        word in task_lower for word in ["frontend", "ui", "interface", "client", "web"]
    ):
        service_scope.append("frontend")
    if any(word in task_lower for word in ["sara", "ai", "intelligence", "context"]):
        service_scope.append("sara")
    if any(word in task_lower for word in ["archon", "knowledge", "documentation"]):
        service_scope.append("archon")

    return {
        "risk_factors": {
            "security": security_implications,
            "performance": performance_implications,
            "architecture": architectural_implications,
            "user_experience": user_experience_implications,
            "infrastructure": infrastructure_implications,
            "data": data_implications,
            "testing": testing_implications,
            "research": research_implications,
        },
        "business_impact": {
            "critical": business_critical,
            "scope_assessment": scope_indicators,
        },
        "service_scope": service_scope,
        "complexity_indicators": {
            "cross_service": len(service_scope) > 1,
            "multiple_domains": sum(
                [
                    security_implications,
                    performance_implications,
                    architectural_implications,
                    user_experience_implications,
                ]
            )
            > 2,
            "high_risk": security_implications and performance_implications,
            "research_heavy": research_implications
            or any(word in task_lower for word in ["best", "standard", "pattern"]),
        },
    }


@queen_agent.tool
async def evaluate_worker_needs(
    ctx: RunContext[None], task_assessment: Dict[str, Any]
) -> Dict[str, Any]:
    """Intelligent evaluation of worker needs based on strategic assessment"""

    risk_factors = task_assessment.get("risk_factors", {})
    business_impact = task_assessment.get("business_impact", {})
    service_scope = task_assessment.get("service_scope", [])
    complexity_indicators = task_assessment.get("complexity_indicators", {})

    # Strategic worker recommendations (not rigid rules)
    worker_recommendations = []

    # Security/Performance critical expertise
    if risk_factors.get("security") or risk_factors.get("performance"):
        worker_recommendations.append(
            {
                "worker_type": "analyzer-worker",
                "strategic_value": "high",
                "reasoning": "Security or performance implications require expert analysis to prevent critical issues",
            }
        )

    # Architectural/Design expertise
    if (
        risk_factors.get("architecture")
        or complexity_indicators.get("cross_service")
        or complexity_indicators.get("multiple_domains")
    ):
        worker_recommendations.append(
            {
                "worker_type": "architect-worker",
                "strategic_value": "high",
                "reasoning": "Complex architectural implications or cross-service coordination requires system design expertise",
            }
        )

    # Backend implementation expertise
    if (
        risk_factors.get("data")
        or "api" in service_scope
        or any(scope in ["crypto-data", "sara"] for scope in service_scope)
    ):
        worker_recommendations.append(
            {
                "worker_type": "backend-worker",
                "strategic_value": "medium",
                "reasoning": "Data/API changes or backend service involvement requires implementation expertise",
            }
        )

    # Frontend/UX expertise
    if risk_factors.get("user_experience") or "frontend" in service_scope:
        worker_recommendations.append(
            {
                "worker_type": "frontend-worker",
                "strategic_value": "medium",
                "reasoning": "UI/UX implications require frontend implementation expertise",
            }
        )

        # Visual design may also be needed for UX-heavy tasks
        if any(
            word in str(task_assessment).lower()
            for word in ["design", "interface", "user", "accessibility"]
        ):
            worker_recommendations.append(
                {
                    "worker_type": "designer-worker",
                    "strategic_value": "low",
                    "reasoning": "Visual design and accessibility considerations for optimal user experience",
                }
            )

    # Infrastructure expertise
    if risk_factors.get("infrastructure") or business_impact.get("critical"):
        worker_recommendations.append(
            {
                "worker_type": "devops-worker",
                "strategic_value": "medium",
                "reasoning": "Infrastructure implications or business-critical deployment requires DevOps expertise",
            }
        )

    # Research expertise
    if complexity_indicators.get("research_heavy") or risk_factors.get("research"):
        worker_recommendations.append(
            {
                "worker_type": "researcher-worker",
                "strategic_value": "medium",
                "reasoning": "Research-heavy task requires investigation of best practices and standards",
            }
        )

    # Testing expertise
    if (
        risk_factors.get("testing")
        or business_impact.get("critical")
        or len(service_scope) > 1
    ):
        worker_recommendations.append(
            {
                "worker_type": "test-worker",
                "strategic_value": "low",
                "reasoning": "Quality assurance needed for business-critical or cross-service changes",
            }
        )

    # Strategic insights for Queen decision-making
    strategic_insights = {
        "coordination_complexity": (
            "high"
            if len(service_scope) > 2
            else "medium" if len(service_scope) > 1 else "low"
        ),
        "risk_mitigation_priority": (
            "critical"
            if (risk_factors.get("security") and risk_factors.get("performance"))
            else "high" if business_impact.get("critical") else "medium"
        ),
        "resource_optimization_opportunity": (
            "high"
            if len(worker_recommendations) > 5
            else "medium" if len(worker_recommendations) > 3 else "low"
        ),
    }

    return {
        "worker_recommendations": worker_recommendations,
        "strategic_insights": strategic_insights,
        "coordination_notes": [
            (
                f"Task spans {len(service_scope)} services: {', '.join(service_scope)}"
                if service_scope
                else "Single service task"
            ),
            (
                f"Risk factors identified: {', '.join([k for k, v in risk_factors.items() if v])}"
                if any(risk_factors.values())
                else "Low risk task"
            ),
            (
                "Business critical - prioritize thoroughness"
                if business_impact.get("critical")
                else "Standard priority task"
            ),
        ],
    }
