# Junho Plate Architecture Rules

This guide defines the approved dependency contract for `ARCH-001` through `ARCH-008`. It is functional and change-reason oriented: protect domain policy and external-effect seams, then keep the rest as light as the feature allows.

Rule map: `ARCH-001`, `ARCH-002`, `ARCH-003`, `ARCH-004`, `ARCH-005`, `ARCH-006`, `ARCH-007`, and `ARCH-008`.

## Allowed dependency arrows

| Arrow | Meaning |
|---|---|
| `routes -> application -> domain` | A route adapts the RR7 request/response protocol; application coordinates the operation; domain owns framework-independent policy. |
| `application -> ports` | An application operation names the external capability it needs without creating a concrete client. |
| `infrastructure -> ports` | Infrastructure implements a port with Supabase, Drizzle, or another external adapter. |
| `routes -> screens -> components` | A route passes serializable data and framework state into presentation composition. |
| `screens -> components` | A screen assembles focused UI pieces and cohesive view models. |
| `composition root -> application + infrastructure` | A server-side composition boundary may connect an implementation to its port. |

Arrows describe dependency direction, not a required call-stack depth. Infrastructure implements ports; ports do not import infrastructure.

## Forbidden dependency arrows

| Arrow | Why it fails |
|---|---|
| `domain -> React/RR7/Supabase/Drizzle` | Framework or persistence changes would force domain-policy changes (`ARCH-001`). |
| `screen/component -> Supabase/Drizzle` | Presentation would own data access and error mapping (`ARCH-002`, `SUPA-003`). |
| `application -> concrete Supabase client` | A use case would lose its external-effect seam (`ARCH-005`). |
| `feature -> another feature's internal path` | The target feature's internals become a cross-feature API (`ARCH-003`). |
| `infrastructure -> presentation` | A lower adapter would depend on a delivery mechanism (`ARCH-002`). |
| `client barrel -> .server implementation` | A public client import could expose server-only code or secrets (`TS-003`, `SEC-001`). |

The feature's explicit public API is the only allowed cross-feature entry. Shared behavior that truly has multiple owners belongs in an intentionally shared core boundary, not in whichever feature happened to need it first.

## Proportional layouts

Select the smallest layout that isolates actual changes. Names describe responsibilities; they are not generators or mandatory folder templates.

| Layout | Appropriate when | Minimum responsibility shape |
|---|---|---|
| **Static** | The route renders fixed or build-time content with no protected server operation | route, screen, components |
| **Server-backed** | Inputs or server reads/writes require validation and an external adapter, but there is no independent business model | route, schemas, application operation when coordination exists, infrastructure, screen, components |
| **Domain-complex** | Business invariants or workflows must remain stable while delivery and persistence change | route, schemas, application, domain, ports, infrastructure, screen, components |

A class, repository, use case, or wrapper is not mandatory without an actual change reason. A function can be an application operation; a plain object can be a domain value; a direct route-to-infrastructure read can remain acceptable for a small projection when it does not carry policy. Conversely, a short file still needs a boundary when it mixes authorization, policy, and external effects.

Create a seam only when it isolates at least one concrete reason to change: business policy, transport adaptation, persistence technology, security authority, external failure mapping, or reusable presentation. Collapse an empty pass-through abstraction that merely renames the next call.

## ARCH-006: infrastructure responsibility purity

Treat a module that imports `node:fs`, a database client, Supabase, Drizzle, a network SDK, or another vendor adapter as infrastructure. Keep that module focused on external I/O, serialization, vendor DTO mapping, transaction details, and infrastructure error translation.

Split the module when it also owns a responsibility that changes for a different reason:

| Mixed responsibility | Move to | Reason |
|---|---|---|
| Entity or block factories, ordering, state transitions, reusable invariants | Pure model or domain module | Product behavior should remain testable without filesystem or vendor imports. |
| Read → change → write coordination or multi-adapter workflow | Application operation | The use case coordinates effects while the adapter performs them. |
| CSS classes, Tailwind tokens, component variants, visual defaults | Screen/component presentation mapping | Visual redesign must not require persistence changes. |
| Product fallback or seed policy | Explicit application/domain factory | Missing data and intentional defaults must not be hidden inside storage behavior. |

