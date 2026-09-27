# Junho Plate Wemake Rule Evidence

This is the human index from the 49 Junho Plate Rule IDs to audited Wemake history, review-derived Junho Plate contracts, and current primary documentation. Wemake is pinned at `21ceb5d55c608772ed374a651eaf1639eaec6d5c`; the committed JSON contains 135 chronological records and was verified on 2026-08-04.

## Evidence interpretation

- `foundation`, `pattern-introduction`, `pattern-refinement`, and `correction` may explain a responsibility transition, but current official docs and the approved contract still outrank them.
- `teaching-transition` and `legacy-risk` are counterexample/context evidence only. They are never a current recommendation.
- “No tagged commit” is an honest gap, not permission to attach an unrelated hash. The rule then relies on the approved contract, a precise Plate path-category observation, or current official documentation.
- Paths below identify changed path categories and paraphrase the audited responsibility movement. They do not reproduce implementation text.

## Rule ID index

| Rule ID | Audited Wemake commit and path evidence | Evidence role | Current source key |
|---|---|---|---|
| ARCH-001 | No tagged commit in the audited index | Current DDD guidance is normative; Plate feature and server-adapter path categories corroborate the boundary without proving import conformance | MS-DDD, PLATE-PATH |
| ARCH-002 | No tagged commit in the audited index | Current DDD guidance is normative; Plate's distinct route, presentation, and adapter categories corroborate dependency separation | MS-DDD, PLATE-PATH |
| ARCH-003 | No tagged commit in the audited index | Plate has separate top-level feature ownership categories; the approved contract defines each feature's explicit entry as its public boundary | PLATE-PATH |
| ARCH-004 | [7ea2938489c0d780131f77d569e4a394b0755662](https://github.com/nomadcoders/wemake/commit/7ea2938489c0d780131f77d569e4a394b0755662), `app/routes.ts`; [a2fd948e70d928bdb3063d2360a6d0ff27a22054](https://github.com/nomadcoders/wemake/commit/a2fd948e70d928bdb3063d2360a6d0ff27a22054), root route/layout scaffold | Positive route registry and root-layout foundation; no mandatory layer count | RR-ROUTE |
| ARCH-005 | No tagged commit in the audited index | Plate isolates external-adapter categories while features use proportional category sets; the approved contract supplies the port rule without mandating repository classes | PLATE-PATH |
| ARCH-006 | No tagged commit in the audited index | Plate separates screen/component, feature api/query, and core server-adapter path categories; the approved contract defines responsibility purity without claiming every file conforms | PLATE-PATH |
| ARCH-007 | No tagged commit in the audited index | Review-derived Junho Plate contract requires explicit Admin, Customer, API, Worker, and shared-core ownership without forcing deployment topology | REVIEW-EVIDENCE |
| ARCH-008 | No tagged commit in the audited index | Review-derived Junho Plate contract requires evidence and scope authority before starter-residue removal | REVIEW-EVIDENCE |
| RR7-001 | [9bf3856cec8027a3df3e58c6b1828a43d5649067](https://github.com/nomadcoders/wemake/commit/9bf3856cec8027a3df3e58c6b1828a43d5649067), route page plus presentation paths; [73566ff6a5728165c42890b189716954f6b04037](https://github.com/nomadcoders/wemake/commit/73566ff6a5728165c42890b189716954f6b04037), message route/query/layout paths | Positive route-owned read transitions | RR-ROUTE |
| RR7-002 | [0eff204384cfa735eaa3325b6b5b94230301e9af](https://github.com/nomadcoders/wemake/commit/0eff204384cfa735eaa3325b6b5b94230301e9af), auth route/query paths; [fc502e6b262e32ab516af8041fcab5c69779905e](https://github.com/nomadcoders/wemake/commit/fc502e6b262e32ab516af8041fcab5c69779905e), notification action/mutation paths | Corrected/positive server mutation boundaries | RR-FORM, RR-ROUTE |
| RR7-003 | [c14569ea751224d0f6cf0f4cc64efe49613482f2](https://github.com/nomadcoders/wemake/commit/c14569ea751224d0f6cf0f4cc64efe49613482f2), route page | Positive refinement to generated route component data | RR-TYPES |
| RR7-004 | [0eff204384cfa735eaa3325b6b5b94230301e9af](https://github.com/nomadcoders/wemake/commit/0eff204384cfa735eaa3325b6b5b94230301e9af), auth route/query paths; [b606a01cb4bfe312a2490ea3bb71138af351f6f2](https://github.com/nomadcoders/wemake/commit/b606a01cb4bfe312a2490ea3bb71138af351f6f2), OAuth route/client paths | Positive server-auth transitions; resource authorization still requires current policy | SUPA-SSR, SUPA-RLS |
| RR7-005 | [a2fd948e70d928bdb3063d2360a6d0ff27a22054](https://github.com/nomadcoders/wemake/commit/a2fd948e70d928bdb3063d2360a6d0ff27a22054), root/route scaffold; [99bbdb1e6e157bbe941ab9857a33d46b5ec822ab](https://github.com/nomadcoders/wemake/commit/99bbdb1e6e157bbe941ab9857a33d46b5ec822ab), validated route page | Foundation ErrorBoundary plus positive 400-status mapping | RR-ERROR, RR-STATUS |
| RR7-006 | [2d4ba7aff8ab8541a3c1016d1d1b15a6d0eea819](https://github.com/nomadcoders/wemake/commit/2d4ba7aff8ab8541a3c1016d1d1b15a6d0eea819), pagination components | Positive URL-state seam; later messaging history remains legacy/partial rather than a clean correction | RR-PENDING, REACT-NO-EFFECT |
| SUPA-001 | [0acd28f36d82fb9542f36bf577873e759d77ec8a](https://github.com/nomadcoders/wemake/commit/0acd28f36d82fb9542f36bf577873e759d77ec8a), route/query/client paths | Correction from a singleton chain to request-scoped SSR client flow | SUPA-SSR, SUPA-SECURE |
| SUPA-002 | No tagged commit in the audited index | Current Supabase error contract plus Plate query/screen seam | SUPA-ERROR |
| SUPA-003 | [3245085cd7d7755aeef233475b25be71041e089f](https://github.com/nomadcoders/wemake/commit/3245085cd7d7755aeef233475b25be71041e089f), notification component/page/query/type paths | Positive query-to-presentation mapping seam | SUPA-TYPES |
| SUPA-004 | [3245085cd7d7755aeef233475b25be71041e089f](https://github.com/nomadcoders/wemake/commit/3245085cd7d7755aeef233475b25be71041e089f), query and `database.types.ts` paths | Positive typed query evidence | SUPA-TYPES |
| SUPA-005 | [b568063272e4032a0529b3c2c9c2cd1079f145de](https://github.com/nomadcoders/wemake/commit/b568063272e4032a0529b3c2c9c2cd1079f145de), message layout/page/query paths | `legacy-risk` counterexample: broad subscription and duplicated loader state despite cleanup | SUPA-REALTIME, REACT-EFFECTS |
| DB-001 | [65282d0da5dbb3575475fcdbdb1997ec20b90e3b](https://github.com/nomadcoders/wemake/commit/65282d0da5dbb3575475fcdbdb1997ec20b90e3b), team schema and sequential migration paths | Positive migration-tracked table refinement | SUPA-MIG |
| DB-002 | [0a47c0a69e9e0d9cfead7483145f56c1ea4c0e02](https://github.com/nomadcoders/wemake/commit/0a47c0a69e9e0d9cfead7483145f56c1ea4c0e02), settings page only | `legacy-risk` counterexample: lesson claims RLS without policy-file evidence | SUPA-RLS, SUPA-SECURE |
| DB-003 | [3e23c51baff7b984c48d2c665cedbcc6e79fd88f](https://github.com/nomadcoders/wemake/commit/3e23c51baff7b984c48d2c665cedbcc6e79fd88f), database function path | Partial correction for safe search path; migration and privileges remain unresolved | SUPA-FUNCTIONS |
| DB-004 | [67d3b45a935dc1b3f92aa96117f0cd24f6462ab7](https://github.com/nomadcoders/wemake/commit/67d3b45a935dc1b3f92aa96117f0cd24f6462ab7), standalone view/query/type paths | `legacy-risk` counterexample: no migration or `security_invoker` evidence | SUPA-TABLES |
| DB-005 | [09e731982f319eedc61e9708f113813831aea6ce](https://github.com/nomadcoders/wemake/commit/09e731982f319eedc61e9708f113813831aea6ce), room mutation/schema/function paths | `legacy-risk` counterexample: related writes are separate | PG-TRANSACTIONS |
| TS-001 | No tagged commit in the audited index | Official TypeScript guidance explains that `any` disables checking and should be avoided outside migration boundaries | TS-ANY, TS-DONT-ANY |
| TS-002 | [c14569ea751224d0f6cf0f4cc64efe49613482f2](https://github.com/nomadcoders/wemake/commit/c14569ea751224d0f6cf0f4cc64efe49613482f2), route page | Positive generated-type refinement; later raw-cast commits remain counterexamples | TS-NARROW |
| TS-003 | [0acd28f36d82fb9542f36bf577873e759d77ec8a](https://github.com/nomadcoders/wemake/commit/0acd28f36d82fb9542f36bf577873e759d77ec8a), server-client/query paths | Corrected server-client flow; current module/bundle review remains required | TS-MODULES |
| ZOD-001 | [99bbdb1e6e157bbe941ab9857a33d46b5ec822ab](https://github.com/nomadcoders/wemake/commit/99bbdb1e6e157bbe941ab9857a33d46b5ec822ab), route page; [0eff204384cfa735eaa3325b6b5b94230301e9af](https://github.com/nomadcoders/wemake/commit/0eff204384cfa735eaa3325b6b5b94230301e9af), auth route/query paths | Positive route validation and later auth correction | ZOD-V3-BASIC |
| ZOD-002 | No tagged commit in the audited index | Zod v3 inference is normative; do not attach an unrelated Wemake hash | ZOD-V3-INFER |
| ZOD-003 | No tagged commit in the audited index | Approved parse-once contract; no historical Wemake recommendation claimed | ZOD-V3-BASIC |
| UI-001 | No tagged commit in the audited index | React component identity guidance plus Plate component path category | REACT-COMPONENT |
| UI-002 | [2c76d525f148d39777c2f1a4f5881b68d07593b4](https://github.com/nomadcoders/wemake/commit/2c76d525f148d39777c2f1a4f5881b68d07593b4), product card/home paths | Positive focused presentation component seam | REACT-PROPS |
| UI-003 | No tagged commit in the audited index | Approved explicit-public-API rule plus TypeScript modules | TS-MODULES |
| UI-004 | [a2fd948e70d928bdb3063d2360a6d0ff27a22054](https://github.com/nomadcoders/wemake/commit/a2fd948e70d928bdb3063d2360a6d0ff27a22054), root route/layout scaffold; [9bf3856cec8027a3df3e58c6b1828a43d5649067](https://github.com/nomadcoders/wemake/commit/9bf3856cec8027a3df3e58c6b1828a43d5649067), route/component paths | Positive root layout and route-fed presentation seams | RR-ROUTE |
| UI-005 | [2d4ba7aff8ab8541a3c1016d1d1b15a6d0eea819](https://github.com/nomadcoders/wemake/commit/2d4ba7aff8ab8541a3c1016d1d1b15a6d0eea819), pagination components | Positive URL-visible navigation state; Realtime history supplies separate risk evidence | REACT-EFFECTS, RR-PENDING |
| UI-006 | No tagged commit in the audited index | Review-derived Junho Plate contract requires preview and customer surfaces to share the published rendering core | REVIEW-EVIDENCE |
| UI-007 | No tagged commit in the audited index | Review-derived stylesheet ownership contract; Vite documents the available CSS Modules mechanism | REVIEW-EVIDENCE, VITE-CSS |
| ERR-001 | [99bbdb1e6e157bbe941ab9857a33d46b5ec822ab](https://github.com/nomadcoders/wemake/commit/99bbdb1e6e157bbe941ab9857a33d46b5ec822ab), validated route page | Positive expected-error/status classification | RR-ERROR |
| ERR-002 | No tagged commit in the audited index | Approved truthful-error contract plus current Supabase error semantics | SUPA-ERROR |
| ERR-003 | [874adeb6b1dc31c78d4654569abc003d3dc3937e](https://github.com/nomadcoders/wemake/commit/874adeb6b1dc31c78d4654569abc003d3dc3937e), delayed community route/query paths | `teaching-transition` counterexample, not fallback guidance | RR-ERROR |
| TEST-001 | No tagged commit in the audited index | Approved risk-value contract plus framework testing limits | RR-TESTING |
| TEST-002 | No tagged commit in the audited index | Approved rejection of test quotas and tests-for-their-own-sake | RR-TESTING |
| BUILD-001 | No tagged commit in the audited index | React Router deployment guidance plus the review-derived built-artifact smoke contract | RR-DEPLOY, REVIEW-EVIDENCE |
| BUILD-002 | No tagged commit in the audited index | Review-derived dependency justification contract; no arbitrary bundle quota is inferred | REVIEW-EVIDENCE |
| AGENT-001 | No tagged commit in the audited index | Current Cloudflare Agents and Workflows guidance defines the preferred compatible runtime split | CF-AGENTS, CF-WORKFLOWS |
| AGENT-002 | No tagged commit in the audited index | Junho Plate Judge boundary plus Cloudflare sub-agent and Workflow primitives | CF-SUBAGENTS, CF-WORKFLOWS |
| SEC-001 | [a0d678874d1de875a6a89456c2b4221522a81ee6](https://github.com/nomadcoders/wemake/commit/a0d678874d1de875a6a89456c2b4221522a81ee6), idea mutation/route/shared client paths | `legacy-risk` counterexample: elevated authority crosses unsafe boundaries | SUPA-SECURE |
| SEC-002 | [a30964afb5ada4dd72adf63f218754174e22531b](https://github.com/nomadcoders/wemake/commit/a30964afb5ada4dd72adf63f218754174e22531b), community mutation/route/schema paths; [fc502e6b262e32ab516af8041fcab5c69779905e](https://github.com/nomadcoders/wemake/commit/fc502e6b262e32ab516af8041fcab5c69779905e), notification action paths | Positive server-mediated effects; current server authorization and RLS still control | SUPA-RLS |
| SEC-003 | [a0d678874d1de875a6a89456c2b4221522a81ee6](https://github.com/nomadcoders/wemake/commit/a0d678874d1de875a6a89456c2b4221522a81ee6), remote API loader/admin-client paths | `legacy-risk` counterexample: side effect lacks action/consent/audit boundary; the approved contract defines the required consent or automation authority | WEMAKE-122, approved contract |

## Current official documentation index

Every current-doc citation records the product, a declared/resolved version or the access date, the direct official URL, and supported Rule IDs. Unversioned React Router pages are current guidance accessed on the stated date; they are not represented as 7.5.1 archive proof. The verified 7.5.1 Type Safety and Pending UI archives are version-specific.

| Product | Version or access date | Direct official URL | Supported Rule IDs |
|---|---|---|---|
| Microsoft .NET Architecture guidance | Accessed 2026-08-04 | [MS-DDD: Designing a DDD-oriented microservice](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice) | ARCH-001, ARCH-002 |
| React Router | Accessed 2026-08-04; installed app is 7.5.1 | [RR-ROUTE: Route Module](https://reactrouter.com/start/framework/route-module) | RR7-001, RR7-004, UI-004 |
| React Router | Installed 7.5.1 | [RR-TYPES: Route Module Type Safety](https://reactrouter.com/7.5.1/how-to/route-module-type-safety) | RR7-003 |
| React Router | Accessed 2026-08-04 | [RR-FORM: Form vs. fetcher](https://reactrouter.com/explanation/form-vs-fetcher) | RR7-002 |
| React Router | Installed 7.5.1 | [RR-PENDING: Pending UI](https://reactrouter.com/7.5.1/start/framework/pending-ui) | RR7-006, UI-005 |
| React Router | Accessed 2026-08-04; installed app is 7.5.1 | [RR-ERROR: Error Boundaries](https://reactrouter.com/how-to/error-boundary) | RR7-005, ERR-001, ERR-003 |
| React Router | Accessed 2026-08-04; installed app is 7.5.1 | [RR-STATUS: Status Codes](https://reactrouter.com/how-to/status) | RR7-005 |
| React Router | Accessed 2026-08-04 | [RR-TESTING: Framework Testing](https://reactrouter.com/start/framework/testing) | TEST-001, TEST-002 |
| React Router | Accessed 2026-09-27; v7 framework mode | [RR-DEPLOY: Deploying](https://reactrouter.com/start/framework/deploying) | BUILD-001 |
| React | Accessed 2026-08-04 | [REACT-COMPONENT: Your First Component](https://react.dev/learn/your-first-component) | UI-001 |
| React | Accessed 2026-08-04 | [REACT-PROPS: Passing Props](https://react.dev/learn/passing-props-to-a-component) | UI-002 |
| React | Accessed 2026-08-04 | [REACT-EFFECTS: Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects) | UI-005 |
| React | Accessed 2026-08-04 | [REACT-NO-EFFECT: You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) | RR7-006, UI-005 |
| Vite | Accessed 2026-09-27 | [VITE-CSS: CSS Modules](https://vite.dev/guide/features.html#css-modules) | UI-007 |
| Cloudflare Agents SDK | Accessed 2026-09-27 | [CF-AGENTS: Agents](https://developers.cloudflare.com/agents/) | AGENT-001 |
| Cloudflare Agents SDK | Accessed 2026-09-27 | [CF-WORKFLOWS: Using Agents with Workflows](https://developers.cloudflare.com/agents/concepts/workflows/) | AGENT-001, AGENT-002 |
| Cloudflare Agents SDK | Accessed 2026-09-27 | [CF-SUBAGENTS: Sub-agents](https://developers.cloudflare.com/agents/runtime/execution/sub-agents/) | AGENT-002 |
| Supabase JS/SSR | Declared `^2.49.1`; lockfile 2.49.4; accessed 2026-08-04 | [SUPA-SSR: Creating a client for SSR](https://supabase.com/docs/guides/auth/server-side/creating-a-client) | RR7-004, SUPA-001 |
| Supabase | Accessed 2026-08-04 | [SUPA-SECURE: Securing your data](https://supabase.com/docs/guides/database/secure-data) | SUPA-001, DB-002, SEC-001 |
| Supabase | Accessed 2026-08-04 | [SUPA-RLS: Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security) | DB-002, SEC-002 |
| Supabase JS | Declared `^2.49.1`; lockfile 2.49.4; accessed 2026-08-04 | [SUPA-ERROR: Handling errors in supabase-js](https://supabase.com/docs/guides/api/handling-errors-in-supabase-js) | SUPA-002, ERR-002 |
| Supabase | Accessed 2026-08-04 | [SUPA-MIG: Database Migrations](https://supabase.com/docs/guides/deployment/database-migrations) | DB-001 |
| Supabase | Accessed 2026-08-04 | [SUPA-TYPES: Generating TypeScript Types](https://supabase.com/docs/guides/api/rest/generating-types) | SUPA-004 |
| Supabase/PostgreSQL | Accessed 2026-08-04 | [SUPA-FUNCTIONS: Database Functions](https://supabase.com/docs/guides/database/functions) | DB-003 |
| Supabase/PostgreSQL | Accessed 2026-08-04 | [SUPA-TABLES: Tables and view security](https://supabase.com/docs/guides/database/tables) | DB-004 |
| Supabase Realtime | Declared supabase-js `^2.49.1`; lockfile 2.49.4; accessed 2026-08-04 | [SUPA-REALTIME: Getting Started](https://supabase.com/docs/guides/realtime/getting_started) | SUPA-005 |
| PostgreSQL | Current docs accessed 2026-08-04 | [PG-TRANSACTIONS: Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html) | DB-005 |
| TypeScript | Accessed 2026-08-04 | [TS-ANY: Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#any) | TS-001 |
| TypeScript | Accessed 2026-08-04 | [TS-DONT-ANY: Declaration-file Do's and Don'ts](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html#any) | TS-001 |
| TypeScript | Accessed 2026-08-04 | [TS-NARROW: Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) | TS-002 |
| TypeScript | Accessed 2026-08-04 | [TS-MODULES: Modules Reference](https://www.typescriptlang.org/docs/handbook/modules/reference.html) | TS-003, UI-003 |
| Zod | Declared `^3.24.2`; lockfile 3.24.3 | [ZOD-V3-BASIC: Basic usage](https://v3.zod.dev/?id=basic-usage) | ZOD-001, ZOD-003 |
| Zod | Declared `^3.24.2`; lockfile 3.24.3 | [ZOD-V3-INFER: Type inference](https://v3.zod.dev/?id=type-inference) | ZOD-002 |

## Plate observation and license boundary

Plate evidence is pinned at `8449384cdfad30f20337bad6536b0c7d46a3dde5` and limited to package metadata and path categories. `PLATE-PATH` means the route registry, feature screen/component/query/schema categories, core server-client/database categories, SQL migration/function categories, and generated database type path were observed. It never means Plate source proved the full rule or that existing Plate code is a recommendation.

Operate only on user-owned local projects. Never package or redistribute Supaplate source, snippets, templates, fixtures, or builders. Wemake citations identify public commit/path history and paraphrase responsibility changes; they do not copy source blocks.
