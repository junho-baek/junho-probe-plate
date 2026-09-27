# Junho Plate TypeScript and Zod Rules

This guide covers `TS-001` through `TS-003` and `ZOD-001` through `ZOD-003`. The audited Plate manifest declares Zod `^3.24.2` and its lockfile resolves Zod 3.24.3, so Zod 3 documentation is the compatible version-specific source.

## Canonical trust flow

Every untrusted value follows this direction:

`unknown -> Zod -> z.infer -> application input -> domain value`

The arrows are ownership transitions:

1. Receive request, FormData, params, URL search params, environment input, external JSON, webhook payload, or another trust boundary as `unknown` or a truthful platform type.
2. Parse once with a Zod schema at the nearest route/infrastructure boundary.
3. Derive the successful transport type with `z.infer`; do not maintain a second manual input interface that can drift.
4. Pass a validated application input into the operation.
5. Construct or call domain values that enforce business invariants independent of Zod and the transport.

Validation establishes a runtime fact. A TypeScript annotation or assertion does not.

## TS-001: no explicit any

Explicit `any` disables downstream type checking and is a hard failure in maintained application code. Prefer `unknown` at a trust boundary, a generic type parameter for reusable code, a discriminated union for alternatives, or the actual generated/vendor type.

Do not hide `any` inside a data bag, callback, ambient declaration, or double assertion. If an upstream library genuinely exposes `any`, confine it to one adapter, validate what crosses into the application, and record the upstream constraint. The adapter's output must be specific.

## TS-002: no suppression or assertion escape hatch

`@ts-ignore`, blanket lint disables, non-null assertions, and broad `as` casts are not runtime validation. They may not be used to force FormData, route params, search params, Supabase results, or external JSON into a desired type.

A narrow assertion is acceptable only when all of these are true:

- The runtime invariant is established immediately beside it by a check the compiler cannot express, or a maintained framework/generated contract supplies the fact.
- The assertion narrows the smallest possible expression and cannot be replaced by ordinary control-flow narrowing.
- The reason is specific, reviewable, and names the upstream limitation.
- The boundary does not allow unvalidated data into application or domain code.

For a known compiler or dependency defect, a precise `@ts-expect-error` may be a temporary exception because it fails when the expected error disappears. It still needs an owner and removal condition. `@ts-ignore` is not that contract.

## TS-003: server/client module safety

Keep `.server` modules, admin clients, secrets, and direct database connections out of client-reachable barrels. An `index.ts` may explicitly re-export a client-safe public API; it must not wildcard-export a directory containing server code. Prefer type-only imports when only a type is needed, but remember that a type-only edge does not make a runtime value safe to expose.

Verify the actual bundler/import graph. Filename convention is a guardrail, not proof that a secret cannot reach the browser.

## ZOD-001: validate trust boundaries

Zod owns runtime parsing at the boundary. Define constraints that the application actually relies on, including required fields, shapes, discriminants, formats, and meaningful cross-field rules. Convert a validation failure into intentional route/action data or a status response; do not catch it as an unexpected success.

Authentication and authorization remain separate checks. A valid identifier is not proof that the caller may access the identified resource.

## ZOD-002: infer from the schema

The schema is the transport contract. Use `z.infer` for the parsed type and feed that type into the application boundary. When a schema transforms input, distinguish its input and output meanings; the application receives the validated output, not the raw transport value.

Generated React Router and database types have different ownership. Route types describe framework arguments and loader/action data; generated database types describe persistence. Zod describes runtime trust. Do not substitute one for another or create a hand-written intersection that merely silences an incompatibility.

## ZOD-003: parse once, then trust the internal contract

After a successful parse, pass the validated value through typed internal boundaries. Do not repeatedly parse the same trusted object in the route, application, repository, and domain layers. Repeated parsing blurs ownership, duplicates error mapping, and can cause transforms to run more than once.

Parse again only at a new trust boundary: persisted schemaless data, a fresh external response, a queue payload, or an independently versioned interface. Domain constructors may still enforce domain invariants; that is policy validation, not a duplicate transport parse.

## Boundary review table

| Input | Boundary owner | Expected output |
|---|---|---|
| FormData, params, URL search params | Route loader/action | Inferred application input or safe validation response |
| External API/webhook JSON | Infrastructure adapter | Validated provider DTO mapped to an application/domain value |
| Environment variables | Server configuration boundary | Validated server-only configuration |
| Supabase raw result | Infrastructure/query boundary | Generated typed result mapped away from vendor response shape |
| Already validated application input | Application/domain | No repeated transport parsing; apply domain invariants only |

## Verification

- Search maintained TypeScript for explicit `any`, `@ts-ignore`, blanket suppression, non-null assertion, and double-cast escape hatches.
- Trace every request/external input from `unknown` through one Zod parse into its inferred application input.
- Compare schemas and manual interfaces; remove duplicate transport types.
- Search for repeated parsing of a value already validated upstream.
- Inspect client-reachable exports and confirm no `.server` implementation or secret-bearing module is reachable.
- Run route type generation and TypeScript checking after changing a route schema or route signature.

## Official documentation evidence

| Product | Version or access date | Direct official URL | Supported Rule IDs |
|---|---|---|---|
| Zod | Declared `^3.24.2`; lockfile 3.24.3 | [Zod v3 basic usage](https://v3.zod.dev/?id=basic-usage) | ZOD-001, ZOD-003 |
| Zod | Declared `^3.24.2`; lockfile 3.24.3 | [Zod v3 type inference](https://v3.zod.dev/?id=type-inference) | ZOD-002 |
| TypeScript | Accessed 2026-08-04 | [Everyday Types: any and assertions](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#any) | TS-001 |
| TypeScript | Accessed 2026-08-04 | [Declaration Do's and Don'ts: any](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html#any) | TS-001 |
| TypeScript | Accessed 2026-08-04 | [Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) | TS-002 |
| TypeScript | Accessed 2026-08-04 | [Modules Reference](https://www.typescriptlang.org/docs/handbook/modules/reference.html) | TS-003, UI-003 |
