---
description: Pure JSON output for Scribe session generation - no formatting or explanations
---

# SCRIBE JSON OUTPUT

**CRITICAL**: Output ONLY raw JSON. No formatting, explanations, or markdown.

## REQUIRED FORMAT

```json
{
  "short_description": "task-name",
  "complexity_level": 1,
  "focus_areas": ["domain"]
}
```

## SCHEMA

- `short_description`: Hyphenated task identifier (string)
- `complexity_level`: 1-4 integer based on task complexity
  - **1-2**: Single-domain (analyzer, backend, frontend)
  - **3-4**: Cross-service/architecture (Queen required)
- `focus_areas`: Domain areas array (strings)

## EXAMPLES

**Task**: "Security analysis of crypto data pipeline"
**Output**: `{"short_description": "crypto-security-analysis", "complexity_level": 2, "focus_areas": ["security", "crypto-data"]}`

**Task**: "Implement portfolio rebalancing across services"
**Output**: `{"short_description": "portfolio-rebalancing", "complexity_level": 4, "focus_areas": ["backend", "integration", "orchestration"]}`

## WORKFLOW

1. Parse task → determine complexity
2. Generate JSON with required schema
3. Output raw JSON only (no markdown blocks)
4. Ensure Docker parseability
