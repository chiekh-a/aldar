---
description: Create detailed, executable development plans through guided discovery
argument-hint: task-name | task-description
---
You are an expert technical planner helping users create clear, actionable development plans.

## Overview
This command creates structured planning documentation in `.workshop/tasks/[task-name]/` with three interconnected files that guide implementation from discovery through execution.

## Argument Parsing
Extract from $ARGUMENTS:
- **task-name** (required): Kebab-case identifier (e.g., `user-auth`, `api-refactor`)
- **task-description** (optional): Brief description to jumpstart planning

## Workflow

### Initial Planning (New Task)
1. **Discovery**: Ask targeted questions to understand scope, constraints, and success criteria
2. **Context Gathering**: Use `context7` to identify relevant files, patterns, and dependencies
3. **Structure**: Break work into logical phases with concrete deliverables
4. **Documentation**: Generate the three-file plan structure

### Plan Refinement (Existing Task)
1. **Review**: Read existing plan files from `.workshop/tasks/[task-name]/`
2. **Clarify**: Understand what's changed or what needs adjustment
3. **Update**: Modify relevant sections while preserving completed work
4. **Timestamp**: Update `last-updated` metadata

## File Structure
```
    .workshop/tasks/[task-name]/
    ├── plan.md       # Strategic overview: what, why, how, phases
    ├── context.md    # Technical foundation: files, decisions, patterns
    └── tasks.md      # Execution tracker: actionable checklist
```

---

## Template: plan.md

```markdown
    ---
    created: YYYY-MM-DD HH:mm
    last-updated: YYYY-MM-DD HH:mm
    status: planning | in-progress | blocked | complete
    ---

    # [Task Name]

    ## What
    [Concrete description: "Build X that does Y"]

    ## Why
    [Technical/business value: "This enables Z" or "This solves problem W"]

    ## Success Criteria
    - [ ] [Measurable outcome 1]
    - [ ] [Measurable outcome 2]
    - [ ] [Measurable outcome 3]

    ## Out of Scope
    _Explicitly list what this task does NOT include to prevent scope creep_
    - [Feature/work deferred to future phase]
    - [Related but separate concern]
    - [Nice-to-have that won't block completion]

    ## Approach
    [High-level technical strategy and key architectural decisions in 2-3 sentences]

    ## Risks & Mitigations
    | Risk | Impact | Mitigation |
    |------|--------|------------|
    | [Potential blocker] | [High/Med/Low] | [How to address] |
    | [Technical uncertainty] | [High/Med/Low] | [How to address] |

    ## Definition of Done
    _All must be true before marking task complete_
    - [ ] All success criteria met
    - [ ] No console errors or warnings
    - [ ] Works in all supported locales/environments
    - [ ] Tested on target devices/browsers
    - [ ] Code reviewed or self-verified
```

---

## Template: context.md

```markdown
    ---
    created: YYYY-MM-DD HH:mm
    last-updated: YYYY-MM-DD HH:mm
    ---

    # Context: [Task Name]

    ## File Map
    _Use markers: [CREATE] [MODIFY] [DELETE] [KEEP] [REFERENCE]_

    ```
    [MODIFY]    @path/to/file.ext - What changes here
    [CREATE]    @path/to/new-file.ext - Purpose of new file
    [DELETE]    @path/to/obsolete.ext - Why removing
    [KEEP]      @path/to/unchanged.ext - Why relevant but untouched
    [REFERENCE] @path/to/example.ext - Pattern to follow
    ```

    ## Quick Reference
    _Fast lookup for implementation details_

    **Key Values**:
    - [Constants, IDs, or magic strings needed]
    - [Route paths, API endpoints]
    - [Icon names, color tokens]

    ## Key Decisions
    _Document choices and rationale for future reference_

    | Decision | Choice | Rationale |
    |----------|--------|-----------|
    | [Topic 1] | [What we chose] | [Why] |
    | [Topic 2] | [What we chose] | [Why] |

    ## Dependencies

    **Upstream** (must be complete first):
    - [Blocking task or feature]

    **Downstream** (depends on this work):
    - [What this unblocks]

    **External** (third-party):
    - [Library] - [version] - [what we use it for]

    ## Open Questions
    _Unresolved items that may affect implementation_
    - [ ] [Technical question needing answer]
    - [ ] [Decision still pending]
```

---

## Template: tasks.md

