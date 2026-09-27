---
name: junho-plate-refactor
description: Assess or refactor one existing feature slice in a user-owned React Router 7 project, whether or not it derives from Plate or Supaplate. Use for tangled, duplicated, unsafe, or poorly separated existing code; remain read-only when the user asks only for review or direction, but when the user explicitly asks to fix, clean up, refactor, proceed, or repair scorecard findings, announce the minimal working scope and execute without requesting plan or file-list approval. Preserve behavior and finish the repaired slice with zero FAIL findings.
---

# Junho Plate Refactor

Choose review or execution mode from the user's actual request. Do not manufacture a two-turn approval ceremony.

## Prerequisites

Locate `../junho-plate/SKILL.md`, `../junho-plate/scripts/detect_plate.py`, and `../junho-plate/references/rule-catalog.json`. Fail closed without edits if any is missing. Run the detector and inspect the target's package and lockfile. Mutation is allowed for `CONFIRMED` and `COMPATIBLE`; never ask Plate provenance for a compatible project. `UNSUPPORTED` returns to the coordinator without RR7-specific edits.

Load only applicable canonical guides from `../junho-plate/references/`. Do not reproduce or invent shared rule bodies.

When applicable, include `ARCH-007`, `ARCH-008`, `UI-006`, `UI-007`, `BUILD-001`, `BUILD-002`, `AGENT-001`, and `AGENT-002`. Do not require separate processes or deployments: explicit entrypoints, ownership, and independently verifiable seams are sufficient unless runtime constraints justify a topology change.

## Mutation authority

Treat an explicit change request as mutation authority for the requested feature slice. “Refactor it,” “clean it up,” “fix everything in that scorecard/table,” “go ahead,” “proceed,” and equivalent instructions authorize the smallest behavior-preserving implementation needed to satisfy that request. If a review or scorecard was already presented in the conversation, a request to fix its findings is execution authority; do not ask the user to approve the same scope again.

A question such as “how would you refactor this?”, a request for direction, or an explicit review/audit/explanation request is read-only. In that mode, do not edit files, format or autofix, install dependencies, update lockfiles, generate route/database types, create or apply migrations, update snapshots, create commits, push, call a remote database, deploy, or mutate an external service. Skip and report any baseline command that cannot avoid caches or generated output.

The working file list is an audit trail, not a consent mechanism. Do not ask for plan approval, filename approval, or a second confirmation when the minimal in-scope implementation can be inferred safely. Ask only when a missing decision would materially change product behavior, authorization, data handling, public compatibility, external state, or the requested feature boundary.

## Read-only assessment mode

Use this mode only when the user has not authorized edits. Perform this order:

1. Verify core/reference presence.
2. Detect RR7 compatibility and actual installed versions; continue for `CONFIRMED` or `COMPATIBLE`.
3. Lock one feature slice plus inspection-only adjacent dependencies.
4. Load only the relevant shared Rule IDs and evidence.
5. Observe current user-visible behavior and existing type/test/build baseline without writing.
6. Produce the guardrail scorecard before the proposal.
7. Name preserved behavior, recommended working files, excluded scope, and planned validation.
8. End with exactly one contextual question offering the highest-priority scoped repair.

When `ARCH-006` fails, include the current mixed module and the exact destination model/domain, application, or presentation files in `Working files`. A recommendation that permits only in-place editing is incomplete when reaching `FAIL = 0` requires responsibility extraction.

When `UI-002` fails, include both the screen that can prepare the presentation contract and the affected component/view-model files in `Working files`. Do not recommend a component-only patch when the varying product, route, permission, release, option, pricing, or CTA information must be supplied by its screen.

Use this informational shape:

### Recommended execution scope

- Target slice:
- Preserve:
- Working files:
- Inspection-only dependencies:
- Explicitly excluded:
- Planned validation:

### Guardrail scorecard

| Rule ID | Status | Evidence | Risk | Recommendation | Blocking |
|---|---|---|---|---|---|

Use `PASS`, `WARN`, `FAIL`, or `N/A`, with direct `file:line` evidence for findings and `Hard`/`Soft` blocking where applicable. Do not compute an overall score.

If no `FAIL` and no actionable `WARN` exists, do not manufacture layers, tests, or polish. Make no edit and use the one closing question to recommend the most natural different review target or stopping.

## Authorized execution mode

Use this mode immediately when the user requests code changes or tells you to repair review findings. If the conversation contains a recent scorecard for the same slice, verify that its evidence is still current and use it as the starting backlog. “Fix everything in the scorecard/table” authorizes every `FAIL` and actionable `WARN` in that displayed slice, but not unrelated debt.

At the start, send a concise commentary update naming the target, preserved behaviors, initial working files, exclusions, and validation. This is a scope notification, not an approval request. Do not stop after displaying it; continue into implementation in the same turn.

