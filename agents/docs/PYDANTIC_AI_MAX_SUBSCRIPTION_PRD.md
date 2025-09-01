# Product Requirements Document: Pydantic AI Max Subscription Integration

## Executive Summary

**Objective**: Enable Pydantic AI workers to use Claude Code's Max subscription instead of requiring separate API credits, eliminating costs while maintaining full compatibility.

**Impact**: Zero API costs for all Pydantic AI operations, access to latest Claude models, and simplified billing management.

**Timeline**: 3 weeks (Research → Implementation → Deployment)

## Problem Statement

### Current State
- Pydantic AI workers require separate API credits (Anthropic, OpenAI, Google)
- User has Claude Code Max subscription but cannot leverage it for Pydantic AI
- Multiple billing sources create cost unpredictability

### Target State
- All Pydantic AI workers route through Claude Code Max subscription
- Single subscription covers all AI operations
- Zero additional API costs

## Requirements

### Functional Requirements

#### FR1: Universal Model Interface
- **Requirement**: Support both default and explicit model selection
- **Acceptance Criteria**: 
  - `Agent('custom:max-subscription')` always uses Sonnet 4 (simple default, no worker detection)
  - `Agent('custom:claude-opus-4')` directly uses Opus 4 model
  - `Agent('custom:claude-sonnet-4')` directly uses Sonnet 4 model  
  - `Agent('custom:claude-3-7-sonnet')` directly uses Sonnet 3.7 model
  - No intelligent routing - explicit model selection only
  - No conflicts with existing model names
  - Backward compatibility maintained

#### FR2: Direct Model Specification
- **Requirement**: Support direct model specification without intelligent routing
- **Acceptance Criteria**:
  - Workers can explicitly specify any available Claude model
  - `custom:claude-opus-4` routes to Opus 4 regardless of worker type
  - `custom:claude-sonnet-4` routes to Sonnet 4 regardless of worker type
  - Claude Code handles actual model execution automatically
  - No worker type detection or complex routing logic

#### FR3: Provider Pattern Implementation
- **Requirement**: Custom provider extending Pydantic AI's base provider classes (provider-agnostic design)
- **Acceptance Criteria**:
  - Only intercepts `custom:` prefixed model names
  - Provider-agnostic architecture (supports future OpenAI, Google providers)
  - Maintains original API response format compatibility  
  - No changes required to existing worker logic

#### FR4: Claude Code Integration
- **Requirement**: Route requests through Claude Code Task tool
- **Acceptance Criteria**:
  - Subprocess execution of `claude-code task` commands with no timeout
  - Simple text-only message format conversion (KISS principle)
  - Full Claude Code error output preservation for debugging

#### FR5: Zero-Config Activation
- **Requirement**: Automatic activation via monkey patching on module import
- **Acceptance Criteria**:
  - No code changes required for existing workers
  - Global availability of all `custom:` models
  - Transparent integration - automatically enabled when shared module imported

### Non-Functional Requirements

#### NFR1: Performance
- **Requirement**: <20% overhead compared to direct API calls
- **Measurement**: Response time benchmarks
- **Tolerance**: Additional latency acceptable for cost savings

#### NFR2: Reliability
- **Requirement**: 99%+ success rate for normal operations
- **Failure Modes**: Fail fast on quota limits or Claude Code errors
- **Recovery**: Session preservation for resumable development

#### NFR3: Compatibility
- **Requirement**: 100% response format compatibility
- **Validation**: Existing worker outputs unchanged
- **Integration**: Queen orchestration works with Max subscription

## Implementation Tasks

### Phase 0: Research & Discovery (3 days)

#### Task 0.1: Claude Code Model Investigation
**Priority**: Critical
**Effort**: 0.5 days
**Owner**: Task Master

**Objectives**:
- Validate Claude Code uses automatic model selection (no manual model parameters)
- Confirm available Claude models through Max subscription
- Test actual model responses to understand which model Claude Code selects

