# Junho Plate Supabase and Database Rules

This guide covers `SUPA-001` through `SUPA-005`, `DB-001` through `DB-005`, and the database-facing security rules. The audited baseline declares @supabase/supabase-js `^2.49.1` and Drizzle `^0.40.1`; its lockfile resolves 2.49.4 and 0.40.1 respectively. Security and data integrity outrank local convenience.

## Client ownership

| Client | Runs where | Credential and session | Allowed responsibility |
|---|---|---|---|
| **browser client** | Browser-only UI | Publishable/anon key plus the user's session; protected by RLS | Auth UI, user-scoped Data API access when intended, Storage, and Realtime subscriptions. It never receives a secret or service role key. |
| **server client** | Loader, action, server handler | Request-scoped cookie/session handling and publishable key | Server reads/writes on behalf of the current user, SSR identity checks, and normal policy-enforced operations. Do not reuse a cross-request singleton carrying session state. |
| **admin client** | Narrow server-only module | Secret/service role credential, no browser session | Explicit administrative operations that truly require elevated authority. Construct and import it only through a `.server` boundary. |

`SUPA-001` and `SEC-001` are hard boundaries. A service role bypasses RLS, so service role use is server-only, narrowly scoped, audited, and never selected merely to avoid writing a policy. Do not put an admin credential into an SSR client that reads user cookies; keep user and administrative authority separate.

## Authorization, RLS, and grants

Enable RLS on every exposed table or view-backed surface and grant only the operations each role needs. A policy must cover both row visibility and write eligibility where applicable. Minimum grants and RLS work together: a permissive table grant is not repaired by UI hiding, and a missing grant is not a reason to use admin authority in normal user flow.

Protected loaders and actions still perform server-side identity and resource-authorization checks. Database policy supplies defense in depth and protects alternate access paths. Test denial as well as success for sensitive reads and mutations.

## Migration and type ownership

Every table, column, index, constraint, policy, grant, view, function, trigger, and Realtime publication change belongs in ordered, reviewable migrations. A dashboard experiment is not complete until its reproducible migration is committed. Regenerate and review generated database types after the migration source changes; do not maintain a competing hand-written copy of generated rows.

### Supabase ownership vs Drizzle ownership

| Concern | Primary owner | Boundary rule |
|---|---|---|
| Table shape, relations, indexes, typed SQL model | Drizzle ownership when the project has adopted Drizzle schema | The Drizzle schema is the TypeScript source for those objects and its generated migration enters the one ordered history. |
| Auth, Storage, Realtime, Data API exposure, RLS, grants, function/view security | Supabase/PostgreSQL ownership | Express these as reviewed SQL migrations and verify them in the Supabase/Postgres environment. |
| Runtime browser/server/admin API calls | Supabase client boundary | Use the correct authority-specific client and generated database types. |
| Direct server SQL and transactions | Drizzle/Postgres infrastructure boundary | Keep it server-only and map results/errors before application or domain code. |

Supabase and Drizzle are not interchangeable. Do not define the same table independently in two canonical schemas or keep two migration histories that can diverge. A project may combine Drizzle-generated DDL with Supabase-specific security SQL, but it needs one explicit deployment order and one reviewed source of truth for each object.

## Functions, views, and atomic writes

Database functions that use elevated authority must set a safe `search_path` and schema-qualify every referenced relation. Review `SECURITY DEFINER` separately, revoke default execute privileges where they are broader than intended, and grant execution only to the roles that need it. Function code, privileges, and its migration must land together (`DB-003`).

Views are access surfaces. Review the underlying tables, exposed columns, owner, grants, and whether `security_invoker` is required so the caller's RLS policies apply. A typed view is not automatically a secure view (`DB-004`).

If multiple writes must preserve one invariant, use an atomic database transaction or a reviewed RPC/function boundary so all changes commit or none do (`DB-005`). Sequential independent Supabase requests do not become atomic because they share an action. For external effects that cannot join the transaction, define idempotency, ordering, and a visible compensation or retry policy rather than reporting fake success.

## Repository error mapping

The infrastructure boundary owns repository error mapping (`SUPA-002`, `SUPA-003`):

- Inspect the Supabase `{ data, error }` result and preserve diagnostic context for server logging.
- Branch on stable structured error codes where the client provides them, not changing message text.
- Map known failures to application/domain outcomes such as not found, conflict, forbidden, or retryable external failure.
- Do not pass raw PostgREST joins, vendor error objects, or nullable transport bags through the domain and into screens.
- Do not catch an error and return an empty array, null, or success unless that value is the truthful modeled outcome.

A repository may be a small function module; a repository class is not mandatory. Add the boundary because vendor response and failure semantics need isolation, not to satisfy a naming pattern.

## Realtime lifecycle

Realtime is an external system, so a subscription may be synchronized in `useEffect`. Each subscription must use the narrowest authorized topic/filter, handle connection errors, and return Realtime cleanup that removes or unsubscribes the exact channel on dependency change and unmount (`SUPA-005`).

Do not copy all loader data into local state simply because Realtime exists. Model the smallest live overlay or request revalidation, define duplicate/order behavior, and keep authorization active for private channels. A global unfiltered subscription, raw payload assertion, missing cleanup, or captured stale identity is a failure.

## Verification checklist

- Trace browser, server, and admin client imports and confirm no elevated credential can reach a client bundle.
- Inspect each exposed table for RLS, write checks, and minimum grants.
- Compare schema, security SQL, migrations, and generated database types after a database change.
- Inspect every privileged function for schema qualification, `search_path`, owner, execute privileges, and migration tracking.
- Inspect each view for `security_invoker`, underlying policies, columns, and grants.
- Exercise partial-failure cases for atomic multi-write operations.
- Mount, change dependencies, and unmount Realtime code to verify one subscription and one cleanup lifecycle.

## Official documentation evidence

| Product | Version or access date | Direct official URL | Supported Rule IDs |
|---|---|---|---|
| Supabase JS/SSR | Declared `^2.49.1`; lockfile 2.49.4; accessed 2026-08-04 | [Creating a Supabase client for SSR](https://supabase.com/docs/guides/auth/server-side/creating-a-client) | RR7-004, SUPA-001 |
| Supabase | Accessed 2026-08-04 | [Securing your data](https://supabase.com/docs/guides/database/secure-data) | SUPA-001, DB-002, SEC-001 |
| Supabase | Accessed 2026-08-04 | [Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security) | DB-002, SEC-002 |
| Supabase JS | Declared `^2.49.1`; lockfile 2.49.4; accessed 2026-08-04 | [Handling errors in supabase-js](https://supabase.com/docs/guides/api/handling-errors-in-supabase-js) | SUPA-002, ERR-002 |
| Supabase | Accessed 2026-08-04 | [Database Migrations](https://supabase.com/docs/guides/deployment/database-migrations) | DB-001 |
| Supabase | Accessed 2026-08-04 | [Generating TypeScript Types](https://supabase.com/docs/guides/api/rest/generating-types) | SUPA-004 |
| Supabase/PostgreSQL | Accessed 2026-08-04 | [Database Functions](https://supabase.com/docs/guides/database/functions) | DB-003 |
| Supabase/PostgreSQL | Accessed 2026-08-04 | [Tables and view security](https://supabase.com/docs/guides/database/tables) | DB-004 |
| Supabase Realtime | Declared supabase-js `^2.49.1`; lockfile 2.49.4; accessed 2026-08-04 | [Getting Started with Realtime](https://supabase.com/docs/guides/realtime/getting_started) | SUPA-005 |
| PostgreSQL | Current docs accessed 2026-08-04 | [Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html) | DB-005 |
