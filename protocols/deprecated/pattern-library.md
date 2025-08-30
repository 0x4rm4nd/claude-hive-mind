---
name: pattern-library
description: Manage successful pattern cataloging and knowledge preservation
arguments: "$ACTION [$PATTERN_NAME] [$SESSION_ID]"
---

# 📚 Hive-Mind Pattern Library Manager

Managing successful implementation patterns and knowledge preservation.

## Pattern Library Management Protocol

### Step 1: Setup and Validation
```bash
ACTION="$1"
PATTERN_NAME="$2"
SESSION_ID="$3"

# Ensure pattern library directory exists
mkdir -p "Docs/hive-mind/PATTERNS"
cd "Docs/hive-mind/PATTERNS"

echo "# Pattern Library Management"
echo "**Action**: ${ACTION}"
echo "**Date**: $(date -Iseconds)"
echo ""

# Validate action
case "$ACTION" in
  "list"|"add"|"search"|"view"|"contribute"|"index"|"stats"|"export")
    echo "✅ Valid action: ${ACTION}"
    ;;
  *)
    echo "❌ Invalid action: ${ACTION}"
    echo "Valid actions: list, add, search, view, contribute, index, stats, export"
    exit 1
    ;;
esac
echo ""
```

### Step 2: List Existing Patterns
```bash
if [ "$ACTION" = "list" ] || [ "$ACTION" = "index" ]; then
  echo "## 📋 Pattern Library Index"
  echo ""
  
  if [ "$(ls -1 *.md 2>/dev/null | wc -l)" -gt 0 ]; then
    echo "### Available Patterns"
    
    for pattern_file in *.md; do
      if [ -f "$pattern_file" ]; then
        pattern_name=$(basename "$pattern_file" .md)
        created_date=$(stat -f "%Sm" "$pattern_file" 2>/dev/null || stat -c "%y" "$pattern_file" 2>/dev/null || echo "Unknown")
        file_size=$(wc -l < "$pattern_file")
        
        # Extract pattern context if available
        context=$(grep "^**Context**:" "$pattern_file" | head -1 | sed 's/^**Context**: //' || echo "No context")
        
        echo "#### ${pattern_name}"
        echo "- **File**: ${pattern_file}"
        echo "- **Created**: ${created_date}"
        echo "- **Size**: ${file_size} lines"
        echo "- **Context**: ${context}"
        echo ""
      fi
    done
    
    echo "### Pattern Categories"
    
    # Group patterns by type
    api_patterns=$(ls -1 *api*.md *endpoint*.md 2>/dev/null | wc -l)
    ui_patterns=$(ls -1 *ui*.md *component*.md *react*.md 2>/dev/null | wc -l)
    db_patterns=$(ls -1 *database*.md *db*.md *schema*.md 2>/dev/null | wc -l)
    security_patterns=$(ls -1 *security*.md *auth*.md 2>/dev/null | wc -l)
    test_patterns=$(ls -1 *test*.md *testing*.md 2>/dev/null | wc -l)
    research_patterns=$(ls -1 *research*.md *context7*.md 2>/dev/null | wc -l)
    
    echo "- **API/Backend Patterns**: ${api_patterns}"
    echo "- **UI/Frontend Patterns**: ${ui_patterns}"
    echo "- **Database Patterns**: ${db_patterns}"
    echo "- **Security Patterns**: ${security_patterns}"
    echo "- **Testing Patterns**: ${test_patterns}"
    echo "- **Research Patterns**: ${research_patterns}"
    echo ""
    
  else
    echo "📝 No patterns in library yet"
    echo ""
    echo "### Getting Started"
    echo "1. Use 'pattern-library add' to create your first pattern"
    echo "2. Use 'pattern-library contribute SESSION_ID' to extract patterns from completed sessions"
    echo "3. Patterns are automatically added when sessions are archived"
    echo ""
  fi
fi
```

