# Junho Plate Testing, Error, and Fallback Rules

This guide covers `ERR-001` through `ERR-003` and `TEST-001` through `TEST-002`. The goal is credible failure prevention and truthful recovery, not a test inventory or defensive code volume.

## Error classification

| Class | Meaning | Default treatment |
|---|---|---|
| Normal empty state | The operation succeeded and there is no matching data | Render an explicit empty UI; do not log it as a system error. |
| Expected domain failure | A known rule rejects the request, such as conflict or invalid transition | Map it to intentional action data or an appropriate status response. |
| Recoverable external failure | A dependency failed in a way the product can safely recover from | Use a visible, bounded, justified fallback only when semantics remain truthful. |
| Unexpected system error | A bug, corruption signal, or unmodeled infrastructure failure | Preserve diagnostics, report server-side, and render the nearest ErrorBoundary. |

Authentication and authorization failures are never empty states. Data corruption and partial writes are never normal external degradation.

## No swallowed errors or fake success

Do not convert an exception into `[]`, `null`, cached content, or `{ ok: true }` unless that is the modeled and observable outcome. A catch-all that removes the difference between “nothing exists” and “the read failed” creates fake success.

Map known vendor failures at the infrastructure boundary. Preserve structured diagnostics for server logging while returning a safe application outcome. Unknown failures continue to the route ErrorBoundary and reporting path. Do not expose secrets, raw SQL, stack traces, or vendor internals to the user.

## Fallback admission rule

A fallback is acceptable only when all four properties can be stated:

1. **Visible** - the user or operator can tell degraded behavior occurred; it is not hidden recovery.
2. **Bounded** - attempts, duration, scope, and exit condition are finite.
3. **Justified** - the failed dependency is recoverable and the substitute preserves the product's meaning.
4. **Observable** - the original failure and fallback outcome are recorded without leaking sensitive data.

Retry only an idempotent operation or one protected by an idempotency key. Stop after the documented bound and preserve the final failure. Do not chain fallbacks until every path appears successful. Never fallback around authorization, RLS, payment confirmation, transactional integrity, schema mismatch, or invalid user input.

Excessively defensive hidden recovery is a defect: broad catches, default objects, silent retries, and speculative compatibility branches make broken invariants look healthy. Prefer one explicit failure boundary over many local guesses.

## Proportional test selection

Every new test must name the real failure it prevents and why a cheaper check is insufficient. If TypeScript, a schema constraint, a linter, or a direct unit test already prevents the same failure, do not add a slower duplicate without a distinct risk.

Choose the cheapest layer that exercises the behavior:

1. Pure domain unit test for an invariant or decision table.
2. Loader/action test for parsing, auth, status, redirect, and route adaptation.
3. Repository/database integration test for RLS, SQL semantics, generated mapping, transaction, or vendor error behavior.
4. Focused E2E for a critical user journey that depends on browser, routing, and server integration together.

The order is a selection guide, not a requirement that each feature have all four layers.

## Test justification record

For each proposed test, record:

- **Real failure prevented:** the specific regression, security gap, invalid transition, data loss, or user-visible break.
- **Why a cheaper check is insufficient:** the boundary or runtime behavior that static typing, schema validation, or a smaller test cannot exercise.
- **Observed behavior:** inputs and externally visible result, not private call counts.
- **Maintenance boundary:** which public contract may change without rewriting the test.

Examples of good proportionality:

| Risk | Cheapest sufficient test | Why cheaper is insufficient |
|---|---|---|
| Domain transition permits an impossible state | Pure domain unit test | A type can describe the values but cannot prove the policy branch. |
| Protected action mutates before authorization | Route-level action test | Static inspection cannot execute denial ordering and side-effect absence. |
| RLS exposes another user's row | Database integration test under the actual role | A mocked repository cannot run the database policy. |
| Multi-write operation partially commits | Transaction/RPC integration test | Unit mocks cannot prove database atomicity. |
| Login redirect and cookie handoff fail only across browser/server | Focused E2E | A route unit test cannot cover the complete browser cookie/navigation exchange. |

## Tests to reject

- A coverage quota, line target, or test count used as a proxy for risk reduction.
- Snapshots created for their own sake, especially large component trees whose meaningful contract is unclear.
- Tests that only restate TypeScript, Zod, or a library's documented behavior.
- Mock setup larger than the behavior under test.
- Assertions about private helper call counts, implementation ordering without a user-visible invariant, or trivial JSX text.
- A regression test with no reproducible failure or no explanation of why a cheaper check is insufficient.

Snapshots can be justified only when the serialized artifact itself is the stable reviewed contract and a focused assertion cannot describe the important change more clearly. Their presence is never a completion gate.

## Fallback verification

- Force the original dependency failure and confirm the UI/operator can see degradation.
- Confirm the fallback stops at its declared bound and does not retry a non-idempotent effect.
- Confirm auth, permission, validation, and integrity failures cannot enter a fallback path.
- Confirm exhausted recovery reaches the ErrorBoundary/reporting path with truthful status.
- Confirm fallback content cannot be mistaken for fresh authoritative data.
- Search catches and defaults for fake success or hidden recovery.

## Plate structural observation

At pinned Plate commit `8449384cdfad30f20337bad6536b0c7d46a3dde5`, verification paths are organized under behavior areas such as `e2e/auth`, `e2e/settings`, and `e2e/users`, while error presentation has dedicated core screen path categories. This observation supports behavior-oriented seams but does not establish a coverage, snapshot, or file-count rule.

## Official documentation evidence

| Product | Version or access date | Direct official URL | Supported Rule IDs |
|---|---|---|---|
| React Router | Accessed 2026-08-04 | [Framework Testing](https://reactrouter.com/start/framework/testing) | TEST-001, TEST-002 |
| React Router | Accessed 2026-08-04; installed app is 7.5.1 | [Error Boundaries](https://reactrouter.com/how-to/error-boundary) | ERR-001, ERR-003, RR7-005 |
| Supabase JS | Declared `^2.49.1`; lockfile 2.49.4; accessed 2026-08-04 | [Handling errors in supabase-js](https://supabase.com/docs/guides/api/handling-errors-in-supabase-js) | ERR-002, SUPA-002 |
