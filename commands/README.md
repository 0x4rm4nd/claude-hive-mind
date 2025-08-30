# Claude Hive-Mind Commands

Essential commands for local session management. All commands use MCP tools only - no bash scripts.

## 🏆 Core Session Management

### `/summon-queen` 
**Purpose**: Start new hive-mind session  
**Usage**: `summon-queen "implement user authentication"`  
**Creates**: Session directory and initial coordination files

### `/resume-session`
**Purpose**: Resume interrupted session  
**Usage**: `resume-session SESSION_ID`  
**Loads**: STATE.json, worker notes, pending notifications from EVENTS.jsonl

### `/analyze-session`
**Purpose**: Check session progress  
**Usage**: `analyze-session SESSION_ID`  
**Shows**: Task status, worker progress, coordination bottlenecks

### `/archive-session`
**Purpose**: Complete session with reflection  
**Usage**: `archive-session SESSION_ID`  
**Creates**: Comprehensive REFLECTION.md and pattern library extracts

## 🔄 Session Flow

```
summon-queen → [development cycle] → analyze-session → archive-session
                 ↓                ↓                    
              Session setup   Workers execute      
                             resume-session       
```

## ⚡ Key Features

- **MCP Tools Only**: No bash scripts, uses Read/Write/Edit tools
- **Local-First**: All session and task management is handled locally
- **True Parallel**: Multiple Task tool calls for concurrent worker execution
- **Unified Events**: Single EVENTS.jsonl for all coordination
- **Session Resume**: Complete state preservation for interruption recovery
- **Learning Loop**: Each session can enrich a local knowledge base/pattern library

All commands are designed for token efficiency and robust session management.