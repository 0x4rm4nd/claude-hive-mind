#!/usr/bin/env python3
"""
Coordination Protocol Implementation 
==========================================
Handles queen-worker coordination patterns with truly dynamic worker selection.
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from .protocol_loader import BaseProtocol, ProtocolConfig

class CoordinationProtocol(BaseProtocol):
    """Manages coordination between queen and workers with scope-based selection"""
    
    # Worker capability matrix
    WORKER_CAPABILITIES = {
        "analyzer-worker": {
            "domains": ["security", "performance", "quality", "code-review"],
            "complexity_threshold": 1,
            "priority": 7
        },
        "architect-worker": {
            "domains": ["design", "scalability", "patterns", "system-architecture"],
            "complexity_threshold": 2,
            "priority": 8
        },
        "backend-worker": {
            "domains": ["api", "database", "server", "business-logic"],
            "complexity_threshold": 2,
            "priority": 6
        },
        "frontend-worker": {
            "domains": ["ui", "ux", "client", "components"],
            "complexity_threshold": 2,
            "priority": 5
        },
        "devops-worker": {
            "domains": ["infrastructure", "deployment", "ci-cd", "containers"],
            "complexity_threshold": 3,
            "priority": 6
        },
        "test-worker": {
            "domains": ["testing", "qa", "validation", "coverage"],
            "complexity_threshold": 1,
            "priority": 4
        },
        "designer-worker": {
            "domains": ["design", "ux", "visual", "wireframes"],
            "complexity_threshold": 2,
            "priority": 5
        },
        "researcher-worker": {
            "domains": ["research", "context", "documentation", "best-practices"],
            "complexity_threshold": 1,
            "priority": 3
        }
    }
    
    # Complexity affects timeouts and synthesis, NOT worker counts
    COMPLEXITY_MATRIX = {
        1: {"timeout": 900, "escalation": 15},    # 15min timeout, 15s escalation
        2: {"timeout": 600, "escalation": 10},    # 10min timeout, 10s escalation  
        3: {"timeout": 300, "escalation": 5},     # 5min timeout, 5s escalation
        4: {"timeout": 120, "escalation": 2}      # 2min timeout, 2s escalation
    }
    
    def plan_workers(self, task: str, complexity_level: int) -> Dict[str, Any]:
        """
        Plan worker deployment dynamically based on task scope analysis.
        Worker count is determined by what's mentioned in the task, NOT complexity.
        
        Examples of truly dynamic selection:
        - "Review the API" → backend-worker, analyzer-worker (2 workers)
        - "Review the API and frontend" → backend-worker, frontend-worker, analyzer-worker (3 workers)
        - "Fix typo in README" → analyzer-worker only (1 worker)
        - "Review entire system" → All relevant workers (5-7 workers)
        """
        # Get complexity parameters (for timeouts only, not worker count)
        complexity_params = self.COMPLEXITY_MATRIX.get(
            complexity_level, 
            self.COMPLEXITY_MATRIX[3]
        )
        
        # Comprehensive task analysis to understand scope
        task_analysis = self.analyze_task_scope(task)
        
        # Select workers based purely on what the task mentions/requires
        selected_workers = self.scope_based_worker_selection(task_analysis, task)
        
        # Generate worker configurations
        worker_configs = {}
        for worker in selected_workers:
            worker_configs[worker["type"]] = {
                "task_description": self.generate_contextual_task(task, worker["type"], task_analysis),
                "specific_focus": worker["focus_areas"],
                "timeout": complexity_params["timeout"],
                "escalation_timeout": complexity_params["escalation"],
                "priority": worker["priority"],
                "dependencies": self.identify_dependencies(worker["type"], selected_workers),
                "selection_reason": worker["reason"]
            }
        
        coordination_plan = {
            "complexity_level": complexity_level,
            "workers": selected_workers,
            "worker_configs": worker_configs,
            "coordination_mode": self.determine_coordination_mode(selected_workers),
            "synthesis_strategy": self.determine_synthesis_strategy(complexity_level),
            "timeout_strategy": complexity_params,
            "verification_loops": self.generate_verification_loops(selected_workers),
            "task_analysis": task_analysis  # Include for transparency
        }
        
        self.log_execution("plan_workers", coordination_plan)
        return coordination_plan
    
    def analyze_task_scope(self, task: str) -> Dict[str, Any]:
        """
        Deep analysis of task to understand what systems/components are involved.
        This determines which workers are needed based on actual task content.
        """
        task_lower = task.lower()
        
        # Track what's explicitly or implicitly mentioned
        components_detected = []
        services_mentioned = []
        
        # Backend detection - be precise
        backend_terms = [
            "backend", "server", "api", "endpoint", "route", "controller",
            "service", "business logic", "domain", "repository", "model",
            "database", "sql", "schema", "migration", "query", "orm"
        ]
        if any(term in task_lower for term in backend_terms):
            components_detected.append("backend")
        
        # Frontend detection - be precise
        frontend_terms = [
            "frontend", "ui", "user interface", "component", "view", "page",
            "react", "vue", "angular", "html", "css", "javascript", "typescript",
            "button", "form", "layout", "display", "screen", "browser", "client"
        ]
        if any(term in task_lower for term in frontend_terms):
            components_detected.append("frontend")
        
        # Infrastructure detection
        infra_terms = [
            "docker", "kubernetes", "k8s", "deploy", "deployment", "ci/cd",
            "pipeline", "infrastructure", "container", "production", "staging"
        ]
        if any(term in task_lower for term in infra_terms):
            components_detected.append("infrastructure")
        
        # Testing detection
        test_terms = [
            "test", "testing", "spec", "coverage", "unit test", "integration",
            "e2e", "jest", "pytest", "qa", "quality assurance", "validation"
        ]
        if any(term in task_lower for term in test_terms):
            components_detected.append("testing")
        
        # Security detection
        security_terms = [
            "security", "auth", "authentication", "authorization", "oauth",
            "jwt", "token", "permission", "vulnerability", "encryption"
        ]
        if any(term in task_lower for term in security_terms):
            components_detected.append("security")
        
        # Performance detection
        perf_terms = [
            "performance", "optimization", "speed", "cache", "latency",
            "slow", "bottleneck", "memory", "cpu", "profiling"
        ]
        if any(term in task_lower for term in perf_terms):
            components_detected.append("performance")
        
        # Architecture detection
        arch_terms = [
            "architecture", "pattern", "design", "scalability", "system design",
            "structure", "refactor", "restructure", "modularity"
        ]
        if any(term in task_lower for term in arch_terms):
            components_detected.append("architecture")
        
        # UX/Design detection
        design_terms = [
            "ux", "user experience", "design", "wireframe", "mockup",
            "visual", "aesthetic", "usability", "accessibility"
        ]
        if any(term in task_lower for term in design_terms):
            components_detected.append("design")
        
        # Determine action type
        action = "review"  # default
        if any(word in task_lower for word in ["build", "create", "implement", "add", "develop"]):
            action = "build"
        elif any(word in task_lower for word in ["fix", "debug", "resolve", "repair", "patch"]):
            action = "fix"
        elif any(word in task_lower for word in ["review", "analyze", "assess", "evaluate", "audit"]):
            action = "review"
        elif any(word in task_lower for word in ["refactor", "optimize", "improve", "enhance"]):
            action = "refactor"
        elif any(word in task_lower for word in ["test", "validate", "verify", "check"]):
            action = "test"
        elif any(word in task_lower for word in ["research", "investigate", "explore"]):
            action = "research"
        
        # Determine scope breadth
        scope = "targeted"
        if any(phrase in task_lower for phrase in ["entire system", "whole application", "full", "complete", "all"]):
            scope = "comprehensive"
        elif any(phrase in task_lower for phrase in ["cross-service", "multiple services", "integration"]):
            scope = "cross-service"
        elif len(components_detected) > 3:
            scope = "broad"
        elif len(components_detected) <= 1:
            scope = "narrow"
        else:
            scope = "moderate"
        
        # Check for specific service mentions (for microservices)
        if "api service" in task_lower or "/api" in task_lower:
            services_mentioned.append("api-service")
        if "frontend service" in task_lower or "/frontend" in task_lower:
            services_mentioned.append("frontend-service")
        if "sara" in task_lower:
            services_mentioned.append("sara-service")
        if "crypto" in task_lower or "crypto-data" in task_lower:
            services_mentioned.append("crypto-service")
        if "archon" in task_lower:
            services_mentioned.append("archon-service")
        
        return {
            "components": components_detected,
            "services": services_mentioned,
            "action": action,
            "scope": scope,
            "is_cross_service": len(services_mentioned) > 1 or scope == "cross-service",
            "is_comprehensive": scope in ["comprehensive", "broad"],
            "requires_coordination": len(components_detected) > 2 or scope == "cross-service"
        }
    
    def scope_based_worker_selection(self, analysis: Dict[str, Any], task: str) -> List[Dict]:
        """
        Select workers based purely on what the task mentions or requires.
        Number of workers is determined by scope, not complexity.
        
        This is the KEY method that ensures dynamic selection.
        """
        task_lower = task.lower()
        workers_needed = set()
        
        # Map components to workers
        component_worker_map = {
            "backend": "backend-worker",
            "frontend": "frontend-worker",
            "infrastructure": "devops-worker",
            "testing": "test-worker",
            "security": "analyzer-worker",
            "performance": "analyzer-worker",
            "architecture": "architect-worker",
            "design": "designer-worker"
        }
        
        # Add workers for detected components
        for component in analysis["components"]:
            if component in component_worker_map:
                workers_needed.add(component_worker_map[component])
        
        # Action-specific additions
        if analysis["action"] == "review":
            # Reviews need analyzer for quality assessment
            workers_needed.add("analyzer-worker")
        elif analysis["action"] == "build":
            # Building needs architecture guidance
            if analysis["scope"] != "narrow":
                workers_needed.add("architect-worker")
        elif analysis["action"] == "fix":
            # Fixes need analyzer to verify
            workers_needed.add("analyzer-worker")
        elif analysis["action"] == "refactor":
            # Refactoring needs both architect and analyzer
            workers_needed.add("architect-worker")
            workers_needed.add("analyzer-worker")
        elif analysis["action"] == "test":
            workers_needed.add("test-worker")
        elif analysis["action"] == "research":
            workers_needed.add("researcher-worker")
        
        # Scope-based additions
        if analysis["is_comprehensive"]:
            # Comprehensive tasks need architecture overview
            workers_needed.add("architect-worker")
            # For true full-system reviews, ensure main domains covered
            if "entire system" in task_lower or "whole application" in task_lower:
                workers_needed.update(["backend-worker", "frontend-worker", "analyzer-worker"])
        
        if analysis["is_cross_service"]:
            # Cross-service needs architecture coordination
            workers_needed.add("architect-worker")
        
        # Special case: documentation-only tasks
        if "readme" in task_lower and "typo" in task_lower and len(analysis["components"]) == 0:
            # Just need analyzer for simple doc fixes
            workers_needed = {"analyzer-worker"}
        
        # Edge case: if no workers selected, use analyzer as fallback
        if not workers_needed:
            workers_needed.add("analyzer-worker")
        
        # Convert to worker list with metadata
        selected = []
        for worker_type in workers_needed:
            if worker_type in self.WORKER_CAPABILITIES:
                capabilities = self.WORKER_CAPABILITIES[worker_type]
                selected.append({
                    "type": worker_type,
                    "focus_areas": capabilities["domains"],
                    "priority": capabilities["priority"],
                    "reason": self.get_selection_reason(worker_type, analysis, task)
                })
        
        # Sort by priority for optimal execution order
        selected.sort(key=lambda x: x["priority"], reverse=True)
        
        return selected
    
    def get_selection_reason(self, worker_type: str, analysis: Dict, task: str) -> str:
        """Generate clear reason for selecting this worker"""
        task_snippet = task[:50] + "..." if len(task) > 50 else task
        
        reasons = {
            "analyzer-worker": f"{analysis['action'].title()} quality and security analysis",
            "architect-worker": f"System design for {analysis['scope']} scope",
            "backend-worker": f"Server-side {analysis['action']} for mentioned API/backend",
            "frontend-worker": f"UI/client-side {analysis['action']} for mentioned frontend",
            "devops-worker": f"Infrastructure {analysis['action']} for deployment concerns",
            "test-worker": f"Testing and validation for {analysis['action']}",
            "designer-worker": f"UX design for {analysis['action']}",
            "researcher-worker": f"Research and context gathering"
        }
        
        return reasons.get(worker_type, f"Domain expertise for {analysis['action']}")
    
    def generate_contextual_task(self, task: str, worker_type: str, analysis: Dict) -> str:
        """Generate worker-specific task description"""
        action = analysis["action"]
        scope = analysis["scope"]
        
        templates = {
            "analyzer-worker": f"Perform {scope} {action} focusing on code quality, security, and performance for: {task}",
            "architect-worker": f"Analyze system architecture and design patterns with {scope} scope for: {task}",
            "backend-worker": f"Execute {action} on server-side components and API logic for: {task}",
            "frontend-worker": f"Handle {action} for UI components and user interface for: {task}",
            "devops-worker": f"Assess infrastructure and deployment aspects for: {task}",
            "test-worker": f"Validate testing coverage and quality assurance for: {task}",
            "designer-worker": f"Create UX improvements and visual designs for: {task}",
            "researcher-worker": f"Research context and best practices for: {task}"
        }
        
        return templates.get(worker_type, f"Perform specialized {action} for: {task}")
    
    def identify_dependencies(self, worker_type: str, all_workers: List[Dict]) -> List[str]:
        """Identify worker dependencies for coordination"""
        dependencies = []
        
        # Define dependency relationships
        dependency_map = {
            "frontend-worker": ["backend-worker", "designer-worker"],
            "backend-worker": ["architect-worker"],
            "test-worker": ["backend-worker", "frontend-worker"],
            "devops-worker": ["architect-worker", "backend-worker"]
        }
        
        if worker_type in dependency_map:
            for dep in dependency_map[worker_type]:
                if any(w["type"] == dep for w in all_workers):
                    dependencies.append(dep)
                    
        return dependencies
    
    def determine_coordination_mode(self, workers: List[Dict]) -> str:
        """Determine coordination strategy based on worker count and dependencies"""
        worker_count = len(workers)
        
        if worker_count == 1:
            return "single_worker"
        elif worker_count == 2:
            return "parallel_independent"
        elif any("dependencies" in w and w["dependencies"] for w in workers):
            return "sequential_dependent"
        else:
            return "parallel_synthesis"
    
    def determine_synthesis_strategy(self, complexity: int) -> str:
        """Determine synthesis approach based on complexity"""
        strategies = {
            1: "simple_aggregation",
            2: "weighted_synthesis",
            3: "cross_reference_analysis",
            4: "deep_integration_synthesis"
        }
        return strategies.get(complexity, "cross_reference_analysis")
    
    def generate_verification_loops(self, workers: List[Dict]) -> Dict[str, Any]:
        """Generate verification checkpoints"""
        return {
            "startup_verification": {
                "check_interval": 5,  # seconds
                "max_attempts": 3,
                "required_events": ["worker_spawned", "worker_configured", "worker_ready"]
            },
            "progress_monitoring": {
                "check_interval": 30,  # seconds
                "heartbeat_required": True,
                "stall_detection": 120  # seconds
            },
            "completion_verification": {
                "required_outputs": ["json_response", "detailed_notes"],
                "validation_checks": ["format_validation", "content_validation"]
            }
        }
    
    def coordinate_execution(self, worker_configs: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate worker execution with monitoring"""
        execution_status = {
            "started_at": datetime.now().isoformat(),
            "workers_spawned": list(worker_configs.keys()),
            "workers_completed": [],
            "workers_failed": [],
            "coordination_events": []
        }
        
        # This would contain actual coordination logic
        # Including spawn verification, progress monitoring, etc.
        
        self.log_execution("coordinate_execution", execution_status)
        return execution_status
    
    def handle_escalation(self, worker_type: str, issue: str) -> Dict[str, Any]:
        """Handle worker escalation"""
        escalation_response = {
            "timestamp": datetime.now().isoformat(),
            "worker": worker_type,
            "issue": issue,
            "action": "retry",  # or "skip", "reassign", "abort"
            "resolution": None
        }
        
        # Escalation logic based on issue type
        if "timeout" in issue.lower():
            escalation_response["action"] = "extend_timeout"
        elif "dependency" in issue.lower():
            escalation_response["action"] = "resolve_dependency"
        elif "error" in issue.lower():
            escalation_response["action"] = "retry"
            
        self.log_execution("handle_escalation", escalation_response)
        return escalation_response