### Step 3: Add New Pattern
```bash
if [ "$ACTION" = "add" ]; then
  echo "## ➕ Add New Pattern"
  echo ""
  
  if [ -z "$PATTERN_NAME" ]; then
    echo "**Pattern Name** (e.g., 'jwt-authentication', 'react-data-fetching'):"
    read -r PATTERN_NAME
  fi
  
  if [ -z "$PATTERN_NAME" ]; then
    echo "❌ Pattern name required"
    exit 1
  fi
  
  # Sanitize pattern name for filename
  PATTERN_FILE=$(echo "$PATTERN_NAME" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g').md
  
  if [ -f "$PATTERN_FILE" ]; then
    echo "⚠️ Pattern file ${PATTERN_FILE} already exists"
    echo "Overwrite? (y/N):"
    read -r OVERWRITE
    if [ "$OVERWRITE" != "y" ] && [ "$OVERWRITE" != "Y" ]; then
      echo "❌ Pattern creation cancelled"
      exit 1
    fi
  fi
  
  echo ""
  echo "### Pattern Creation Wizard"
  echo ""
  
  echo "**Context** (What problem does this solve?):"
  read -r PATTERN_CONTEXT
  
  echo ""
  echo "**Technology Stack** (Libraries, frameworks, tools used):"
  read -r PATTERN_TECH
  
  echo ""
  echo "**Use Case** (When to use this pattern):"
  read -r PATTERN_USECASE
  
  echo ""
  echo "**Success Criteria** (How to know it's working):"
  read -r PATTERN_SUCCESS
  
  # Create pattern file
  cat > "$PATTERN_FILE" << EOF
# Pattern: ${PATTERN_NAME}

**Created**: $(date -Iseconds)
**Category**: [TO BE CATEGORIZED]
**Source**: Manual addition
**Maturity**: Draft

## Context
${PATTERN_CONTEXT:-What problem this pattern solves}

## Problem Statement
[Describe the specific problem or challenge this pattern addresses]

## Solution Overview
[High-level description of the pattern approach]

## Technology Stack
${PATTERN_TECH:-Technologies and tools used}

## Implementation Details

### Core Components
[List the main components or pieces of the pattern]

### Code Example
\`\`\`typescript
// Example implementation
// TODO: Add actual code example
\`\`\`

### Configuration
[Any configuration or setup required]

## Usage Guidelines

### When to Use
${PATTERN_USECASE:-Scenarios where this pattern is appropriate}

### When NOT to Use
[Scenarios where this pattern should be avoided]

### Prerequisites
[What needs to be in place before using this pattern]

## Success Criteria
${PATTERN_SUCCESS:-How to validate the pattern is working correctly}

## Testing Strategy
[How to test implementations using this pattern]

## Security Considerations
[Security implications and best practices]

## Performance Implications
[Performance characteristics and optimization tips]

## Common Pitfalls
[Mistakes to avoid when implementing this pattern]

## Variations
[Alternative approaches or modifications to the pattern]

## Related Patterns
[Links to other patterns that work well with this one]

## References
[External documentation, articles, or resources]

## Examples in SmartWalletFX
[Specific implementations or usage within the SmartWalletFX codebase]

## Lessons Learned
[Key insights gained from using this pattern]

## Future Improvements
[Potential enhancements or evolution of the pattern]

---

*Pattern Library Entry - Update as implementation evolves*
EOF
  
  echo "✅ Pattern ${PATTERN_NAME} created successfully"
  echo ""
  echo "**File**: ${PATTERN_FILE}"
  echo "**Next Steps**:"
  echo "1. Edit the pattern file to add implementation details"
  echo "2. Add code examples and usage guidelines"
  echo "3. Update as the pattern evolves through use"
  echo ""
fi
```

