# Junho Plate Component and Presentation Rules

This guide covers `UI-001` through `UI-007` and the presentation side of the architecture contract. It separates route protocol, screen composition, reusable component APIs, feature exports, renderer parity, and stylesheet ownership without turning file counts or prop counts into design laws.

## Responsibility table

| Boundary | Owns | Must not own |
|---|---|---|
| **route** | RR7 loader/action protocol, generated Route types, trust-boundary parsing, server auth/authorization, redirects, status, and data adaptation | Long vendor queries, domain policy, or reusable presentation details |
| **screen** | Presentation composition of layout, components, loader/action outcomes, pending, empty, and expected-error UI | Repository calls, Supabase/Drizzle clients, domain decisions, or large transport transforms |
| **component** | Rendering and user intent through explicit UI props, events, Form, or fetcher interactions | Route authentication, persistence, raw database joins, or hidden global protocol state |
| **index** | Explicit public API re-exports for the feature | Logic, side effects, environment reads, client creation, wildcard leakage, or mixed server/client exports |

The screen only owns presentation composition. The index only owns the public API. A route may be visually small while still owning a critical adapter boundary; a component may be visually large while remaining cohesive.

## Screen layout versus route layout

Use **screen composition** for the visual arrangement of one route. Use an ordinary reusable **Layout component** when the same frame is a presentation API with explicit props or children. Use a React Router **nested parent or pathless layout route with `<Outlet />`** only when the route tree owns a stable shell, shared route data/boundary, or cohesive parent-child context while matched child screens change.

Do not add a route layout merely because a screen is long. Extract cohesive presentation components first. Conversely, do not keep several real child routes inside one screen through pathname conditionals just to avoid an Outlet-bearing parent. Apply the admission table in `rr7-rules.md`, then keep the screen at the active route level focused on presentation composition (`ARCH-004`, `UI-004`).

## UI-001: component definitions are stable modules

Define reusable or stateful components at module scope. A component declared inside another component receives a new identity as the parent renders, hides reuse and test seams, and makes ownership harder to see. Small render helpers that are plain functions and carry no component identity may remain local when they improve clarity.

Do not split every JSX fragment into a component. Extract when the unit has a reusable visual contract, independent interaction/state, a meaningful name, or a separate reason to change.

## UI-002: explicit props and cohesive view models

Prefer props named for UI meaning rather than vendor response structure. Map a raw Supabase join or loader transport object before it becomes the component API. A cohesive view model is allowed when several fields represent one presentation concept and change together.

Avoid vague `data`, `config`, or `options` bags that mix unrelated responsibilities. A view model is not permission to expose every database column; it is a deliberate screen-to-component contract.

Let the screen prepare the correct presentation contract for the current item and state. Let the component render it. Any value that can vary by product, route, permission, release state, or selected option belongs in semantic props or a cohesive named view model rather than a product-specific literal hidden inside a reusable component.

| Varying concern | Screen/view-model value | Component responsibility |
|---|---|---|
| Description or release message | Final display copy or an explicit message model | Render the supplied copy. |
| Badge appearance | `{ label, variant: "sale" | "default" }` | Map the semantic variant to CSS classes. |
| Pricing and CTA | `{ kind, current, previous, cta: { label, to } }` | Render price and link without parsing localized labels. |
| Versions or tabs | `{ id, label, status, selected, disabled }[]` | Render interaction state without treating array index as meaning. |
| Artwork treatment | `artTone: "forest" | "neutral"` | Map the semantic tone to Tailwind classes inside presentation. |

Do not infer domain or interaction meaning from display strings such as `discount === "무료"` or `children.includes("%")`. Do not make `index === 0` mean selected when selection is real state. Do not import a persistence row or broad data record as a reusable component's public props merely because its fields are convenient. The screen may consume route/application data, select the fields the UI needs, and construct `ProductSummaryViewModel` or another presentation-specific contract.

Stable component-owned chrome, such as a label that truly never varies across items or routes, may remain local. A component may also map semantic presentation variants to CSS. The failure is hidden item-specific content or policy, not every JSX literal.

Prop count is only a smell, not a metric gate. Many coherent props can be clearer than one opaque bag, and a component with few props can still mix unrelated behavior. Review coupling, naming, cohesion, and change reasons; never fail a component because it crosses an arbitrary number.

## UI-003: index as public API

An `index.ts` explicitly re-exports the narrow feature API another feature may consume. It contains no computation or initialization, does not read environment variables, and never constructs a browser, server, or admin client. Avoid wildcard exports because they turn new internal files into accidental public API.

Keep server-only exports on an explicitly server-only path. A client-reachable index must not re-export `.server` implementations, admin clients, database connections, or values that cause server modules to load.