**Available Models (Internal Mapping)**:
- `claude-opus-4-1-20250805` (Opus 4.1)
- `claude-opus-4-20250514` (Opus 4)
- `claude-sonnet-4-20250514` (Sonnet 4)
- `claude-3-7-sonnet-20250219` (Sonnet 3.7)
- `claude-3-5-haiku-20241022` (Haiku 3.5)

**Note**: Opus models unavailable to Pro plan users

**Deliverables**:
- Confirmation of automatic model selection behavior
- Test results showing which model Claude Code actually uses
- Updated model mapping strategy based on findings

**Testing Commands**:
```bash
# Test which model Claude Code actually uses
claude-code task --config '{"subagent_type":"general-purpose","description":"model identification","prompt":"What model are you? Provide your exact model name and version."}'
```

#### Task 0.2: Model Mapping Strategy  
**Priority**: Medium
**Effort**: 0.5 days
**Owner**: Task Master

**Objectives**:
- Implement simple model name mapping without worker detection
- Create clean model name to Claude Code model name mapping
- Validate all supported model mappings

**Approach**: Direct model specification - no worker detection complexity

**Deliverables**:
- Model mapping dictionary implementation
- Validation of all Claude Code model name mappings
- Simple fallback to Sonnet 4 for unknown models

#### Task 0.3: Performance Baseline
**Priority**: Medium
**Effort**: 1 day  
**Owner**: Task Master

**Objectives**:
- Measure Claude Code Task subprocess overhead
- Test concurrent request handling
- Establish performance thresholds

**Deliverables**:
- Performance benchmark report
- Concurrency test results
- Acceptable latency thresholds

### Phase 1: Core Implementation (5 days)

#### Task 1.1: MaxSubscriptionProvider Implementation
**Priority**: Critical
**Effort**: 2 days
**Owner**: Task Master
**Dependencies**: Task 0.1 (model availability)

**Objectives**:
- Implement custom provider class extending AnthropicProvider
- Create message format conversion methods
- Build Claude Code subprocess execution

**File**: `.claude/agents/pydantic_ai/shared/max_subscription_provider.py` (single file - clean implementation)

**Key Components**:
```python
class MaxSubscriptionProvider(AnthropicProvider):
    def __init__(self):
        self.worker_model_mapping = {
            'queen-orchestrator': 'custom:claude-opus-4',     # Maps to claude-opus-4-20250514
            'analyzer-worker': 'custom:claude-3-7-sonnet',    # Maps to claude-3-7-sonnet-20250219
            'architect-worker': 'custom:claude-sonnet-4',     # Maps to claude-sonnet-4-20250514
            # ... other mappings - all workers default to Sonnet 4 except Queen
        }
        
        self.default_model = 'custom:claude-sonnet-4'  # Default for custom:max-subscription
        
        self.claude_code_model_mapping = {
            'custom:claude-opus-4': 'claude-opus-4-20250514',
            'custom:claude-sonnet-4': 'claude-sonnet-4-20250514', 
            'custom:claude-3-7-sonnet': 'claude-3-7-sonnet-20250219',
            'custom:claude-3-5-haiku': 'claude-3-5-haiku-20241022',
        }
    
    async def request_structured_response(self, messages, model_name, **kwargs):
        if model_name == 'custom:max-subscription':
            # Simple default - always Sonnet 4, no worker detection
            actual_model = self.default_model
        elif model_name.startswith('custom:claude-'):
            # Direct model specification (e.g., 'custom:claude-opus-4')
            actual_model = model_name
        else:
            # Fallback to default model
            actual_model = self.default_model
            
        prompt = self._format_messages_for_claude_code(messages)
        claude_code_model = self.claude_code_model_mapping.get(actual_model, actual_model)
        response = await self._execute_claude_code_task(prompt, claude_code_model)
        return self._format_as_anthropic_response(response, actual_model)
```

**Deliverables**:
- Complete MaxSubscriptionProvider class
- Message format conversion methods
- Basic error handling
- Unit tests