### Step 4: Search Patterns
```bash
if [ "$ACTION" = "search" ]; then
  echo "## 🔍 Pattern Search"
  echo ""
  
  if [ -z "$PATTERN_NAME" ]; then
    echo "**Search Query** (technology, problem, or keyword):"
    read -r SEARCH_QUERY
  else
    SEARCH_QUERY="$PATTERN_NAME"
  fi
  
  if [ -z "$SEARCH_QUERY" ]; then
    echo "❌ Search query required"
    exit 1
  fi
  
  echo "Searching for: **${SEARCH_QUERY}**"
  echo ""
  
  # Search in pattern files
  matches=$(grep -l -i "$SEARCH_QUERY" *.md 2>/dev/null || true)
  
  if [ -n "$matches" ]; then
    echo "### Matching Patterns"
    
    for match_file in $matches; do
      pattern_name=$(basename "$match_file" .md)
      
      echo "#### ${pattern_name}"
      echo "**File**: ${match_file}"
      
      # Show context around matches
      context_lines=$(grep -n -i -A 2 -B 1 "$SEARCH_QUERY" "$match_file" | head -10)
      if [ -n "$context_lines" ]; then
        echo "**Relevant Content**:"
        echo "$context_lines" | sed 's/^/  /'
      fi
      echo ""
    done
    
  else
    echo "❌ No patterns found matching '${SEARCH_QUERY}'"
    echo ""
    echo "### Suggestions"
    echo "1. Try broader search terms"
    echo "2. Use 'pattern-library list' to see all available patterns"
    echo "3. Consider adding a new pattern if this is a novel approach"
    echo ""
  fi
fi
```

### Step 5: View Pattern Details
```bash
if [ "$ACTION" = "view" ]; then
  echo "## 👀 View Pattern Details"
  echo ""
  
  if [ -z "$PATTERN_NAME" ]; then
    echo "**Pattern Name** (or partial name):"
    read -r PATTERN_NAME
  fi
  
  if [ -z "$PATTERN_NAME" ]; then
    echo "❌ Pattern name required"
    exit 1
  fi
  
  # Find matching pattern file
  pattern_file=""
  
  # Try exact match first
  if [ -f "${PATTERN_NAME}.md" ]; then
    pattern_file="${PATTERN_NAME}.md"
  else
    # Try partial match
    matches=$(ls -1 *"${PATTERN_NAME}"*.md 2>/dev/null || true)
    match_count=$(echo "$matches" | wc -w)
    
    if [ "$match_count" -eq 1 ]; then
      pattern_file="$matches"
    elif [ "$match_count" -gt 1 ]; then
      echo "Multiple patterns found:"
      echo "$matches" | sed 's/^/- /'
      echo ""
      echo "Please be more specific or choose one:"
      read -r pattern_file
    fi
  fi
  
  if [ -z "$pattern_file" ] || [ ! -f "$pattern_file" ]; then
    echo "❌ Pattern not found: ${PATTERN_NAME}"
    echo ""
    echo "Available patterns:"
    ls -1 *.md 2>/dev/null | sed 's/\.md$//' | sed 's/^/- /' || echo "No patterns available"
    exit 1
  fi
  
  echo "### Pattern: $(basename "$pattern_file" .md)"
  echo ""
  
  # Display pattern content
  cat "$pattern_file"
  echo ""
fi
```