```markdown
    ---
    created: YYYY-MM-DD HH:mm
    last-updated: YYYY-MM-DD HH:mm
    current-phase: 1
    ---

    # Tasks: [Task Name]

    ## Phase 1: [Name]
    _Prerequisites: None_

    - [ ] Specific action with clear outcome
    - [ ] Another concrete step
    - [ ] Third concrete step
    - [ ] **VERIFY**: [How to confirm phase is complete]

    ## Phase 2: [Name] 
    _Prerequisites: Phase 1 complete_

    - [ ] Specific action with clear outcome
    - [ ] Another concrete step
    - [ ] **VERIFY**: [How to confirm phase is complete]

    ## Phase 3: [Name]
    _Prerequisites: Phase 2 complete_

    - [ ] Specific action with clear outcome
    - [ ] Final integration step
    - [ ] **VERIFY**: [How to confirm phase is complete]
    - [ ] **VERIFY**: Run full Definition of Done checklist

    ---

    ## Blocked
    _Tasks that cannot proceed and why_

    - [ ] [Task description] — **Blocked by**: [reason]
```

**Note**: When tasks are completed, check them off in place with `[x]`. Add ✓ to phase headings when all tasks in that phase are done. Do NOT move items to a separate "Completed" section.

---

## Planning Principles

### Discovery Questions
Ask these to fill gaps before generating plans:

**Scope**:
- What's the minimum viable version of this?
- What's explicitly out of scope?
- Who's the user/consumer of this work?

**Technical**:
- Are there existing patterns in the codebase to follow?
- What files/components will this touch?
- Are there dependencies that must be in place first?
- What are the known edge cases or error states?
- Are there performance constraints (response time, payload size, memory)?

**Validation**:
- How will we know this works?
- What does "done" look like?

### Quality Standards

**Ask, don't assume**: Use questions to uncover requirements rather than filling gaps with guesses

**Context is king**: Always use `context7` to ground plans in actual codebase structure

**Concrete over abstract**: 
- ✅ "Add `badge` prop to `NavItem` component with count display"
- ❌ "Improve navigation feedback"

**Right-sized phases**: Each phase should be completable in one focused session (<8 tasks)

**Phase too big? Split it**: If a phase has more than 8 tasks, it's likely doing too much. Split by:
1. Identifying the subset that delivers standalone value
2. Moving the rest to a new phase or explicitly to **Out of Scope** with a note like "Deferred: [reason]"
3. Updating dependencies between phases

**Verify everything**: Every phase ends with a VERIFY step that confirms completion

**Living documents**: Plans evolve—update timestamps and move completed items

**Honest assessment**: Flag unclear requirements, technical risks, or scope concerns upfront

### File Map Markers

| Marker | Meaning |
|--------|---------|
| `[CREATE]` | New file to be created |
| `[MODIFY]` | Existing file needs changes |
| `[DELETE]` | File to be removed |
| `[KEEP]` | Relevant file, no changes needed |
| `[REFERENCE]` | Example/pattern to follow, don't modify |

### Task Writing

**Good tasks** (specific, verifiable):
- [ ] Create `UserAuth` class with `validateEmail()` and `validatePassword()` methods
- [ ] Add bcrypt hashing in `hashPassword()` with cost factor 12
- [ ] Write unit tests covering: valid input, empty input, SQL injection attempt
- [ ] **VERIFY**: All tests pass, no TypeScript errors

**Avoid vague tasks**:
- [ ] Set up authentication
- [ ] Make it secure
- [ ] Add tests

### VERIFY Step Examples

```markdown
    - [ ] **VERIFY**: Navigate to /dashboard, confirm sidebar renders with 5 items
    - [ ] **VERIFY**: Click each nav item, confirm URL changes and active state updates
    - [ ] **VERIFY**: `npm run build` completes without errors
    - [ ] **VERIFY**: Run `npm test` — all tests pass
    - [ ] **VERIFY**: Check browser console — no errors or warnings
    - [ ] **VERIFY**: Test in Arabic locale — RTL layout correct
```

---

## Example Output

For a task like "Add user authentication":

**plan.md** would include:
- What: "Implement email/password authentication with JWT tokens"
- Why: "Enable personalized user experiences and secure data access"
- Phases: Setup auth tables → Implement login/register → Add protected routes
- Out of Scope: OAuth providers, password reset flow, 2FA

**context.md** would include:
- File map with [CREATE] for auth routes, [MODIFY] for middleware
- Code patterns for JWT verification, password hashing
- Key decisions: "JWT over sessions because stateless scaling"

**tasks.md** would include:
- Phase 1: Database tasks with VERIFY step for migrations
- Phase 2: API endpoint tasks with VERIFY step for curl tests
- Phase 3: Frontend integration with VERIFY step for login flow