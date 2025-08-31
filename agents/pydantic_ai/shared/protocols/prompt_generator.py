#!/usr/bin/env python3
"""
Worker Prompt Generation Protocol
=================================
Framework-enforced prompt file creation for workers.
"""
import os
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
from .session_management import SessionManagement
from .logging_protocol import LoggingProtocol, ProtocolConfig


@dataclass
class WorkerPromptSpec:
    """Specification for generating worker-specific prompts"""

    worker_type: str
    task_focus: str
    priority: str
    estimated_duration: str
    rationale: str
    complexity_level: int
    session_id: str
    target_service: str = "unknown"
    dependencies: List[str] = None
    focus_areas: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.focus_areas is None:
            self.focus_areas = []


class PromptGenerator:
    """Framework-enforced worker prompt file creation"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.config = ProtocolConfig(
            {"session_id": session_id, "agent_name": "queen-orchestrator"}
        )
        self.logger = LoggingProtocol(self.config)

    def create_worker_prompts(
        self, worker_specs: List[WorkerPromptSpec], batch_logging: bool = True
    ) -> Dict[str, str]:
        """
        Create prompt files for all assigned workers.
        Framework-enforced: Cannot be skipped, must create valid files.
        """
        session_path = SessionManagement.get_session_path(self.session_id)
        prompts_dir = f"{session_path}/workers/prompts"

        # Ensure prompts directory exists (framework-enforced)
        os.makedirs(prompts_dir, exist_ok=True)

        created_files = {}
        failed_prompts = []

        for spec in worker_specs:
            try:
                prompt_content = self._generate_prompt_content(spec)
                prompt_file = f"{prompts_dir}/{spec.worker_type}.prompt"

                # Write prompt file (framework-enforced output)
                with open(prompt_file, "w") as f:
                    f.write(prompt_content)

                created_files[spec.worker_type] = prompt_file

                # Individual logging (only if batch_logging is disabled)
                if not batch_logging:
                    self.logger.log_event(
                        "worker_prompt_created",
                        {
                            "worker_type": spec.worker_type,
                            "prompt_file": prompt_file,
                            "task_focus": spec.task_focus,
                            "complexity": spec.complexity_level,
                        },
                    )

            except Exception as e:
                failed_prompts.append({
                    "worker_type": spec.worker_type,
                    "error": str(e),
                    "exception_type": str(type(e))
                })

                # Log error (framework-enforced error handling)
                self.logger.log_event(
                    "worker_prompt_creation_failed",
                    {
                        "worker_type": spec.worker_type,
                        "error": str(e),
                        "exception_type": str(type(e)),
                    },
                )
                raise

        # Consolidated batch logging (default behavior)
        if batch_logging and created_files:
            # Convert absolute path to relative path from project root
            project_root = "/Users/Armand/Development/SmartWalletFX"
            relative_prompts_dir = prompts_dir.replace(f"{project_root}/", "") if prompts_dir.startswith(project_root) else prompts_dir
            
            self.logger.log_event(
                "worker_prompts_created",
                {
                    "worker_types": list(created_files.keys()),
                    "total_prompts": len(created_files),
                    "prompt_folder": relative_prompts_dir,
                    "complexity_level": worker_specs[0].complexity_level if worker_specs else 1,
                },
            )

        return created_files

    def _generate_prompt_content(self, spec: WorkerPromptSpec) -> str:
        """Generate structured prompt content for a specific worker"""

        # Worker-specific configurations
        worker_configs = {
            "analyzer-worker": {
                "expertise": "Security analysis, performance optimization, code quality assessment",
                "tools": [
                    "security scanners",
                    "performance profilers",
                    "code analyzers",
                ],
                "outputs": [
                    "security_analysis.md",
                    "performance_assessment.md",
                    "quality_report.md",
                ],
                "focus_areas": [
                    "vulnerabilities",
                    "performance bottlenecks",
                    "code smells",
                    "security patterns",
                ],
            },
            "architect-worker": {
                "expertise": "System design, scalability patterns, technical architecture",
                "tools": [
                    "architecture analyzers",
                    "pattern matchers",
                    "dependency mappers",
                ],
                "outputs": [
                    "architecture_analysis.md",
                    "scalability_recommendations.md",
                    "design_patterns.md",
                ],
                "focus_areas": [
                    "system design",
                    "scalability",
                    "maintainability",
                    "technical debt",
                ],
            },
            "backend-worker": {
                "expertise": "API development, database design, service implementation",
                "tools": ["API analyzers", "database schema tools", "service mappers"],
                "outputs": [
                    "backend_analysis.md",
                    "api_recommendations.md",
                    "database_assessment.md",
                ],
                "focus_areas": [
                    "API design",
                    "data models",
                    "business logic",
                    "integration patterns",
                ],
            },
            "frontend-worker": {
                "expertise": "UI/UX implementation, component architecture, state management",
                "tools": [
                    "component analyzers",
                    "bundle analyzers",
                    "accessibility checkers",
                ],
                "outputs": [
                    "frontend_analysis.md",
                    "component_recommendations.md",
                    "ux_assessment.md",
                ],
                "focus_areas": [
                    "component structure",
                    "state management",
                    "user experience",
                    "performance",
                ],
            },
            "designer-worker": {
                "expertise": "User experience design, visual design, accessibility",
                "tools": [
                    "design analyzers",
                    "accessibility checkers",
                    "usability evaluators",
                ],
                "outputs": [
                    "design_analysis.md",
                    "accessibility_report.md",
                    "ux_recommendations.md",
                ],
                "focus_areas": [
                    "user experience",
                    "accessibility",
                    "visual design",
                    "usability",
                ],
            },
            "devops-worker": {
                "expertise": "Infrastructure, deployment, monitoring, CI/CD pipelines",
                "tools": [
                    "infrastructure scanners",
                    "deployment analyzers",
                    "monitoring tools",
                ],
                "outputs": [
                    "infrastructure_analysis.md",
                    "deployment_recommendations.md",
                    "monitoring_assessment.md",
                ],
                "focus_areas": [
                    "infrastructure",
                    "deployment",
                    "monitoring",
                    "automation",
                ],
            },
            "researcher-worker": {
                "expertise": "Technical research, best practices, industry standards",
                "tools": [
                    "research databases",
                    "pattern libraries",
                    "standards analyzers",
                ],
                "outputs": [
                    "research_findings.md",
                    "best_practices.md",
                    "standards_compliance.md",
                ],
                "focus_areas": [
                    "best practices",
                    "industry standards",
                    "emerging patterns",
                    "technology trends",
                ],
            },
            "test-worker": {
                "expertise": "Testing strategy, quality assurance, test coverage",
                "tools": ["test analyzers", "coverage tools", "quality metrics"],
                "outputs": [
                    "testing_analysis.md",
                    "coverage_report.md",
                    "quality_recommendations.md",
                ],
                "focus_areas": [
                    "test coverage",
                    "quality metrics",
                    "testing strategy",
                    "automated testing",
                ],
            },
        }

        config = worker_configs.get(
            spec.worker_type,
            {
                "expertise": "General analysis and assessment",
                "tools": ["code analyzers", "pattern matchers"],
                "outputs": ["analysis.md", "recommendations.md"],
                "focus_areas": ["code quality", "best practices"],
            },
        )

        return f"""---