### Step 6: Contribute Patterns from Session
```bash
if [ "$ACTION" = "contribute" ]; then
  echo "## 🤝 Contribute Patterns from Session"
  echo ""
  
  if [ -z "$SESSION_ID" ]; then
    echo "**Session ID** to extract patterns from:"
    read -r SESSION_ID
  fi
  
  if [ -z "$SESSION_ID" ]; then
    echo "❌ Session ID required"
    exit 1
  fi
  
  SESSION_DIR="../sessions/${SESSION_ID}"
  
  if [ ! -d "$SESSION_DIR" ]; then
    echo "❌ Session ${SESSION_ID} not found"
    exit 1
  fi
  
  echo "Extracting patterns from session ${SESSION_ID}..."
  echo ""
  
  # Extract task information
  if [ -s "${SESSION_DIR}/STATE.json" ]; then
    TASK_NAME=$(jq -r '.task' "${SESSION_DIR}/STATE.json")
    echo "**Session Task**: ${TASK_NAME}"
  fi
  
  # Extract successful patterns from worker notes
  pattern_count=0
  
  for worker_file in "${SESSION_DIR}/workers"/*.md; do
    if [ -s "$worker_file" ]; then
      worker_name=$(basename "$worker_file" .md)
      
      # Look for pattern-related content
      pattern_content=$(grep -A 5 -B 2 -i "pattern\|approach\|solution\|successful\|recommend" "$worker_file")
      
      if [ -n "$pattern_content" ]; then
        pattern_file="session_${SESSION_ID}_${worker_name}_patterns.md"
        
        cat > "$pattern_file" << EOF
# Session ${SESSION_ID} Patterns - ${worker_name}

**Source Session**: ${SESSION_ID}
**Worker**: ${worker_name}
**Task**: ${TASK_NAME}
**Extracted**: $(date -Iseconds)
**Category**: Session-derived
**Maturity**: Field-tested

## Context
Patterns discovered during implementation of: ${TASK_NAME}

## Implementation Insights
${pattern_content}

## Worker Notes Source
Extracted from: \`${SESSION_DIR}/workers/${worker_name}-notes.md\`

EOF
        
        # Add research synthesis if available
        if [ -s "${SESSION_DIR}/RESEARCH_SYNTHESIS.md" ]; then
          echo "" >> "$pattern_file"
          echo "## Research Context" >> "$pattern_file"
          echo "Related research findings from session:" >> "$pattern_file"
          grep -A 3 -B 1 "$worker_name\|$(echo $worker_name | sed 's/-worker//')" "${SESSION_DIR}/RESEARCH_SYNTHESIS.md" >> "$pattern_file" 2>/dev/null || true
        fi
        
        # Add decision context if available
        if [ -s "${SESSION_DIR}/DECISIONS.md" ]; then
          echo "" >> "$pattern_file"
          echo "## Decision Context" >> "$pattern_file"
          echo "Related decisions from session:" >> "$pattern_file"
          tail -10 "${SESSION_DIR}/DECISIONS.md" >> "$pattern_file"
        fi
        
        echo "---" >> "$pattern_file"
        echo "" >> "$pattern_file"
        echo "*Auto-extracted pattern from hive-mind session ${SESSION_ID}*" >> "$pattern_file"
        
        echo "✅ Extracted pattern: ${pattern_file}"
        pattern_count=$((pattern_count + 1))
      fi
    fi
  done
  
  if [ "$pattern_count" -eq 0 ]; then
    echo "⚠️ No obvious patterns found in session ${SESSION_ID} worker notes"
    echo ""
    echo "### Manual Pattern Creation"
    echo "Consider manually reviewing the session files and creating patterns for:"
    echo "- Successful implementation approaches"
    echo "- Research-backed technology choices"
    echo "- Problem-solving strategies that worked well"
    echo "- Integration patterns with existing systems"
  else
    echo ""
    echo "✅ Extracted ${pattern_count} patterns from session ${SESSION_ID}"
    echo ""
    echo "### Next Steps"
    echo "1. Review and refine the extracted pattern files"
    echo "2. Add code examples and implementation details"
    echo "3. Categorize patterns appropriately"
    echo "4. Cross-reference with related patterns"
  fi
  echo ""
fi
```

