# Pydantic AI Max Subscription Integration Plan

## Overview
This document outlines the implementation plan for integrating Pydantic AI with Claude Code's Max subscription, eliminating the need for separate API credits while maintaining full compatibility with existing worker architecture.

## Problem Statement
- Pydantic AI workers currently require separate API credits for Anthropic, OpenAI, or Google models
- User has Claude Code Max subscription but cannot leverage it for Pydantic AI workers
- Current architecture relies on HTTP API calls that bypass subscription benefits

## Solution Architecture

### Core Concept: Custom Provider Pattern
Leverage Pydantic AI's provider architecture to route model requests through Claude Code's Max subscription instead of direct API calls.

```
Current Flow:
Pydantic AI → AnthropicProvider → HTTP API → Anthropic Servers (requires credits)

New Flow:  
Pydantic AI → MaxSubscriptionProvider → Claude Code Task → Max Subscription (no credits)
```

### Model Selection Strategy

#### Universal Model Name Interface
Workers use a single, safe custom model name that won't conflict with existing models:
```python
# Single universal interface
agent = Agent('custom:max-subscription')
```

#### Intelligent Worker-Specific Routing
The MaxSubscriptionProvider automatically routes to optimal models based on worker type:

```python
WORKER_MODEL_MAPPING = {
    'queen-orchestrator': 'claude-3-opus',          # Complex orchestration needs maximum capability
    'analyzer-worker': 'claude-3.7-sonnet',        # Security analysis needs accuracy
    'architect-worker': 'claude-4-sonnet',         # System design needs latest capabilities  
    'backend-worker': 'claude-4-sonnet',           # Implementation needs latest features
    'frontend-worker': 'claude-4-sonnet',          # UI development needs latest capabilities
    'designer-worker': 'claude-4-sonnet',          # Design needs creative capabilities
    'devops-worker': 'claude-4-sonnet',            # Infrastructure needs latest knowledge
    'researcher-worker': 'claude-4-sonnet',        # Research needs comprehensive analysis
    'test-worker': 'claude-4-sonnet',              # Testing needs thorough analysis
    'scribe': 'claude-3.7-sonnet',                 # Simple tasks, default fallback
}

# Fallback hierarchy
DEFAULT_MODEL = 'claude-3.7-sonnet'  # If 3.7 unavailable, fall back to latest available
FALLBACK_MODELS = ['claude-3.5-sonnet-20241022', 'claude-3-5-sonnet-latest']
```

## Critical Implementation Questions

### Claude Code Model Availability & Selection
1. **Model Verification**: Which Claude models are actually available through Claude Code Max subscription?
   - Is Claude 3.7 Sonnet available in Claude Code?
   - Is Claude 4 Sonnet available? (Or is it Claude 3.5 Sonnet?)
   - What's the latest Opus version accessible?

2. **Model Selection in Claude Code**: How can we specify which Claude model to use?
   - Does Claude Code Task tool accept model parameters?
   - Does it automatically use the best available model?
   - Can we pass model preferences in the task configuration?

### Technical Architecture Decisions
3. **Worker Type Detection**: How do we identify which worker is making the request?
   - Parse from the calling stack/context?
   - Require workers to explicitly identify themselves?
   - Use session metadata or task configuration?

4. **Performance & Concurrency**: 
   - Should we cache subprocess connections or create fresh ones?
   - How do we handle multiple concurrent requests from different workers?
   - What's the acceptable overhead of subprocess creation vs API calls?

5. **Claude Code Integration**:
   - Can we validate Claude Code authentication before making requests?
   - Should we check Claude Code availability on provider initialization?
   - How do we handle Claude Code updates that might change the Task interface?

### Error Handling & Reliability
6. **Failure Modes**:
   - What if Claude Code returns empty/malformed responses?
   - How do we distinguish Claude Code errors from Claude model errors?
   - Should we implement request timeouts and how long?

7. **Quota Management**:
   - How do we detect Max subscription quota limits?
   - Should we implement usage tracking/monitoring?
   - Can we provide early warnings before hitting limits?

### Configuration & Maintenance
8. **Model Mapping Updates**:
   - Should worker-model mappings be configurable via environment variables?
   - How do we handle new Claude models becoming available?
   - Should there be per-session model override capabilities?

9. **Backward Compatibility**:
   - What happens to existing worker configs that specify real model names?
   - Should we provide automatic migration warnings?
   - Do we need a gradual rollout strategy?