Storage-specific serialization, legacy-row normalization, vendor error mapping, and a trivial read-only projection may remain beside the adapter when they contain no reusable product policy. Do not fail a module for importing several infrastructure utilities, exporting several adapter functions, or being long. Fail `ARCH-006` only when direct evidence shows infrastructure plus domain, application, or presentation ownership in the same module.

Use the smallest readable split. Plain functions are sufficient: for example, keep file I/O in `skill-content-file.repository.server.ts`, pure creation and movement in `skill-content.model.ts`, read-modify-write coordination in `update-skill-content.server.ts`, and semantic-to-Tailwind mapping in presentation. Do not introduce a class, generic repository base, or port unless it isolates an actual substitution, policy, or test seam.

## ARCH-007: runtime surface ownership

Treat Admin, Customer, API, Worker, and shared rendering or domain code as explicit runtime surfaces. Each surface needs a named entrypoint, an owner, and a dependency direction. The goal is not separate infrastructure: one process and one deployable are acceptable when the code still makes each surface independently traceable and verifiable.

Do not require separate processes or deployments merely to make the diagram look distributed. Split deployment topology only when scaling, security, failure isolation, release cadence, or platform constraints require it. Otherwise prefer explicit modules and one intentionally shared core.

## ARCH-008: scoped starter residue cleanup

Starter routes, sample features, configuration, and dependencies are claims about what the delivered product supports. Within the authorized slice, remove confirmed dead residue or name its current consumer and owner. Confirm deadness from route registration, import reachability, package scripts, runtime configuration, and build output rather than filenames alone.

Do not turn slice cleanup into repository-wide deletion. Dynamic imports, externally addressed routes, deployment tooling, and generated consumers can evade a simple text search. Retain uncertain or out-of-scope residue with the evidence needed for a later decision.

## Layer responsibilities

- Route modules own request data, params, URL search params, trust-boundary parsing, server authentication/authorization, application invocation, and RR7 response/status adaptation.
- Application operations own orchestration and depend on domain values and named ports. They do not import UI state or construct vendor clients.
- Domain code owns invariants and decisions with no React, RR7, Supabase, or Drizzle import.
- Infrastructure owns vendor calls, generated database types, raw response/error mapping, and transaction or RPC details.
- Screens own presentation composition and framework-visible pending, empty, expected-failure, and success states.
- Components own rendering and user intent through explicit UI props or a cohesive view model.
- An `index.ts` owns explicit public re-exports only; it owns no logic, client construction, environment reads, or side effects.

## Conflict precedence

When sources disagree, apply this exact order:

1. **Approved Junho Plate contract**
2. **Security and data integrity**
3. **Installed-version official documentation**
4. **Plate/Supaplate structure**
5. **Audited Wemake evidence**
6. **Heuristics**

The approved contract is the authority for functional DDD and public-boundary rules. Security can make a locally convenient convention unacceptable. Official documentation must match the installed behavior. Plate and Wemake are evidence, not normative proof. A heuristic alone may produce `WARN`; it never produces `FAIL` or a hard blocker.

## Evidence limits

The Plate checkout was observed read-only at `8449384cdfad30f20337bad6536b0c7d46a3dde5`. Its path categories include `app/routes.ts`, feature `api`, `screens`, `components`, `queries`, and `schema` paths; server clients under `app/core/lib`; a Drizzle client under `app/core/db`; `sql/migrations`; and `database.types.ts`.

No domain, application, ports, repository, or universal public-index path category was observed. The approved Junho Plate contract defines those responsibilities; Plate's separate route, presentation, feature, and server-adapter path categories corroborate separation without being treated as proof that every existing import conforms. No Plate source text, snippet, template, fixture, or builder is reproduced here.

## Official architecture evidence

| Product | Version or access date | Direct official URL | Supported Rule IDs |
|---|---|---|---|
| Microsoft .NET Architecture guidance | Accessed 2026-08-04 | [Designing a DDD-oriented microservice](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice) | ARCH-001, ARCH-002 |

## Review outcomes

- `PASS` when dependencies follow an allowed arrow and each present seam isolates a real responsibility.
- `WARN` when a documented transition or flatter layout is reasonable but deserves a future check.
- `FAIL` when a forbidden arrow crosses domain, authorization, server/client, presentation/data, or feature-public boundaries.
- Do not fail a feature for file length, function length, prop count, class absence, or layer count alone.
