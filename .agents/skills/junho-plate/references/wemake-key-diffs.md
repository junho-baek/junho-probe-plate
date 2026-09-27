# Junho Plate Wemake Key Diffs

This narrative is pinned to Wemake commit `21ceb5d55c608772ed374a651eaf1639eaec6d5c` and the committed 135-record audit. It describes responsibility movement by commit and changed path category. It contains no copied implementation and never treats a course transition or legacy branch as current guidance.

## Route config and layout

**Evidence.** [a2fd948e70d928bdb3063d2360a6d0ff27a22054](https://github.com/nomadcoders/wemake/commit/a2fd948e70d928bdb3063d2360a6d0ff27a22054) establishes the framework/root shell and root layout. [7ea2938489c0d780131f77d569e4a394b0755662](https://github.com/nomadcoders/wemake/commit/7ea2938489c0d780131f77d569e4a394b0755662) adds explicit route-registry and demo-route paths. [b669fde2192fbc54880d24c19dac0d9e8b6bebfe](https://github.com/nomadcoders/wemake/commit/b669fde2192fbc54880d24c19dac0d9e8b6bebfe) later adds a product layout and nested route registration.

**Responsibility movement.** Route topology becomes explicit before feature behavior grows, and nested presentation gains a layout seam. The nested-layout commit is a `teaching-transition`: its loaders are fake and its action is empty, so only the route/layout structure is useful evidence.

**Audit caveat.** Despite its title, [43420ba21ba7889e08b29043b3af3d4babd2d1ef](https://github.com/nomadcoders/wemake/commit/43420ba21ba7889e08b29043b3af3d4babd2d1ef) changes route-local metadata and stylesheet links but does not introduce a layout. The audited index records that observed behavior, so Junho Plate cites the root and nested-layout commits above for layout evidence.

**Current conclusion.** Keep route registration and layouts framework-native, but require real loader/action ownership before calling a route complete (`ARCH-004`, `UI-004`).

## Generated Route types

**Evidence.** [27b4717b8257a2f61c1ca17458c3996c182cf35f](https://github.com/nomadcoders/wemake/commit/27b4717b8257a2f61c1ca17458c3996c182cf35f) introduces an intentionally untyped loader-data lesson with debug output. [c14569ea751224d0f6cf0f4cc64efe49613482f2](https://github.com/nomadcoders/wemake/commit/c14569ea751224d0f6cf0f4cc64efe49613482f2) replaces the untyped component contract with generated Route props. [c9b8baec70fa8939a9c064be37db6022c940d75b](https://github.com/nomadcoders/wemake/commit/c9b8baec70fa8939a9c064be37db6022c940d75b) removes the demo/debug loader path while adding route-owned redirect/resource behavior.

**Responsibility movement.** Framework data types move from an ad hoc component annotation to the generated route boundary. The type refinement alone does not make fake data or logging production-ready; the following control-flow commit removes that lesson artifact.

**Current conclusion.** Generate Route types for loader, action, component, and error contracts, while keeping application/domain inputs framework-independent (`RR7-003`, `TS-002`).

## Zod and ErrorBoundary

**Evidence.** The root scaffold [a2fd948e70d928bdb3063d2360a6d0ff27a22054](https://github.com/nomadcoders/wemake/commit/a2fd948e70d928bdb3063d2360a6d0ff27a22054) establishes a typed root ErrorBoundary. [99bbdb1e6e157bbe941ab9857a33d46b5ec822ab](https://github.com/nomadcoders/wemake/commit/99bbdb1e6e157bbe941ab9857a33d46b5ec822ab) adds Zod validation for a route parameter, explicit 400 responses, and a route error boundary. [0eff204384cfa735eaa3325b6b5b94230301e9af](https://github.com/nomadcoders/wemake/commit/0eff204384cfa735eaa3325b6b5b94230301e9af) later corrects auth actions with validation.

**Responsibility movement.** External input becomes a route-owned runtime decision and expected failures become HTTP/route outcomes instead of implicit component assumptions.

**Caveat.** Validation is not universal in the pinned history: [a1befc3516d1bebaf2071971bef8d51485e245bf](https://github.com/nomadcoders/wemake/commit/a1befc3516d1bebaf2071971bef8d51485e245bf) leaves an optimistic route parameter unvalidated, and [70224a3e386ef06b28a0fc28d2490b64fa2cb708](https://github.com/nomadcoders/wemake/commit/70224a3e386ef06b28a0fc28d2490b64fa2cb708) casts raw message FormData. Those are legacy risks, not recommendations.

**Current conclusion.** Follow `unknown -> Zod -> z.infer -> application input -> domain value`, map expected status, and let unexpected errors reach an ErrorBoundary (`ZOD-001`, `RR7-005`, `ERR-001`).

## Query and screen

**Evidence.** [d9d9cadd3c9ebd765834da102f5bc7cda954cd40](https://github.com/nomadcoders/wemake/commit/d9d9cadd3c9ebd765834da102f5bc7cda954cd40) creates database-adapter, query, loader-backed page, and presentation-component paths. [594f62ec2d6c14387a689027be8f5b5bf0f67338](https://github.com/nomadcoders/wemake/commit/594f62ec2d6c14387a689027be8f5b5bf0f67338) swaps query implementation toward a typed singleton Supabase client. [0acd28f36d82fb9542f36bf577873e759d77ec8a](https://github.com/nomadcoders/wemake/commit/0acd28f36d82fb9542f36bf577873e759d77ec8a) later passes request-scoped clients from loaders into feature query modules.

**Responsibility movement.** Pages/screens consume query results rather than embedding persistence. Client creation then moves toward the request/server boundary while query modules remain feature infrastructure seams.

**Caveat.** [67d3b45a935dc1b3f92aa96117f0cd24f6462ab7](https://github.com/nomadcoders/wemake/commit/67d3b45a935dc1b3f92aa96117f0cd24f6462ab7) adds a standalone view and screen assertions; [9068f40f7ee0a98066e2ea08acd661536cb2d0f0](https://github.com/nomadcoders/wemake/commit/9068f40f7ee0a98066e2ea08acd661536cb2d0f0) removes assertions through a type overlay but does not provide runtime validation, migration tracking, or view security.

**Current conclusion.** Keep query/vendor mapping outside screens, map raw results before presentation/domain boundaries, and do not confuse a static type overlay with database security (`SUPA-003`, `UI-004`).

## Supabase SSR

**Evidence.** [594f62ec2d6c14387a689027be8f5b5bf0f67338](https://github.com/nomadcoders/wemake/commit/594f62ec2d6c14387a689027be8f5b5bf0f67338) through [9068f40f7ee0a98066e2ea08acd661536cb2d0f0](https://github.com/nomadcoders/wemake/commit/9068f40f7ee0a98066e2ea08acd661536cb2d0f0) retains a typed module-level client as a pre-SSR teaching pattern. [0acd28f36d82fb9542f36bf577873e759d77ec8a](https://github.com/nomadcoders/wemake/commit/0acd28f36d82fb9542f36bf577873e759d77ec8a) introduces browser/server separation and a request-scoped server client across loader/query paths. [0eff204384cfa735eaa3325b6b5b94230301e9af](https://github.com/nomadcoders/wemake/commit/0eff204384cfa735eaa3325b6b5b94230301e9af) propagates generated cookie headers in auth redirects.

**Responsibility movement.** User session ownership moves from a shared singleton into request-scoped server adaptation, while browser access retains a separate client role.

**Caveat.** The SSR correction is partial: ordinary loaders in that commit create response headers but do not consistently attach refreshed cookie headers, and it does not repair standalone view/function security.

**Current conclusion.** Separate browser, request-scoped server, and narrow admin clients; verify cookie propagation for the installed SSR stack rather than copying the historical implementation (`SUPA-001`, `TS-003`).

## loader and action

**Evidence.** [86cefbb6a7793bd0830bf59c88e9cfe3ebb92164](https://github.com/nomadcoders/wemake/commit/86cefbb6a7793bd0830bf59c88e9cfe3ebb92164) and [27b4717b8257a2f61c1ca17458c3996c182cf35f](https://github.com/nomadcoders/wemake/commit/27b4717b8257a2f61c1ca17458c3996c182cf35f) are fake/debug loader lessons; [c9b8baec70fa8939a9c064be37db6022c940d75b](https://github.com/nomadcoders/wemake/commit/c9b8baec70fa8939a9c064be37db6022c940d75b) removes that demo path. [b4025d60d9e1859b5f6b0278846e4c73b0c282a6](https://github.com/nomadcoders/wemake/commit/b4025d60d9e1859b5f6b0278846e4c73b0c282a6) introduces a delayed/raw login action; [0eff204384cfa735eaa3325b6b5b94230301e9af](https://github.com/nomadcoders/wemake/commit/0eff204384cfa735eaa3325b6b5b94230301e9af) corrects it to validated server auth.

The clearest complete mutation chain is [5034ee6cd1700da4fe979f936c69acf284f4fb91](https://github.com/nomadcoders/wemake/commit/5034ee6cd1700da4fe979f936c69acf284f4fb91) to [9821875b81b37db6b0793371cec6891ad0ced095](https://github.com/nomadcoders/wemake/commit/9821875b81b37db6b0793371cec6891ad0ced095): an incomplete reply mutation becomes a complete validated interaction.

**Current conclusion.** Loader owns route reads, action owns mutations, and fake delay/log/empty handler lessons are not production patterns. The auth correction is itself partial because a logout side effect remains loader/GET-oriented (`RR7-001`, `RR7-002`).

## Auth and RLS

**Evidence.** [7158f18a009ae1b436100d71c24d37de517e46f6](https://github.com/nomadcoders/wemake/commit/7158f18a009ae1b436100d71c24d37de517e46f6) establishes auth route/layout/page paths. The action chain [b4025d60d9e1859b5f6b0278846e4c73b0c282a6](https://github.com/nomadcoders/wemake/commit/b4025d60d9e1859b5f6b0278846e4c73b0c282a6) to [0eff204384cfa735eaa3325b6b5b94230301e9af](https://github.com/nomadcoders/wemake/commit/0eff204384cfa735eaa3325b6b5b94230301e9af) moves fake login behavior to validated Supabase auth.

**RLS caveat.** [0a47c0a69e9e0d9cfead7483145f56c1ea4c0e02](https://github.com/nomadcoders/wemake/commit/0a47c0a69e9e0d9cfead7483145f56c1ea4c0e02) changes only a settings-page path and includes no policy artifact. A later broad merge [4cbba8b6d4b19fb808a9b2f10cc75a0b5d127dcb](https://github.com/nomadcoders/wemake/commit/4cbba8b6d4b19fb808a9b2f10cc75a0b5d127dcb) exposes only narrow message-room policy evidence, not comprehensive RLS. Standalone profile-trigger history remains legacy risk.

**Current conclusion.** Auth actions do not prove RLS. Verify server authorization, table policies, minimum grants, migrations, and function/view security independently (`RR7-004`, `DB-002`, `SEC-002`).

## Form and fetcher

**Evidence.** [962b941fe4d610f4c4380e1556b9d5dcfc26a94f](https://github.com/nomadcoders/wemake/commit/962b941fe4d610f4c4380e1556b9d5dcfc26a94f) introduces shared form controls and a submit shell. [b669fde2192fbc54880d24c19dac0d9e8b6bebfe](https://github.com/nomadcoders/wemake/commit/b669fde2192fbc54880d24c19dac0d9e8b6bebfe) still has an empty action. [5034ee6cd1700da4fe979f936c69acf284f4fb91](https://github.com/nomadcoders/wemake/commit/5034ee6cd1700da4fe979f936c69acf284f4fb91) to [9821875b81b37db6b0793371cec6891ad0ced095](https://github.com/nomadcoders/wemake/commit/9821875b81b37db6b0793371cec6891ad0ced095) completes a validated Form reply flow.

Fetcher mechanics progress through [4169ccfec4a752b672d88115cad4db27c0d41180](https://github.com/nomadcoders/wemake/commit/4169ccfec4a752b672d88115cad4db27c0d41180), [ccd8ec5edb517dc0e61cb5c9c110ab1dabc821f5](https://github.com/nomadcoders/wemake/commit/ccd8ec5edb517dc0e61cb5c9c110ab1dabc821f5), and [a1befc3516d1bebaf2071971bef8d51485e245bf](https://github.com/nomadcoders/wemake/commit/a1befc3516d1bebaf2071971bef8d51485e245bf). All three remain `teaching-transition`; the last is functional but delayed and unvalidated.

**Current conclusion.** Choose Form for navigation and fetcher for in-place work, but validate in the action and never cite the fake-success teaching sequence as a complete mutation boundary (`RR7-002`).

## Optimistic UI

**Evidence.** The fetcher sequence begins with logged fake results at [4169ccfec4a752b672d88115cad4db27c0d41180](https://github.com/nomadcoders/wemake/commit/4169ccfec4a752b672d88115cad4db27c0d41180), connects component submission at [ccd8ec5edb517dc0e61cb5c9c110ab1dabc821f5](https://github.com/nomadcoders/wemake/commit/ccd8ec5edb517dc0e61cb5c9c110ab1dabc821f5), and adds a real optimistic toggle at [a1befc3516d1bebaf2071971bef8d51485e245bf](https://github.com/nomadcoders/wemake/commit/a1befc3516d1bebaf2071971bef8d51485e245bf). [d13c78798176354cea7a00ec69a145b5c15417dc](https://github.com/nomadcoders/wemake/commit/d13c78798176354cea7a00ec69a145b5c15417dc) removes the artificial delay during a broad integration.

**Caveat.** The delay removal is only partial correction and the commit is `legacy-risk`: route validation, query-then-write atomicity/race behavior, and explicit failure handling remain unresolved.

**Current conclusion.** Optimism must derive from fetcher submission data, retain truthful rollback/error behavior, and never depend on delay or unvalidated input (`RR7-006`, `UI-005`).

## Realtime and function security

**Evidence.** [09e731982f319eedc61e9708f113813831aea6ce](https://github.com/nomadcoders/wemake/commit/09e731982f319eedc61e9708f113813831aea6ce) introduces separate room writes and an unqualified standalone function. [7d732d73688877eb834f1fd321d015dda0080974](https://github.com/nomadcoders/wemake/commit/7d732d73688877eb834f1fd321d015dda0080974) adds a messages view with unresolved migration/security evidence. [70224a3e386ef06b28a0fc28d2490b64fa2cb708](https://github.com/nomadcoders/wemake/commit/70224a3e386ef06b28a0fc28d2490b64fa2cb708) casts raw message form data. [b568063272e4032a0529b3c2c9c2cd1079f145de](https://github.com/nomadcoders/wemake/commit/b568063272e4032a0529b3c2c9c2cd1079f145de) adds Realtime while duplicating loader state and using broad/stale/raw subscription handling.

[3e23c51baff7b984c48d2c665cedbcc6e79fd88f](https://github.com/nomadcoders/wemake/commit/3e23c51baff7b984c48d2c665cedbcc6e79fd88f) qualifies relations for an empty search path, but leaves migration and privilege gaps. [6d58ab9afa611d77f1b5add657dfc370fb674529](https://github.com/nomadcoders/wemake/commit/6d58ab9afa611d77f1b5add657dfc370fb674529) removes stale timestamp text and narrows `shouldRevalidate` to pathname changes, but retains the pre-existing delayed hard-coded reply, raw FormData cast, and duplicated Realtime state. [c24587b2f8b30b27340c0f721ae2f4cf7270a495](https://github.com/nomadcoders/wemake/commit/c24587b2f8b30b27340c0f721ae2f4cf7270a495) introduces the recursive hard-coded bot trigger; [21ceb5d55c608772ed374a651eaf1639eaec6d5c](https://github.com/nomadcoders/wemake/commit/21ceb5d55c608772ed374a651eaf1639eaec6d5c) adds a recursion guard.

**Caveat.** These corrections are partial. SQL remains standalone/unmigrated with incomplete privilege handling, the bot identity remains hard-coded, and Realtime remains broadly filtered with stale/raw handling. Commit [6d58ab9afa611d77f1b5add657dfc370fb674529](https://github.com/nomadcoders/wemake/commit/6d58ab9afa611d77f1b5add657dfc370fb674529) is a narrow UI/revalidation correction; it neither introduces nor removes the pre-existing delayed reply and does not repair the larger messaging risks.

**Current conclusion.** Current guidance comes from Supabase/PostgreSQL docs: authorized narrow subscriptions with cleanup, no duplicated loader state, migration-tracked functions/views, safe `search_path`, least privileges, and atomic writes (`SUPA-005`, `DB-003`, `DB-005`).

## Evidence boundary

Wemake supplies audited historical evidence, not normative templates. Plate/Supaplate source, snippets, fixtures, templates, and builders are not included or inferred from this public history.