### Testing & Validation
10. **Testing Strategy**:
    - How do we test without consuming Max subscription quota?
    - Should we create a mock Claude Code executable for CI/CD?
    - How do we validate response format compatibility?

11. **Monitoring & Debugging**:
    - Should we log all Max subscription requests for debugging?
    - How do we provide usage analytics and performance metrics?
    - What level of error detail should we expose to users?

## Implementation Plan

### Phase 1: Custom Provider Implementation

#### 1.1 MaxSubscriptionProvider Class
**File**: `.claude/agents/pydantic_ai/shared/max_subscription_provider.py`

```python
from typing import Any, Dict, List, Optional
import asyncio
import json
import subprocess
from pydantic_ai.providers.anthropic import AnthropicProvider

class MaxSubscriptionProvider(AnthropicProvider):
    """Provider that routes Anthropic requests through Claude Code's Max subscription"""
    
    def __init__(self, claude_code_executable: str = "claude-code"):
        # Override parent __init__ to avoid HTTP client setup
        self.claude_code_executable = claude_code_executable
        self.worker_model_mapping = {
            'queen-orchestrator': 'claude-3-opus',
            'analyzer-worker': 'claude-3.7-sonnet', 
            'architect-worker': 'claude-4-sonnet',
            'backend-worker': 'claude-4-sonnet',
            'frontend-worker': 'claude-4-sonnet', 
            'designer-worker': 'claude-4-sonnet',
            'devops-worker': 'claude-4-sonnet',
            'researcher-worker': 'claude-4-sonnet',
            'test-worker': 'claude-4-sonnet',
            'scribe': 'claude-3.7-sonnet',
        }
        self.default_model = 'claude-3.7-sonnet'
        self.fallback_models = ['claude-3.5-sonnet-20241022', 'claude-3-5-sonnet-latest']
    
    async def request_structured_response(self, messages, model_name, **kwargs):
        """Route request through Claude Code instead of Anthropic API"""
        if model_name == 'custom:max-subscription':
            # Detect worker type and select appropriate model
            actual_model = self._select_model_for_worker()
        else:
            # Fallback for other model names (shouldn't happen with our setup)
            actual_model = self.default_model
            
        prompt = self._format_messages_for_claude_code(messages)
        claude_response = await self._execute_claude_code_task(prompt, actual_model)
        return self._format_as_anthropic_response(claude_response, actual_model)
    
    def _select_model_for_worker(self) -> str:
        """Detect worker type and return appropriate model"""
        # TODO: Implement worker type detection logic
        # For now, return default model
        return self.default_model
```

**Key Features**:
- Inherits from AnthropicProvider for compatibility
- Overrides HTTP-based methods to use subprocess calls
- Maintains Anthropic API response format
- Maps model names to Claude Code compatible versions

#### 1.2 Claude Code Integration Layer
**File**: `.claude/agents/pydantic_ai/shared/claude_code_integration.py`

```python
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from .max_subscription_provider import MaxSubscriptionProvider

def create_max_subscription_model():
    """Create AnthropicModel that uses Max subscription via proxy"""
    provider = MaxSubscriptionProvider()
    # Always use the universal custom model name
    return AnthropicModel('custom:max-subscription', provider=provider)

def create_max_subscription_agent(**agent_kwargs):
    """Create Pydantic AI Agent using Max subscription"""
    model = create_max_subscription_model()
    return Agent(model, **agent_kwargs)

# Convenience function for existing code
def agent_with_max_subscription(**agent_kwargs):
    """Drop-in replacement for Agent('anthropic:claude-3-5-sonnet-latest')"""
    return Agent('custom:max-subscription', **agent_kwargs)
```

### Phase 2: Global Integration

#### 2.1 Monkey Patch for Existing Workers
**File**: `.claude/agents/pydantic_ai/shared/monkey_patch.py`

