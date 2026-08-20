# Claude Workflow Toolkit plan schema v1

Use this schema for plans intended to be executed incrementally by fresh agents.

```markdown
<!-- cwt-plan:v1 -->
# <Plan title>

## Request contract

### Goal
<one concise outcome>

### Explicit requirements
- ...

### Derived requirements
- ...

### Non-goals
- ...

### Constraints
- ...

## Existing context reused
- `<source>` -> <fact/routing information reused>

## Change map

| Action | Repository | Path | Symbol / area | Why |
| --- | --- | --- | --- | --- |
| MODIFY | backend | `src/...` | `Class.method()` | ... |
| CREATE | web | `src/...` | new module | ... |

Every path must be verified, except a `CREATE` path which must be a deliberate new location consistent with nearby structure.

## Execution increments

### Increment 1 — <name>

Status: pending

Depends on: none

#### Goal
...

#### Files
- MODIFY `path/to/file` — `symbol()`
- CREATE `path/to/new-file`

#### Existing behavior / facts
- ...

#### Required behavior
1. ...

#### Constraints / decisions
- DECISION: ...
- CONSTRAINT: ...

#### Validation
- `command`
- tests / observable checks

#### Done when
- ...

### Increment 2 — <name>
...

## Final verification
- integration/regression checks
- cleanup/removal criteria
- compatibility checks
```

## Status values

Use one of:

- `pending`
- `in_progress`
- `blocked`
- `completed`

Downstream executors should choose the first `pending` increment whose dependencies are `completed`.

## Path policy

- Existing file: verify before listing.
- New file: label `CREATE`.
- Deletion: verify and label `DELETE`.
- Prefer symbol names to line ranges.
- If exact location is truly unresolved, do not guess. Put it under an explicit `Open discovery` note and resolve it before implementation whenever possible.

## Increment policy

An increment should be independently executable and leave the codebase coherent. Do not split a single atomic edit just to create multiple increments. Prefer compatibility layers or staged migration boundaries when a large change must span sessions.

## Context policy

Include only facts that reduce future discovery or prevent wrong implementation decisions. Avoid copying source code, directory trees, dependency inventories, or material already cheap to retrieve by an exact read.