#### Task 1.2: Worker Type Detection Implementation
**Priority**: High
**Effort**: 1 day
**Owner**: Task Master  
**Dependencies**: Task 0.2 (detection strategy)

**Objectives**:
- Implement chosen worker detection method
- Create model selection logic
- Test detection accuracy

**Deliverables**:
- Worker type detection implementation
- Model selection method
- Detection accuracy tests

#### Task 1.3: Claude Code Task Integration
**Priority**: Critical
**Effort**: 2 days
**Owner**: Task Master
**Dependencies**: Task 0.1 (Claude Code interface)

**Objectives**:
- Implement subprocess task execution
- Handle Claude Code errors and timeouts
- Create response parsing logic

**Key Methods**:
```python
async def _execute_claude_code_task(self, prompt: str, model: str) -> str:
    task_config = {
        "subagent_type": "general-purpose",
        "description": "Max subscription proxy request",
        "prompt": f"Original: {prompt}\nTarget model: {model}\nRespond with ONLY the response content."
    }
    
    process = await asyncio.create_subprocess_exec(
        'claude-code', 'task', '--config', json.dumps(task_config),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    # ... error handling and response parsing
```

**Deliverables**:
- Claude Code subprocess integration
- Error handling for all failure modes
- Timeout and retry logic
- Response format validation

### Phase 2: Integration & Testing (5 days)

#### Task 2.1: Monkey Patch System
**Priority**: High
**Effort**: 1 day
**Owner**: Task Master

**Objectives**:
- Create global monkey patch for AnthropicModel
- Enable `custom:max-subscription` model name
- Preserve existing model behavior

**File**: `.claude/agents/pydantic_ai/shared/monkey_patch.py`

**Implementation**:
```python
def enable_max_subscription_globally():
    OriginalAnthropicModel = anthropic_module.AnthropicModel
    
    class MaxSubscriptionAnthropicModel(OriginalAnthropicModel):
        def __init__(self, model_name: str, provider=None, **kwargs):
            if model_name == 'custom:max-subscription':
                if provider is None:
                    provider = MaxSubscriptionProvider()
            super().__init__(model_name, provider, **kwargs)
    
    anthropic_module.AnthropicModel = MaxSubscriptionAnthropicModel
```

**Deliverables**:
- Monkey patch implementation
- Automatic initialization in `__init__.py`
- Verification tests

#### Task 2.2: Individual Worker Testing
**Priority**: High
**Effort**: 2 days
**Owner**: Task Master
**Dependencies**: Task 1.1, 1.2, 1.3

**Objectives**:
- Test each worker type with Max subscription
- Verify response quality and format
- Confirm zero API credit usage

**Test Commands**:
```bash
# Test each worker type
python cli.py analyzer --session test-session --task "Security analysis test"
python cli.py architect --session test-session --task "Architecture review test"  
python cli.py backend --session test-session --task "Backend implementation test"
# ... etc for all worker types
```

**Deliverables**:
- Worker-specific test results
- Response quality comparison
- Performance metrics
- Error handling validation

#### Task 2.3: Queen Orchestration Testing
**Priority**: Critical
**Effort**: 2 days
**Owner**: Task Master
**Dependencies**: Task 2.2

**Objectives**:
- Test Queen orchestrator with Max subscription
- Verify worker spawning and coordination
- Validate session management

**Test Scenario**:
```bash
# Test full Queen orchestration
python cli.py queen --session test-session --task "Analyze crypto-data architecture focusing on security, performance, and scalability" --model custom:max-subscription
```

**Deliverables**:
- Queen orchestration validation
- Multi-worker coordination test
- Session persistence verification
- Complete crypto-data analysis execution

### Phase 3: Production Deployment (2 days)

#### Task 3.1: Production Configuration
**Priority**: Medium
**Effort**: 0.5 days
**Owner**: Task Master

**Objectives**:
- Configure environment variables
- Set up monitoring and logging
- Create deployment documentation

**Deliverables**:
- Production configuration guide
- Environment setup instructions
- Monitoring dashboard setup

