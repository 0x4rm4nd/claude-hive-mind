# Task Complexity Analysis Protocol
#task-complexity #assessment #workflow #optimization #level-3

## Purpose
Automated task complexity assessment for hive-mind workflow optimization with tag-based context filtering and fast escalation integration.

## Complexity Levels

### Level 1: Simple Task (40% of tasks, < 1 hour)
#level-1 #simple #direct-worker #minimal-session

**Characteristics**:
- Single file modification
- No cross-system dependencies
- Clear implementation path
- Minimal research required

**Examples**:
- Fix typo or minor bug
- Add simple validation rule
- Update configuration value
- Small CSS adjustments

**Workflow**: Direct worker assignment + minimal session directory + tag-filtered context
**Context Loading**: Single domain tags only (#frontend OR #backend, no cross-domain)
**Escalation**: Standard 15min timeouts (low priority)

### Level 2: Enhanced Task (30% of tasks, 1-2 hours)
#level-2 #enhanced #research-coordination #standard-session

**Characteristics**:
- Multiple file modifications
- Single domain (frontend OR backend)
- Some research required
- Clear architecture pattern

**Examples**:
- Add new API endpoint
- Create new React component
- Database schema modification
- Simple feature implementation

**Workflow**: Research Worker + Primary Worker + standard session directory + domain-specific context
**Context Loading**: Primary domain tags + related patterns (#backend + #api + #database)
**Escalation**: Medium priority 10min timeouts for coordination events

### Level 3: Cross-Domain Task (20% of tasks, 2-6 hours)
#level-3 #cross-domain #lightweight-hivemind #comprehensive-session

**Characteristics**:
- Multiple system domains
- Cross-service integration
- Significant research required
- Architecture decisions needed

**Examples**:
- User authentication system
- Payment processing integration
- Real-time notifications
- Data synchronization features

**Workflow**: Lightweight hive-mind (2-3 workers) + comprehensive session directory + cross-domain context
**Context Loading**: Multi-domain tags + cross-domain filtering (#frontend + #backend + #security + #api)
**Escalation**: High priority 5min timeouts for cross-worker coordination

### Level 4: Complex Project (10% of tasks, > 6 hours)
#level-4 #complex-project #full-hivemind #complete-infrastructure

**Characteristics**:
- Multiple interconnected features
- New architecture patterns
- Extensive research and design
- Cross-cutting concerns

**Examples**:
- Complete service redesign
- New microservice implementation
- Major security overhaul
- Performance optimization project

**Workflow**: Full hive-mind coordination + complete session infrastructure + comprehensive context
**Context Loading**: All relevant tags + comprehensive filtering + pattern library access
**Escalation**: Critical priority 2min timeouts for project coordination

## 🔧 Task Complexity Assessment Utilities (Executable)
*Low-level utilities that rarely change - copy these into your agent implementation*

```python
# Tag Analysis Utilities
def estimate_required_tags(user_request):
    """Estimate which memory bank tags will be needed"""
    keywords = user_request.lower()
    required_tags = []
    
    # Domain tags
    if any(word in keywords for word in ['frontend', 'ui', 'react', 'component']): 
        required_tags.append('frontend')
    if any(word in keywords for word in ['backend', 'api', 'server', 'database']): 
        required_tags.append('backend')
    if any(word in keywords for word in ['auth', 'security', 'login', 'permission']): 
        required_tags.append('security')
    if any(word in keywords for word in ['test', 'testing', 'spec', 'validation']): 
        required_tags.append('testing')
    
    # Complexity tags
    if any(word in keywords for word in ['refactor', 'redesign', 'architecture']): 
        required_tags.append('level-3')
    elif any(word in keywords for word in ['integrate', 'connect', 'sync']): 
        required_tags.append('level-2')
    else: 
        required_tags.append('level-1')
        
    return required_tags

def estimate_context_scope_needed(user_request):
    """Estimate memory bank context scope needed"""
    keywords = user_request.lower()
    
    if any(word in keywords for word in ['system', 'architecture', 'integration', 'cross']):
        return 'multi-domain'  # Need related context
    elif any(word in keywords for word in ['feature', 'component', 'endpoint']):
        return 'related-tags'  # Need some related context
    else:
        return 'single-tag'  # Just primary domain

def assess_coordination_urgency(user_request):
    """Assess escalation timeout requirements"""
    keywords = user_request.lower()
    
    if any(word in keywords for word in ['urgent', 'critical', 'blocker', 'production']):
        return 'critical'  # 2min timeouts
    elif any(word in keywords for word in ['important', 'priority', 'integration']):
        return 'high'  # 5min timeouts  
    elif any(word in keywords for word in ['feature', 'enhancement', 'improvement']):
        return 'medium'  # 10min timeouts
    else:
        return 'standard'  # 15min timeouts

# Complexity Scoring Utilities
def analyze_scope_keywords(user_request):
    """Analyze scope indicators from user request"""
    keywords = user_request.lower()
    indicators = []
    
    if any(word in keywords for word in ['multiple', 'several', 'various']):
        indicators.append('multiple files')
    if any(word in keywords for word in ['new', 'create', 'add', 'implement']):
        indicators.append('new feature')
    if any(word in keywords for word in ['refactor', 'redesign', 'restructure']):
        indicators.append('refactor')
    
    return indicators

def identify_technical_complexity(user_request):
    """Identify technical complexity keywords"""
    keywords = user_request.lower()
    technical_keywords = []
    
    if any(word in keywords for word in ['security', 'auth', 'permission']):
        technical_keywords.append('security')
    if any(word in keywords for word in ['performance', 'optimize', 'scale']):
        technical_keywords.append('performance')
    if any(word in keywords for word in ['integrate', 'api', 'service']):
        technical_keywords.append('integration')
    
    return technical_keywords

def estimate_service_domains(user_request):
    """Estimate number of service domains involved"""
    keywords = user_request.lower()
    domains = set()
    
    if any(word in keywords for word in ['frontend', 'ui', 'react']):
        domains.add('frontend')
    if any(word in keywords for word in ['backend', 'api', 'server']):
        domains.add('backend')
    if any(word in keywords for word in ['database', 'data', 'storage']):
        domains.add('database')
    if any(word in keywords for word in ['security', 'auth']):
        domains.add('security')
    
    return len(domains)

def calculate_complexity_score(analysis):
    """Calculate complexity score from analysis components"""
    score = 0
    
    # Scope scoring with tag awareness
    if 'multiple files' in analysis['scope_indicators']: 
        score += 1
    if 'new feature' in analysis['scope_indicators']: 
        score += 1
    if 'refactor' in analysis['scope_indicators']: 
        score += 2
    if len(analysis['tag_requirements']) > 2: 
        score += 1  # Multi-domain
    
    # Technical complexity scoring
    if analysis['domain_span'] > 1: 
        score += 2
    if 'security' in analysis['technical_keywords']: 
        score += 1
    if 'performance' in analysis['technical_keywords']: 
        score += 1
    if 'integration' in analysis['technical_keywords']: 
        score += 1
    
    # Context and coordination complexity
    if analysis['context_scope'] == 'multi-domain': 
        score += 2
    elif analysis['context_scope'] == 'related-tags': 
        score += 1
    if analysis['escalation_urgency'] in ['critical', 'high']: 
        score += 2
    elif analysis['escalation_urgency'] == 'medium': 
        score += 1
    
    return score

def map_score_to_complexity_level(score):
    """Map complexity score to level 1-4"""
    if score <= 2: 
        return 1
    elif score <= 5: 
        return 2
    elif score <= 9: 
        return 3
    else: 
        return 4

# Workflow Selection Utilities
def get_workflow_config_for_complexity(complexity_level):
    """Get workflow configuration based on complexity level"""
    configs = {
        1: {
            'type': 'direct_worker',
            'session_structure': 'minimal',
            'coordination_files': [],
            'research_phase': False,
            'reflection_required': False,
            'escalation_timeout': '15min',
            'escalation_priority': 'low'
        },
        2: {
            'type': 'simple_coordination', 
            'session_structure': 'standard',
            'coordination_files': ['EVENTS.jsonl', 'BACKLOG.jsonl'],
            'research_phase': 'minimal',
            'reflection_required': True,
            'escalation_timeout': '10min',
            'escalation_priority': 'medium'
        },
        3: {
            'type': 'lightweight_hivemind',
            'session_structure': 'comprehensive',
            'coordination_files': ['EVENTS.jsonl', 'BACKLOG.jsonl'],
            'research_phase': 'comprehensive',
            'reflection_required': True,
            'escalation_timeout': '5min',
            'escalation_priority': 'high'
        },
        4: {
            'type': 'full_hivemind',
            'session_structure': 'complete',
            'coordination_files': ['EVENTS.jsonl', 'BACKLOG.jsonl'],
            'research_phase': 'extensive',
            'reflection_required': True,
            'escalation_timeout': '2min',
            'escalation_priority': 'critical'
        }
    }
    return configs.get(complexity_level, configs[2])
```

## 📋 Task Complexity Assessment Protocol (Instructions)
*Coordination workflows and decision-making - follow these steps using the utilities above*

### Complexity Assessment Workflow

**When assessing task complexity:**

#### Step 1: Analyze Task Requirements
1. **Use utility**: `estimate_required_tags(user_request)` to identify domain involvement
2. **Use utility**: `estimate_context_depth_needed(user_request)` for memory bank requirements  
3. **Use utility**: `assess_coordination_urgency(user_request)` for escalation timeouts
4. **Use utility**: `estimate_service_domains(user_request)` for cross-domain complexity

#### Step 2: Calculate Complexity Score
1. **Use utility**: `analyze_scope_keywords(user_request)` for scope indicators
2. **Use utility**: `identify_technical_complexity(user_request)` for technical requirements
3. **Compile analysis** into structured assessment data
4. **Use utility**: `calculate_complexity_score(analysis)` to get numeric score
5. **Use utility**: `map_score_to_complexity_level(score)` to determine Level 1-4

#### Step 3: Configure Workflow Based on Complexity
1. **Use utility**: `get_workflow_config_for_complexity(complexity_level)` for base config
2. **Override escalation urgency** if analysis indicates different priority
3. **Adjust context loading** based on specific tag requirements
4. **Apply worker selection** based on domain requirements

### Tag-Enhanced Assessment Framework

**Primary Assessment Criteria with Tag Integration:**

#### Scope Analysis
- File count impact (1 file = L1, 2-3 files = L2, 4+ files = L3+)
- Service boundaries crossed (0 = L1-2, 1 = L2-3, 2+ = L3-4)
- Tag domains required (single = L1-2, dual = L2-3, multi = L3-4)
- New vs existing patterns (existing = L1-2, new = L3-4)

#### Technical Dependencies & Context Requirements
- External APIs/libraries required (0 = L1, 1-2 = L2, 3+ = L3-4)
- Database changes needed (none = L1, simple = L2, complex = L3-4)
- Infrastructure modifications (none = L1-2, required = L3-4)
- Memory bank context scope needed (single-tag = L1, related-tags = L2, multi-domain = L3-4)

#### Research & Knowledge Requirements
- Context7 research needed (none = L1, minimal = L2, moderate = L3, extensive = L4)
- Security considerations (basic = L1-2, moderate = L3, critical = L4)
- Performance implications (none = L1-2, some = L3, critical = L4)
- Pattern library access needed (none = L1, specific = L2, cross-domain = L3, comprehensive = L4)

#### Coordination & Escalation Complexity
- Existing code modification depth (surface = L1-2, moderate = L3, deep = L4)
- Cross-worker coordination needed (none = L1, minimal = L2, moderate = L3, extensive = L4)
- Testing scope required (unit = L1-2, integration = L3, e2e = L4)
- Escalation urgency required (standard = L1, medium = L2, high = L3, critical = L4)

### Context Loading Strategy by Complexity

#### Level 1 Context Loading:
- Primary worker domain tag only (#frontend OR #backend OR #testing)
- No cross-domain access
- No pattern library access
- Standard memory bank sections only

#### Level 2 Context Loading:
- Primary domain + related tags (#backend + #api + #database)
- Limited cross-domain for specific integrations
- Basic pattern library access for known patterns
- Domain-specific memory bank sections + activeContext.md

#### Level 3 Context Loading:
- Multi-domain tags + cross-domain filtering (#frontend + #backend + #security + #api + #ux)
- Strategic cross-domain access via worker tag matrices
- Cross-domain pattern library access
- Comprehensive memory bank + systemPatterns.md + archive examples

#### Level 4 Context Loading:
- All relevant tags + comprehensive filtering
- Complete cross-domain access
- Full pattern library + anti-pattern awareness
- Complete memory bank + reflection insights + architectural decisions

### Session Directory Structure Integration

**All tasks require session directories for audit trail preservation:**

#### Level 1: Minimal Session Structure
```
Docs/hive-mind/sessions/{session-id}/
├── SESSION.md          # Task summary, worker assignment, completion status
├── STATE.json          # Basic resumption data with Archon task ID
└── workers/
    └── {worker}-notes.md    # Single worker's implementation notes
```

#### Level 2: Standard Session Structure  
```
Docs/hive-mind/sessions/{session-id}/
├── SESSION.md          # Enhanced with research summary
├── STATE.json          # Multi-worker coordination state
├── EVENTS.jsonl        # Worker coordination events
├── BACKLOG.jsonl       # Task breakdown and progress tracking
├── workers/            # Multi-worker implementation notes
└── archive/
    └── REFLECTION.md   # Session learning and pattern extraction
```

#### Level 3-4: Comprehensive/Complete Session Infrastructure
- Full project context documentation
- Complete coordination state preservation
- Cross-worker decision documentation
- Comprehensive research integration
- Pattern library contributions

### Integration with Archive/Reflect Mode

**Archive/reflect triggers by complexity:**

#### Archive Mode Triggers
- **Level 1**: Basic archive on task completion
- **Level 2**: Archive + reflection on completion or milestone
- **Level 3**: Comprehensive archive on completion, phase completion, or blocker resolution
- **Level 4**: Full lifecycle archiving on completion, milestones, decision points

#### Reflection Mode Requirements
- **Level 2+**: Automatic reflection creation with complexity-appropriate depth
- **Level 3+**: Pattern extraction and pattern library contribution
- **Level 4**: Comprehensive project insights and architectural decision capture

---

**Implementation Status**: Clean protocol ready. Task complexity assessment properly separated into utilities and instructions following Smart Hybrid Approach.