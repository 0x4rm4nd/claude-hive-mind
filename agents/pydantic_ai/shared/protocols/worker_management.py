#!/usr/bin/env python3
"""
Worker Management Protocol - Unified worker prompt handling
===========================================================
Framework-enforced prompt creation and parsing for all worker types.
Consolidates prompt generation and reading into single source of truth.
"""

import os
import re
import yaml
import json
from typing import Dict, List, Any
from dataclasses import dataclass, field
from .session_management import SessionManagement, iso_now
from .protocol_loader import BaseProtocol
from .protocol_interface import ProtocolMetadata


# Single source of truth for all worker configurations
WORKER_CONFIGS = {
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


@dataclass
class WorkerSpec:
    """Unified specification for worker prompt generation and parsing"""

    worker_type: str
    task_focus: str
    priority: str
    estimated_duration: str
    rationale: str
    complexity_level: int
    session_id: str
    target_service: str = "unknown"
    dependencies: List[str] = field(default_factory=list)
    focus_areas: List[str] = field(default_factory=list)
    # Enhanced context from orchestration
    codebase_insights: List[Dict] = field(default_factory=list)
    success_metrics: List[str] = field(default_factory=list)
    identified_risks: List[str] = field(default_factory=list)
    coordination_notes: List[str] = field(default_factory=list)
    orchestration_plan: Any = None


class WorkerManager(BaseProtocol):
    """
    Unified worker prompt creation and parsing with proper protocol compliance.
    
    The WorkerManager handles the complete lifecycle of worker prompts:
    - Generation from WorkerSpec configurations
    - Template creation with strategic context
    - File parsing and validation
    - Task instruction extraction
    
    Example Usage:
    
    Basic Worker Prompt Creation:
    ```python
    from shared.protocols import WorkerManager, WorkerSpec
    
    # Initialize manager
    manager = WorkerManager({"session_id": "my-session", "agent_name": "orchestrator"})
    
    # Create worker specification
    spec = WorkerSpec(
        worker_type="backend-worker",
        task_focus="API endpoint implementation", 
        priority="high",
        estimated_duration="2-4 hours",
        rationale="Critical user authentication endpoints needed",
        complexity_level=3,
        session_id="my-session",
        target_service="api-service"
    )
    
    # Generate prompts
    created_files = manager.create_worker_prompts([spec])
    print(f"Created: {list(created_files.keys())}")  # ['backend-worker']
    ```
    
    Reading and Parsing Worker Prompts:
    ```python
    # Parse existing prompt file
    prompt_data = manager.read_prompt_file("backend-worker")
    
    # Extract task instructions
    instructions = manager.get_task_instructions("backend-worker")
    
    # Access parsed components
    print(f"Worker expertise: {instructions['worker_expertise']}")
    print(f"Success criteria: {instructions['success_criteria']}")
    print(f"Available tools: {instructions['available_tools']}")
    ```
    
    Queen Orchestration Integration:
    ```python
    from shared.protocols import create_worker_prompts_from_plan
    
    # Create prompts from orchestration plan (advanced usage)
    created_files = create_worker_prompts_from_plan(
        session_id="orchestration-session",
        orchestration_plan=queen_plan  # From Queen agent
    )
    ```
    """

    # Protocol metadata - unique to WorkerManager
    _metadata = ProtocolMetadata(
        name="WorkerManager", 
        version="2.0.0",
        description="Framework-enforced worker prompt lifecycle management with strategic orchestration",
        capabilities=["logging", "session_aware", "worker_prompts", "template_generation", "prompt_parsing"]
    )

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize WorkerManager with proper BaseProtocol inheritance"""
        if config is None:
            config = {
                "session_id": "default-session",
                "agent_name": "worker-manager",
            }
        super().__init__(config)
        self.prompt_data = None

    def create_worker_prompts(self, worker_specs: List[WorkerSpec]) -> Dict[str, str]:
        """
        Create prompt files for all assigned workers.
        Framework-enforced: Cannot be skipped, must create valid files.
        """
        session_path = SessionManagement.get_session_path(self.config.session_id)
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

            except Exception as e:
                failed_prompts.append(
                    {
                        "exception_type": str(type(e)),
                        "error": str(e),
                        "worker_type": spec.worker_type,
                    }
                )

                self.log_debug(
                    "worker_prompt_creation_failed",
                    {
                        "exception_type": str(type(e)),
                        "error": str(e),
                        "worker_type": spec.worker_type,
                    },
                    "ERROR",
                )
                raise

        # Consolidated batch logging
        if created_files:
            # Convert absolute path to relative path from project root
            project_root = SessionManagement.detect_project_root()
            relative_prompts_dir = (
                prompts_dir.replace(f"{project_root}/", "")
                if prompts_dir.startswith(project_root)
                else prompts_dir
            )

            self.log_event(
                "worker_prompts_created",
                {
                    "worker_types": list(created_files.keys()),
                    "total_prompts": len(created_files),
                    "prompt_folder": relative_prompts_dir,
                    "complexity_level": (
                        worker_specs[0].complexity_level if worker_specs else 1
                    ),
                },
            )

        return created_files

    def read_prompt_file(self, worker_type: str) -> Dict[str, Any]:
        """
        Read and parse worker-specific prompt file.

        Returns:
            Dict containing parsed prompt data including task instructions,
            focus areas, dependencies, success criteria, and output requirements.
        """
        try:
            # Get session path using unified session management
            session_path = SessionManagement.get_session_path(self.config.session_id)
            prompt_file_path = f"{session_path}/workers/prompts/{worker_type}.prompt"

            # Parse standard format
            prompt_data = self._parse_prompt_content(prompt_file_path)

            # Validate required fields
            self._validate_prompt_data(prompt_data)

            # Store for later reference
            self.prompt_data = prompt_data

            # Log successful prompt reading
            SessionManagement.append_to_events(
                self.config.session_id,
                {
                    "type": "prompt_file_read",
                    "agent": self.config.agent_name or worker_type,
                    "details": {
                        "status": "success",
                        "file": prompt_file_path,
                        "worker": worker_type,
                    },
                    "timestamp": iso_now(),
                },
            )

            return prompt_data

        except FileNotFoundError as e:
            # CRITICAL: Prompt file must exist - protocol violation
            raise FileNotFoundError(
                f"Protocol violation: Worker prompt file must exist at {prompt_file_path}"
            ) from e

        except Exception as e:
            raise

    def get_task_instructions(self, worker_type: str = None) -> Dict[str, Any]:
        """Get parsed task instructions for the worker"""
        if not self.prompt_data:
            worker_type = worker_type or self.config.agent_name
            self.prompt_data = self.read_prompt_file(worker_type)
        return self.prompt_data

    def _generate_prompt_content(self, spec: WorkerSpec) -> str:
        """Generate structured prompt content for a specific worker"""

        config = WORKER_CONFIGS.get(
            spec.worker_type,
            {
                "expertise": "General analysis and assessment",
                "tools": ["code analyzers", "pattern matchers"],
                "outputs": ["analysis.md", "recommendations.md"],
                "focus_areas": ["code quality", "best practices"],
            },
        )

        # Extract target services from codebase insights
        target_services = []
        if spec.codebase_insights:
            target_services = [
                insight.get("service_name", "unknown")
                for insight in spec.codebase_insights
            ]
        primary_target_service = (
            target_services[0] if target_services else "system-wide"
        )

        # Generate codebase context section
        codebase_context = ""
        if spec.codebase_insights:
            codebase_context = "\n## Codebase Context\n"
            for insight in spec.codebase_insights:
                service_name = insight.get("service_name", "unknown")
                key_files = insight.get("key_files", [])
                architecture_notes = insight.get("architecture_notes", [])
                potential_issues = insight.get("potential_issues", [])

                codebase_context += f"### {service_name}\n"
                if key_files:
                    codebase_context += f"**Key Files**: {', '.join(key_files)}\n"
                if architecture_notes:
                    codebase_context += (
                        f"**Architecture**: {' | '.join(architecture_notes)}\n"
                    )
                if potential_issues:
                    codebase_context += (
                        f"**Known Issues**: {' | '.join(potential_issues)}\n"
                    )
                codebase_context += "\n"

        # Generate risk context section
        risk_context = ""
        if spec.identified_risks:
            risk_context = "\n## Critical Risk Context\n"
            for i, risk in enumerate(spec.identified_risks, 1):
                risk_context += f"{i}. {risk}\n"

        # Generate strategic success metrics
        strategic_metrics = ""
        if spec.success_metrics:
            strategic_metrics = "\n## Strategic Success Metrics (Queen-Defined)\n"
            for metric in spec.success_metrics:
                strategic_metrics += f"- {metric}\n"

        # Generate coordination strategy
        coordination_strategy = ""
        if spec.coordination_notes:
            coordination_strategy = "\n## Strategic Coordination\n"
            for note in spec.coordination_notes:
                coordination_strategy += f"- {note}\n"

        return f"""---
worker_type: {spec.worker_type}
session_id: {spec.session_id}
task_focus: {spec.task_focus}
priority: {spec.priority}
estimated_duration: {spec.estimated_duration}
complexity_level: {spec.complexity_level}
target_services: {target_services}
primary_target: {primary_target_service}
dependencies: {spec.dependencies}
focus_areas: {spec.focus_areas or config['focus_areas']}
created_by: queen-orchestrator
---

# {spec.worker_type.replace('-', ' ').title()} Task Instructions

## Primary Task
{spec.task_focus}

## Worker Expertise
{config['expertise']}

## Strategic Rationale
{spec.rationale}
{codebase_context}
{risk_context}
{strategic_metrics}
{coordination_strategy}
## Success Criteria
- Complete analysis of assigned focus areas
- Generate comprehensive findings with evidence
- Provide actionable recommendations targeting identified issues
- Document potential risks and mitigation strategies
- Create required output files
- Address codebase-specific issues identified by Queen

## Output Requirements
### Required Files
{chr(10).join(f"- `workers/notes/{output}`" for output in config['outputs'])}

### JSON Response Format
```json
{{
    "worker_type": "{spec.worker_type}",
    "status": "completed",
    "task_focus": "{spec.task_focus}",
    "target_services": {target_services},
    "findings": [
        {{
            "category": "string",
            "severity": "high|medium|low",
            "description": "string", 
            "evidence": "string",
            "recommendation": "string",
            "target_service": "string"
        }}
    ],
    "analysis_summary": "string",
    "key_recommendations": ["string"],
    "potential_blockers": ["string"],
    "next_steps": ["string"],
    "risk_mitigation": ["string"],
    "strategic_alignment": "string"
}}
```

## Available Tools
{chr(10).join(f"- {tool}" for tool in config['tools'])}

## Focus Areas (Priority Order)
{chr(10).join(f"{i+1}. {area}" for i, area in enumerate(spec.focus_areas or config['focus_areas']))}

## Worker Dependencies
{chr(10).join(f"- Wait for: {dep}" for dep in spec.dependencies) if spec.dependencies else "- No dependencies - start immediately"}

## Enhanced Coordination Context
- **Session**: {spec.session_id}
- **Complexity Level**: {spec.complexity_level}/10
- **Primary Target**: {primary_target_service}
- **Priority**: {spec.priority}
- **Strategic Value**: Address Queen-identified issues in codebase insights
- **Coordination**: Work aligns with overall orchestration strategy

---

**QUEEN'S DIRECTIVE**: This prompt integrates strategic context from orchestration analysis. Your work must address the specific issues identified in the codebase insights and align with the success metrics defined above. Follow the coordination strategy to ensure your output integrates effectively with other workers.
"""

    def _parse_prompt_content(self, file_path: str) -> Dict[str, Any]:
        """
        Parse prompt file content into structured data.

        Expected format:
        - YAML frontmatter with metadata
        - Markdown sections for different instruction types
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Split YAML frontmatter and markdown content
            if not content.startswith("---"):
                raise ValueError("Prompt file must start with YAML frontmatter")

            # Find the end of frontmatter
            parts = content.split("---", 2)
            if len(parts) < 3:
                raise ValueError("Invalid YAML frontmatter format")

            frontmatter_text = parts[1].strip()
            markdown_content = parts[2].strip()

            # Parse YAML frontmatter
            frontmatter = yaml.safe_load(frontmatter_text) or {}

            # Parse markdown sections
            markdown_sections = self._parse_markdown_sections(markdown_content)

            # Combine into structured data
            return {
                # From YAML frontmatter
                "worker_type": frontmatter.get("worker_type", ""),
                "session_id": frontmatter.get("session_id", ""),
                "task_description": frontmatter.get("task_focus", ""),
                "priority": frontmatter.get("priority", "medium"),
                "estimated_duration": frontmatter.get("estimated_duration", "1-2h"),
                "complexity_level": frontmatter.get("complexity_level", 1),
                "target_services": frontmatter.get("target_services", []),
                "primary_target": frontmatter.get("primary_target", "unknown"),
                "dependencies": frontmatter.get("dependencies", []),
                "focus_areas": frontmatter.get("focus_areas", []),
                "created_by": frontmatter.get("created_by", "unknown"),
                # From markdown sections
                "worker_expertise": markdown_sections.get("worker_expertise", ""),
                "rationale": markdown_sections.get("strategic_rationale", ""),
                "success_criteria": markdown_sections.get("success_criteria", []),
                "output_requirements": markdown_sections.get("output_requirements", {}),
                "available_tools": markdown_sections.get("available_tools", []),
                "codebase_context": markdown_sections.get("codebase_context", {}),
                "risk_context": markdown_sections.get("critical_risk_context", []),
                "coordination_strategy": markdown_sections.get(
                    "strategic_coordination", []
                ),
                # Combined metadata
                "timeout": 3600,  # Default timeout
                "full_content": content,
                "parsed_sections": list(markdown_sections.keys()),
            }

        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML frontmatter in prompt file: {e}")
        except Exception as e:
            raise RuntimeError(f"Error parsing prompt file {file_path}: {e}")

    def _parse_markdown_sections(self, markdown_content: str) -> Dict[str, Any]:
        """Parse markdown sections into structured data"""
        sections = {}

        # Split by headers
        lines = markdown_content.split("\n")
        current_section = None
        current_content = []

        for line in lines:
            if line.startswith("##"):
                # Save previous section
                if current_section:
                    sections[current_section] = self._process_section_content(
                        current_section, "\n".join(current_content).strip()
                    )

                # Start new section
                current_section = (
                    line.replace("##", "").strip().lower().replace(" ", "_")
                )
                current_content = []
            elif line.startswith("#") and not line.startswith("##"):
                # Skip main headers
                continue
            else:
                current_content.append(line)

        # Save last section
        if current_section:
            sections[current_section] = self._process_section_content(
                current_section, "\n".join(current_content).strip()
            )

        return sections

    def _process_section_content(self, section_name: str, content: str) -> Any:
        """Process section content based on section type"""
        if section_name in [
            "success_criteria",
            "available_tools",
            "focus_areas_priority_order",
            "worker_dependencies",
        ]:
            # List-based sections
            items = []
            for line in content.split("\n"):
                line = line.strip()
                if line and (
                    line.startswith("- ")
                    or line.startswith("1. ")
                    or line.startswith("2. ")
                    or line.startswith("3. ")
                ):
                    # Remove list markers
                    item = re.sub(r"^[-\d\.]\s*", "", line).strip()
                    if item:
                        items.append(item)
            return items

        elif section_name == "output_requirements":
            # Extract file requirements
            files = []
            json_format = {}

            # Look for file listings
            file_matches = re.findall(r"- `([^`]+)`", content)
            files.extend(file_matches)

            # Look for JSON format
            json_match = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
            if json_match:
                try:
                    json_format = json.loads(json_match.group(1))
                except:
                    json_format = {"format": "json", "raw": json_match.group(1)}

            return {
                "required_files": files,
                "json_format": json_format,
                "raw_content": content,
            }

        elif section_name in ["codebase_context", "critical_risk_context"]:
            # Context sections - extract key points
            points = []
            for line in content.split("\n"):
                line = line.strip()
                if line and (
                    line.startswith("- ")
                    or line.startswith("**")
                    or line.startswith("###")
                ):
                    points.append(line)

            return {"key_points": points, "full_content": content}

        else:
            # Default: return as string
            return content

    def _validate_prompt_data(self, data: Dict[str, Any]) -> None:
        """Validate that prompt data contains required fields"""
        required_fields = ["task_description", "focus_areas", "success_criteria"]

        for field in required_fields:
            if field not in data or not data[field]:
                self.log_debug(
                    "Prompt validation failed - missing required field",
                    {
                        "missing_field": field,
                        "required_fields": required_fields,
                        "available_fields": list(data.keys()),
                        "validation_failure": True,
                    },
                    "ERROR",
                )
                raise ValueError(f"Missing required field in prompt: {field}")


def create_worker_prompts_from_plan(
    session_id: str, orchestration_plan
) -> Dict[str, str]:
    """
    Convenience function to create worker prompts from Queen orchestration plan.
    Framework-enforced integration point with enhanced strategic context.
    """
    manager = WorkerManager(
        {"session_id": session_id, "agent_name": "queen-orchestrator"}
    )

    # Extract orchestration context
    target_service = getattr(orchestration_plan, "target_service", "unknown")
    codebase_insights = getattr(orchestration_plan, "codebase_insights", [])
    success_metrics = getattr(orchestration_plan, "success_metrics", [])
    identified_risks = getattr(orchestration_plan, "identified_risks", [])
    coordination_notes = getattr(orchestration_plan, "coordination_notes", [])

    # Convert orchestration plan to enhanced worker specs
    worker_specs = []
    for assignment in orchestration_plan.worker_assignments:
        spec = WorkerSpec(
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
            # Enhanced strategic context
            codebase_insights=codebase_insights,
            success_metrics=success_metrics,
            identified_risks=identified_risks,
            coordination_notes=coordination_notes,
            orchestration_plan=orchestration_plan,
        )
        worker_specs.append(spec)

    return manager.create_worker_prompts(worker_specs)
