# {task-title}

**Session ID**: {session-id}  
**Created**: {timestamp}  
**Status**: {complexity-level}_initialization  
**Type**: {task-type}
**Complexity Level**: {complexity-level}
**Estimated Duration**: {duration-based-on-complexity}  
**Priority**: {priority-level}

## Original Request
{user-provided-task-description}

## Task Analysis & Scope

### Primary Objective
**Goal**: {primary-objective-description}
**Success Measure**: {how-to-know-when-complete}

### Requirements & Acceptance Criteria
{#if complexity-level >= 2}
**User Story**: As a {user-type}, I want {functionality} so that {benefit}

**Acceptance Criteria**:
- [ ] {criterion-1}
- [ ] {criterion-2}
- [ ] {criterion-3}
{/if}

{#if task-type === "bug-investigation"}
**Bug Details**:
- **Steps to Reproduce**: {reproduction-steps}
- **Expected vs Actual**: {expected} vs {actual-behavior}
- **Environment**: {environment-details}
{/if}

### Technical Scope
**Systems/Components Affected**:
{#if complexity-level >= 2}
- **Backend**: {api-endpoints-business-logic-database}
- **Frontend**: {ui-components-state-management-interactions}
- **Database**: {schema-changes-migrations-queries}
- **Testing**: {unit-integration-e2e-requirements}
- **Infrastructure**: {deployment-monitoring-configuration}
{#else}
- **Primary Component**: {main-component-affected}
- **Secondary Impacts**: {related-systems-if-any}
{/if}

## Research & Context Loading

### Research Requirements
{#if complexity-level === 1}
**Pattern Library Review** (Minimal Research):
- [ ] Check existing similar patterns in codebase
- [ ] Validate against current project conventions
- [ ] Quick technology lookup if needed
{/if}

{#if complexity-level === 2}
**Targeted Research** (Quick Research):
- [ ] Context7 research on {primary-technology}
- [ ] Best practices for {task-type}
- [ ] Security/performance considerations
- [ ] Integration patterns with existing architecture
{/if}

{#if complexity-level >= 3}
**Comprehensive Research** (Multi-Domain):
- [ ] Context7 research across multiple domains
- [ ] Architecture pattern analysis
- [ ] Security compliance requirements
- [ ] Performance optimization strategies
- [ ] Cross-system integration approaches
- [ ] SmartWalletFX-specific financial/crypto considerations
{/if}

### Context Loading Requirements
{#if complexity-level === 1}
**Level 1 Context**: Single domain tags, minimal session structure
{/if}
{#if complexity-level === 2}
**Level 2 Context**: Primary domain + related tags, standard session structure
{/if}
{#if complexity-level >= 3}
**Level 3+ Context**: Multi-domain tags, comprehensive session structure, cross-worker coordination
{/if}

## Worker Assignment & Coordination

### Current Phase: {current-phase}
{phase-description-based-on-complexity}

### Worker Status
{#if complexity-level === 1}
- **Primary Worker**: {assigned-worker} - {status} - {task-description}
{/if}

{#if complexity-level === 2}
- **Research Worker**: {status} - Targeted research for {domain}
- **Primary Worker**: {status} - Implementation lead
- **Test Worker**: {status} - Validation and testing
{/if}

{#if complexity-level >= 3}
- **Researcher Worker**: {status} - Multi-domain Context7 research coordination
- **Service Architect**: {status} - Architecture planning and scalability design
- **Backend Worker**: {status} - Backend implementation and API development
- **Frontend Worker**: {status} - UI implementation and user experience
- **Designer Worker**: {status} - UX design and design system integration
- **Test Worker**: {status} - Comprehensive testing strategy and implementation
- **Analyzer Worker**: {status} - Security analysis and performance optimization
- **DevOps Worker**: {status} - Infrastructure and deployment management
{/if}

### Coordination Configuration
{#if complexity-level === 1}
**Escalation**: Standard 15min timeouts, minimal coordination
{/if}
{#if complexity-level === 2}
**Escalation**: 10min timeouts, basic EVENTS.jsonl coordination
{/if}
{#if complexity-level >= 3}
**Escalation**: {5min-for-level-3|2min-for-level-4} timeouts, full hive-mind coordination
**Communication**: Active EVENTS.jsonl monitoring and cross-worker notifications
{/if}

## Implementation Strategy

### Approach
{#if task-type === "feature-development"}
**Development Approach**: {incremental|big-bang|phased} feature implementation
{/if}
{#if task-type === "bug-investigation"}
**Investigation Approach**: {systematic-analysis|rapid-debugging|root-cause-focused}
{/if}
{#if task-type === "maintenance-task"}
**Maintenance Approach**: {careful-incremental|comprehensive-update|optimization-focused}
{/if}
{#if task-type === "integration-project"}
**Integration Approach**: {api-first|data-first|security-first}
{/if}

### Phase Breakdown
{#if complexity-level === 1}
1. **Direct Implementation**: Single worker completes task with basic validation
2. **Basic Testing**: Verify functionality and no regressions
3. **Simple Archive**: Document completion and any lessons learned
{/if}

{#if complexity-level === 2}
1. **Research Phase**: Targeted research and pattern analysis
2. **Planning Phase**: Create implementation plan with task breakdown
3. **Implementation Phase**: Execute plan with basic coordination
4. **Validation Phase**: Test and validate implementation
5. **Archive Phase**: Document results and extract patterns
{/if}

{#if complexity-level >= 3}
1. **Research Phase**: Comprehensive multi-domain research and synthesis
2. **Architecture Phase**: System design and integration planning
3. **Implementation Phase**: Parallel worker execution with coordination
4. **Integration Phase**: System integration and cross-component testing
5. **Validation Phase**: Security review, performance testing, quality assurance
6. **Archive Phase**: Comprehensive documentation and pattern library contribution
{/if}

## Quality Gates & Success Criteria

### Quality Gates Checklist
{#if complexity-level === 1}
- [ ] **Implementation Complete**: Task objective accomplished
- [ ] **Basic Testing**: Functionality verified and no obvious regressions
- [ ] **Documentation**: Minimal documentation updated
{/if}

{#if complexity-level === 2}
- [ ] **Research Complete**: Targeted research findings applied
- [ ] **Implementation Complete**: All requirements implemented
- [ ] **Testing Complete**: Comprehensive testing with passing results
- [ ] **Quality Review**: Code quality and standards compliance
- [ ] **Documentation**: Technical documentation updated
{/if}

{#if complexity-level >= 3}
- [ ] **Research Phase**: Comprehensive research completed and synthesized
- [ ] **Architecture Phase**: System design validated and documented
- [ ] **Implementation Phase**: All components developed with research backing
- [ ] **Integration Phase**: Cross-system integration validated
- [ ] **Security Review**: Security analysis and validation completed
- [ ] **Performance Validation**: Performance requirements met and benchmarked
- [ ] **Documentation**: Comprehensive technical and user documentation
- [ ] **Deployment Ready**: Feature/fix ready for production deployment
{/if}

### Success Criteria
{#if task-type === "feature-development"}
- [ ] Feature implements all acceptance criteria exactly as specified
- [ ] User experience validated through design review
- [ ] Performance benchmarks met or exceeded
{/if}
{#if task-type === "bug-investigation"}
- [ ] Bug no longer reproducible with original steps
- [ ] Fix addresses root cause, not just symptoms
- [ ] No regressions introduced by the fix
{/if}
{#if task-type === "maintenance-task"}
- [ ] Maintenance objective completed as specified
- [ ] No breaking changes introduced to existing functionality
- [ ] Code quality metrics maintained or improved
{/if}
{#if task-type === "integration-project"}
- [ ] Integration functional for all required features
- [ ] Proper error handling and recovery implemented
- [ ] Security review passed for external integrations
{/if}

**Universal Success Criteria**:
- [ ] Code follows established project standards and patterns
- [ ] Comprehensive test coverage with passing tests
- [ ] Security considerations addressed appropriately
- [ ] Technical documentation complete and accurate

## Risk Assessment & Mitigation

### Risk Analysis
**Risk Level**: {low|medium|high} (based on complexity and scope)

**Identified Risks**:
{#if complexity-level >= 2}
- **Technical Risk**: {technical-complexity-or-unknowns}
- **Integration Risk**: {cross-system-dependencies-or-conflicts}
- **Performance Risk**: {scalability-or-performance-concerns}
- **Security Risk**: {security-implications-or-vulnerabilities}
{/if}

### Mitigation Strategies
{#if complexity-level >= 2}
- [ ] {mitigation-approach-1}
- [ ] {mitigation-approach-2}
- [ ] {rollback-plan-if-needed}
{/if}

## Progress Tracking

### Timeline Tracking
{#if complexity-level === 1}
- **Task Start**: {timestamp}
- **Completion Target**: {estimated-completion}
{/if}

{#if complexity-level >= 2}
- **Research Phase**: {start-time} → {target-completion}
- **Implementation Phase**: {target-start} → {target-completion}
- **Validation Phase**: {target-start} → {target-completion}
- **Final Completion**: {target-date}
{/if}

### Archon Integration
**Archon Project ID**: {archon-project-id}
**Task IDs**: {comma-separated-task-ids}
**Status Sync**: {automatic-updates-configured}

### Session Metrics
- **Research Duration**: {time-spent-on-research}
- **Implementation Tasks**: {total-created} created, {completed} completed
- **Worker Coordination Events**: {event-count}
- **Quality Gate Completions**: {completed}/{total}

## Knowledge Capture

### Patterns & Learnings
{#if complexity-level >= 2}
**Successful Patterns**:
- [ ] {pattern-1-for-future-reuse}
- [ ] {pattern-2-for-future-reuse}

**Lessons Learned**:
- [ ] {lesson-1-for-future-sessions}
- [ ] {lesson-2-for-future-sessions}

**Pattern Library Contributions**:
- [ ] {reusable-pattern-or-template}
{/if}

### Memory Bank Updates
{#if complexity-level >= 3}
**Memory Bank Contributions**:
- [ ] Technical decisions with rationale
- [ ] Architecture patterns and trade-offs
- [ ] Performance optimizations discovered
- [ ] Security considerations and solutions
{/if}

## Phase History
- **{current-phase}**: {timestamp} - {phase-description-and-initial-actions}

---

*This session template adapts to complexity levels 1-4 and task types (feature-development, bug-investigation, maintenance-task, integration-project, research-project) for consistent hive-mind coordination*