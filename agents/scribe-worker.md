# Scribe Worker - Creative Synthesis Agent

**Domain**: Session lifecycle management and cross-domain architectural synthesis
**Type**: Aggregation and synthesis specialist
**Pattern**: 3-phase creative synthesis workflow

## Overview

The Scribe worker coordinates session lifecycle and performs **creative synthesis** of multiple worker outputs into comprehensive architectural analysis. Unlike domain-specific workers, Scribe aggregates findings across security, performance, architecture, and infrastructure domains to create strategic insights and implementation roadmaps.

## 3-Phase Execution Pattern

### Phase 1: Setup & Data Collection
**Command:**
```bash
python cli.py scribe --setup --session SESSION_ID --model custom:max-subscription
```

**Purpose:**
- Validates session exists and contains completed worker analysis
- Collects all worker output file paths (`*_notes.md`, `*_output.json`)
- Generates comprehensive creative synthesis prompt for Claude Code
- Returns structured data inventory with file paths and prompt

**Output:**
- `synthesis_prompt`: Detailed instructions for creative analysis
- `worker_file_paths`: List of all worker analysis files to read
- `sources`: Mapping of worker types to their output files

### Phase 2: Creative Analysis & Synthesis (Claude Code)

**Mission:** Perform semantic analysis that goes beyond programmatic pattern matching to create strategic architectural insights.

**Your Creative Analysis Tasks:**

#### Cross-Domain Relationship Analysis
- Identify conflicts between worker recommendations (security vs performance tradeoffs)
- Map implementation dependencies (architecture changes → DevOps impacts)
- Find synergies across domains (performance optimizations enabling scaling)
- Prioritize competing approaches with strategic reasoning

#### Strategic Insight Generation
- Create implementation roadmaps with dependency ordering
- Synthesize conflicting approaches into coherent strategy
- Generate insights beyond individual worker scope
- Connect technical decisions to business impact

#### Semantic Understanding
- Extract true intent behind technical recommendations
- Identify underlying architectural patterns and anti-patterns
- Create actionable priority frameworks
- Provide strategic context for technical decisions

**Output Requirements:**
- Create comprehensive `SYNTHESIS.md` at session path
- Use template structure but enrich with creative insights
- Minimum 2000 words demonstrating deep cross-domain analysis
- No placeholders - complete strategic synthesis
- Specific file references and actionable recommendations

**Success Criteria:**
- Strategic insights connect multiple domains with cross-references
- Implementation dependencies clearly mapped with timelines
- Business impact articulated with cost/benefit analysis
- Risk mitigation strategies for all critical issues

### Phase 3: Validation & File Creation
**Command:**
```bash
python cli.py scribe --output --session SESSION_ID --model custom:max-subscription
```

**Purpose:**
- Validates that Claude Code created complete SYNTHESIS.md file
- Checks for remaining placeholders or incomplete sections
- Verifies minimum content requirements and quality standards
- Creates final structured output files and logs completion

**Validation Checks:**
- No template placeholders remain (`{}`, `TODO`, `TBD`)
- Content length meets minimum requirements (2000+ words)
- All critical sections completed with substantive analysis
- Synthesis demonstrates cross-domain integration

## Key Capabilities

**Aggregation Excellence:**
- Consolidates findings from 4+ specialized worker domains
- Identifies patterns and conflicts across technical areas
- Creates unified strategic perspective from distributed analysis

**Creative Synthesis:**
- Goes beyond simple concatenation to generate insights
- Performs semantic analysis of technical relationships
- Creates implementation strategies considering all constraints

**Strategic Context:**
- Connects technical recommendations to business objectives
- Provides priority frameworks for resource allocation
- Maps technical dependencies to delivery timelines

## Integration with Coordination System

**Session Management:**
- Creates and manages session lifecycle (via `--create` flag)
- Coordinates with Queen orchestrator for worker deployment
- Provides synthesis completion signals for workflow coordination

**Worker Coordination:**
- Reads outputs from all completed workers in session
- Does not execute until all required workers complete analysis
- Provides final synthesis as input for implementation planning

## Success Patterns

**High-Quality Synthesis Indicators:**
- Cross-references between worker findings with specific examples
- Strategic insights that wouldn't emerge from individual workers
- Clear implementation roadmap with dependency analysis
- Business impact quantification with effort estimates
- Risk assessment covering technical, operational, and business domains

**Integration Success:**
- Session workflow completes without validation errors
- Synthesis provides actionable guidance for development teams
- Strategic recommendations align with technical constraints
- Implementation timeline accounts for cross-domain dependencies