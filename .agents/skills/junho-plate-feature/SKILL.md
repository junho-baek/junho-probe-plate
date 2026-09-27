---
name: junho-plate-feature
description: Proactively implement a complete, minimal vertical feature slice in a user-owned React Router 7 project, whether or not it derives from Plate or Supaplate. Use for new routes, screens, authenticated CRUD, Supabase or Drizzle-backed behavior when installed, forms, interactions, and meaningful behavior changes when the request is sufficiently specified; ask only before material product, permission, data, compatibility, paid-service, scope, or external-state decisions.
---

# Junho Plate Feature

Build the requested feature to a truthful local completion. Do not stop for plan approval when a `CONFIRMED` or `COMPATIBLE` local feature is sufficiently specified.

## Entry workflow

Follow this order:

1. Locate `../junho-plate/SKILL.md`, `../junho-plate/scripts/detect_plate.py`, and `../junho-plate/references/rule-catalog.json`; fail closed without edits if canonical core is absent.
2. Detect RR7 compatibility and inspect actual declared and resolved package versions.
3. Confirm that the request authorizes implementation, not only review or planning.
4. Inspect existing domains, features, routes, schema, migrations, and public APIs for reuse, duplication, or conflict.
5. Identify only unresolved decisions that materially change behavior or authority.
6. Choose the minimum justified layer set.
7. Begin implementation immediately when the local feature is sufficiently specified.

Continue for `CONFIRMED` and `COMPATIBLE`. For `COMPATIBLE`, use the existing project as the source of truth, apply only rules supported by installed capabilities, and move it incrementally toward Junho Plate boundaries without copying a template or requiring unused Supabase, Drizzle, or Zod layers. Never ask Plate provenance. For `UNSUPPORTED`, explain the missing RR7 compatibility, make no framework-specific edit, and ask one contextual next-step question.

Load only applicable Rule IDs and guides from `../junho-plate/references/`; do not copy or invent canonical rule bodies.

When applicable, include `ARCH-007`, `ARCH-008`, `UI-006`, `UI-007`, `BUILD-001`, `BUILD-002`, `AGENT-001`, and `AGENT-002`. Do not require separate processes or deployments: require explicit ownership and independently verifiable seams.

## Material decision gate

Ask before implementation only when one of these decisions is unresolved:

- product behavior has multiple materially different outcomes;
- authentication or authorization policy is missing;
- existing data must be transformed or deleted;
- public API compatibility would break;
- a paid or external service must be created;
- the feature requires out-of-scope refactoring.

Ask one decision at a time, recommend the safest likely default first, and stop without partial edits when the answer controls architecture, authority, or the data model. Do not ask for plan approval, preferred filenames, layer names, or other choices that can be inferred safely from the request and repository.

## Minimum layer selection

Choose by responsibility, not ceremony:

| Feature shape | Required default | Add only when justified |
|---|---|---|
| Static/presentation | route, screen, components | schema for actual external input |
| Server read/write | route, schema, application function/port, infrastructure, screen, components | domain for an invariant; migration for a schema change |
| Domain-complex | route, schema, application, domain, port, infrastructure, screen, components | integration or E2E test for a real cross-boundary risk |

This table is proportional. Never require a `domain/` directory, class repository, abstract factory, one-call wrapper, generic base service, or fixed file count when it isolates no change reason or test seam.

## Autonomous local authority

Within the requested feature, create or change route/layout registration, Zod schemas, loader/action/Form/fetcher flow, justified application/domain/infrastructure code, screens/components/view models, explicit client/server public APIs, local migration files, locally generated types, and minimum-sufficient tests. Resolve small in-scope structural defects needed for the feature.

Report unrelated debt as a later `junho-plate-refactor` candidate; do not silently absorb or edit it.

Without later explicit consent, do not apply linked or remote Supabase migrations, deploy, create a paid service, perform destructive data work, break a public API, commit, push, or restructure an unrelated feature.

## Implementation loop

Use this dependency-guided sequence, omitting steps that do not apply:

1. Write observable acceptance behaviors.
2. Add only a test that prevents a material regression not cheaply caught by types or direct inspection.
3. Implement a trust-boundary schema.
4. Implement a domain invariant only when one exists.
5. Define an application function and port around real use-case orchestration.
6. Implement the Supabase, Drizzle, or external adapter with error mapping.
7. Implement loader and action as thin React Router 7 adapters.
8. Apply the canonical Outlet admission table and choose the smallest honest route-tree shape.
9. Compose the screen and components from explicit UI data.
10. Expose explicit client/server APIs and register routes.
11. Write a local migration and synchronize generated types when schema changes.
12. Classify empty, domain, external, and system failures.
13. Run the guardrail scorecard and automatically repair every in-scope `FAIL`.
14. Run proportional verification.

The sequence is not a requirement to create every named file or layer.

For agentic features, prefer Cloudflare Agents SDK when the environment already supports it or the task explicitly targets Cloudflare. Use Agent for durable identity and interactive state, Workflows for durable multi-step execution, and a producer/Judge split only when independent evidence is valuable. A Judge reads immutable candidate evidence and cannot replace deterministic tests, policy gates, type checks, or builds.

