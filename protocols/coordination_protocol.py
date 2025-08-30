#!/usr/bin/env python3
"""
Coordination Protocol for Multi-Agent Task Management
Ensures proper event ordering, logging, and session management
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib
import time


class CoordinationProtocol:
    """Manages multi-agent coordination, session creation, and event logging"""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize coordination protocol with project root detection"""
        self.project_root = project_root or self._find_project_root()
        self.sessions_dir = self.project_root / "Docs" / "hive-mind" / "sessions"
        self.current_session = None
        self.session_path = None
        
    def _find_project_root(self) -> Path:
        """Find project root by looking for key markers"""
        current = Path.cwd()
        markers = ['.git', 'package.json', 'requirements.txt', 'pyproject.toml', 'Docs']
        
        while current != current.parent:
            for marker in markers:
                if (current / marker).exists():
                    # Special case: if we're in .claude/agents, go up to project root
                    if '.claude' in str(current):
                        while '.claude' in str(current):
                            current = current.parent
                    return current
            current = current.parent
        
        return Path.cwd()  # Fallback to current directory
    
    def generate_session_id(self, task_description: str) -> str:
        """Generate session ID in YYYY-MM-DD-HH-mm-TASKSLUG format"""
        now = datetime.now()
        date_part = now.strftime("%Y-%m-%d-%H-%M")
        
        # Create task slug (min 15 chars)
        original_length = len(task_description)
        task_slug = task_description.lower()
        task_slug = ''.join(c if c.isalnum() or c == '-' else '-' for c in task_slug)
        task_slug = '-'.join(filter(None, task_slug.split('-')))[:50]  # Max 50 chars
        
        # Ensure minimum length
        if len(task_slug) < 15:
            task_slug = task_slug.ljust(15, '-')
        
        session_id = f"{date_part}-{task_slug}"
        
        # Log technical details about ID generation (if session path exists)
        if hasattr(self, 'session_path') and self.session_path:
            self.log_debug(
                "Session ID generated",
                "INFO",
                details={
                    "session_id": session_id,
                    "timestamp": now.isoformat(),
                    "original_task_length": original_length,
                    "slug_length": len(task_slug),
                    "total_id_length": len(session_id)
                }
            )
        
        return session_id
    
    def create_session_structure(self, session_id: str, task_description: str, complexity_level: int = 2) -> Dict[str, Any]:
        """Create complete session directory structure and files"""
        self.current_session = session_id
        self.session_path = self.sessions_dir / session_id
        
        # Create directories
        self.session_path.mkdir(parents=True, exist_ok=True)
        (self.session_path / "workers").mkdir(exist_ok=True)
        (self.session_path / "workers" / "json").mkdir(exist_ok=True)
        (self.session_path / "workers" / "prompts").mkdir(exist_ok=True)
        (self.session_path / "workers" / "decisions").mkdir(exist_ok=True)
        
        # Initialize STATE.json with complete template structure
        state = self._generate_state_json(session_id, task_description, complexity_level)
        
        with open(self.session_path / "STATE.json", 'w') as f:
            json.dump(state, f, indent=2)
        
        # Initialize EVENTS.jsonl (empty, will be appended to)
        (self.session_path / "EVENTS.jsonl").touch()
        
        # Initialize DEBUG.jsonl with first entry
        debug_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "debug_initialized",
            "agent": "queen-orchestrator",
            "details": "DEBUG.jsonl file created for session debugging"
        }
        with open(self.session_path / "DEBUG.jsonl", 'w') as f:
            f.write(json.dumps(debug_entry) + '\n')
        
        # Initialize SESSION.md with rich template
        session_md = self._generate_session_markdown(session_id, task_description, complexity_level)
        with open(self.session_path / "SESSION.md", 'w') as f:
            f.write(session_md)
        
        return state
    
    def log_event(self, event_type: str, details: Dict[str, Any], worker: str = "queen-orchestrator") -> None:
        """Append event to EVENTS.jsonl - NEVER overwrites, always appends"""
        if not self.session_path:
            self.log_debug(
                "log_event failed - no active session",
                "ERROR",
                details={
                    "event_type": event_type,
                    "worker": worker,
                    "session_path": str(self.session_path) if self.session_path else None,
                    "error": "No active session. Create session first."
                }
            )
            raise ValueError("No active session. Create session first.")
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "worker": worker,
            "session_id": self.current_session,
            "details": details
        }
        
        # CRITICAL: Append mode to prevent overwriting + ensure file exists
        events_file = self.session_path / "EVENTS.jsonl"
        if not events_file.exists():
            events_file.touch()  # Create if missing
        
        with open(events_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
    
    def log_debug(self, message: str, level: str = "INFO", agent: str = "queen-orchestrator", details: Any = None) -> None:
        """Append debug information to DEBUG.jsonl"""
        if not self.session_path:
            return  # Silent fail for debug logs before session creation
        
        debug_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "agent": agent,
            "message": message,
            "details": details
        }
        
        # CRITICAL: Append mode to prevent overwriting + ensure file exists
        debug_file = self.session_path / "DEBUG.jsonl"
        if not debug_file.exists():
            debug_file.touch()  # Create if missing
        
        with open(debug_file, 'a') as f:
            f.write(json.dumps(debug_entry) + '\n')
    
    def log_queen_spawn(self, task_description: str, complexity_level: int) -> None:
        """Log queen activation - MUST be first operational event"""
        self.log_event(
            event_type="queen_spawned",
            details={
                "task_description": task_description,
                "complexity_level": complexity_level,
                "initialization_complete": True,
                "session_structure_created": True
            }
        )
        # Debug: Log technical details about initialization
        self.log_debug(
            "Queen initialization parameters",
            "INFO",
            details={
                "process_id": os.getpid(),
                "python_version": sys.version,
                "working_directory": str(self.project_root),
                "sessions_directory": str(self.sessions_dir)
            }
        )
    
    def log_session_created(self) -> None:
        """Log session creation event - should come AFTER queen spawn"""
        self.log_event(
            event_type="session_created",
            details={
                "session_path": str(self.session_path),
                "structure_validated": True,
                "files_initialized": ["STATE.json", "EVENTS.jsonl", "DEBUG.jsonl", "SESSION.md"]
            }
        )
        # Debug: Log generated paths and file sizes
        self.log_debug(
            "Session files initialized",
            "INFO",
            details={
                "session_id": self.current_session,
                "absolute_path": str(self.session_path.absolute()),
                "parent_dir": str(self.session_path.parent),
                "files_created": {
                    "STATE.json": os.path.getsize(self.session_path / "STATE.json") if (self.session_path / "STATE.json").exists() else 0,
                    "EVENTS.jsonl": os.path.getsize(self.session_path / "EVENTS.jsonl") if (self.session_path / "EVENTS.jsonl").exists() else 0,
                    "DEBUG.jsonl": os.path.getsize(self.session_path / "DEBUG.jsonl") if (self.session_path / "DEBUG.jsonl").exists() else 0,
                    "SESSION.md": os.path.getsize(self.session_path / "SESSION.md") if (self.session_path / "SESSION.md").exists() else 0
                }
            }
        )
    
    def plan_workers(self, task_description: str, complexity_level: int, session_id: str) -> Dict[str, Any]:
        """Plan worker allocation using intelligent Queen decision-making"""
        # Analyze task for domain keywords and requirements
        task_lower = task_description.lower()
        workers_needed = []
        task_analysis = self._analyze_task_requirements(task_description, complexity_level)
        
        # Intelligent domain-based worker selection
        # Security and performance analysis needs
        if any(word in task_lower for word in ['security', 'vulnerability', 'audit', 'penetration']):
            workers_needed.append('analyzer-worker')
        elif any(word in task_lower for word in ['performance', 'optimize', 'speed', 'efficiency']):
            workers_needed.append('analyzer-worker')
        elif 'analyze' in task_lower and 'analyzer-worker' not in workers_needed:
            workers_needed.append('analyzer-worker')
        
        # Architecture and design needs
        if any(word in task_lower for word in ['architecture', 'design', 'structure', 'refactor']):
            workers_needed.append('architect-worker')
        elif any(word in task_lower for word in ['pattern', 'scalability', 'system design']):
            workers_needed.append('architect-worker')
        
        # Backend development needs
        if any(word in task_lower for word in ['api', 'endpoint', 'backend', 'server']):
            workers_needed.append('backend-worker')
        elif any(word in task_lower for word in ['database', 'schema', 'migration', 'query']):
            workers_needed.append('backend-worker')
        elif any(word in task_lower for word in ['service', 'microservice', 'business logic']):
            workers_needed.append('backend-worker')
        
        # Frontend development needs
        if any(word in task_lower for word in ['ui', 'ux', 'frontend', 'component']):
            workers_needed.append('frontend-worker')
        elif any(word in task_lower for word in ['client', 'interface', 'react', 'vue', 'angular']):
            workers_needed.append('frontend-worker')
        elif any(word in task_lower for word in ['styling', 'css', 'responsive', 'layout']):
            workers_needed.append('frontend-worker')
        
        # Testing needs
        if any(word in task_lower for word in ['test', 'testing', 'qa', 'quality']):
            workers_needed.append('test-worker')
        elif any(word in task_lower for word in ['coverage', 'validation', 'unit test', 'integration']):
            workers_needed.append('test-worker')
        elif complexity_level >= 3:  # Complex tasks always need testing
            if 'test-worker' not in workers_needed:
                workers_needed.append('test-worker')
        
        # DevOps and infrastructure needs
        if any(word in task_lower for word in ['deploy', 'deployment', 'infrastructure', 'docker']):
            workers_needed.append('devops-worker')
        elif any(word in task_lower for word in ['ci', 'cd', 'pipeline', 'kubernetes', 'aws']):
            workers_needed.append('devops-worker')
        
        # Queen's intelligent decision: Add workers based on task complexity and interdependencies
        workers_needed = self._apply_intelligent_worker_selection(
            workers_needed, task_analysis, complexity_level
        )
        
        # Remove duplicates while preserving order
        workers_needed = list(dict.fromkeys(workers_needed))
        
        # Log intelligent worker selection with detailed rationale
        self.log_event(
            event_type="worker_selection_completed",
            details={
                "workers_selected": workers_needed,
                "selection_rationale": task_analysis.get('rationale', 'Intelligent task analysis'),
                "task_domains": task_analysis.get('domains', []),
                "complexity_factors": task_analysis.get('complexity_factors', []),
                "total_workers": len(workers_needed),
                "selection_method": "intelligent_queen_decision"
            }
        )
        
        # Create worker configurations
        worker_configs = []
        all_assignments = {}  # Track all assignments for consolidated logging
        
        for worker in workers_needed:
            config = self._create_worker_config(worker, task_description, complexity_level)
            worker_configs.append(config)
            
            # Collect assignment details for consolidated logging
            all_assignments[worker] = {
                "task": config["task_description"],
                "focus_areas": config.get("specific_focus", []),
                "priority": config["priority"],
                "timeout": config["timeout"],
                "dependencies": config.get("dependencies", [])
            }
        
        # Log ALL task assignments in a single consolidated event
        self.log_event(
            event_type="all_tasks_assigned",
            details={
                "total_workers": len(workers_needed),
                "workers": workers_needed,
                "assignments": all_assignments,
                "complexity_level": complexity_level,
                "status": "all_workers_configured"
            }
        )
        
        # Debug: Log technical details about worker configuration
        self.log_debug(
            "Worker configuration completed",
            "INFO",
            details={
                "config_count": len(worker_configs),
                "total_timeout_seconds": sum(c["timeout"] for c in worker_configs),
                "priority_distribution": {
                    f"priority_{p}": len([c for c in worker_configs if c["priority"] == p])
                    for p in set(c["priority"] for c in worker_configs)
                },
                "dependency_graph": {
                    w: c.get("dependencies", []) for w, c in zip(workers_needed, worker_configs)
                }
            }
        )
        
        return {
            "workers": workers_needed,
            "configs": worker_configs,
            "complexity_level": complexity_level
        }
    
    def _create_worker_config(self, worker_type: str, task_description: str, complexity_level: int) -> Dict[str, Any]:
        """Create configuration for a specific worker"""
        # Worker-specific task descriptions
        worker_tasks = {
            "analyzer-worker": f"Analyze security, performance, and code quality for: {task_description}",
            "architect-worker": f"Review architecture, design patterns, and scalability for: {task_description}",
            "backend-worker": f"Examine backend implementation, APIs, and data layer for: {task_description}",
            "frontend-worker": f"Review UI/UX implementation and client-side code for: {task_description}",
            "test-worker": f"Assess testing strategy, coverage, and quality assurance for: {task_description}",
            "devops-worker": f"Evaluate infrastructure, deployment, and CI/CD for: {task_description}"
        }
        
        # Worker focus areas
        worker_focus = {
            "analyzer-worker": ["security", "performance", "quality", "vulnerabilities"],
            "architect-worker": ["design", "patterns", "scalability", "architecture"],
            "backend-worker": ["api", "database", "server", "business-logic"],
            "frontend-worker": ["ui", "ux", "client", "components"],
            "test-worker": ["testing", "coverage", "qa", "validation"],
            "devops-worker": ["infrastructure", "deployment", "ci-cd", "monitoring"]
        }
        
        # Calculate timeout based on complexity
        timeout_map = {1: 900, 2: 600, 3: 300, 4: 120}
        timeout = timeout_map.get(complexity_level, 300)
        
        return {
            "worker_type": worker_type,
            "task_description": worker_tasks.get(worker_type, task_description),
            "specific_focus": worker_focus.get(worker_type, []),
            "priority": self._calculate_priority(worker_type, complexity_level),
            "timeout": timeout,
            "dependencies": self._get_dependencies(worker_type)
        }
    
    def _analyze_task_requirements(self, task_description: str, complexity_level: int) -> Dict[str, Any]:
        """Analyze task to determine requirements and domains"""
        task_lower = task_description.lower()
        analysis = {
            'domains': [],
            'complexity_factors': [],
            'rationale': '',
            'requires_coordination': False,
            'estimated_scope': 'single' if complexity_level == 1 else 'multi'
        }
        
        # Identify primary domains
        if 'full' in task_lower or 'entire' in task_lower or 'comprehensive' in task_lower:
            analysis['domains'].append('full-stack')
            analysis['requires_coordination'] = True
        
        if 'security' in task_lower or 'vulnerability' in task_lower:
            analysis['domains'].append('security')
        
        if 'performance' in task_lower or 'optimize' in task_lower:
            analysis['domains'].append('performance')
        
        if 'api' in task_lower or 'backend' in task_lower:
            analysis['domains'].append('backend')
        
        if 'ui' in task_lower or 'frontend' in task_lower:
            analysis['domains'].append('frontend')
        
        if 'test' in task_lower or 'quality' in task_lower:
            analysis['domains'].append('testing')
        
        if 'deploy' in task_lower or 'infrastructure' in task_lower:
            analysis['domains'].append('devops')
        
        # Analyze complexity factors
        if complexity_level >= 3:
            analysis['complexity_factors'].append('multi-system-integration')
            analysis['requires_coordination'] = True
        
        if 'migration' in task_lower or 'upgrade' in task_lower:
            analysis['complexity_factors'].append('data-migration')
        
        if 'real-time' in task_lower or 'websocket' in task_lower:
            analysis['complexity_factors'].append('real-time-communication')
        
        if 'scale' in task_lower or 'scalability' in task_lower:
            analysis['complexity_factors'].append('scalability-requirements')
        
        # Generate rationale
        domain_str = ', '.join(analysis['domains']) if analysis['domains'] else 'general'
        complexity_str = ', '.join(analysis['complexity_factors']) if analysis['complexity_factors'] else 'standard'
        
        analysis['rationale'] = (
            f"Queen intelligence selected workers based on identified domains ({domain_str}) "
            f"with complexity factors ({complexity_str}) for level {complexity_level} task. "
            f"Coordination required: {analysis['requires_coordination']}"
        )
        
        return analysis
    
    def _apply_intelligent_worker_selection(self, initial_workers: List[str], 
                                           task_analysis: Dict[str, Any], 
                                           complexity_level: int) -> List[str]:
        """Apply Queen's intelligence to refine worker selection"""
        workers = initial_workers.copy()
        
        # Level 1: Minimal workers, only what's absolutely needed
        if complexity_level == 1:
            # If no workers selected, pick the most relevant one
            if not workers:
                if 'backend' in task_analysis['domains']:
                    workers.append('backend-worker')
                elif 'frontend' in task_analysis['domains']:
                    workers.append('frontend-worker')
                else:
                    workers.append('analyzer-worker')  # Default to analyzer for investigation
        
        # Level 2: Add complementary workers for better coverage
        elif complexity_level == 2:
            # Ensure we have at least one implementation worker
            has_impl = any(w in workers for w in ['backend-worker', 'frontend-worker'])
            if not has_impl and not workers:
                workers.append('backend-worker')  # Default implementation worker
            
            # Add analyzer if we have implementation but no analysis
            if has_impl and 'analyzer-worker' not in workers:
                workers.append('analyzer-worker')
        
        # Level 3: Comprehensive coverage with coordination
        elif complexity_level == 3:
            # Ensure architecture planning for complex tasks
            if 'architect-worker' not in workers and task_analysis['requires_coordination']:
                workers.insert(0, 'architect-worker')  # Architect goes first for planning
            
            # Ensure testing for complex implementations
            if any(w in workers for w in ['backend-worker', 'frontend-worker']):
                if 'test-worker' not in workers:
                    workers.append('test-worker')
            
            # Add analyzer for complex tasks if not present
            if 'analyzer-worker' not in workers and len(workers) < 4:
                workers.append('analyzer-worker')
        
        # Level 4: Full team with all necessary specialists
        elif complexity_level >= 4:
            # Start with architect for complex planning
            if 'architect-worker' not in workers:
                workers.insert(0, 'architect-worker')
            
            # Ensure all critical workers for complex tasks
            critical_workers = []
            if task_analysis['requires_coordination']:
                critical_workers = ['architect-worker', 'analyzer-worker']
            
            # Add implementation workers if dealing with full-stack
            if 'full-stack' in task_analysis['domains']:
                if 'backend-worker' not in workers:
                    workers.append('backend-worker')
                if 'frontend-worker' not in workers:
                    workers.append('frontend-worker')
            
            # Always include testing and analysis for level 4
            if 'test-worker' not in workers:
                workers.append('test-worker')
            if 'analyzer-worker' not in workers:
                workers.append('analyzer-worker')
            
            # Add DevOps for deployment considerations
            if 'devops' in task_analysis['domains'] and 'devops-worker' not in workers:
                workers.append('devops-worker')
        
        return workers
    
    def _calculate_priority(self, worker_type: str, complexity_level: int) -> int:
        """Calculate worker priority based on type and complexity"""
        base_priority = {
            "analyzer-worker": 1,
            "architect-worker": 1,
            "backend-worker": 2,
            "frontend-worker": 2,
            "test-worker": 3,
            "devops-worker": 3
        }
        return base_priority.get(worker_type, 2)
    
    def _get_dependencies(self, worker_type: str) -> List[str]:
        """Get worker dependencies"""
        dependencies = {
            "frontend-worker": ["backend-worker"],
            "test-worker": ["backend-worker", "frontend-worker"],
            "devops-worker": ["backend-worker", "test-worker"]
        }
        return dependencies.get(worker_type, [])
    
    def create_worker_prompts(self, worker_configs: List[Dict[str, Any]], session_id: str) -> List[str]:
        """Create prompt files for all workers and log ONCE when complete"""
        if not self.session_path:
            self.log_debug(
                "create_worker_prompts failed - no active session",
                "ERROR",
                details={
                    "session_id": session_id,
                    "worker_count": len(worker_configs),
                    "session_path": str(self.session_path) if self.session_path else None,
                    "error": "No active session"
                }
            )
            raise ValueError("No active session")
        
        prompt_files = []
        prompts_dir = self.session_path / "workers" / "prompts"
        
        for config in worker_configs:
            worker_type = config["worker_type"]
            prompt_file = prompts_dir / f"{worker_type}.prompt"
            
            prompt_content = f"""# Worker: {worker_type}
# Session: {session_id}
# Generated: {datetime.now().isoformat()}

## Task
{config['task_description']}

## Focus Areas
{json.dumps(config['specific_focus'], indent=2)}

## Context
- Session ID: {session_id}
- Priority: {config['priority']}
- Timeout: {config['timeout']} seconds
- Dependencies: {json.dumps(config.get('dependencies', []))}

## Instructions
1. Analyze the assigned domain thoroughly
2. Generate detailed notes and findings FIRST
3. Create structured JSON output based on your analysis
4. Ensure all findings are evidence-based
5. Log progress to session DEBUG.jsonl
6. Save outputs to:
   - workers/decisions/{worker_type}-analysis.md (detailed notes)
   - workers/json/{worker_type}.json (structured data)

## Output Requirements
- Detailed markdown analysis in decisions folder
- Structured JSON in json folder
- Progress events in EVENTS.jsonl (append only)
- Debug information in DEBUG.jsonl (append only)
"""
            
            with open(prompt_file, 'w') as f:
                f.write(prompt_content)
            
            prompt_files.append(str(prompt_file))
        
        # Log ONCE after ALL prompts are created
        self.log_event(
            event_type="prompts_created",
            details={
                "total_prompts": len(prompt_files),
                "workers": [c["worker_type"] for c in worker_configs],
                "prompt_files": prompt_files,
                "status": "all_prompts_generated"
            }
        )
        
        # Debug: Log technical details about prompt files
        self.log_debug(
            "Prompt generation completed",
            "INFO",
            details={
                "prompts_directory": str(prompts_dir),
                "file_count": len(prompt_files),
                "file_sizes": {
                    os.path.basename(f): os.path.getsize(f) if os.path.exists(f) else 0
                    for f in prompt_files
                },
                "total_size_bytes": sum(
                    os.path.getsize(f) if os.path.exists(f) else 0
                    for f in prompt_files
                )
            }
        )
        
        return prompt_files
    
    def generate_spawn_instructions(self, worker_configs: List[Dict[str, Any]], prompt_files: List[str], 
                                   session_id: str, task_description: str, complexity_level: int) -> Dict[str, Any]:
        """Generate spawn instructions for Claude Code to execute"""
        workers_to_spawn = []
        
        for config, prompt_file in zip(worker_configs, prompt_files):
            workers_to_spawn.append({
                "worker_type": config["worker_type"],
                "task_description": config["task_description"],
                "specific_focus": config["specific_focus"],
                "priority": config["priority"],
                "prompt_file": prompt_file,
                "timeout": config["timeout"]
            })
        
        return {
            "coordination_action": "spawn_workers",
            "session_id": session_id,
            "task": task_description,
            "complexity_level": complexity_level,
            "workers_to_spawn": workers_to_spawn,
            "session_path": str(self.session_path),
            "total_workers": len(workers_to_spawn)
        }
    
    def update_state(self, updates: Dict[str, Any]) -> None:
        """Atomically update STATE.json"""
        if not self.session_path:
            self.log_debug(
                "update_state failed - no active session",
                "ERROR",
                details={
                    "updates": updates,
                    "session_path": str(self.session_path) if self.session_path else None,
                    "error": "No active session"
                }
            )
            raise ValueError("No active session")
        
        state_file = self.session_path / "STATE.json"
        
        # Read current state
        with open(state_file, 'r') as f:
            state = json.load(f)
        
        # Apply updates
        state.update(updates)
        state["update_count"] = state.get("update_count", 0) + 1
        state["last_updated"] = datetime.now().isoformat()
        
        # Write atomically
        temp_file = state_file.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(state, f, indent=2)
        
        temp_file.replace(state_file)
    
    def validate_session_structure(self) -> bool:
        """Validate that all required session files and directories exist"""
        if not self.session_path:
            return False
        
        required_files = [
            self.session_path / "STATE.json",
            self.session_path / "EVENTS.jsonl",
            self.session_path / "DEBUG.jsonl",
            self.session_path / "SESSION.md"
        ]
        
        required_dirs = [
            self.session_path / "workers",
            self.session_path / "workers" / "json",
            self.session_path / "workers" / "prompts",
            self.session_path / "workers" / "decisions"
        ]
        
        validation_errors = []
        
        for file in required_files:
            if not file.exists():
                validation_errors.append(f"Missing file: {file.name}")
                self.log_debug(
                    "Validation error: Missing required file",
                    "ERROR",
                    details={
                        "file_path": str(file),
                        "expected_type": "file",
                        "parent_exists": file.parent.exists()
                    }
                )
        
        for dir in required_dirs:
            if not dir.exists():
                validation_errors.append(f"Missing directory: {dir.name}")
                self.log_debug(
                    "Validation error: Missing required directory",
                    "ERROR",
                    details={
                        "directory_path": str(dir),
                        "expected_type": "directory",
                        "parent_exists": dir.parent.exists()
                    }
                )
        
        if validation_errors:
            self.log_debug(
                "Session structure validation failed",
                "ERROR",
                details={
                    "error_count": len(validation_errors),
                    "errors": validation_errors
                }
            )
            return False
        
        # Log successful validation with technical details
        self.log_debug(
            "Session structure validation passed",
            "INFO",
            details={
                "files_validated": len(required_files),
                "directories_validated": len(required_dirs),
                "session_path": str(self.session_path),
                "total_size_bytes": sum(
                    os.path.getsize(f) if f.exists() else 0
                    for f in required_files
                )
            }
        )
        return True
    
    def _generate_session_markdown(self, session_id: str, task_description: str, complexity_level: int) -> str:
        """Generate rich SESSION.md from template"""
        timestamp = datetime.now().isoformat()
        
        # Determine task type from description
        task_lower = task_description.lower()
        task_type = "maintenance-task"  # default
        if any(word in task_lower for word in ['bug', 'fix', 'error', 'issue', 'broken']):
            task_type = "bug-investigation"
        elif any(word in task_lower for word in ['feature', 'add', 'implement', 'create', 'new']):
            task_type = "feature-development"
        elif any(word in task_lower for word in ['integrate', 'integration', 'connect', 'api']):
            task_type = "integration-project"
        elif any(word in task_lower for word in ['research', 'investigate', 'analyze', 'study']):
            task_type = "research-project"
        
        # Extract task title (first 50 chars or first sentence)
        task_title = task_description.split('.')[0][:50]
        if len(task_title) == 50:
            task_title += "..."
        
        # Calculate duration based on complexity
        duration_map = {
            1: "15-30 minutes",
            2: "30-60 minutes", 
            3: "1-3 hours",
            4: "3-8 hours"
        }
        duration = duration_map.get(complexity_level, "2-4 hours")
        
        # Generate priority
        priority = "high" if complexity_level >= 3 else "medium" if complexity_level == 2 else "normal"
        
        # Build the rich session markdown
        session_md = f"""# {task_title}

**Session ID**: {session_id}  
**Created**: {timestamp}  
**Status**: level_{complexity_level}_initialization  
**Type**: {task_type}
**Complexity Level**: {complexity_level}
**Estimated Duration**: {duration}  
**Priority**: {priority}

## Original Request
{task_description}

## Task Analysis & Scope

### Primary Objective
**Goal**: {task_description.split('.')[0] if '.' in task_description else task_description[:100]}
**Success Measure**: Task completed as specified with all quality gates passed

### Requirements & Acceptance Criteria
"""
        
        if complexity_level >= 2:
            session_md += f"""
**User Story**: As a developer, I want {task_description[:50]}... so that the system functions as intended

**Acceptance Criteria**:
- [ ] Primary objective completed
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Code review completed
"""
        
        if task_type == "bug-investigation":
            session_md += f"""

**Bug Details**:
- **Steps to Reproduce**: See task description
- **Expected vs Actual**: System should function correctly vs current issue
- **Environment**: Production/Development environment
"""
        
        session_md += """

### Technical Scope
**Systems/Components Affected**:
"""
        
        if complexity_level >= 2:
            session_md += """
- **Backend**: API endpoints, business logic, database operations
- **Frontend**: UI components, state management, user interactions  
- **Database**: Schema changes, migrations, query optimizations
- **Testing**: Unit tests, integration tests, end-to-end tests
- **Infrastructure**: Deployment, monitoring, configuration
"""
        else:
            session_md += """
- **Primary Component**: Main system component affected
- **Secondary Impacts**: Related systems that may be impacted
"""
        
        session_md += """

## Research & Context Loading

### Research Requirements
"""
        
        if complexity_level == 1:
            session_md += """
**Pattern Library Review** (Minimal Research):
- [ ] Check existing similar patterns in codebase
- [ ] Validate against current project conventions
- [ ] Quick technology lookup if needed
"""
        elif complexity_level == 2:
            session_md += """
**Targeted Research** (Quick Research):
- [ ] Context7 research on primary technology
- [ ] Best practices for task type
- [ ] Security/performance considerations
- [ ] Integration patterns with existing architecture
"""
        else:
            session_md += """
**Comprehensive Research** (Multi-Domain):
- [ ] Context7 research across multiple domains
- [ ] Architecture pattern analysis
- [ ] Security compliance requirements
- [ ] Performance optimization strategies
- [ ] Cross-system integration approaches
- [ ] SmartWalletFX-specific financial/crypto considerations
"""
        
        session_md += f"""

### Context Loading Requirements
**Level {complexity_level} Context**: """
        
        if complexity_level == 1:
            session_md += "Single domain tags, minimal session structure"
        elif complexity_level == 2:
            session_md += "Primary domain + related tags, standard session structure"
        else:
            session_md += "Multi-domain tags, comprehensive session structure, cross-worker coordination"
        
        session_md += f"""

## Worker Assignment & Coordination

### Current Phase: initialization
Session initialization and worker planning phase

### Worker Status
"""
        
        if complexity_level == 1:
            session_md += """- **Primary Worker**: pending - Single worker to complete task
"""
        elif complexity_level == 2:
            session_md += """- **Research Worker**: pending - Targeted research for domain
- **Primary Worker**: pending - Implementation lead
- **Test Worker**: pending - Validation and testing
"""
        else:
            session_md += """- **Researcher Worker**: pending - Multi-domain Context7 research coordination
- **Service Architect**: pending - Architecture planning and scalability design
- **Backend Worker**: pending - Backend implementation and API development
- **Frontend Worker**: pending - UI implementation and user experience
- **Designer Worker**: pending - UX design and design system integration
- **Test Worker**: pending - Comprehensive testing strategy and implementation
- **Analyzer Worker**: pending - Security analysis and performance optimization
- **DevOps Worker**: pending - Infrastructure and deployment management
"""
        
        session_md += """

### Coordination Configuration
"""
        
        if complexity_level == 1:
            session_md += "**Escalation**: Standard 15min timeouts, minimal coordination"
        elif complexity_level == 2:
            session_md += "**Escalation**: 10min timeouts, basic EVENTS.jsonl coordination"
        else:
            timeout = "5min" if complexity_level == 3 else "2min"
            session_md += f"""**Escalation**: {timeout} timeouts, full hive-mind coordination
**Communication**: Active EVENTS.jsonl monitoring and cross-worker notifications"""
        
        session_md += f"""

## Implementation Strategy

### Approach
"""
        
        if task_type == "feature-development":
            session_md += "**Development Approach**: Incremental feature implementation with continuous validation"
        elif task_type == "bug-investigation":
            session_md += "**Investigation Approach**: Systematic analysis with root cause identification"
        elif task_type == "maintenance-task":
            session_md += "**Maintenance Approach**: Careful incremental updates with regression prevention"
        elif task_type == "integration-project":
            session_md += "**Integration Approach**: API-first with comprehensive error handling"
        else:
            session_md += "**Research Approach**: Comprehensive investigation with documentation"
        
        session_md += """

### Phase Breakdown
"""
        
        if complexity_level == 1:
            session_md += """1. **Direct Implementation**: Single worker completes task with basic validation
2. **Basic Testing**: Verify functionality and no regressions
3. **Simple Archive**: Document completion and any lessons learned
"""
        elif complexity_level == 2:
            session_md += """1. **Research Phase**: Targeted research and pattern analysis
2. **Planning Phase**: Create implementation plan with task breakdown
3. **Implementation Phase**: Execute plan with basic coordination
4. **Validation Phase**: Test and validate implementation
5. **Archive Phase**: Document results and extract patterns
"""
        else:
            session_md += """1. **Research Phase**: Comprehensive multi-domain research and synthesis
2. **Architecture Phase**: System design and integration planning
3. **Implementation Phase**: Parallel worker execution with coordination
4. **Integration Phase**: System integration and cross-component testing
5. **Validation Phase**: Security review, performance testing, quality assurance
6. **Archive Phase**: Comprehensive documentation and pattern library contribution
"""
        
        session_md += """

## Quality Gates & Success Criteria

### Quality Gates Checklist
"""
        
        if complexity_level == 1:
            session_md += """- [ ] **Implementation Complete**: Task objective accomplished
- [ ] **Basic Testing**: Functionality verified and no obvious regressions
- [ ] **Documentation**: Minimal documentation updated
"""
        elif complexity_level == 2:
            session_md += """- [ ] **Research Complete**: Targeted research findings applied
- [ ] **Implementation Complete**: All requirements implemented
- [ ] **Testing Complete**: Comprehensive testing with passing results
- [ ] **Quality Review**: Code quality and standards compliance
- [ ] **Documentation**: Technical documentation updated
"""
        else:
            session_md += """- [ ] **Research Phase**: Comprehensive research completed and synthesized
- [ ] **Architecture Phase**: System design validated and documented
- [ ] **Implementation Phase**: All components developed with research backing
- [ ] **Integration Phase**: Cross-system integration validated
- [ ] **Security Review**: Security analysis and validation completed
- [ ] **Performance Validation**: Performance requirements met and benchmarked
- [ ] **Documentation**: Comprehensive technical and user documentation
- [ ] **Deployment Ready**: Feature/fix ready for production deployment
"""
        
        session_md += f"""

### Success Criteria
"""
        
        if task_type == "feature-development":
            session_md += """- [ ] Feature implements all acceptance criteria exactly as specified
- [ ] User experience validated through design review
- [ ] Performance benchmarks met or exceeded
"""
        elif task_type == "bug-investigation":
            session_md += """- [ ] Bug no longer reproducible with original steps
- [ ] Fix addresses root cause, not just symptoms
- [ ] No regressions introduced by the fix
"""
        elif task_type == "maintenance-task":
            session_md += """- [ ] Maintenance objective completed as specified
- [ ] No breaking changes introduced to existing functionality
- [ ] Code quality metrics maintained or improved
"""
        elif task_type == "integration-project":
            session_md += """- [ ] Integration functional for all required features
- [ ] Proper error handling and recovery implemented
- [ ] Security review passed for external integrations
"""
        
        session_md += """

**Universal Success Criteria**:
- [ ] Code follows established project standards and patterns
- [ ] Comprehensive test coverage with passing tests
- [ ] Security considerations addressed appropriately
- [ ] Technical documentation complete and accurate

## Risk Assessment & Mitigation

### Risk Analysis
"""
        
        risk_level = "high" if complexity_level >= 3 else "medium" if complexity_level == 2 else "low"
        session_md += f"""**Risk Level**: {risk_level} (based on complexity and scope)

**Identified Risks**:
"""
        
        if complexity_level >= 2:
            session_md += """- **Technical Risk**: Complexity of implementation or unknown factors
- **Integration Risk**: Cross-system dependencies or compatibility issues
- **Performance Risk**: Scalability concerns or resource constraints
- **Security Risk**: Potential vulnerabilities or data exposure

### Mitigation Strategies
- [ ] Incremental implementation with continuous validation
- [ ] Comprehensive testing at each phase
- [ ] Rollback plan prepared if issues arise
- [ ] Security review before deployment
"""
        else:
            session_md += """- **Technical Risk**: Minimal due to limited scope
- **Integration Risk**: Low impact on other systems

### Mitigation Strategies
- [ ] Basic testing before completion
- [ ] Quick rollback if needed
"""
        
        session_md += f"""

## Progress Tracking

### Timeline Tracking
"""
        
        if complexity_level == 1:
            session_md += f"""- **Task Start**: {timestamp}
- **Completion Target**: Within {duration}
"""
        else:
            session_md += f"""- **Research Phase**: {timestamp} → TBD
- **Implementation Phase**: TBD → TBD
- **Validation Phase**: TBD → TBD
- **Final Completion**: Target within {duration}
"""
        
        session_md += f"""

### Archon Integration
**Archon Project ID**: smartwalletfx-{session_id[:8]}
**Task IDs**: TBD
**Status Sync**: Automatic updates configured

### Session Metrics
- **Research Duration**: 0 minutes
- **Implementation Tasks**: 0 created, 0 completed
- **Worker Coordination Events**: 0
- **Quality Gate Completions**: 0/{3 if complexity_level == 1 else 5 if complexity_level == 2 else 8}

## Knowledge Capture

### Patterns & Learnings
"""
        
        if complexity_level >= 2:
            session_md += """**Successful Patterns**:
- [ ] Patterns identified during implementation
- [ ] Reusable solutions discovered

**Lessons Learned**:
- [ ] Challenges encountered and solutions
- [ ] Process improvements identified

**Pattern Library Contributions**:
- [ ] Reusable patterns to be documented
"""
        else:
            session_md += """**Patterns**: To be identified during implementation
**Lessons**: To be captured upon completion
"""
        
        if complexity_level >= 3:
            session_md += """

### Memory Bank Updates
**Memory Bank Contributions**:
- [ ] Technical decisions with rationale
- [ ] Architecture patterns and trade-offs
- [ ] Performance optimizations discovered
- [ ] Security considerations and solutions
"""
        
        session_md += f"""

## Phase History
- **initialization**: {timestamp} - Session created, workers being planned

---

*This session adapts to complexity level {complexity_level} and task type {task_type} for optimal hive-mind coordination*
"""
        
        return session_md
    
    def _generate_state_json(self, session_id: str, task_description: str, complexity_level: int) -> Dict[str, Any]:
        """Generate complete STATE.json from template"""
        timestamp = datetime.now().isoformat()
        
        # Build complete state structure following template
        state = {
            "session_id": session_id,
            "task": task_description,  # Changed from task_description to task
            "status": "research_phase",  # Start with research phase
            "created_at": timestamp,
            "updated_at": timestamp,
            "current_phase": {
                "name": "research_phase",
                "started_at": timestamp,
                "progress_percentage": 0,
                "next_action": "Queen: Delegate Context7 research to appropriate workers"
            },
            "research_complete": False,
            "research_synthesis_file": "RESEARCH_SYNTHESIS.md",
            "context": {
                "tokens_used": 0,
                "estimated_remaining": 100000,
                "can_resume": True,
                "resume_point": "Session initialization complete, ready for research delegation",
                "resume_count": 0
            },
            "workers": {
                "researcher-worker": {
                    "status": "pending",
                    "task": "Multi-domain research coordination",
                    "research_domains": [],
                    "completed_domains": []
                },
                "backend-worker": {
                    "status": "pending",
                    "task": "Backend-specific research and implementation",
                    "research_domains": [],
                    "current_task": None
                },
                "frontend-worker": {
                    "status": "pending",
                    "task": "Frontend-specific research and implementation",
                    "research_domains": [],
                    "current_task": None
                },
                "service-architect": {
                    "status": "pending",
                    "task": "Architecture research and system design",
                    "research_domains": [],
                    "current_task": None
                },
                "analyzer-worker": {
                    "status": "pending",
                    "task": "Security and performance research",
                    "research_domains": [],
                    "current_task": None
                },
                "test-worker": {
                    "status": "pending",
                    "task": "Testing strategy research and implementation",
                    "research_domains": [],
                    "current_task": None
                },
                "devops-worker": {
                    "status": "pending",
                    "task": "Infrastructure research and deployment",
                    "research_domains": [],
                    "current_task": None
                },
                "designer-worker": {
                    "status": "pending",
                    "task": "UX research and design implementation",
                    "research_domains": [],
                    "current_task": None
                }
            },
            "research_progress": {
                "domains_identified": [],
                "domains_assigned": [],
                "domains_completed": [],
                "synthesis_status": "pending",
                "conflicts_identified": [],
                "conflicts_resolved": []
            },
            "implementation_progress": {
                "tasks_created": 0,
                "tasks_completed": 0,
                "workers_active": 0,
                "blocking_issues": 0
            },
            "quality_gates": {
                "research_phase_complete": False,
                "implementation_plan_created": False,
                "security_review_complete": False,
                "performance_validation_complete": False,
                "pattern_library_updated": False
            },
            "metrics": {
                "session_duration_hours": 0,
                "research_duration_minutes": 0,
                "implementation_duration_hours": 0,
                "worker_coordination_events": 1,
                "successful_task_completions": 0,
                "pattern_contributions": 0
            },
            "session_metadata": {
                "hive_mind_version": "1.0",
                "research_methodology": "context7_first",
                "coordination_protocol": "file_based",
                "quality_assurance": "multi_gate",
                "resumption_capability": "full_state",
                "complexity_level": complexity_level
            },
            # Additional fields for backward compatibility
            "complexity_level": complexity_level,
            "worker_configs": {},
            "coordination_status": {
                "phase": "initialization",
                "workers_spawned": [],
                "workers_completed": [],
                "synthesis_ready": False
            },
            "update_count": 0,
            "last_updated": timestamp
        }
        
        return state


