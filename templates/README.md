# Claude Templates Directory

## Overview
This directory contains all templates for the Claude Code hive-mind system, including protocol templates, worker implementation guides, and system configuration templates.

## Directory Structure
```
.claude/templates/
├── workers/
│   └── implementation-template.md  # Worker implementation standards
├── state-v2-template.json         # Session state structure
├── worker-state-template.json     # Worker state structure
├── event-template.json            # Event logging structure  
├── debug-entry-template.json      # Debug logging structure
├── session-template.md            # Session initialization template
├── worker-notes-template.md       # Worker output notes template
├── logging-functions.py           # Universal logging functions
└── README.md                      # This file
```

## Template Categories

### Worker Implementation
- **`workers/implementation-template.md`** - Mandatory implementation standards for all worker agents, including event logging, file naming conventions, and compliance requirements

### JSON Templates
- **state-v2-template.json** - STATE.json v2.0 structure for session management
- **worker-state-template.json** - Individual worker state structure within STATE.json
- **event-template.json** - EVENTS.jsonl entry structure
- **debug-entry-template.json** - DEBUG.jsonl entry structure
- **backlog-item-template.json** - Backlog item structure for task management

### Python Function Templates
- **logging-functions.py** - Universal logging functions (log_event, log_debug, extract_session_id)
- **state-management-functions.py** - STATE.json manipulation functions (update_state, recover_state, check_worker_health)

### YAML Templates
- **worker-selection-matrix.yaml** - Domain-to-worker mapping for intelligent worker selection

### Markdown Templates
- **session-template.md** - Session initialization document template
- **research-synthesis-template.md** - Research synthesis document structure
- **worker-notes-template.md** - Worker output notes template
- **template-guide.md** - Usage guide for template system

## Usage Guidelines

### For Protocol Authors
1. **Never embed templates** - Always reference template files
2. **Use clear references** - Include path: `.claude/templates/[template-name]`
3. **Document parameters** - Explain template placeholders and usage

### For Agent Implementers
1. **Load templates dynamically** - Read template files at runtime
2. **Replace placeholders** - Use proper variable substitution
3. **Maintain structure** - Don't modify template structure without updating protocol

## Template Versioning
- Templates follow protocol versioning (currently v2.0)
- Breaking changes require new template files (e.g., state-v2-template.json)
- Legacy templates are removed - no backwards compatibility maintained

## Fresh Start Approach
As of 2025-08-30, all legacy templates and migration logic have been removed:
- No v1 to v2 migration support
- Clean break from previous implementations
- Sessions created before this date are incompatible

## Adding New Templates
1. Extract embedded content from protocol file
2. Create appropriately named template file
3. Update protocol to reference template
4. Update this README with template description
5. Document in CHANGELOG.md