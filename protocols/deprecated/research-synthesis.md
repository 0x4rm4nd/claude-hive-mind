---
name: research-synthesis  
description: Aggregate and synthesize Context7 research findings from multiple workers
arguments: "$SESSION_ID"
---

# 🔬 Research Synthesis Command

Synthesizing Context7 research findings from all workers for session **$SESSION_ID**.

## Research Synthesis Protocol

### Step 1: Load Session and Validate Research Phase
```bash
SESSION_ID="$SESSION_ID"
SESSION_DIR="Docs/hive-mind/sessions/${SESSION_ID}"

if [ ! -d "${SESSION_DIR}" ]; then
  echo "❌ Session ${SESSION_ID} not found"
  exit 1
fi

cd "${SESSION_DIR}"

# Check if we're in research phase
STATUS=$(jq -r '.status' STATE.json)
RESEARCH_COMPLETE=$(jq -r '.research_complete' STATE.json)

echo "# Research Synthesis - Session ${SESSION_ID}"
echo ""
echo "**Current Status**: ${STATUS}"
echo "**Research Complete**: ${RESEARCH_COMPLETE}"
echo ""

if [ "$STATUS" != "research_phase" ] && [ "$RESEARCH_COMPLETE" = "true" ]; then
  echo "ℹ️ Research phase already complete, generating updated synthesis..."
else
  echo "🔄 Research phase active, synthesizing current findings..."
fi
echo ""
```

### Step 2: Collect Research from All Workers
```bash
echo "## 📊 Research Collection Status"
echo ""

# Check research status from each worker
workers=("researcher" "backend" "frontend" "service-architect" "analyzer" "test" "devops" "designer")

echo "### Worker Research Status"
for worker in "${workers[@]}"; do
  worker_file="workers/${worker}-worker-notes.md"
  
  if [ -s "$worker_file" ]; then
    lines=$(wc -l < "$worker_file")
    research_entries=$(grep -c -i "context7\|research\|mcp__context7\|library\|framework" "$worker_file" 2>/dev/null || echo "0")
    
    if [ "$research_entries" -gt 0 ]; then
      echo "✅ **${worker}**: ${lines} lines, ${research_entries} research entries"
    else
      echo "📝 **${worker}**: ${lines} lines, no explicit research entries"
    fi
  else
    echo "❌ **${worker}**: No notes file found"
  fi
done
echo ""
```

### Step 3: Extract and Organize Research Findings
```bash
echo "## 🔍 Research Findings Extraction"
echo ""

# Create comprehensive research synthesis
cat > RESEARCH_SYNTHESIS.md << EOF
# Research Synthesis: $(jq -r '.task' STATE.json)

**Session ID**: ${SESSION_ID}
**Synthesis Date**: $(date -Iseconds)
**Status**: $(jq -r '.status' STATE.json)

## Context7 Research Findings

EOF

# Process each worker's research contributions
for worker in "${workers[@]}"; do
  worker_file="workers/${worker}-worker-notes.md"
  
  if [ -s "$worker_file" ]; then
    # Check if worker has research content
    research_content=$(grep -A 5 -B 2 -i "context7\|mcp__context7\|library.*research\|framework.*research\|recommended.*library" "$worker_file" 2>/dev/null)
    
    if [ -n "$research_content" ]; then
      echo "### ${worker} Worker Research" >> RESEARCH_SYNTHESIS.md
      echo "" >> RESEARCH_SYNTHESIS.md
      echo "$research_content" >> RESEARCH_SYNTHESIS.md
      echo "" >> RESEARCH_SYNTHESIS.md
      echo "---" >> RESEARCH_SYNTHESIS.md
      echo "" >> RESEARCH_SYNTHESIS.md
      
      echo "✅ Extracted research from ${worker} worker"
    fi
  fi
done

echo ""
```