## UI-004: screen composition

A screen receives route-owned data and composes layout and components. It renders success, pending, empty, and expected failure states and wires user intent to RR7 Form/fetcher primitives. It may derive a cohesive view model for presentation.

A screen does not query Supabase or Drizzle, decide domain policy, authorize the caller, or perform a mutation in an effect. Move vendor mapping to infrastructure, policy to domain/application, and request/status handling to the route.

## UI-005: state ownership

Use `useState` for ephemeral UI only: open/closed controls, focus, temporary selection, an uncommitted input draft, or a local interaction that does not need to survive navigation or sharing.

Use `useEffect` for external synchronization only: DOM/browser APIs, timers, analytics, third-party widgets, or subscriptions with cleanup. Do not use an effect to copy props, calculate render data, watch action results, fetch loader-owned server data, or reproduce RR7 pending state.

URL search params own shareable filters, sorting, tabs, and pagination. Loader data owns server results. `useNavigation` and fetcher state own pending. Layout loaders/matches/outlet context own route-tree data. Derive render values during render when possible.

## UI-006: preview and customer renderer parity

An Admin preview exists to show what the customer will receive. Feed both surfaces the same validated published view model and render it through one component registry or shared rendering core. Admin controls, diagnostics, and navigation may wrap that core, but they must not duplicate the component-selection or content-transformation switch.

Verify parity with at least one representative fixture that exercises conditional sections and semantic variants. Compare semantic output rather than browser-specific wrapper markup. A duplicated renderer is a `FAIL` when the two paths can drift independently.

## UI-007: stylesheet ownership and scoping

Every reachable stylesheet needs an owner. Prefer CSS Modules, an explicit feature namespace, a Web Component or Shadow boundary, or one canonical shared global definition. Generic global classes owned independently by Admin and Customer can collide after bundling even when each screen looks correct alone.

Intentional resets, design tokens, and utilities may remain global when they have one documented definition. Search source and built CSS for duplicate reachable selectors, then render the affected surfaces together when collision risk is real.

## Review signals

| Signal | Review question | Outcome rule |
|---|---|---|
| Many props | Do they form one UI concept, or several change reasons? | A smell for review, never a numeric FAIL. |
| Large screen | Is it still composition, or does it contain policy/query/transformation work? | Fail only for the mixed responsibility, not size. |
| Generic prop bag | Does the child understand database/vendor shape? | Replace with explicit props or a cohesive view model. |
| Local state from loader data | Is it a time-bounded edit draft with commit/cancel? | Otherwise render loader data directly. |
| Effect after action | Is it synchronizing a genuine external system? | Otherwise move work to the event/action flow. |
| Feature import | Does it enter through the explicit public API? | Internal cross-feature paths violate the boundary. |

## Plate structural observation

At pinned Plate commit `8449384cdfad30f20337bad6536b0c7d46a3dde5`, `app/routes.ts`, feature `screens`, feature/core `components`, and server/API/query paths are distinct path categories. This is structure-only evidence. It does not prove that every existing file follows the Junho Plate responsibility rules, and it supplies no source text or template.

## Official documentation evidence

| Product | Version or access date | Direct official URL | Supported Rule IDs |
|---|---|---|---|
| React | Accessed 2026-08-04 | [Your First Component](https://react.dev/learn/your-first-component) | UI-001 |
| React | Accessed 2026-08-04 | [Passing Props to a Component](https://react.dev/learn/passing-props-to-a-component) | UI-002 |
| TypeScript | Accessed 2026-08-04 | [Modules Reference](https://www.typescriptlang.org/docs/handbook/modules/reference.html) | UI-003, TS-003 |
| React Router | Accessed 2026-08-04; installed app is 7.5.1 | [Route Module](https://reactrouter.com/start/framework/route-module) | UI-004, RR7-001, RR7-004 |
| React Router | Accessed 2026-08-05; installed app is 7.5.1 | [Framework Routing](https://reactrouter.com/start/framework/routing) | UI-004, ARCH-004 |
| React Router | Accessed 2026-08-05; v7 API | [Outlet API](https://api.reactrouter.com/v7/functions/react-router.Outlet.html) | UI-004, ARCH-004 |
| React | Accessed 2026-08-04 | [Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects) | UI-005 |
| React | Accessed 2026-08-04 | [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) | UI-005, RR7-006 |
| React Router | Installed 7.5.1 | [Pending UI](https://reactrouter.com/7.5.1/start/framework/pending-ui) | UI-005, RR7-006 |
| Vite | Accessed 2026-09-27 | [CSS Modules](https://vite.dev/guide/features.html#css-modules) | UI-007 |
