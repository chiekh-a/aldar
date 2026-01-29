---
description: Execute development plans phase-by-phase with verification
argument-hint: task-name
---
You are an expert developer executing structured plans with precision.

## Overview
This command executes plans created by `plan-preparer` in `.workshop/tasks/[task-name]/`, working through phases systematically with verification at each step.

> **Resuming a previous session?** Skip to Step 2: Assess State. The tasks.md file is your checkpoint—current-phase and checked items tell you exactly where to continue.

## Argument Parsing
Extract from $ARGUMENTS:
- **task-name** (required): Kebab-case identifier matching existing plan folder

---

## Workflows

### 1. Load Context
```
    Read all three files:
    - .workshop/tasks/[task-name]/plan.md
    - .workshop/tasks/[task-name]/context.md  
    - .workshop/tasks/[task-name]/tasks.md
```

### 2. Assess State
- Check `current-phase` in tasks.md frontmatter
- Scan current phase for completed `[x]` vs pending `[ ]` tasks
- Identify any items in the Blocked section

### 3. Execute Current Phase
For each unchecked task in the current phase:
1. **Announce**: State what you're doing
2. **Execute**: Implement the change
3. **Mark**: Check off the task
4. **Commit**: Update tasks.md after each task

### 4. Verify Phase
When all phase tasks complete:
1. Run the **VERIFY** step(s)
2. If pass: Add ✓ to phase heading, increment `current-phase` in frontmatter
3. If fail: Document issue, attempt fix or mark as blocked

### 5. Repeat or Complete
- Continue to next phase, or
- If final phase verified: Mark plan status as `complete`

## Sub-Agent Delegation

### Available Agents

| Agent | Domain | Delegate When |
|-------|--------|---------------|
| `ux-ui-expert` | Components, styling, design systems, accessibility | Visual implementation, theming, responsive layout, a11y fixes |
| `nextjs-expert` | App Router, server components, API routes, middleware | Routing, data fetching, server actions, Next.js patterns |
| `python-expert` | Python backend, scripting, async, data processing | Backend logic, scripts, data pipelines, Python debugging |
| `llm-expert` | Agent orchestration, graph workflows, state machines | Google ADK, tool nodes, checkpointing, agent flows |
| `database-expert` | Schema design, queries, migrations, indexing | Drizzle or SQLAlchemy schemas, migrations, query optimization, relations |
| `testing-expert` | Test code, coverage, test architecture | Writing tests: unit, integration, E2E, mocks, fixtures |
| `debugging-expert` | Runtime issues, error diagnosis, behavior verification | VERIFY failures, server issues, API testing, log analysis, issue isolation |
| `devops-expert` | CI/CD, containers, deployment, infrastructure | GitHub Actions, Docker, Vercel/AWS config, env management |
| `stripe-expert` | Payments, subscriptions, webhooks, billing | Checkout flows, subscription logic, Stripe webhooks |
| `clerk-expert` | Authentication, sessions, user management, RBAC | Auth middleware, protected routes, user sync, roles |

### Boundary Rules
- **Frontend**: `ux-ui-expert` owns *how it looks*, `nextjs-expert` owns *how it routes/fetches*
- **Python**: `python-expert` owns *general Python*, `llm-expert` owns *agent orchestration and LLM-related*
- **Data**: `database-expert` owns *schema/queries*, other agents consume via defined interfaces
- **Testing**: `testing-expert` *writes tests*, `debugging-expert` *runs things and isolates issues*
- **Fix routing**: `debugging-expert` *diagnoses*, then hands off to domain expert to *fix*

### When to Delegate

**Delegate when:**
- Task is self-contained with clear inputs/outputs
- Phase has no unresolved Open Questions
- Work doesn't require cross-phase decisions

**Keep in main executor when:**
- Work affects Key Decisions in context.md
- Blocker requires re-planning
- Failure cascades beyond current phase

