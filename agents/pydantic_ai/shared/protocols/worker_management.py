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
from .worker_templates import load_template, format_template
from .worker_templates.worker_configs import WORKER_CONFIGS


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
        capabilities=[
            "logging",
            "session_aware",
            "worker_prompts",
            "template_generation",
            "prompt_parsing",
        ],
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

    def read_prompt_file(self, worker_type: str) -> str:
        """
        Read worker-specific prompt file as plain text.

        Returns:
            String containing the Queen-generated prompt content.
        """
        try:
            # Get session path using unified session management
            session_path = SessionManagement.get_session_path(self.config.session_id)
            prompt_file_path = f"{session_path}/workers/prompts/{worker_type}.prompt"

            # Read plain text prompt
            prompt_content = self._parse_prompt_content(prompt_file_path)

            # Store for later reference
            self.prompt_data = prompt_content

            # Log successful prompt reading with relative path
            try:
                project_root = SessionManagement.detect_project_root()
                relative_path = prompt_file_path.replace(f"{project_root}/", "") if prompt_file_path.startswith(project_root) else prompt_file_path
            except:
                relative_path = prompt_file_path
                
            self.log_event(
                "prompt_file_read",
                {
                    "status": "success",
                    "file": relative_path,
                    "worker": worker_type,
                },
            )

            return prompt_content

        except FileNotFoundError as e:
            # CRITICAL: Prompt file must exist - protocol violation
            raise FileNotFoundError(
                f"Protocol violation: Worker prompt file must exist at {prompt_file_path}"
            ) from e

        except Exception as e:
            raise e

    def get_task_instructions(self, worker_type: str = None) -> Dict[str, Any]:
        """Get parsed task instructions for the worker"""
        if not self.prompt_data:
            worker_type = worker_type or self.config.agent_name
            self.prompt_data = self.read_prompt_file(worker_type)
        return self.prompt_data

    def _generate_prompt_content(self, spec: WorkerSpec) -> str:
        """Generate personalized, concise prompt content using external templates"""
        try:
            # Load template from external file
            template_content = load_template(spec.worker_type)

            # Get relevant context for the worker
            context = self._get_relevant_context(spec)

            # Format template with task-specific content
            return format_template(template_content, spec.task_focus, context)

        except FileNotFoundError:
            # Fallback for unknown worker types
            return self._create_generic_prompt(spec)

    def _create_generic_prompt(self, spec: WorkerSpec) -> str:
        """Create generic prompt for unknown worker types"""
        config = WORKER_CONFIGS.get(
            "generic",
            {
                "expertise": "General analysis and assessment",
                "focus_areas": ["code quality", "best practices"],
            },
        )

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
        """Extract and format factual context for the worker (no analysis from Queen)"""
        context_parts = []

        if spec.codebase_insights:
            for insight in spec.codebase_insights:
                service = getattr(insight, "service_name", "Unknown Service")
                files = getattr(insight, "key_files", [])
                description = getattr(insight, "service_description", "")
                tech_stack = getattr(insight, "technology_stack", [])
                interactions = getattr(insight, "interaction_points", [])

                context_parts.append(
                    f"• {service}: {', '.join(files[:5]) if files else 'Core components'}"
                )
                if description:
                    context_parts.append(f"  Description: {description}")
                if tech_stack:
                    context_parts.append(f"  Tech Stack: {', '.join(tech_stack)}")
                if interactions:
                    context_parts.append(
                        f"  Interactions: {', '.join(interactions[:2])}"
                    )

        return (
            "\n".join(context_parts)
            if context_parts
            else "General system analysis required"
        )

    def _parse_prompt_content(self, file_path: str) -> str:
        """
        Read prompt file content as plain text.

        Queen-generated prompts are plain text format, not YAML frontmatter.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            return content

        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
        except Exception as e:
            raise RuntimeError(f"Error reading prompt file {file_path}: {e}")

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
            complexity_level=orchestration_plan.coordination_complexity,
            session_id=session_id,
            target_service=target_service,
            dependencies=getattr(assignment, "dependencies", []),
            focus_areas=getattr(assignment, "focus_areas", []),
            # Enhanced strategic context
            codebase_insights=codebase_insights,
            coordination_notes=coordination_notes,
            orchestration_plan=orchestration_plan,
        )
        worker_specs.append(spec)

    return manager.create_worker_prompts(worker_specs)