## React Router ownership

Use the installed release's generated `Route.LoaderArgs`, `Route.ActionArgs`, and `Route.ComponentProps` at the route adapter.

| State or operation | Owner |
|---|---|
| Server reads | `loader` |
| Navigating writes | `action` + `Form` |
| Non-navigating writes | `action` + `fetcher` |
| Shareable filters and pagination | URL search params |
| Navigation or submission pending | `useNavigation` or `fetcher.state` |
| Route-tree shared data | layout loader, matches, or outlet context |
| Ephemeral open, focus, selection, or draft | `useState` |
| External subscription, widget, timer, or browser API | `useEffect` with cleanup |

Before registering a route family, apply `../junho-plate/references/rr7-rules.md`'s nested-parent/layout-route/Outlet admission table. Keep one screen's visual arrangement in screen composition. Introduce an Outlet-bearing parent only for a stable parent responsibility across real child routes, and keep child-specific reads, mutations, validation, and authorization in the child route.

Do not copy loader data into state, fetch loader-owned data in an effect, watch action results in an effect, maintain derived-state effects, or reconstruct React Router pending state with booleans.

## Trust, authorization, and boundaries

Treat params, URL search params, FormData, environment values, and external responses as trust boundaries. Parse them with Zod and derive transport types with `z.infer`; pass validated values into application/domain code without repeated transport parsing.

Authenticate and authorize protected reads, writes, and effects on the server against the requested resource before execution. UI visibility is not enforcement.

Keep vendor calls and raw response/error shapes in infrastructure. Map Supabase/Drizzle rows and errors to the application contract before presentation. A route parses, authorizes, calls, and maps only. A screen composes pending, empty, expected-error, and success presentation. Components receive explicit props or a cohesive view model, never a raw nested Supabase join. Define components at module scope.

Have the screen prepare a presentation-ready named view model for each item-varying component. Pass varying description, release copy, options, selected/disabled state, badges, pricing, CTA, and semantic visual variants through that contract. Keep components free of item-specific literals, raw persistence-record props, localized-label parsing, and index-based semantic state; let presentation map semantic variants to CSS classes.

Use explicit `index.ts` re-exports only. Put `.server` APIs behind a separate server entrypoint so a client-reachable public API cannot expose them.

## Schema-changing features

When the feature actually changes schema or database authority, track the table, policy, function, view, grant, and publication change in local migrations. Add owner/resource RLS and minimum grants. Keep secret/service-role use server-only. Review safe function `search_path` and privileges, view `security_invoker`, generated type synchronization, and transaction/RPC needs for atomic multi-write invariants. Do not generate unused SQL for a feature that has no database change.

## Errors and fallback

Distinguish normal empty state, expected domain failure, recoverable external failure, and unexpected system error. Map expected route outcomes to intentional action data or status; let unexpected route failures reach an ErrorBoundary and server reporting. Never turn authentication, authorization, corruption, or external read errors into `[]`, `null`, or fake success.

Allow retry or fallback only when it is bounded, visible, observable, and safe for an idempotent operation. Do not add speculative defensive branches.

## Minimum-sufficient tests

For every new test, record the material failure it prevents and why a cheaper type, schema, inspection, or smaller test is insufficient. Prefer, in order: a pure invariant test, a loader/action test, a repository/database integration test, and only then a critical-path E2E when the risk crosses those boundaries.

Do not create coverage-driven tests, blanket E2E, snapshots without a reviewed artifact contract, library re-tests, or mock-heavy private interaction counts.

## Self-review and completion

Maintain the standard scorecard:

| Rule ID | Status | Evidence | Risk | Recommendation | Blocking |
|---|---|---|---|---|---|

Before completion, inspect the entire changed feature slice plus necessary adjacent edges. Repair all in-scope `FAIL` results automatically. Completion requires `FAIL = 0`, no unresolved hard blocker, a retained reason for every `WARN`, passing relevant typegen/typecheck/test/build checks, demonstrated acceptance behaviors, and no unauthorized external effect. A failed relevant check means incomplete work, not completion with a caveat.

Run only verification proportional to the changed risk. Build when routing/bundling can change; run database integration only for database semantics; do not run a full E2E suite for a static page.

When `BUILD-001` applies, run the declared production build and smoke the built artifact rather than treating the dev server as equivalent. When the same published content appears in Admin and Customer surfaces, verify one shared preview and customer renderer contract under `UI-006`; verify stylesheet ownership under `UI-007`. Inspect every added runtime dependency under `BUILD-002`.

After a verified slice, report a **checkpoint candidate** with changed files, verification evidence, and a rollback point. Create a commit only with explicit user authority; never convert the checkpoint recommendation into an automatic Git mutation.

## Closing precedence

End every user-facing turn with exactly one contextual question and no second question:

1. If a material decision is unresolved, recommend a default and ask that one decision.
2. If local migration work is complete, recommend and ask whether to apply the exact migration remotely.
3. If a check is blocked, ask for the single action needed to unblock it.
4. Otherwise recommend one adjacent feature slice for a read-only review.

Never append “anything else?” or another generic invitation.
