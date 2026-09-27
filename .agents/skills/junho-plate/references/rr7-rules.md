# Junho Plate React Router 7 Rules

This guide applies `RR7-001` through `RR7-006` and the router-facing parts of `ERR-001`, `SEC-002`, and `UI-005`. The audited Plate baseline uses React Router 7.5.1 in Framework Mode. Prefer its native protocol over recreating a client data framework inside React.

## Ownership map

| Concern | Default owner | Guardrail |
|---|---|---|
| Server reads | `loader` | Load before render, return the smallest serializable route contract, and let RR7 revalidate it (`RR7-001`). |
| Server mutations | `action` | Authenticate, authorize, parse, execute, and return/throw an intentional response (`RR7-002`, `RR7-004`). |
| Navigating submission | `Form` | Use when the URL or history should represent the new context. Read pending state from navigation. |
| Non-navigating work | `fetcher` | Use when the user stays in context. Read result and pending state from that fetcher. |
| Route signatures | generated `Route types` | Use route-generated loader, action, component, error, params, and data contracts (`RR7-003`). |
| Shareable filters and paging | URL search params | The URL owns committed search, sort, filter, tab, and page state (`RR7-006`). |
| Parent-route shared data | layout data | A layout loader, typed matches, or outlet context owns data shared down the route tree. |
| Navigation progress | `useNavigation` | Do not create a parallel global loading boolean. |
| Local submission progress | `fetcher.state` | Keep independent work local to its fetcher. |
| Expected HTTP outcome | status response | Return or throw a meaningful status with a safe payload. |
| Unexpected route failure | `ErrorBoundary` | Let the closest route boundary render the failure and keep server logging separate (`RR7-005`). |

## Nested parent, layout route, and Outlet admission

Treat route-tree structure as an ownership decision, not a file-shortening technique. React Router uses `<Outlet />` as the replacement seam where the active child route renders inside a matched parent. Distinguish these shapes before registering routes:

| Need | Use | Do not use |
|---|---|---|
| Arrange one screen's sections, columns, or purchase panel | Screen composition and ordinary presentation components | A route layout created only to reduce line count |
| Reuse a visual frame outside one route branch, with no route-owned data or boundary | An ordinary `Layout` component with explicit props/children | Outlet context as a generic component API |
| Keep a path-bearing parent shell while its index, reviews, curriculum, or purchase child changes | A nested parent route that renders `<Outlet />` | Manual pathname branching that imports and switches every child screen |
| Share a shell, loader data, pending/error boundary, or cohesive route-local context without adding a URL segment | A pathless React Router layout route that renders `<Outlet />` | A fake URL segment or a wrapper route with no stable parent responsibility |
| Group child URLs under a common path but render no parent UI and own no parent data | A route prefix | An empty layout component |

Admit an Outlet-bearing parent only when a parent responsibility remains stable while actual child route modules change. Meaningful child URLs, a shared shell, parent-owned data, or a route-level pending/error boundary are valid reasons. A long screen, one JSX wrapper, or a hypothetical future child is not enough by itself (`ARCH-004`, `UI-004`).

For example, model a skill detail family as a parent `/skills/:slug` route with an index child plus `reviews`, `curriculum`, and `purchase` children when those are real navigable screens. Let the parent render the product shell, tabs, and `<Outlet />`; let the matched child own only its screen-specific content. If those sections are not distinct URLs or route lifecycles, keep them as components inside one screen.

Keep data ownership proportional:

- Let the parent loader read only data required across the route family, such as the stable product identity and shell projection. Let each child loader/action own child-specific reads, mutations, validation, and status mapping.
- Read parent loader data through the installed release's typed route data or match API. Use typed outlet context only for a cohesive route-local UI value or callback that genuinely belongs to the parent-child relationship.
- Do not copy loader data into outlet context, turn outlet context into a broad service locator, or move every descendant query into the parent loader. Those choices couple unrelated children and broaden revalidation.
- Let `<Outlet />` identify the child replacement point. Do not inspect the pathname in the parent to choose imported child screens when nested route registration can express the same URL contract.
- A parent auth loader may establish identity, redirect, or shared shell data. It does not replace resource-level authorization inside each protected child loader/action (`RR7-004`).

Do not issue a `FAIL` merely because a feature has no layout route. Report a violation only when direct evidence meets an existing rule, such as duplicated shared loader work (`RR7-001`), manual route-protocol branching inside a screen (`UI-004`), or a protected child action without server authorization (`RR7-004`). Otherwise, a justified route-tree improvement is at most a contextual `WARN`.

## Loader and SSR rules

A route's required server data belongs in its loader. Under SSR, authentication and protected reads execute at the server boundary before the screen renders. Client navigation still uses the RR7 data protocol; it is not a reason for effect-based fetch.

Keep loaders adapter-sized: interpret request params and URL search params, validate the trust boundary, obtain server identity, authorize access, call an application or infrastructure operation, then map its outcome. Put reusable queries and business policy behind the route rather than embedding long vendor-specific work in the module.

Use a `clientLoader` only for an actual browser-only source, an explicit hydration strategy, or another documented client-data reason. An empty client loader, a second copy of server data, or a loader that exists only to introduce delay has no production ownership.

## Action, Form, and fetcher rules

