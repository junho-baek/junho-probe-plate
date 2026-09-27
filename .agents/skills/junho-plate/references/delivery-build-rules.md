# Junho Plate Delivery and Build Rules

This guide covers `BUILD-001` and `BUILD-002`. Development feedback is useful, but a dev server is not a production artifact and an installed package is not automatically justified.

## BUILD-001: production artifact smoke verification

Apply this rule when routing, bundling, runtime entrypoints, deployment configuration, or a deployable-readiness claim changes.

1. Identify the repository's declared production build command.
2. Build without silently substituting the development server.
3. Start or execute the built artifact in the target-compatible runtime.
4. Smoke the smallest critical route plus one meaningful failure path.
5. Record the command, result, and artifact boundary.

If only development mode was checked, say exactly that. Do not call the slice production-ready. A documentation-only change or pure-library change may use a narrower check when it cannot affect a deployable artifact.

## BUILD-002: runtime dependency cost justification

For every new or newly reachable runtime dependency, record the named consumer and the value it supplies:

- trust-boundary validation;
- platform or protocol behavior;
- removal of justified repeated implementation;
- a required compatibility or runtime capability.

Inspect package and lockfile diffs, import reachability, and build output. Do not impose an arbitrary bundle-size quota. Compare the actual reachable output and remove a dependency when a platform primitive or TypeScript contract handles a trivial internal value without losing runtime safety.

Development-only tooling is judged by repeatable verification or generation value, not browser bundle cost.

## Git checkpoint boundary

After a verified slice, report a **checkpoint candidate** containing changed files, verification evidence, and the rollback point. Create a commit only with explicit mutation authority. A checkpoint recommendation is not permission to mutate Git state.

## Official documentation evidence

| Product | Version or access date | Direct official URL | Supported Rule IDs |
|---|---|---|---|
| React Router | Accessed 2026-09-27; v7 framework mode | [Deploying](https://reactrouter.com/start/framework/deploying) | BUILD-001 |
