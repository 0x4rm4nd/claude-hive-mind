# Worker Configuration Registry
# ============================
# Centralized configuration for all worker types with expertise, tools, outputs, and focus areas.

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