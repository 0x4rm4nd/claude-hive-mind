# Claude API Service

Docker-based Claude CLI service that provides HTTP API access to Claude with full workspace access. This service solves the nested subprocess authentication issues by running Claude CLI in a clean Docker environment.

## Purpose

**Problem Solved**: Pydantic AI running within Claude Code creates nested subprocess calls that lose Max subscription authentication context, causing "Credit balance is too low" errors.

**Solution**: This Docker service runs Claude CLI independently with full workspace access, accessible via HTTP API.

## Architecture

```
Pydantic AI (in Claude Code)
    ↓ HTTP Request
Claude API Service (Docker)
    ↓ Direct subprocess (no nesting!)  
Claude CLI (with Max subscription)
```

## Features

- 🔧 **Max subscription integration** - Routes Pydantic AI through Claude Max subscription
- 🚀 **Eliminates nested subprocess issues** - Clean Docker environment for Claude CLI
- 🔍 **Complexity assessment** - AI-powered task complexity analysis for scribe runner
- 🐳 **Simple Docker service** - Minimal overhead, focused on core integration

## Quick Start

### 1. Start the Service

```bash
cd .claude/claude-api-service
docker-compose up -d
```

### 2. **REQUIRED: Authenticate Claude CLI in Container**

⚠️ **Manual Step Required**: You must authenticate Claude CLI inside the Docker container:

```bash
docker exec -it claude-max-api claude setup-token
```

This will:
- Open a browser window for Claude authentication
- Generate a long-lived OAuth token (valid for 1 year)
- Enable Max subscription access within the Docker environment

**Note**: This is a one-time setup. The authentication persists until the Docker volume is removed.

### 3. Verify Health

```bash
curl http://localhost:47291/health
```

### 4. Test Claude Integration

```bash
curl -X POST http://localhost:47291/claude \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Say hello from Docker!", "model": "sonnet"}'
```

## API Endpoints

### Core Claude Operations

- **POST /claude** - Generic Claude CLI proxy for any Pydantic AI request

### Health & Status

- **GET /health** - Service health check
- **GET /** - Service information and available endpoints

## Usage Examples

### Generic Claude Request

```bash
curl -X POST http://localhost:47291/claude \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Any prompt for Claude - analysis, generation, planning, etc.",
    "model": "sonnet",
    "timeout": 120
  }'
```

### Pydantic AI Integration Example

```bash
# This is what happens when you use Agent('custom:max-subscription')
curl -X POST http://localhost:47291/claude \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "System: You are a helpful assistant.\n\nUser: Explain quantum computing",
    "model": "sonnet"
  }'
```

### Check Service Health

```bash
curl http://localhost:47291/health
```

## Configuration

### Environment Variables

- `WORKSPACE_ROOT` - Path to project workspace (default: `/workspace`)
- `CLAUDE_CONFIG_PATH` - Path to Claude config (default: `/claude-config`) 
- `PORT` - API service port (default: `8080`, exposed on: `47291`)

### Docker Volumes

- `../../:/workspace:ro` - Mount project workspace (read-only) for Claude CLI analysis
- `~/.claude:/claude-config:ro` - Mount Claude config (read-only) for reference

**Note**: Claude authentication is done directly in the container via `claude setup-token`, not through mounted volumes.

## Integration with Pydantic AI

The service automatically integrates with Pydantic AI through `ClaudeAPISubscriptionProvider`:

```python
# Automatically used when custom:max-subscription model is requested
agent = Agent('custom:max-subscription')  
result = agent.run_sync('Analyze the API service authentication')
```

The provider:
1. Auto-starts the Docker service if not running
2. Routes Pydantic AI requests to the API service  
3. Returns structured responses compatible with Pydantic AI

## Core Purpose

The service provides a simple HTTP interface to Claude CLI for:

- **Pydantic AI Integration** - Routes `Agent('custom:max-subscription')` calls
- **Scribe Runner Support** - Provides complexity assessment for session creation
- **Max Subscription Access** - Uses Claude Code's subscription without API costs

## Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (for testing)
python server.py

# Service runs on http://localhost:47291
```

### Docker Development

```bash
# Build and run
docker-compose up --build

# View logs
docker-compose logs -f claude-api

# Stop service
docker-compose down
```

## Troubleshooting

### Service Won't Start

```bash
# Check Docker status
docker-compose ps

# View logs
docker-compose logs claude-api

# Rebuild if needed
docker-compose up --build -d
```

### Claude CLI Authentication Issues

If you see authentication errors:

```bash
# Check if Claude CLI is authenticated
docker exec claude-max-api claude --print --model sonnet "test"

# If you see "Invalid API key · Please run /login", re-authenticate:
docker exec -it claude-max-api claude setup-token
```

Common authentication issues:
- **"Invalid API key"**: Run `docker exec -it claude-max-api claude setup-token`
- **Service timeout**: Claude CLI might be hanging on authentication prompt
- **Container restarts**: Authentication persists in Docker volumes, not affected by restarts

```bash
# Check health endpoint
curl http://localhost:47291/health

# Verify Claude CLI access in container  
docker-compose exec claude-api claude --help
```

### Pydantic AI Integration Issues

```bash
# Test the provider directly
cd .claude/agents/pydantic_ai
python -c "
from shared.claude_api_subscription_provider import ClaudeAPISubscriptionProvider
import asyncio

async def test():
    provider = ClaudeAPISubscriptionProvider()
    result = await provider.call_complexity_assessment('Test task')
    print(result)

asyncio.run(test())
"
```

## Architecture Benefits

### ✅ **Eliminates Nested Subprocess Issues**
- Claude CLI runs in clean Docker environment
- No authentication context inheritance problems
- Reliable Max subscription access

### ✅ **Full Workspace Access**
- Complete project repository mounted
- Cross-service analysis capabilities
- File modification potential (future feature)

### ✅ **Scalable Architecture**
- Independent Docker service
- HTTP API for easy integration
- Can be extended with additional features

### ✅ **Development Integration**
- Works with existing Docker Compose setup
- Auto-starts when needed
- Health checks and monitoring