# Helper class for workers to use
class WorkerLogger:
    """Helper class for workers to properly log to session files"""
    
    def __init__(self, session_path: Path, worker_name: str):
        self.session_path = Path(session_path)
        self.worker_name = worker_name
        self.session_id = self.session_path.name
    
    def log_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """Append event to EVENTS.jsonl - NEVER overwrite, always append"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "worker": self.worker_name,
            "session_id": self.session_id,
            "details": details
        }
        
        # CRITICAL: Append mode + ensure file exists + error handling
        events_file = self.session_path / "EVENTS.jsonl"
        if not events_file.exists():
            events_file.touch()  # Create if missing
        
        try:
            with open(events_file, 'a') as f:
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            # If logging fails, don't break the worker
            print(f"WARNING: Failed to log event {event_type} for {self.worker_name}: {e}")
    
    def log_debug(self, message: str, level: str = "INFO", details: Any = None) -> None:
        """Append debug log to DEBUG.jsonl - NEVER overwrite, always append"""
        debug_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "agent": self.worker_name,
            "message": message,
            "details": details
        }
        
        # CRITICAL: Append mode + ensure file exists + error handling
        debug_file = self.session_path / "DEBUG.jsonl"
        if not debug_file.exists():
            debug_file.touch()  # Create if missing
        
        try:
            with open(debug_file, 'a') as f:
                f.write(json.dumps(debug_entry) + '\n')
        except Exception as e:
            # If logging fails, don't break the worker
            print(f"WARNING: Failed to log debug for {self.worker_name}: {e}")
    
    def save_analysis(self, content: str) -> None:
        """Save analysis markdown to decisions folder - MANDATORY for all workers"""
        output_file = self.session_path / "workers" / "decisions" / f"{self.worker_name}-analysis.md"
        output_file.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
        with open(output_file, 'w') as f:
            f.write(content)
        
        # Debug: Log technical details about saved analysis
        self.log_debug(
            "Analysis document saved",
            "INFO",
            details={
                "file_path": str(output_file),
                "file_size_bytes": os.path.getsize(output_file),
                "content_length": len(content),
                "line_count": content.count('\n')
            }
        )
    
    def save_json(self, data: Dict[str, Any]) -> None:
        """Save structured JSON to json folder - MANDATORY for all workers"""
        output_file = self.session_path / "workers" / "json" / f"{self.worker_name}.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Debug: Log technical details about saved JSON
        self.log_debug(
            "JSON output saved",
            "INFO",
            details={
                "file_path": str(output_file),
                "file_size_bytes": os.path.getsize(output_file),
                "key_count": len(data.keys()) if isinstance(data, dict) else None,
                "data_type": type(data).__name__
            }
        )


# Example usage for Queen Orchestrator
def orchestrate_task(task_description: str, complexity_level: int = 2):
    """Main orchestration function demonstrating proper protocol usage"""
    
    # Step 1: Initialize protocol
    coordinator = CoordinationProtocol()
    
    # Step 2: Generate session ID
    session_id = coordinator.generate_session_id(task_description)
    
    # Step 3: Create session structure (but don't log session_created yet)
    state = coordinator.create_session_structure(session_id, task_description, complexity_level)
    
    # Step 4: CRITICAL - Log Queen spawn FIRST (before any other events)
    coordinator.log_queen_spawn(task_description, complexity_level)
    
    # Step 5: Log session creation AFTER queen spawn
    coordinator.log_session_created()
    
    # Step 6: Plan workers (automatically logs selection)
    worker_plan = coordinator.plan_workers(task_description, complexity_level, session_id)
    
    # Step 7: Create worker prompts (logs ONCE when all complete)
    prompt_files = coordinator.create_worker_prompts(worker_plan["configs"], session_id)
    
    # Step 8: Generate spawn instructions
    spawn_instructions = coordinator.generate_spawn_instructions(
        worker_plan["configs"],
        prompt_files,
        session_id,
        task_description,
        complexity_level
    )
    
    # Step 9: Update state
    coordinator.update_state({
        "status": "workers_spawning",
        "coordination_status": {
            "phase": "execution",
            "workers_spawned": worker_plan["workers"],
            "workers_completed": [],
            "synthesis_ready": False
        }
    })
    
    # Step 10: Validate everything
    if coordinator.validate_session_structure():
        coordinator.log_debug(
            "Orchestration completed successfully",
            "INFO",
            details={
                "session_id": session_id,
                "worker_count": len(spawn_instructions["workers_to_spawn"]),
                "total_complexity_level": complexity_level,
                "spawn_instructions_size": len(json.dumps(spawn_instructions))
            }
        )
        return spawn_instructions
    else:
        coordinator.log_debug(
            "Critical: Session validation failed after orchestration",
            "ERROR",
            details={
                "session_id": session_id,
                "session_path": str(coordinator.session_path),
                "recovery_action": "Manual intervention required",
                "error": "Failed to create valid session structure"
            }
        )
        raise ValueError("Failed to create valid session structure")


if __name__ == "__main__":
    # Example usage
    result = orchestrate_task(
        "Analyze crypto-data service architecture for security and performance",
        complexity_level=3
    )
    print(json.dumps(result, indent=2))