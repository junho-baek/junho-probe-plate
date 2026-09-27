---
name: junho-plate-review
description: Perform a strict, evidence-first, read-only architecture and code review of one feature slice in a user-owned React Router 7 project, whether or not it derives from Plate or Supaplate. Use when the coordinator or user asks to audit, assess, inspect, or explain existing code without changing files, dependencies, generated output, Git state, database state, or external services.
---

# Junho Plate Review

Review only. Do not repair, format, generate, install, migrate, or mutate anything.

## Fixed workflow

Follow this order:

1. Verify the coordinator's Plate detection result or re-run `../junho-plate/scripts/detect_plate.py <project-root>`.
2. Lock the scope to one feature slice and necessary adjacent dependencies.
3. Read applicable canonical catalog entries and evidence.
4. Inspect the current type and test baseline only through proven read-only checks.
5. Produce the scorecard with direct `file:line` evidence.
6. Prioritize actionable failures.
7. Recommend nothing when `FAIL` and `WARN` are both empty.
8. End with exactly one contextual question.

Continue for `CONFIRMED` and `COMPATIBLE`. If detection is `UNSUPPORTED`, return control to the `junho-plate` coordinator through the host's native skill mechanism and make no RR7-specific review claim. Never ask a compatible project's Plate provenance. If any required canonical reference is missing, refuse to invent a rule.

## Read-only boundary

The review may read files and metadata but must not alter:

- source, configuration, fixture, or documentation files;
- formatting or lint output, including any autofix;
- installed dependencies, lockfiles, or package-manager state;
- migrations, schemas, policies, database rows, or generated database types;
- route types, build output, snapshots, coverage files, caches, or other generated files;
- staged files, commits, branches, worktrees, or any other Git state;
- Supabase projects, deployed apps, remote APIs, queues, email, payment systems, or other external services.

Never use `--fix`, `--write`, update modes, dependency installation, migration commands, generators, or tests that mutate external state. Do not run a command that may write a cache or generated output unless a proven read-only alternative redirects all output to a temporary location outside the project. If no safe alternative exists, report that the check was not run and use `N/A` or a clearly evidenced limitation.

Capture `git status --short` before and after any local checks when Git is available. A review is invalid if it changes the target tree.

## Scope lock

Name the primary feature slice before inspection. Include only adjacent code required to trace its real dependency path: route registration/module, schemas, application/domain code, ports/adapters/queries, screen/components, public index, relevant migrations/types, and directly related tests. Follow a cross-feature or shared-core edge only when the slice imports it or a security/data invariant requires it.

Do not turn one feature review into a whole-repository style audit. Repository-wide secret or forbidden-import searches are allowed only when necessary to establish whether the reviewed slice can leak through a reachable bundle or public boundary; report that expanded read scope.

## Canonical evidence

Always read `../junho-plate/references/rule-catalog.json`. Load only the applicable sibling guides:

- `../junho-plate/references/architecture-rules.md`
- `../junho-plate/references/rr7-rules.md`
- `../junho-plate/references/supabase-rules.md`
- `../junho-plate/references/typescript-zod-rules.md`
- `../junho-plate/references/component-rules.md`
- `../junho-plate/references/testing-fallback-rules.md`
- `../junho-plate/references/delivery-build-rules.md`
- `../junho-plate/references/agent-runtime-rules.md`

Load a `wemake-*` reference only to explain historical rationale, never to override the current catalog or installed-version behavior. Apply only rules whose scope intersects the locked slice; mark unrelated rules `N/A` rather than forcing `PASS`.

Apply `ARCH-007`, `ARCH-008`, `UI-006`, `UI-007`, `BUILD-001`, and `BUILD-002` only when their runtime surfaces, preview/customer rendering, styles, build artifact, or dependency changes intersect the slice. Do not require separate processes or deployments; review ownership and verifiability, not topology theater. For agentic slices, apply `AGENT-001` and `AGENT-002` only when Cloudflare compatibility or multi-agent judging is in scope.

## Inspection and status rules

Inspect imports, request/data flow, runtime trust boundaries, server authority, vendor mapping, presentation ownership, error paths, and relevant existing tests. For a route family, apply the canonical Outlet admission table: distinguish screen composition, an ordinary Layout component, a nested parent route, a pathless layout route, and a route prefix; do not treat screen length alone as evidence. Read the target project's package and lockfile before judging framework behavior.

For every in-scope module that imports `node:fs`, Supabase, Drizzle, a database client, a network SDK, or another vendor adapter, trace all exported and reusable behavior under `ARCH-006`. Report a `Soft` `FAIL` when the same module also owns entity factories, ordering or state transitions, read-modify-write use-case orchestration, product fallback policy, or CSS/Tailwind presentation tokens. Do not fail storage-specific serialization, compatibility normalization, vendor error mapping, or a trivial policy-free projection merely because several functions share one adapter file.

For every reusable or item-varying presentation component, apply `UI-002`: compare at least two plausible items or states and trace where description, release copy, options, selected/disabled state, badges, pricing, CTA, and visual variants originate. Report a `Soft` `FAIL` when the component hides item-specific literals, imports a persistence/data record as its public contract, parses localized display labels to recover meaning, or treats array position as real selection state. Accept stable component-owned chrome and local semantic-variant-to-CSS mapping.

When Admin preview and Customer output represent the same published content, trace whether both reach one shared renderer and view model. Inspect built artifact evidence rather than a dev server claim, and inspect package/lockfile changes plus bundle reachability for runtime dependency cost. A review remains read-only: report missing build evidence rather than producing the artifact.

Use statuses exactly:

- `PASS`: direct evidence shows the applicable contract is satisfied.
- `WARN`: a non-blocking risk or transition is real but does not meet the catalog's fail condition. Write the specific reason and future trigger for every WARN.
- `FAIL`: direct evidence meets the catalog's fail condition.
- `N/A`: the rule does not apply or a safe read-only check cannot establish it. State which case applies.

Never infer `PASS` from missing evidence. Never create an overall numeric score, percentage, letter grade, or weighted total.

## Scorecard

Use this exact column order:

| Rule ID | Status | Evidence | Risk | Recommendation | Blocking |
|---|---|---|---|---|---|

Requirements:

- Cite a real catalog Rule ID and direct `file:line` evidence for every `FAIL` and `WARN`.
- Keep `Evidence` observational; do not paste large source blocks.
- Explain the user, security, data, or maintenance consequence in `Risk`.
- Recommend the smallest behavior-preserving boundary change that addresses the evidence.
- Set `Blocking` to `Hard` only for a catalog hard blocker or a relevant failed type/test baseline that prevents a truthful completion claim.
- Set `Blocking` to `Soft` for actionable non-hard `FAIL` or `WARN`; use `—` for `PASS` and `N/A`.

If no applicable `FAIL` or `WARN` exists, state that no change is recommended and do not invent polish work.

## Priority and completion

Order findings by:

1. Security and authorization
2. Data integrity and database policy
3. Type safety and input validation
4. React Router/framework ownership
5. Architecture and dependency direction
6. Components and state ownership
7. Error, fallback, and justified tests
8. Optional polish

Do not claim that the slice is ready or complete while a `Hard` finding or a relevant existing type/test failure remains. Report unrun checks separately from findings and never disguise them as passing.

## Closing contract

End the response with exactly one contextual question and no other questions. When findings exist, ask whether the user wants the highest-priority scoped fix handed to `junho-plate-refactor` through the host's native skill mechanism. When nothing is wrong, recommend nothing and ask which Plate feature slice to inspect next.