```python
import pydantic_ai.models.anthropic as anthropic_module
from .max_subscription_provider import MaxSubscriptionProvider

def enable_max_subscription_globally():
    """Monkey-patch all Anthropic models to use Max subscription"""
    OriginalAnthropicModel = anthropic_module.AnthropicModel
    
    class MaxSubscriptionAnthropicModel(OriginalAnthropicModel):
        def __init__(self, model_name: str, provider=None, **kwargs):
            # Route custom:max-subscription through our provider
            if model_name == 'custom:max-subscription':
                if provider is None:
                    provider = MaxSubscriptionProvider()
                super().__init__(model_name, provider, **kwargs)
            else:
                # For other model names, use original behavior
                super().__init__(model_name, provider, **kwargs)
    
    anthropic_module.AnthropicModel = MaxSubscriptionAnthropicModel
    print("✅ Custom Max subscription model 'custom:max-subscription' now available")

def patch_existing_workers():
    """Update existing worker configurations to use Max subscription"""
    # This could be used to automatically convert existing workers
    # For now, workers need to be updated manually to use 'custom:max-subscription'
    pass
```

#### 2.2 Automatic Initialization
**File**: `.claude/agents/pydantic_ai/shared/__init__.py`

Add to existing file:
```python
# Import and apply Max subscription patch
from .monkey_patch import enable_max_subscription_globally

# Enable Max subscription for all workers on module import
enable_max_subscription_globally()
```

### Phase 3: Message Format Conversion

#### 3.1 Anthropic API to Claude Code Format
```python
def _format_messages_for_claude_code(self, messages: List[Dict[str, Any]]) -> str:
    """Convert Anthropic API messages to Claude Code format"""
    formatted = []
    
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        
        # Handle multi-part content (text + images)
        if isinstance(content, list):
            text_parts = [part.get("text", "") for part in content if part.get("type") == "text"]
            content = " ".join(text_parts)
        
        formatted.append(f"{role.capitalize()}: {content}")
    
    return "\n\n".join(formatted)
```

#### 3.2 Claude Code to Anthropic API Response
```python
def _format_as_anthropic_response(self, claude_response: str, model: str) -> Dict[str, Any]:
    """Convert Claude Code response to Anthropic API format"""
    import uuid
    
    return {
        "id": f"msg_{uuid.uuid4()}",
        "type": "message", 
        "role": "assistant",
        "content": [{"type": "text", "text": claude_response}],
        "model": model,
        "usage": {
            "input_tokens": 0,  # Not tracked by proxy
            "output_tokens": len(claude_response.split())  # Rough estimate
        },
        "stop_reason": "end_turn"
    }
```

### Phase 4: Claude Code Task Execution

#### 4.1 Subprocess Task Spawning
```python
async def _execute_claude_code_task(self, prompt: str, model: str) -> str:
    """Execute request via Claude Code Task tool"""
    
    task_config = {
        "subagent_type": "general-purpose",
        "description": "Max subscription proxy request", 
        "prompt": f"""You are proxying a request from Pydantic AI to use Claude Code's Max subscription.

Original request: {prompt}
Target model: {self._model_names.get(model, model)}

Respond with ONLY the AI model's response content. No additional formatting, metadata, or explanations."""
    }
    
    # Create subprocess to execute claude-code task
    process = await asyncio.create_subprocess_exec(
        self.claude_code_executable, 
        "task",
        "--config", json.dumps(task_config),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    
    if process.returncode != 0:
        raise Exception(f"Claude Code task failed: {stderr.decode()}")
        
    return stdout.decode().strip()
```

## Testing Strategy

### Integration Testing
1. **Test Individual Components**:
   ```bash
   # Test MaxSubscriptionProvider directly
   python -m pytest shared/test_max_subscription_provider.py
   ```

2. **Test Worker Integration**:
   ```bash
   # Test Queen orchestrator with Max subscription
   python cli.py queen --session test-session --task "Test Max subscription integration" --model anthropic:claude-3-5-sonnet-latest
   ```

3. **Test Existing Workers**:
   ```bash
   # Verify all existing workers use Max subscription
   python cli.py analyzer --session test-session --task "Security analysis test"
   python cli.py architect --session test-session --task "Architecture review test"
   ```

### Validation Criteria
- ✅ No API credit usage during Pydantic AI worker execution
- ✅ Identical response quality compared to direct API calls
- ✅ Zero code changes required for existing workers
- ✅ Proper error handling and timeout management
- ✅ Response format compatibility with Pydantic AI expectations

## Deployment Steps

### Step 1: Implementation
1. Create MaxSubscriptionProvider class
2. Implement message format converters
3. Add Claude Code task execution logic
4. Create monkey patch system

### Step 2: Integration
1. Update shared/__init__.py to enable globally
2. Test with individual worker types
3. Verify Queen orchestration compatibility

### Step 3: Validation
1. Run comprehensive test suite
2. Monitor for API credit usage (should be zero)
3. Compare response quality and accuracy
4. Test error handling and edge cases