An action is the server mutation boundary even when the UI submits imperatively. Parse untrusted FormData once, authenticate and authorize on the server, invoke the operation, and convert expected outcomes to action data, status, or redirect.

Choose `Form` when completion changes navigation context or should create a browser-history entry. Choose `fetcher` for background or in-place work such as toggling a row, loading a popover, or submitting one list item without changing the URL. The choice is about navigation intent, not personal style.

Do not watch action data in an effect to launch another request. The action should complete the server operation, return a composed result, redirect, or expose a next user decision. RR7 automatically revalidates affected loader data after actions; do not build an action-result watcher effect to reproduce that protocol.

### Remote and destructive effects

`SEC-003` is a Junho Plate safety contract, not a claim derived from the Form-versus-fetcher documentation. External sends, purchases, deletes, privileged changes, and irreversible actions require explicit informed consent immediately before execution, unless a documented server automation has pre-approved scope, authorization, and an audit trail. A loader must not trigger such work merely because a page was read. The route action verifies consent or automation authority on the server before invoking the effect.

## Generated types and route state

Generate and consume the route's `Route.LoaderArgs`, `Route.ActionArgs`, `Route.ComponentProps`, and `Route.ErrorBoundaryProps` equivalents available to the installed release. Application input and domain types remain framework-independent; generated types stop at the route adapter.

Committed navigation state belongs to RR7. Read params and URL search params directly; read loader data and layout data from generated component props or the appropriate route match. `useState` is only for ephemeral UI such as an open panel, temporary focus, an uncommitted draft, or local selection. `useEffect` is only for external synchronization such as a DOM API, browser API, timer, analytics system, third-party widget, or subscription with cleanup.

## Pending, status, and errors

Use `useNavigation` for page-level navigation/submission pending states and a fetcher's own state for independent background work. Pending UI must correspond to the actual navigation or form action so unrelated controls do not appear busy.

Distinguish normal empty data, an expected domain failure, a recoverable external failure, and an unexpected system failure. Empty data renders a normal empty screen. Expected failures become typed action data or a status response. A missing protected resource normally produces an appropriate status. Unexpected failures reach the nearest `ErrorBoundary` and server-side reporting; do not turn them into an empty array or fake success.

## Server authentication

Client UI may hide controls for convenience, but it is never the authorization boundary. Every protected loader and action verifies server identity and resource permission before the protected read or mutation. RLS is defense in depth, not a substitute for route-level intent checks, and client-only auth cannot protect server data.

## Explicit anti-pattern table

| Anti-pattern | Failure it creates | Replacement |
|---|---|---|
| **effect-based fetch** | Required route data arrives after render, creates race/cleanup work, and bypasses RR7 revalidation | Move the server read to a loader; retain effects only for an external system. |
| **action-result watcher** effects | A mutation becomes a render-triggered request chain and can repeat or drift from navigation | Finish the operation in the action or expose a deliberate next user event. |
| **duplicated loader state** | Local state becomes stale after revalidation and needs manual synchronization | Render from loader data; keep only an explicit ephemeral draft locally. |
| **client-only auth** | A caller can bypass UI checks and invoke the protected server path | Authenticate and authorize in each protected loader/action and enforce database policy. |

## Lightweight exceptions

- A browser-only API may use a client loader or effect when the reason and hydration behavior are explicit.
- A local draft may begin from loader data while editing, but it must have an explicit commit/cancel lifecycle and must not masquerade as canonical server state.
- An imperative `fetcher.submit` is acceptable when a native form cannot express the interaction, but the server work still belongs to an action.
- Do not add a use case, repository, class, or wrapper solely because a route has a loader or action. Add one only when it isolates policy, vendor mapping, reuse, or an external failure boundary.

## Official documentation evidence

| Product | Version or access date | Direct official URL | Supported Rule IDs |
|---|---|---|---|
| React Router | Accessed 2026-08-04; installed app is 7.5.1 | [Route Module](https://reactrouter.com/start/framework/route-module) | RR7-001, RR7-004, UI-004 |
| React Router | Accessed 2026-08-05; installed app is 7.5.1 | [Framework Routing](https://reactrouter.com/start/framework/routing) | RR7-001, ARCH-004, UI-004 |
| React Router | Accessed 2026-08-05; v7 API | [Outlet API](https://api.reactrouter.com/v7/functions/react-router.Outlet.html) | ARCH-004, UI-004 |
| React Router | Installed 7.5.1 | [Route Module Type Safety](https://reactrouter.com/7.5.1/how-to/route-module-type-safety) | RR7-003 |
| React Router | Accessed 2026-08-04 | [Form vs. fetcher](https://reactrouter.com/explanation/form-vs-fetcher) | RR7-002 |
| React Router | Installed 7.5.1 | [Pending UI](https://reactrouter.com/7.5.1/start/framework/pending-ui) | RR7-006, UI-005 |
| React Router | Accessed 2026-08-04; installed app is 7.5.1 | [Error Boundaries](https://reactrouter.com/how-to/error-boundary) | RR7-005, ERR-001, ERR-003 |
| React Router | Accessed 2026-08-04; installed app is 7.5.1 | [Status Codes](https://reactrouter.com/how-to/status) | RR7-005 |
| React | Accessed 2026-08-04 | [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) | RR7-006, UI-005 |