worker_type: {spec.worker_type}
session_id: {spec.session_id}
task_focus: {spec.task_focus}
priority: {spec.priority}
estimated_duration: {spec.estimated_duration}
complexity_level: {spec.complexity_level}
target_service: {spec.target_service}
dependencies: {spec.dependencies}
focus_areas: {spec.focus_areas or config['focus_areas']}
created_by: queen-orchestrator
---

# {spec.worker_type.replace('-', ' ').title()} Task Instructions

## Primary Task
{spec.task_focus}

## Worker Expertise
{config['expertise']}

## Rationale
{spec.rationale}

## Success Criteria
- Complete analysis of assigned focus areas
- Generate comprehensive findings with evidence
- Provide actionable recommendations
- Document potential risks and mitigation strategies
- Create required output files

## Output Requirements
### Required Files
{chr(10).join(f"- `workers/notes/{output}`" for output in config['outputs'])}

### JSON Response Format
```json
{{
    "worker_type": "{spec.worker_type}",
    "status": "completed",
    "task_focus": "{spec.task_focus}",
    "findings": [
        {{
            "category": "string",
            "severity": "high|medium|low",
            "description": "string", 
            "evidence": "string",
            "recommendation": "string"
        }}
    ],
    "analysis_summary": "string",
    "key_recommendations": ["string"],
    "potential_blockers": ["string"],
    "next_steps": ["string"]
}}
```

## Available Tools
{chr(10).join(f"- {tool}" for tool in config['tools'])}

## Focus Areas (Priority Order)
{chr(10).join(f"{i+1}. {area}" for i, area in enumerate(spec.focus_areas or config['focus_areas']))}

## Dependencies
{chr(10).join(f"- {dep}" for dep in spec.dependencies) if spec.dependencies else "- No dependencies"}

## Coordination Notes
- Session: {spec.session_id}
- Complexity Level: {spec.complexity_level}/4
- Target Service: {spec.target_service}
- Priority: {spec.priority}

## Protocol Compliance
- Follow worker-startup-protocol.md exactly
- Log all significant events to EVENTS.jsonl
- Update session state upon task completion
- Signal completion with status update

---

**IMPORTANT**: This prompt file was generated by the Queen orchestrator. Follow all instructions exactly as specified. Your task completion will be validated against these success criteria.
"""


def create_worker_prompts_from_plan(
    session_id: str, orchestration_plan, batch_logging: bool = True
) -> Dict[str, str]:
    """
    Convenience function to create worker prompts from Queen orchestration plan.
    Framework-enforced integration point.
    """
    generator = PromptGenerator(session_id)

    # Convert orchestration plan to worker specs
    worker_specs = []
    target_service = getattr(orchestration_plan, "target_service", "unknown")

    for assignment in orchestration_plan.worker_assignments:
        spec = WorkerPromptSpec(
            worker_type=assignment.worker_type,
            task_focus=assignment.task_focus,
            priority=assignment.priority,
            estimated_duration=assignment.estimated_duration,
            rationale=assignment.rationale,
            complexity_level=orchestration_plan.complexity_assessment,
            session_id=session_id,
            target_service=target_service,
            dependencies=getattr(assignment, "dependencies", []),
            focus_areas=getattr(assignment, "focus_areas", []),
        )
        worker_specs.append(spec)

    return generator.create_worker_prompts(worker_specs, batch_logging=batch_logging)