### Step 4: Activation
1. Deploy to .claude/agents/pydantic_ai/shared/
2. Restart any running Pydantic AI processes
3. Verify automatic activation via monkey patch
4. Document successful integration

## Benefits

### Immediate Benefits
- **Zero API Costs**: All Pydantic AI workers use Max subscription
- **Transparent Integration**: No code changes needed for existing workers
- **Latest Models**: Access to newest Claude models through Max subscription
- **Improved Reliability**: No quota limits or rate limiting issues

### Long-term Benefits
- **Scalable Architecture**: Can extend to other subscription-based services
- **Cost Control**: Predictable subscription costs vs variable API usage
- **Enhanced Features**: Access to Max subscription exclusive features
- **Simplified Management**: Single subscription vs multiple API keys

## Risk Mitigation

### Technical Risks
- **Performance Impact**: Subprocess overhead vs direct HTTP calls
  - *Mitigation*: Benchmark and optimize task execution
- **Error Handling**: Claude Code task failures
  - *Mitigation*: Comprehensive error handling and fallback mechanisms
- **Format Compatibility**: Response format differences
  - *Mitigation*: Extensive testing and format validation

### Operational Risks  
- **Dependency on Claude Code**: Requires Claude Code availability
  - *Mitigation*: Fallback to direct API calls if Claude Code unavailable
- **Breaking Changes**: Claude Code Task tool changes
  - *Mitigation*: Version compatibility checks and adaptation layer

## Success Metrics

### Performance Metrics
- Response time comparable to direct API calls (target: <20% overhead)
- Zero API credit consumption
- 100% compatibility with existing worker outputs
- Error rate <1% for normal operations

### Quality Metrics
- Response accuracy matches direct API calls
- No degradation in worker performance
- Successful Queen orchestration with Max subscription
- Complete crypto-data analysis execution

## Next Steps: Critical Questions to Resolve

### Phase 0: Research & Discovery (Before Implementation)
**Priority 1: Claude Code Model Capabilities**
1. **Test Claude Code model availability** - What models can we actually access?
   ```bash
   # Test different model requests through Claude Code
   claude-code task --config '{"subagent_type":"general-purpose","description":"model test","prompt":"What model are you?"}'
   ```

2. **Investigate model selection** - Can we specify models in Claude Code Task calls?
   ```bash
   # Try different task configurations to see if model selection is possible
   claude-code task --model claude-3-opus --config '{"prompt":"test"}'  # Does this work?
   ```

**Priority 2: Worker Type Detection Strategy**
- Option A: Parse from calling context/stack trace
- Option B: Modify worker constructors to pass worker type
- Option C: Use task metadata/session context

**Priority 3: Performance Baseline**
- Measure Claude Code Task overhead vs direct API calls
- Test concurrent request handling
- Establish acceptable latency thresholds

### Phase 1: Minimal Viable Implementation
Based on research findings, implement core functionality:

1. **Basic MaxSubscriptionProvider** with hardcoded model selection
2. **Simple worker type detection** (chosen approach from Phase 0)
3. **Universal model name support** (`custom:max-subscription`)
4. **Basic error handling** and quota detection

### Phase 2: Advanced Features  
1. **Intelligent model routing** based on worker types
2. **Configuration system** for model mappings
3. **Comprehensive error handling** and recovery
4. **Performance optimizations** and caching

## Implementation Timeline

### Week 1: Research & Core Implementation
- Day 1-2: Research Claude Code model capabilities and selection
- Day 3-4: Implement basic MaxSubscriptionProvider 
- Day 5-7: Basic message format conversion and Claude Code integration

### Week 2: Worker Integration & Testing  
- Day 1-2: Worker type detection and intelligent routing
- Day 3-4: Monkey patch system and global integration
- Day 5-7: Testing with individual workers and Queen orchestration

### Week 3: Advanced Features & Deployment
- Day 1-3: Configuration system and error handling improvements
- Day 4-5: Performance optimization and concurrent request handling  
- Day 6-7: Production deployment and monitoring setup

## Conclusion

This implementation provides a robust, scalable solution for integrating Pydantic AI workers with Claude Code's Max subscription. The provider pattern ensures compatibility while the monkey patch approach requires zero code changes to existing workers.

The solution transforms API credit consumption into subscription utilization, providing cost predictability and access to the latest Claude models without additional charges.