### TEST vs VERIFY

| | VERIFY | TEST |
|---|--------|------|
| **What** | Workflow checkpoint | Code artifact |
| **Lives in** | tasks.md (per phase) | Codebase (`__tests__/`, `*.spec.ts`) |
| **Written by** | `plan-preparer` | `testing-expert` |
| **Purpose** | "Is this phase done?" | "Does this code work?" |

VERIFY steps may *invoke* tests (e.g., `**VERIFY**: npm test passes`), but VERIFY is the checkpoint; tests are the mechanism.

### Context Packet (What Sub-Agents Receive)
```markdown
    ### Mission
    [Single task or phase being delegated]

    ### Boundaries
    **Do**: [Specific deliverable]
    **Don't**: [Relevant out-of-scope items]
    **Done when**: [VERIFY step or success criteria]

    ### File Context
    [Relevant entries only from context.md file map]

    ### Key Decisions
    [Only decisions affecting this work]

    ### Constraints
    [Dependencies, gotchas, technical limits]
```

### Status Report (What Sub-Agents Return)
```markdown
    ### Result
    [COMPLETE | PARTIAL | BLOCKED | FAILED]

    ### Tasks Resolved
    - [x] Completed task
    - [ ] Incomplete task (if any)

    ### Files Touched
    - [CREATED] @path/to/new.ts
    - [MODIFIED] @path/to/existing.ts

    ### VERIFY Outcome
    [PASS | FAIL: description]

    ### Discoveries
    - `[SCOPE_GAP]` Missing X
    - `[QUESTION]` Should we handle Y?

    ### Blockers (if any)
    - Blocked by: [impediment]
    - Needs: [what would unblock]
```

### Edge Case Handling
```
    Sub-agent returns →
    ├─ COMPLETE + PASS     → Check off, continue
    ├─ COMPLETE + FAIL     → Spawn Fix agent (max 1 retry)
    ├─ PARTIAL             → New agent for remainder (max 1 retry)
    ├─ BLOCKED             → Add to Blocked section, notify user
    └─ FAILED              → Escalate to main executor (no retry)
```

**Escalate immediately (no retry):**
- Sub-agent requests context not in packet
- Error touches files outside File Context
- Sub-agent suggests changing Key Decisions
- Same task fails twice

**When sub-agent needs more context**, it returns a Context Request. Main executor either provides it, makes the decision, absorbs the task, or escalates to user.

## Execution Rules

**Follow the plan**: Don't improvise scope. If something's missing, note it but stay on track.

**Use context.md**: Reference file map markers and patterns before touching code.

**One task at a time**: Complete and verify each task before moving on.

**Update as you go**: Keep tasks.md current—it's your checkpoint system.

**Verify strictly**: Don't skip VERIFY steps. They catch issues early.

**Surface blockers fast**: If blocked, update tasks.md and report immediately.

**Capture drift, don't act on it**: If you discover the plan missed something, don't fix it inline. Add to context.md under Open Questions:
- [ ] `[DISCOVERED]` Need to handle rate limiting on auth endpoint
Address discoveries after the current phase, during a plan review checkpoint.

## Task Update Format

When completing a task, check it off in place (do NOT move to Completed section):
```markdown
# Before:
- [ ] Create auth middleware

# After (check the box in place):
- [x] Create auth middleware
```

When a phase is complete, add ✓ to the phase heading:
```markdown
## Phase 1: Setup ✓
```

## Status Updates

Provide brief status after each:
- **Task**: "✓ Created `AuthMiddleware` class"
- **Phase**: "Phase 2 complete. All VERIFY steps passed. Moving to Phase 3."
- **Blocker**: "⚠ Blocked: Missing database credentials. Added to Blocked section."

## Completion

When final VERIFY passes:
1. Update plan.md `status: complete`
2. Check all "Definition of Done" items
3. Summary: phases completed, files changed, any notes for future work