### Step 4: Technology Stack Synthesis
```bash
echo "## 🛠️ Technology Stack Synthesis"
echo ""

# Add technology stack recommendations section
cat >> RESEARCH_SYNTHESIS.md << 'EOF'

## Technology Stack Recommendations

### Primary Technology Selections

#### Backend Technologies
*Synthesis of backend worker and architecture research*

#### Frontend Technologies  
*Synthesis of frontend worker and designer research*

#### Database & Storage
*Synthesis of backend worker and service architect research*

#### Security Framework
*Synthesis of analyzer worker and backend worker security research*

#### Testing Framework
*Synthesis of test worker research*

#### DevOps & Infrastructure
*Synthesis of devops worker research*

EOF

# Extract specific technology recommendations from worker notes
echo "### Extracting Technology Recommendations"

# Backend technologies
backend_tech=$(grep -i -A 3 -B 1 "recommend.*\(api\|database\|server\|node\|express\|fastify\)" workers/backend-worker-notes.md 2>/dev/null | head -10)
if [ -n "$backend_tech" ]; then
  echo "**Backend recommendations found**:" >> RESEARCH_SYNTHESIS.md
  echo "$backend_tech" >> RESEARCH_SYNTHESIS.md
  echo "" >> RESEARCH_SYNTHESIS.md
fi

# Frontend technologies  
frontend_tech=$(grep -i -A 3 -B 1 "recommend.*\(react\|vue\|next\|ui\|component\)" workers/frontend-worker-notes.md 2>/dev/null | head -10)
if [ -n "$frontend_tech" ]; then
  echo "**Frontend recommendations found**:" >> RESEARCH_SYNTHESIS.md
  echo "$frontend_tech" >> RESEARCH_SYNTHESIS.md
  echo "" >> RESEARCH_SYNTHESIS.md
fi

# Security recommendations
security_tech=$(grep -i -A 3 -B 1 "security.*\(recommend\|library\|framework\|best.*practice\)" workers/analyzer-worker-notes.md 2>/dev/null | head -10)
if [ -n "$security_tech" ]; then
  echo "**Security recommendations found**:" >> RESEARCH_SYNTHESIS.md
  echo "$security_tech" >> RESEARCH_SYNTHESIS.md
  echo "" >> RESEARCH_SYNTHESIS.md
fi

echo "✅ Technology recommendations synthesized"
echo ""
```

### Step 5: Implementation Strategy Synthesis
```bash
echo "## 🎯 Implementation Strategy Development"
echo ""

cat >> RESEARCH_SYNTHESIS.md << 'EOF'

## Implementation Strategy

### Research-Informed Approach

#### Phase 1: Foundation Setup
*Based on service architect and backend research*

#### Phase 2: Core Implementation  
*Based on backend and frontend research*

#### Phase 3: Integration & Testing
*Based on test worker and analyzer research*

#### Phase 4: Security & Performance
*Based on analyzer and backend research*

#### Phase 5: Deployment & Monitoring
*Based on devops research*

### Best Practices Integration

#### Development Practices
*Synthesis of coding best practices from multiple workers*

#### Security Practices
*Synthesis of security research from analyzer and backend workers*

#### Performance Practices
*Synthesis of performance research from multiple workers*

#### Testing Practices
*Synthesis of testing research and strategies*

EOF

# Extract implementation approaches from worker notes
echo "### Synthesizing Implementation Approaches"

# Look for implementation patterns and approaches
impl_patterns=""
for worker in "${workers[@]}"; do
  worker_file="workers/${worker}-worker-notes.md"
  if [ -s "$worker_file" ]; then
    patterns=$(grep -i -A 2 -B 1 "approach\|pattern\|implementation.*strategy\|best.*practice" "$worker_file" 2>/dev/null | head -5)
    if [ -n "$patterns" ]; then
      impl_patterns="${impl_patterns}\n\n**${worker} Approaches:**\n${patterns}"
    fi
  fi
done

if [ -n "$impl_patterns" ]; then
  echo -e "$impl_patterns" >> RESEARCH_SYNTHESIS.md
  echo "✅ Implementation approaches synthesized"
else
  echo "⚠️ Limited implementation approaches found in worker notes"
fi

echo ""
```

### Step 6: Conflict Resolution & Gap Analysis
```bash
echo "## ⚖️ Research Conflict Resolution"
echo ""

cat >> RESEARCH_SYNTHESIS.md << 'EOF'

## Research Conflicts & Resolutions

### Technology Conflicts Identified
*Analysis of conflicting recommendations between workers*

### Gap Analysis
*Areas where research is incomplete or missing*

### Unified Decisions
*Final technology and approach decisions with rationale*

EOF

# Analyze potential conflicts
echo "### Analyzing Research Conflicts"

# Look for conflicting technology recommendations
conflicts_found=""

# Check for different library recommendations for same purpose
if [ -s workers/backend-worker-notes.md ] && [ -s workers/service-architect-notes.md ]; then
  backend_libs=$(grep -i -o "\(express\|fastify\|koa\|nest\)" workers/backend-worker-notes.md 2>/dev/null | sort -u)
  architect_libs=$(grep -i -o "\(express\|fastify\|koa\|nest\)" workers/service-architect-notes.md 2>/dev/null | sort -u)
  
  if [ -n "$backend_libs" ] && [ -n "$architect_libs" ]; then
    if [ "$backend_libs" != "$architect_libs" ]; then
      conflicts_found="Backend vs Architecture: Different framework recommendations\n"
    fi
  fi
fi

if [ -n "$conflicts_found" ]; then
  echo "**Conflicts Found:**" >> RESEARCH_SYNTHESIS.md
  echo -e "$conflicts_found" >> RESEARCH_SYNTHESIS.md
  echo "✅ Research conflicts identified and documented"
else
  echo "✅ No major research conflicts detected" >> RESEARCH_SYNTHESIS.md
  echo "✅ Research appears consistent across workers"
fi

echo ""
```

