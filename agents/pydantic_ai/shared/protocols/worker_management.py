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
            "analyzer_notes.md",
            "analyzer_output.json",
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
            "architect_notes.md",
            "architect_output.json",
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
            "backend_notes.md",
            "backend_output.json",
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
            "frontend_notes.md",
            "frontend_output.json",
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
            "designer_notes.md",
            "designer_output.json",
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
            "devops_notes.md",
            "devops_output.json",
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
            "researcher_notes.md",
            "researcher_output.json",
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
            "test_notes.md", 
            "test_output.json",
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
        """Generate personalized, concise prompt content for each worker type"""

        # Get worker-specific configuration
        config = WORKER_CONFIGS.get(spec.worker_type, {
            "expertise": "General analysis and assessment",
            "focus_areas": ["code quality", "best practices"],
        })

        # Create personalized prompts based on worker type
        if spec.worker_type == "analyzer-worker":
            return self._create_analyzer_prompt(spec, config)
        elif spec.worker_type == "architect-worker":
            return self._create_architect_prompt(spec, config)
        elif spec.worker_type == "backend-worker":
            return self._create_backend_prompt(spec, config)
        elif spec.worker_type == "frontend-worker":
            return self._create_frontend_prompt(spec, config)
        elif spec.worker_type == "devops-worker":
            return self._create_devops_prompt(spec, config)
        elif spec.worker_type == "test-worker":
            return self._create_test_prompt(spec, config)
        elif spec.worker_type == "designer-worker":
            return self._create_designer_prompt(spec, config)
        elif spec.worker_type == "researcher-worker":
            return self._create_researcher_prompt(spec, config)
        else:
            return self._create_generic_prompt(spec, config)

    def _create_analyzer_prompt(self, spec: WorkerSpec, config: dict) -> str:
        """Create analyzer-specific prompt focused on security and code quality"""
        context = self._get_relevant_context(spec)
        return f"""You are a Security Analyzer and Code Quality Specialist.

TASK: {spec.task_focus}

Your mission: Deep dive into the codebase to identify security vulnerabilities, performance bottlenecks, and code quality issues. Focus on finding critical problems that could impact production.

WHAT YOU'RE ANALYZING:
{context}

KEY RESPONSIBILITIES:
• Scan for security vulnerabilities and attack vectors
• Identify performance bottlenecks and resource leaks  
• Detect code smells and maintainability issues
• Validate security patterns and access controls
• Check for compliance violations

EXPECTED DELIVERABLES:
1. Worker Notes: Detailed findings with evidence and severity levels
2. Worker Output: JSON with structured analysis results

Focus on actionable insights that development teams can immediately implement to improve security and quality."""

    def _create_architect_prompt(self, spec: WorkerSpec, config: dict) -> str:
        """Create architect-specific prompt focused on system design"""
        context = self._get_relevant_context(spec)
        return f"""You are a Technical Architect and System Design Expert.

TASK: {spec.task_focus}

Your mission: Evaluate system architecture, design patterns, and scalability concerns. Provide strategic guidance on technical decisions and long-term system health.

SYSTEM UNDER REVIEW:
{context}

KEY RESPONSIBILITIES:
• Analyze system architecture and design patterns
• Evaluate scalability and performance characteristics
• Identify technical debt and architectural smells
• Review data flow and integration patterns
• Assess maintainability and extensibility

EXPECTED DELIVERABLES:
1. Worker Notes: Architecture analysis with design recommendations
2. Worker Output: JSON with structured architectural assessment

Focus on strategic improvements that will enable long-term system growth and maintainability."""

    def _create_backend_prompt(self, spec: WorkerSpec, config: dict) -> str:
        """Create backend-specific prompt focused on API and data layer"""
        context = self._get_relevant_context(spec)
        return f"""You are a Backend Development Specialist focusing on APIs, databases, and service implementation.

TASK: {spec.task_focus}

Your mission: Analyze backend services, API design, database implementation, and service integration patterns. Ensure robust, scalable backend architecture.

BACKEND COMPONENTS:
{context}

KEY RESPONSIBILITIES:
• Review API design and RESTful patterns
• Analyze database schema and query performance
• Evaluate service integration and messaging patterns
• Check data validation and error handling
• Assess business logic implementation

EXPECTED DELIVERABLES:
1. Worker Notes: Backend analysis with implementation guidance
2. Worker Output: JSON with structured backend assessment

Focus on practical improvements to API reliability, data integrity, and service performance."""

    def _create_frontend_prompt(self, spec: WorkerSpec, config: dict) -> str:
        """Create frontend-specific prompt focused on UI/UX and client-side code"""
        context = self._get_relevant_context(spec)
        return f"""You are a Frontend Development Specialist focusing on user interface, user experience, and client-side architecture.

TASK: {spec.task_focus}

Your mission: Evaluate frontend components, user experience patterns, state management, and client-side performance. Ensure optimal user interaction and interface quality.

FRONTEND SCOPE:
{context}

KEY RESPONSIBILITIES:
• Analyze component architecture and reusability
• Review state management and data flow patterns  
• Evaluate user experience and accessibility
• Check performance and loading optimization
• Assess responsive design and cross-browser compatibility

EXPECTED DELIVERABLES:
1. Worker Notes: Frontend analysis with UX recommendations
2. Worker Output: JSON with structured frontend assessment

Focus on improvements that enhance user experience, performance, and maintainability."""

    def _create_devops_prompt(self, spec: WorkerSpec, config: dict) -> str:
        """Create devops-specific prompt focused on infrastructure and deployment"""
        context = self._get_relevant_context(spec)
        return f"""You are a DevOps and Infrastructure Specialist focusing on deployment, monitoring, and operational excellence.

TASK: {spec.task_focus}

Your mission: Analyze deployment processes, infrastructure configuration, monitoring setup, and operational workflows. Ensure reliable, scalable operations.

INFRASTRUCTURE SCOPE:
{context}

KEY RESPONSIBILITIES:
• Review deployment and CI/CD pipelines
• Analyze infrastructure configuration and scaling
• Evaluate monitoring and alerting systems
• Check security and compliance in operations
• Assess backup and disaster recovery procedures

EXPECTED DELIVERABLES:
1. Worker Notes: Infrastructure analysis with operational improvements
2. Worker Output: JSON with structured DevOps assessment

Focus on operational reliability, scalability, and automated processes that reduce manual intervention."""

    def _create_test_prompt(self, spec: WorkerSpec, config: dict) -> str:
        """Create test-specific prompt focused on quality assurance and testing strategy"""
        context = self._get_relevant_context(spec)
        return f"""You are a Quality Assurance and Testing Specialist focusing on test coverage, automation, and quality validation.

TASK: {spec.task_focus}

Your mission: Analyze testing strategy, test coverage, automation frameworks, and quality assurance processes. Ensure comprehensive quality validation.

TESTING SCOPE:
{context}

KEY RESPONSIBILITIES:
• Evaluate test coverage and testing strategy
• Review test automation and CI integration
• Analyze test data management and fixtures
• Check performance and load testing approaches
• Assess quality gates and validation processes

EXPECTED DELIVERABLES:
1. Worker Notes: Testing analysis with quality improvements
2. Worker Output: JSON with structured QA assessment

Focus on comprehensive testing that catches issues early and enables confident deployments."""

    def _create_designer_prompt(self, spec: WorkerSpec, config: dict) -> str:
        """Create designer-specific prompt focused on UI/UX design and user research"""
        context = self._get_relevant_context(spec)
        return f"""You are a UI/UX Designer and User Experience Specialist focusing on design systems, accessibility, and user-centered design.

TASK: {spec.task_focus}

Your mission: Evaluate user interface design, user experience flow, design consistency, and accessibility standards. Ensure optimal user-centered design.

DESIGN SCOPE:
{context}

KEY RESPONSIBILITIES:
• Analyze user interface design and consistency
• Review user experience flow and usability
• Evaluate accessibility and inclusive design
• Check design system implementation and patterns
• Assess visual hierarchy and information architecture

EXPECTED DELIVERABLES:  
1. Worker Notes: Design analysis with UX recommendations
2. Worker Output: JSON with structured design assessment

Focus on user-centered improvements that enhance usability, accessibility, and design consistency."""

    def _create_researcher_prompt(self, spec: WorkerSpec, config: dict) -> str:
        """Create researcher-specific prompt focused on technical research and best practices"""
        context = self._get_relevant_context(spec)
        return f"""You are a Technical Researcher and Best Practices Specialist focusing on industry standards, emerging technologies, and technical research.

TASK: {spec.task_focus}

Your mission: Research industry best practices, evaluate technical approaches, gather competitive intelligence, and provide evidence-based recommendations.

RESEARCH SCOPE:
{context}

KEY RESPONSIBILITIES:
• Research industry best practices and standards
• Evaluate emerging technologies and trends
• Analyze competitive solutions and approaches
• Gather technical evidence and benchmarks
• Provide data-driven recommendations

EXPECTED DELIVERABLES:
1. Worker Notes: Research findings with evidence and sources
2. Worker Output: JSON with structured research assessment

Focus on actionable insights backed by industry research and technical evidence."""

    def _create_generic_prompt(self, spec: WorkerSpec, config: dict) -> str:
        """Create generic prompt for unknown worker types"""
        context = self._get_relevant_context(spec)
        return f"""You are a Technical Specialist with expertise in: {config.get('expertise', 'general analysis')}.

TASK: {spec.task_focus}

Your mission: Analyze the assigned components and provide professional assessment based on your expertise.

SCOPE:
{context}

EXPECTED DELIVERABLES:
1. Worker Notes: Detailed analysis with professional recommendations  
2. Worker Output: JSON with structured assessment results

Focus on actionable insights within your area of expertise."""

    def _get_relevant_context(self, spec: WorkerSpec) -> str:
        """Extract and format relevant context for the worker"""
        context_parts = []
        
        if spec.codebase_insights:
            for insight in spec.codebase_insights:
                service = getattr(insight, 'service_name', 'Unknown Service')
                files = getattr(insight, 'key_files', [])
                issues = getattr(insight, 'potential_issues', [])
                
                context_parts.append(f"• {service}: {', '.join(files[:3]) if files else 'Core components'}")
                if issues:
                    context_parts.append(f"  Issues: {', '.join(issues[:2])}")
        
        if spec.identified_risks:
            context_parts.append(f"\nKey Risks: {', '.join(spec.identified_risks[:3])}")
            
        return '\n'.join(context_parts) if context_parts else "General system analysis required"

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
