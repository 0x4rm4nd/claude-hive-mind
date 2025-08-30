# Session Template Guide

> **Purpose**: Guide for using the unified session template that automatically adapts to complexity levels (1-4) and task types. This eliminates template proliferation while ensuring appropriate structure for all hive-mind sessions.

---

## 🎯 Single Template System

### Single Template, Multiple Configurations

The `session-template.md` adapts to:
- **Complexity Levels**: 1 (simple) → 4 (complex project)
- **Task Types**: feature-development, bug-investigation, maintenance-task, integration-project, research-project
- **Research Depth**: Minimal → Comprehensive based on complexity
- **Worker Assignment**: 1 worker → Full hive-mind based on needs

### Automatic Adaptation Matrix

| Complexity | Duration | Research Depth | Workers | Coordination | Use Cases |
|------------|----------|----------------|---------|--------------|-----------|
| **Level 1** | <1 hour | Minimal | 1 worker | Basic | Simple fixes, config changes, minor updates |
| **Level 2** | 1-2 hours | Quick research | 2-3 workers | Standard | Bug fixes, single feature, targeted improvements |
| **Level 3** | 2-6 hours | Multi-domain | 2-4 workers | Fast escalation | Cross-domain features, integrations |
| **Level 4** | 6+ hours | Comprehensive | 3-8 workers | Full coordination | Major features, architecture changes |

---

## 🔧 How the Unified Template Works

### Template Configuration Process

1. **Complexity Assessment**: Queen determines Level 1-4 using task-complexity-analysis.md
2. **Task Type Detection**: Automatically identified from user request keywords
3. **Template Population**: Unified template adapts sections based on complexity/type
4. **Worker Assignment**: Template suggests appropriate worker sets

### Configuration Examples

#### Level 1 - Simple Task Configuration
```yaml
complexity_level: 1
task_type: "maintenance-task" 
worker_assignment: "single_primary_worker"
research_depth: "minimal_pattern_library"
coordination: "basic_completion_tracking"
session_structure: "minimal"
```

#### Level 3 - Cross-Domain Feature Configuration  
```yaml
complexity_level: 3
task_type: "feature-development"
worker_assignment: "multi_domain_coordination"
research_depth: "comprehensive_context7"
coordination: "fast_escalation_5min"
session_structure: "comprehensive"
```

### Automatic Section Adaptation

**Research Requirements** (adapts to complexity):
- Level 1: Pattern library review only
- Level 2: Targeted Context7 + pattern analysis  
- Level 3+: Multi-domain research + architecture analysis

**Worker Status** (adapts to complexity):
- Level 1: Single primary worker
- Level 2: Research + implementation + validation workers
- Level 3+: Full specialist team with coordination

**Quality Gates** (adapts to complexity):
- Level 1: Basic implementation + testing
- Level 2: Research + implementation + quality review
- Level 3+: Full gates including security, performance, architecture

---

## 📋 Template Usage Instructions

### Using the Unified Template

**Single Template File**: `session-template.md`
**Configuration**: Automatically adapts based on complexity assessment and task type
**Benefits**: 
- No template selection decisions needed
- Consistent structure across all sessions
- Appropriate depth based on complexity
- Eliminates template maintenance overhead

#### 1. Complexity Assessment First
```python
# Queen uses task-complexity-analysis.md to determine:
complexity_level = assess_task_complexity(user_request)  # 1-4
task_type = detect_task_type(user_request)  # feature-development, bug-investigation, etc.
```

#### 2. Automatic Template Configuration
- Template automatically shows appropriate sections for complexity level
- Worker assignments suggest right team size and specialization
- Research depth scales from minimal to comprehensive
- Quality gates include only relevant checkpoints

#### 3. Session Customization
- Replace `{placeholder-text}` with project-specific details
- Complexity-based sections automatically include/exclude content
- Worker assignments adapt to actual needs
- Template evolves as complexity understanding changes

#### 4. Dynamic Adaptation
- Sessions can upgrade/downgrade complexity as understanding improves
- Worker team can expand/contract based on actual coordination needs
- Template supports complexity overrides and learning

---

## 🎯 Integration with Complexity Assessment

### Automatic Task Type & Complexity Detection
```python
# Unified system automatically determines both:
task_analysis = {
    "implement user authentication": {
        "task_type": "feature-development",
        "complexity_level": 3,  # Cross-domain security + UI + backend
        "estimated_duration": "2-4 days"
    },
    "fix login error": {
        "task_type": "bug-investigation", 
        "complexity_level": 2,  # Analysis + focused fix
        "estimated_duration": "4-8 hours"
    },
    "update dependencies": {
        "task_type": "maintenance-task",
        "complexity_level": 1,  # Direct maintenance
        "estimated_duration": "1-2 hours" 
    }
}
```

### Template Effectiveness Metrics
- **Complexity Accuracy**: How often initial assessment matches actual complexity
- **Template Adaptation**: Frequency of complexity level changes during sessions
- **Worker Efficiency**: Worker utilization vs template suggestions
- **Session Success**: Completion rate across complexity levels

### Session Learning Integration
- **Override Tracking**: Learn from complexity level overrides
- **Pattern Recognition**: Improve task type detection from user requests
- **Template Evolution**: Refine template sections based on actual usage

---

**Template Version**: 2.0  
**Last Updated**: Current  
**Replaces**: All individual template files (feature-development, bug-investigation, etc.)  
**Usage**: Single template for all session types with automatic adaptation

The session template eliminates template selection overhead while ensuring appropriate structure and depth for every complexity level and task type.