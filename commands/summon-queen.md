---
name: summon-queen
description: Launch multi-agent orchestration with Queen coordinator
arguments: $ARGUMENTS
---

# 👑 Constraint-Based Multi-Agent Orchestration System

## 🚨 MANDATORY PRE-EXECUTION VALIDATION

**YOU ARE TEMPORARILY DISABLED FROM TECHNICAL ANALYSIS**

Until ALL orchestration steps complete successfully, you CANNOT:
- Provide architecture analysis
- Make security recommendations  
- Suggest performance improvements
- Give implementation guidance
- Analyze code or systems

**Why This Constraint Exists:**
Multi-agent specialist analysis produces superior results that general analysis cannot match. Specialist agents have access to:
- Domain-specific knowledge bases (Context7, Memory Bank)
- Specialized analysis tools and techniques
- Cross-domain integration capabilities
- Deep expertise in their specific areas

## 🔒 TECHNICAL ENFORCEMENT GATES

### Gate 1: Command Recognition 
```
✅ PASSED: /summon-queen command used
📋 Task: $ARGUMENTS
🎯 Outcome: Multi-specialist analysis with superior insights
```

### Gate 2: Mandatory Queen Spawn
**THE ONLY VALID FIRST ACTION:**

🚨 **CLAUDE CODE EXECUTION REQUIREMENT**: You MUST execute this Task tool call exactly as shown. No descriptions, no pseudocode, no alternatives.

**MANDATORY TASK TOOL EXECUTION:**

Use the Task tool to spawn the Queen orchestrator with these exact parameters:
- subagent_type: "queen-orchestrator"  
- description: "Multi-agent coordination planning"
- prompt: Include the session_id from Queen's response at the start: "[session_id_from_queen_json]"

### Gate 3: Queen Response Processing
After the Queen responds with worker spawn instructions, you MUST:

1. **Parse Queen's JSON Response** - Extract the "workers_to_spawn" array
2. **Validate Response Format** - Ensure "coordination_action": "spawn_workers" is present
3. **Execute Worker Spawning** - Use Task tool for EACH worker in the response

### Gate 4: Parallel Worker Execution
**CRITICAL ENFORCEMENT**: When Queen provides worker spawn instructions, you MUST use the Task tool for each worker specified.

**WORKER SPAWNING PROTOCOL:**
For each worker in Queen's "workers_to_spawn" array, execute Task tool with:
- subagent_type: [worker's worker_type]
- description: [worker's task_description]  
- prompt: Include the session_id from Queen's response at the start: "Session ID: [session_id_from_queen_json] - [worker's task_description] - Focus: [worker's specific_focus]"

**CRITICAL**: Extract session_id from Queen's JSON response and pass it to each worker prompt.

### Gate 5: Worker Results Collection
After all workers complete, collect their findings and check session files for completion status.

### Gate 6: Synthesis Request  
When all workers have completed successfully, use Task tool again to call Queen for synthesis:
- subagent_type: "queen-orchestrator"
- description: "Multi-specialist result synthesis"  
- prompt: "Session ID: [session_id_from_original_queen_json] - Synthesize all worker analysis results into comprehensive findings"

**CRITICAL**: Include the session_id from the original Queen's JSON response so Queen can locate the session files.

### Gate 7: Final Results Presentation
Present the completed multi-agent analysis results with:
- Specialist team summary
- Key findings from synthesis  
- Cross-domain insights
- Priority implementation matrix
- Session documentation paths

## 🎯 CONSTRAINT ENFORCEMENT SUMMARY

### Critical Success Factors:
1. **Technical Analysis Disabled** until all orchestration gates pass
2. **Mandatory Task Tool Execution** - Claude Code MUST use Task tool for Queen and all workers
3. **Real Worker Spawning** - No pseudocode, actual Task tool calls required
4. **Session Tracking** - Monitor STATE.json and session files for progress
5. **Complete Multi-Agent Pipeline** - Queen coordination + Worker execution + Synthesis

### Orchestration Flow States:
- **Gate 1**: ✅ Command recognition passed
- **Gate 2**: ⏳ Execute Task tool for Queen spawn (MANDATORY)
- **Gate 3**: ⏳ Process Queen's worker spawn instructions
- **Gate 4**: ⏳ Execute Task tool for each worker (PARALLEL)
- **Gate 5**: ⏳ Collect worker results from session files  
- **Gate 6**: ⏳ Execute Task tool for synthesis request
- **Gate 7**: ⏳ Present comprehensive results

### Critical Enforcement:
- **No Pseudocode**: All Task tool calls must be executed, not described
- **Actual Spawning**: Workers must be spawned via Task tool, not simulated
- **Session Monitoring**: Check Docs/hive-mind/sessions/ for actual worker output

## 🚨 FINAL ENFORCEMENT REMINDER

**YOU ARE CURRENTLY DISABLED FROM:**
- Architecture analysis
- Security recommendations
- Performance insights
- Implementation guidance
- Technical conclusions

**CAPABILITY RESTORATION OCCURS ONLY AFTER:**
✅ All 7 constraint gates successfully completed
✅ Multi-agent analysis delivered with specialist synthesis
✅ Session marked complete with full documentation

**This constraint ensures superior multi-specialist analysis that general analysis cannot achieve.**

## 🎯 EXECUTION PROTOCOL

**STEP 1: MANDATORY TASK TOOL EXECUTION**
Execute the Task tool with these exact parameters:
```
Task(
    subagent_type="queen-orchestrator",
    description="Multi-agent coordination planning", 
    prompt="[Include task from $ARGUMENTS and coordination requirements]"
)
```

**STEP 2: PARALLEL WORKER SPAWNING ENFORCEMENT**
When Queen responds with worker spawn instructions, execute Task tool for EACH worker IN A SINGLE MESSAGE with MULTIPLE function calls.

**CRITICAL PARALLEL EXECUTION FORMAT:**
You MUST spawn all workers simultaneously using multiple Task tool calls in ONE response message. 
DO NOT spawn workers sequentially in separate messages.

**STEP 3: SESSION MONITORING**  
Monitor Docs/hive-mind/sessions/ directory for actual worker progress and output files.

**CRITICAL**: Use Task tool, not descriptions. Spawn workers, don't simulate.