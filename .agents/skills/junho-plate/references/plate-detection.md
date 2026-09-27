# Junho Plate Compatibility Contract

This reference decides whether Junho Plate may apply its guardrails. Plate/Supaplate lineage is useful historical context, not an admission requirement. Any user-owned React Router 7 project may be reviewed, refactored, or extended toward the same responsibility boundaries.

## Decision table

| State | Required finding | Coordinator consequence |
|---|---|---|
| `CONFIRMED` | React Router 7 is declared and local evidence or direct user confirmation identifies Plate/Supaplate lineage | Route automatically. Apply only rules supported by installed capabilities and report missing optional signals. |
| `COMPATIBLE` | React Router 7 is declared but Plate/Supaplate lineage is absent, generic, or unverified | Route automatically. Treat the current project as the source of truth and improve it toward Junho Plate boundaries without pretending it has Plate provenance. |
| `UNSUPPORTED` | A valid React Router 7 dependency cannot be established from the target package manifest | Make no framework-specific edit. Explain the missing RR7 compatibility and ask one contextual question about a separate migration or another workflow. |

Both `CONFIRMED` and `COMPATIBLE` permit automatic routing. Never ask whether a compatible project was derived from Plate or Supaplate.

## Eligibility and capability evidence

Evaluate these concerns separately:

1. **Eligibility** - a declared React Router 7 package permits the workflow. Provenance, Supabase, Drizzle, Zod, `app/routes.ts`, `app/features`, and a server-client marker are not eligibility requirements.
2. **Installed capabilities** - record Supabase, Drizzle, Zod, route registry, feature directories, and server-only adapters when present. Load and enforce only the rules that apply; absence is a capability or architecture gap, not a reason to refuse the project.
3. **Project structure** - preserve sound existing conventions. Move toward Junho Plate responsibility boundaries incrementally; do not copy a template, rename everything, or impose unused layers merely to resemble a reference repository.
4. **Origin** - local provenance evidence or `--user-confirmed` distinguishes `CONFIRMED` from `COMPATIBLE` only. It never changes mutation authority or which installed-version behavior is valid.

Pass `--user-confirmed` only after the user directly states Plate/Supaplate lineage. It does not override a missing or incompatible React Router version and never authorizes security, data, scope, or external-state expansion.

## Version inspection

Inspect the target repository, not this reference, on every run:

1. Resolve the repository root and read its own package manifest.
2. Record the application package version and the declared React Router, Supabase JS, Drizzle, and Zod versions.
3. Inspect the target lockfile or package-manager inventory when present to distinguish a declared range from its resolved installation.
4. Use documentation compatible with the installed major/minor behavior. Never substitute the documentation site's current release for the target version.

The pinned reference Plate package metadata at commit `8449384cdfad30f20337bad6536b0c7d46a3dde5` establishes this audited baseline: package 1.0; declared ranges react-router `^7.5.1`, @supabase/supabase-js `^2.49.1`, Drizzle `^0.40.1`, and Zod `^3.24.2`; lockfile resolutions react-router 7.5.1, @supabase/supabase-js 2.49.4, Drizzle 0.40.1, and Zod 3.24.3. These are evidence for this baseline only; another user project must be inspected independently.

## State transitions

- React Router 7 plus a local provenance marker or direct confirmation yields `CONFIRMED`.
- React Router 7 without provenance yields `COMPATIBLE` and proceeds without a provenance question.
- Missing Supabase, Drizzle, Zod, route registry, feature folders, or server markers remains visible in `missing` but does not block routing.
- Missing or incompatible React Router 7 yields `UNSUPPORTED`, even when Plate lineage is user-confirmed.
- New evidence may cause a fresh detection run. Do not mutate the previous result in place or treat silence as confirmation.

## Read-only provenance and license boundary

Plate observations are limited to path categories and package metadata at the pinned local checkout. Do not quote, copy, or turn Plate/Supaplate implementation into examples.

Junho Plate operates on user-owned local React Router 7 projects. It applies derived responsibility rules and installed-version best practices; it never packages, copies, or redistributes Supaplate source, snippets, templates, fixtures, or builders. Compatibility means architectural guidance, not source or lineage equivalence.
