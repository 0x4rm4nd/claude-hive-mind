# Claude Hive-Mind Commands

Essential commands for session management and Archon integration. All commands use MCP tools only - no bash scripts.

## 🏆 Core Session Management

### `/summon-queen` 
**Purpose**: Start new hive-mind session  
**Usage**: `summon-queen "implement user authentication"`  
**Creates**: Session directory, Archon integration, initial coordination files

### `/resume-session`
**Purpose**: Resume interrupted session  
**Usage**: `resume-session SESSION_ID`  
**Loads**: STATE.json, worker notes, pending notifications from EVENTS.jsonl

### `/analyze-session`
**Purpose**: Check session progress  
**Usage**: `analyze-session SESSION_ID`  
**Shows**: Task status, worker progress, coordination bottlenecks

## 📋 Task & Progress Monitoring  

### `/task-bridge`
**Purpose**: Monitor Archon task progress  
**Usage**: `task-bridge SESSION_ID`  
**Updates**: SESSION.md with current progress, identifies bottlenecks

### `/archive-session`
**Purpose**: Complete session with reflection  
**Usage**: `archive-session SESSION_ID`  
**Creates**: Comprehensive REFLECTION.md, pattern library extracts, Archon KB upload

## 🏗️ Knowledge Integration

### `/research-to-archon`  
**Purpose**: Upload research to Archon KB  
**Usage**: `research-to-archon SESSION_ID`  
**Uploads**: Session research findings for future RAG retrieval

### `/archon-init`
**Purpose**: Initialize Archon integration  
**Usage**: Auto-triggered by `/summon-queen`  
**Sets up**: Project connection, task creation, session structure

## 🔄 Session Flow

```
summon-queen → archon-init → [development cycle] → task-bridge → research-to-archon → archive-session
                 ↓                ↓                    ↓
              Archon setup    Workers execute      Monitor progress
                             resume-session       
                             analyze-session
```

## ⚡ Key Features

- **MCP Tools Only**: No bash scripts, uses Read/Write/Edit tools
- **Archon Integration**: Task sync, knowledge base, progress tracking  
- **True Parallel**: Multiple Task tool calls for concurrent worker execution
- **Unified Events**: Single EVENTS.jsonl for all coordination
- **Session Resume**: Complete state preservation for interruption recovery
- **Learning Loop**: Each session enriches knowledge base for future sessions

All commands are designed for token efficiency and robust session management.