### Step 7: SmartWalletFX Integration Analysis
```bash
echo "## 🏦 SmartWalletFX Integration Analysis"
echo ""

cat >> RESEARCH_SYNTHESIS.md << 'EOF'

## SmartWalletFX-Specific Integration

### Financial Application Requirements
*Security, compliance, and performance requirements for financial data*

### Existing Architecture Integration
*How research recommendations integrate with current SmartWalletFX architecture*

### Crypto/DeFi Considerations
*Blockchain and cryptocurrency-specific requirements and optimizations*

### Performance Requirements
*Financial data processing performance and scalability needs*

### Security & Compliance
*Financial industry security standards and regulatory compliance*

EOF

# Extract SmartWalletFX-specific considerations
echo "### Extracting SmartWalletFX-Specific Insights"

smartwallet_insights=""
for worker in "${workers[@]}"; do
  worker_file="workers/${worker}-worker-notes.md"
  if [ -s "$worker_file" ]; then
    insights=$(grep -i -A 3 -B 1 "smartwallet\|financial\|crypto\|defi\|blockchain\|security.*financial" "$worker_file" 2>/dev/null)
    if [ -n "$insights" ]; then
      smartwallet_insights="${smartwallet_insights}\n\n**${worker} Financial Insights:**\n${insights}"
    fi
  fi
done

if [ -n "$smartwallet_insights" ]; then
  echo -e "$smartwallet_insights" >> RESEARCH_SYNTHESIS.md
  echo "✅ SmartWalletFX-specific insights synthesized"
else
  echo "⚠️ Limited SmartWalletFX-specific research found"
fi

echo ""
```

### Step 8: Finalize Research Synthesis
```bash
echo "## ✅ Research Synthesis Completion"
echo ""

# Add synthesis completion metadata
cat >> RESEARCH_SYNTHESIS.md << EOF

---

## Synthesis Metadata

**Completed**: $(date -Iseconds)
**Session ID**: ${SESSION_ID}
**Workers Contributed**: $(find workers -name "*.md" -size +0 | wc -l)
**Total Research Lines**: $(find workers -name "*.md" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}' || echo "0")

**Next Phase**: Implementation planning based on synthesized research findings

**Quality Assurance**: Research recommendations validated across multiple worker perspectives
EOF

# Update session state to mark research as complete
jq --arg timestamp "$(date -Iseconds)" '
  .research_complete = true |
  .updated_at = $timestamp |
  .current_phase.name = "planning_phase" |
  .current_phase.progress_percentage = 30 |
  .current_phase.next_action = "Queen: Create research-informed task breakdown"
' STATE.json > STATE.tmp && mv STATE.tmp STATE.json

# Log research synthesis completion
echo '{"ts":"'$(date -Iseconds)'","agent":"queen","event":"research.synthesized","session_id":"'${SESSION_ID}'","workers_contributed":"'$(find workers -name "*.md" -size +0 | wc -l)'","synthesis_file":"RESEARCH_SYNTHESIS.md"}' >> EVENTS.jsonl

echo "✅ RESEARCH_SYNTHESIS.md updated with comprehensive findings"
echo "✅ Session state updated: research_complete = true"
echo "✅ Ready for implementation planning phase"

echo ""
echo "## 📋 Synthesis Summary"
synthesis_lines=$(wc -l < RESEARCH_SYNTHESIS.md)
echo "**Research Synthesis**: ${synthesis_lines} lines"
echo "**Workers Contributed**: $(find workers -name "*.md" -size +0 | wc -l)"
echo "**Research Phase**: Complete ✅"
echo "**Next Phase**: Implementation Planning"

echo ""
echo "---"
echo ""
echo "🎉 **Research synthesis complete for Session ${SESSION_ID}!**"
echo ""
echo "The research findings have been unified into a comprehensive implementation strategy."
echo "Queen can now proceed with research-informed task breakdown and worker assignments."
```

## Usage

This command creates a comprehensive research synthesis by:

- **Collecting** all worker research findings
- **Organizing** technology recommendations by domain
- **Resolving** conflicts between worker recommendations  
- **Integrating** SmartWalletFX-specific requirements
- **Documenting** unified implementation strategy
- **Preparing** for research-informed implementation phase

The result is a unified `RESEARCH_SYNTHESIS.md` that serves as the foundation for all subsequent implementation decisions.