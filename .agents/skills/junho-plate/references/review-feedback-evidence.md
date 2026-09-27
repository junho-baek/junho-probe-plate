# Junho Plate Review-Derived Evidence

This document preserves generalized engineering findings supplied by the repository owner. It is not an official framework source and does not reproduce proprietary source code.

The reusable findings are:

- Admin, Customer, and API responsibilities need explicit boundaries even when they share one deployable.
- A screen should compose named responsibilities rather than hide UI, business policy, and external I/O in one large module.
- A public index should expose a deliberate API rather than implementation.
- Preview and customer rendering should share a rendering core so they cannot drift.
- Global stylesheet ownership must prevent collisions across surfaces.
- A development server does not prove that the production artifact boots.
- Runtime dependencies need a named boundary or consumer; one trivial internal constant is insufficient justification.
- Confirmed unused starter capability should be removed inside the authorized scope, while uncertain or unrelated cleanup remains separate.
- Pure transformations deserve isolated verification proportional to their risk.
- A verified checkpoint should be described, but Git commits require explicit authority.

These findings motivate `ARCH-007`, `ARCH-008`, `UI-006`, `UI-007`, `BUILD-001`, and `BUILD-002`. Rule outcomes still require direct evidence from the project under review.
