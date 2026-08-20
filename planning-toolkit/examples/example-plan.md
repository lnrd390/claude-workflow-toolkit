<!-- cwt-plan:v1 -->
# Add refresh-token rotation

## Request contract

### Goal
Rotate refresh tokens after every successful refresh without changing the public login/refresh response contract.

### Explicit requirements
- Old refresh tokens must become unusable after successful rotation.
- Existing login behavior must remain unchanged.

### Derived requirements
- Rotation and replacement persistence must be atomic.
- Existing token hashing/expiry rules should be reused.

### Non-goals
- Redesign authentication.
- Replace credential login.

### Constraints
- Preserve the current API response schema.

## Existing context reused
- `CLAUDE.md` identifies the backend repository and canonical test command.
- Existing auth routing points to the service/repository files below; source was verified before planning.

## Change map

| Action | Repository | Path | Symbol / area | Why |
| --- | --- | --- | --- | --- |
| MODIFY | backend | `src/auth/AuthService.ts` | `AuthService.refreshToken()` | orchestrate rotation |
| MODIFY | backend | `src/auth/RefreshTokenRepository.ts` | `consume()` | atomic consume+replace |
| MODIFY | backend | `tests/auth/refresh-token.test.ts` | refresh tests | regression coverage |

## Execution increments

### Increment 1 — Implement atomic refresh-token rotation

Status: pending

Depends on: none

#### Goal
Rotate a valid refresh token and invalidate the presented token in one persistence transaction.

#### Files
- MODIFY `src/auth/AuthService.ts` — `AuthService.refreshToken()`
- MODIFY `src/auth/RefreshTokenRepository.ts` — `consume()`
- MODIFY `tests/auth/refresh-token.test.ts` — refresh-token cases

#### Existing behavior / facts
- `AuthService.refreshToken()` validates the current refresh token and already delegates persistence to `RefreshTokenRepository`.

#### Required behavior
1. Consume the presented refresh token.
2. Generate and persist its replacement atomically.
3. Return the existing public response shape with the replacement token.
4. Reject reuse of the consumed token.

#### Constraints / decisions
- DECISION: persistence atomicity belongs in `RefreshTokenRepository.consume()`.
- CONSTRAINT: reuse existing hashing and expiry utilities.
- CONSTRAINT: do not change login behavior or public API schema.

#### Validation
- `pnpm test tests/auth/refresh-token.test.ts`
- Cover successful rotation, old-token reuse, expiration, and rollback on replacement persistence failure.

#### Done when
- listed tests pass;
- the old token fails after successful rotation;
- no response-schema change is introduced.

## Final verification
- Run the backend auth test suite.
- Confirm no unrelated auth files changed.