### Step 7: Pattern Statistics
```bash
if [ "$ACTION" = "stats" ]; then
  echo "## 📊 Pattern Library Statistics"
  echo ""
  
  total_patterns=$(ls -1 *.md 2>/dev/null | wc -l)
  echo "**Total Patterns**: ${total_patterns}"
  
  if [ "$total_patterns" -gt 0 ]; then
    echo ""
    echo "### Pattern Sources"
    session_patterns=$(ls -1 session_*.md 2>/dev/null | wc -l)
    manual_patterns=$(grep -l "Manual addition" *.md 2>/dev/null | wc -l)
    
    echo "- **Session-derived**: ${session_patterns}"
    echo "- **Manually added**: ${manual_patterns}"
    echo "- **Other sources**: $((total_patterns - session_patterns - manual_patterns))"
    echo ""
    
    echo "### Pattern Maturity"
    draft_patterns=$(grep -l "Maturity.*Draft" *.md 2>/dev/null | wc -l)
    tested_patterns=$(grep -l "Field-tested\|Production" *.md 2>/dev/null | wc -l)
    
    echo "- **Draft**: ${draft_patterns}"
    echo "- **Field-tested**: ${tested_patterns}"
    echo "- **Unknown maturity**: $((total_patterns - draft_patterns - tested_patterns))"
    echo ""
    
    echo "### Content Analysis"
    total_lines=$(find . -name "*.md" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}' || echo "0")
    avg_lines=$((total_lines / total_patterns))
    
    echo "- **Total content**: ${total_lines} lines"
    echo "- **Average pattern size**: ${avg_lines} lines"
    echo ""
    
    echo "### Recent Activity"
    recent_patterns=$(find . -name "*.md" -mtime -7 2>/dev/null | wc -l)
    echo "- **Patterns updated in last week**: ${recent_patterns}"
    
    echo ""
    echo "### Most Referenced Technologies"
    echo "**Top technologies mentioned in patterns**:"
    
    # Extract technology mentions
    tech_mentions=$(grep -h -i -o -E "(react|node|express|fastify|postgresql|redis|typescript|javascript|python|docker|kubernetes|aws|jwt|oauth)" *.md 2>/dev/null | sort | uniq -c | sort -nr | head -5)
    
    if [ -n "$tech_mentions" ]; then
      echo "$tech_mentions" | awk '{printf "- **%s**: %d mentions\n", $2, $1}'
    else
      echo "- No technology patterns detected yet"
    fi
    echo ""
  fi
fi
```

### Step 8: Export Pattern Library
```bash
if [ "$ACTION" = "export" ]; then
  echo "## 📤 Export Pattern Library"
  echo ""
  
  export_file="pattern_library_export_$(date +%Y%m%d_%H%M).md"
  
  cat > "$export_file" << EOF
# SmartWalletFX Pattern Library Export

**Generated**: $(date -Iseconds)
**Total Patterns**: $(ls -1 *.md 2>/dev/null | wc -l)

This export contains all patterns from the SmartWalletFX hive-mind pattern library.

## Table of Contents

EOF
  
  # Add table of contents
  for pattern_file in *.md; do
    if [ -f "$pattern_file" ] && [ "$pattern_file" != "$export_file" ]; then
      pattern_name=$(basename "$pattern_file" .md)
      echo "- [${pattern_name}](#$(echo $pattern_name | tr ' ' '-' | tr '[:upper:]' '[:lower:]'))" >> "$export_file"
    fi
  done
  
  echo "" >> "$export_file"
  echo "---" >> "$export_file"
  echo "" >> "$export_file"
  
  # Add all pattern content
  for pattern_file in *.md; do
    if [ -f "$pattern_file" ] && [ "$pattern_file" != "$export_file" ]; then
      echo "" >> "$export_file"
      cat "$pattern_file" >> "$export_file"
      echo "" >> "$export_file"
      echo "---" >> "$export_file"
      echo "" >> "$export_file"
    fi
  done
  
  echo "✅ Pattern library exported to: ${export_file}"
  
  export_size=$(wc -l < "$export_file")
  echo "**Export size**: ${export_size} lines"
  echo ""
  echo "### Usage"
  echo "- Share with team members for knowledge transfer"
  echo "- Use as reference documentation"
  echo "- Archive for project documentation"
  echo "- Import into other pattern libraries"
  echo ""
fi
```

## Usage Examples

```bash
# List all patterns
./pattern-library.md list

# Add new pattern interactively
./pattern-library.md add

# Add specific pattern
./pattern-library.md add "jwt-authentication-pattern"

# Search for patterns
./pattern-library.md search "react"

# View specific pattern
./pattern-library.md view "jwt-authentication"

# Extract patterns from session
./pattern-library.md contribute SESSION_ID

# View library statistics
./pattern-library.md stats

# Export entire library
./pattern-library.md export

# Create index of all patterns
./pattern-library.md index
```

This tool provides comprehensive pattern library management for preserving and sharing successful implementation approaches across hive-mind sessions.