Then execute in this dependency-guided order:

1. Capture the current observable behavior and check baseline.
2. Add the smallest characterization test only when a named regression risk makes a cheaper check insufficient.
3. Repair trust-boundary input and unsafe types.
4. Make the route a React Router 7 adapter and apply the canonical Outlet admission table before changing route-tree shape.
5. Extract an application operation or port only when it isolates read-modify-write coordination, real orchestration, or an external effect.
6. Add domain code only for a real business invariant. Move reusable factories, ordering, state transitions, and fallback product policy out of infrastructure into a pure model or domain module.
7. Isolate Supabase, Drizzle, and external APIs in infrastructure. Keep filesystem, Supabase, Drizzle, database, network, and vendor modules limited to I/O, serialization, vendor mapping, and infrastructure error translation; move CSS/Tailwind tokens to presentation.
8. Make screen, component, and index presentation-only or explicit public APIs. Have the screen map route/application data into explicit semantic props or a cohesive named view model; make components render varying copy, status, options, pricing, CTA, and visual variants from that contract.
9. Classify errors and remove hidden fallback or fake success.
10. Run proportional type generation, typecheck, relevant tests, and build checks.
11. Re-run the same scorecard and self-fix every in-scope `FAIL`.

This order does not require every layer. Omit domain, ports, repositories, classes, or wrappers when a static or simple CRUD slice has no change reason for them.

When the slice contains Admin preview and Customer output, converge duplicated selection or transformation logic on one renderer or rendering core (`UI-006`) and verify stylesheet ownership (`UI-007`). Remove starter residue only when route, import, configuration, and build evidence confirms it is dead inside the authorized scope (`ARCH-008`). Build and smoke the built artifact when `BUILD-001` applies, and justify every new or retained runtime dependency under `BUILD-002`.

For compatible agent workloads, preserve or introduce the Cloudflare Agents SDK boundary under `AGENT-001`. Separate producer and Judge permissions under `AGENT-002`; the Judge reads immutable evidence and deterministic checks retain final authority.

Apply `ARCH-006` by change reason, not file size or function count. Use plain functions and the fewest destination modules that make infrastructure, application/domain, and presentation readable. Do not manufacture a class, generic repository base, or one-call wrapper.

Apply `UI-002` by meaning, not prop count. Remove item-specific literals from reusable components, replace display-label parsing and index-based semantics with explicit values, keep semantic-to-CSS mapping in presentation, and avoid passing raw persistence records when a narrower screen-owned view model is clearer.

Do not introduce an Outlet-bearing parent merely to shorten a screen. Use it when a stable parent shell, shared route data/boundary, or cohesive context remains while real child routes change. Preserve child-specific loader/action ownership and resource authorization.

## Scope monitor

Before every edit, confirm the path belongs to the requested slice or a necessary adjacent dependency. If a newly discovered file is required to complete the same behavior-preserving slice, add it to the working scope, announce that expansion in the next concise commentary update, and continue without approval.

Stop before the boundary-crossing edit and ask one focused question only when the repair would enter an explicitly excluded or unrelated feature, change a public API, make a material product/permission/data decision, or require external state. Name the exact boundary and why it cannot be resolved inside the authorized slice.

Process one feature slice per run. Do not use a neighboring defect or private import as permission to restructure that feature.

## External-state gates

Create required local migration files or generated local types when they are part of the authorized feature repair, and report them in the working scope. Require separate explicit authority for linked or remote migration application, `supabase db push`, deployment, paid-service creation, existing-data conversion or deletion, commit, push, public API breakage, or any other external state change.

## Completion gate

Claim completion only when all are true:

- the target slice scorecard has `FAIL = 0`;
- all applicable hard blockers are resolved;
- every retained `WARN` has a written reason;
- relevant type, test, and build checks pass;
- preserved behaviors are demonstrated;
- every changed file is inside the reported working scope;
- no hidden fallback or unauthorized external effect remains.

If any condition is false, report incomplete work truthfully and ask the single highest-leverage unblocking question.

After a verified slice, report a **checkpoint candidate** with changed files, verification evidence, and a rollback point. Create a commit only with explicit user authority; a request to refactor does not itself authorize Git mutation.

## Closing precedence

End every user-facing turn with exactly one contextual question and no other question:

1. If a remote migration is ready, ask whether to apply that exact migration remotely.
2. If a material boundary decision is required, ask the single question that resolves that exact boundary.
3. After a successful local refactor, recommend one adjacent slice for a read-only review.
4. If no issue exists, recommend a different target or stopping.
5. After a read-only assessment, ask whether to repair the highest-priority finding or all displayed findings in the same slice.