#### Task 3.2: Deployment & Validation
**Priority**: Critical
**Effort**: 1.5 days
**Owner**: Task Master

**Objectives**:
- Deploy to production environment
- Monitor for API credit usage (should be zero)
- Validate all workers function correctly

**Deployment Steps**:
1. Deploy files to `.claude/agents/pydantic_ai/shared/`
2. Restart Pydantic AI processes
3. Monitor system behavior
4. Validate worker functionality

**Deliverables**:
- Production deployment
- Usage monitoring report
- System validation results
- User documentation

## Acceptance Criteria

### Primary Success Metrics
- ✅ **Zero API Credit Usage**: No charges to Anthropic, OpenAI, or Google accounts
- ✅ **Response Quality**: Identical output quality compared to direct API calls  
- ✅ **Performance**: <20% overhead compared to direct API calls
- ✅ **Compatibility**: 100% compatibility with existing worker outputs
- ✅ **Reliability**: 99%+ success rate for normal operations

### Secondary Success Metrics
- ✅ **Universal Interface**: `Agent('custom:max-subscription')` works across all workers
- ✅ **Intelligent Routing**: Queen uses Opus, others use Sonnet 4/3.7
- ✅ **Error Handling**: Graceful failures with clear error messages
- ✅ **Zero Config**: No changes required to existing worker code
- ✅ **Queen Orchestration**: Full crypto-data analysis completes successfully

## Risk Mitigation

### Technical Risks

#### Risk: Claude Code Model Availability
**Impact**: High
**Probability**: Medium
**Mitigation**: Research Phase 0 tasks validate model availability before implementation

#### Risk: Performance Overhead  
**Impact**: Medium
**Probability**: Low
**Mitigation**: Performance benchmarking in Task 0.3, optimization in Phase 3

#### Risk: Worker Type Detection Failure
**Impact**: High  
**Probability**: Low
**Mitigation**: Multiple detection strategies evaluated in Task 0.2

### Operational Risks

#### Risk: Claude Code Dependency
**Impact**: Medium
**Probability**: Low  
**Mitigation**: Fail-fast strategy with clear error messages, session preservation, subprocess-per-request isolation

#### Risk: Max Subscription Quota Limits
**Impact**: Medium
**Probability**: Medium
**Mitigation**: Quota monitoring, early warning system, session resumption capability

## Dependencies

### External Dependencies
- Claude Code availability and Max subscription access
- Pydantic AI framework stability
- Python subprocess execution capability

### Internal Dependencies  
- Existing Pydantic AI worker architecture
- Session management system
- Queen orchestration system

## Success Metrics & KPIs

### Immediate Metrics (Week 1)
- Model availability matrix completed
- MaxSubscriptionProvider implementation complete
- Basic worker tests passing

### Intermediate Metrics (Week 2)  
- All worker types tested and validated
- Queen orchestration functional
- Zero API credit usage confirmed

### Final Metrics (Week 3)
- Production deployment successful
- Full crypto-data analysis completion
- Documentation and monitoring in place

## Deliverables Summary

### Code Deliverables
- `.claude/agents/pydantic_ai/shared/max_subscription_provider.py` (single file - complete implementation)
- Updated `.claude/agents/pydantic_ai/shared/__init__.py` (automatic activation)

### Documentation Deliverables
- Model availability matrix
- Worker detection design document
- Performance benchmark report
- Production deployment guide
- User documentation

### Testing Deliverables
- Unit tests for MaxSubscriptionProvider
- Integration tests for all worker types
- Queen orchestration validation tests
- Performance and reliability tests

## Conclusion

This PRD provides a comprehensive plan for integrating Pydantic AI with Claude Code's Max subscription, eliminating API costs while maintaining full functionality. The phased approach ensures thorough research, robust implementation, and reliable deployment.

**Expected Outcome**: Complete cost elimination for AI operations while preserving all existing functionality and enabling access to the latest Claude models through Max subscription.