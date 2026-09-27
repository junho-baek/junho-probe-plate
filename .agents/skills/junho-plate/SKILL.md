---
name: junho-plate
description: Coordinate guarded work in user-owned React Router 7 projects, whether or not they derive from Plate or Supaplate. Use for architecture or code review, refactoring and cleanup of existing code, and building or changing features; detect RR7 compatibility and installed capabilities, apply shared safety gates and Plate-informed responsibility boundaries, then route to the exact Junho Plate sibling workflow.
---

# Junho Plate

Act as the coordinator. Do not copy or perform a child skill's detailed workflow here.

## Required sequence

Follow this order without skipping or reordering:

1. Detect project compatibility.
2. Inspect installed versions.
3. Establish requested scope and authority.
4. Load only relevant canonical references.
5. Classify the work as review, refactor, or feature.
6. Apply the shared hard gates.
7. Hand off to the exact sibling workflow.
8. Verify the child result.
9. End with exactly one contextual question.

## 1. Detect project compatibility

Resolve this skill directory and run the detector against the user's project:

```bash
python3 <junho-plate-skill-dir>/scripts/detect_plate.py <project-root>
```

Pass `--user-confirmed` only when the user directly states Plate or Supaplate lineage. The flag records origin; it is not required to use Junho Plate and never overrides missing React Router 7 compatibility.

Handle the JSON `status` exactly:

- `CONFIRMED`: continue. Local evidence or direct confirmation identifies Plate/Supaplate lineage.
- `COMPATIBLE`: continue without a provenance question. Treat the target project as the source of truth and improve it toward Junho Plate boundaries without claiming Plate lineage.
- `UNSUPPORTED`: a valid React Router 7 dependency was not established. Make no framework-specific edit and end with exactly one contextual question about a separate migration or another workflow.

For both eligible states, treat missing Supabase, Drizzle, Zod, route registry, feature directories, or server markers as capability or architecture signals, not refusal reasons. Apply only relevant rules and never install a missing technology merely to imitate Supaplate.

## 2. Inspect installed versions

Read the target project's `package.json` and available lockfile. Record declared ranges separately from resolved versions for React Router, Supabase, Drizzle, Zod, React, TypeScript, and any relevant test tooling. Use documentation compatible with the target project; never substitute the audited reference project's versions.

## 3. Establish scope and authority

Identify the requested feature slice and only the adjacent dependencies needed to reason about it. Respect the user's mutation authority:

- A review or audit is read-only.
- Cleanup, restructuring, or repair of existing behavior is refactor work.
- New or changed product behavior is feature work.

If a missing choice would materially change the result, make no edit and use the single closing question to resolve it. Do not broaden scope because a nearby issue is visible.

## 4. Load canonical references

Require the sibling `references/` directory and `references/rule-catalog.json`. If either is missing or unreadable, refuse to invent rules, make no edit, and ask exactly one question about restoring or locating the canonical Junho Plate skill.

Load `plate-detection.md` plus only the guides relevant to the request:

- Architecture or boundaries: `architecture-rules.md`, `component-rules.md`
- React Router or React state: `rr7-rules.md`, `component-rules.md`
- Supabase, Drizzle, SQL, or Realtime: `supabase-rules.md`
- TypeScript or trust-boundary parsing: `typescript-zod-rules.md`
- Errors, fallback, or tests: `testing-fallback-rules.md`
- Production build, deployable artifact, runtime dependency, or checkpoint evidence: `delivery-build-rules.md`
- Agent architecture, preview parity involving agent output, multi-agent orchestration, or Judge review: `agent-runtime-rules.md`
- Historical rationale only when needed: the `wemake-*` references

Treat the rule catalog as the machine-readable decision contract. Current security and installed-version behavior outrank historical examples.

When an agent workload is requested and Cloudflare Agents SDK is supported by the task constraints and installed capabilities, use it as the default runtime profile. Do not force or install it in an incompatible environment. Pass `AGENT-001` and `AGENT-002` to the child so it can separate producer, Judge, and deterministic acceptance responsibilities without adding ornamental agents.

## 5. Classify and route

Choose one destination only:

- Review, audit, or explanation without edits -> `junho-plate-review`
- Existing-code cleanup, repair, or architectural restructuring -> `junho-plate-refactor`
- New behavior or a meaningful behavior change -> `junho-plate-feature`

When a request contains both feature and cleanup work, route by the user's primary outcome and give the child the smallest explicit combined scope. Do not reproduce its scorecard, migration, planning, or implementation procedure in this coordinator.

Treat those canonical names as host-neutral identifiers. Invoke the selected sibling through the current host's native skill mechanism: Codex may present a dollar-prefixed invocation hint, while Claude Code should use its Skill tool and exposes `/junho-plate-review`, `/junho-plate-refactor`, and `/junho-plate-feature` as manual user commands. These are invocation adapters only; never copy a sibling workflow into this coordinator or silently perform it inline.

## 6. Apply shared hard gates

Before handoff, identify applicable hard blockers from the catalog. Never downgrade or bypass:

- secret exposure, missing server authorization, or unapproved remote/destructive effects (`SEC-*`);
- unsafe RLS, privilege, migration, function/view, or atomicity behavior (`DB-*`, relevant `SUPA-*`);
- explicit `any` or unsafe suppression at maintained boundaries (`TS-*`);
- unvalidated request, FormData, params, environment, or external input (`ZOD-*`).

If the requested action would violate a hard gate, stop that action, explain the exact Rule ID and evidence, and use the one closing question to offer the safest scoped alternative.

## 7. Hand off and verify

Invoke the selected canonical sibling through the host-native mechanism and pass: detection result, inspected versions, requested scope, mutation authority, applicable Rule IDs, loaded reference paths, and any hard blocker. Let the child own its workflow.

After the child returns, verify that it stayed within scope and authority, handled applicable hard gates, used target-compatible behavior, and reported validation truthfully. Do not claim completion while a relevant hard blocker or failed required check remains.

## Closing contract

Every response that yields control to the user ends with exactly one question tailored to the current result. Ask no other question in that response. If there is nothing to fix, briefly say so and ask what Plate slice or feature to inspect next. If recommendations or changes remain, ask which single next action the user wants taken.
