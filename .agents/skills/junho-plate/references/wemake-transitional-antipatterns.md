# Junho Plate Wemake Transitional Antipatterns

This register prevents course sequencing and historical risk from becoming Junho Plate advice. It is pinned to Wemake `21ceb5d55c608772ed374a651eaf1639eaec6d5c`. A `teaching-transition` or `legacy-risk` is not a current recommendation, even when a later commit keeps part of it.

## How to read this register

- **Introduction** identifies the first audited commit or chain that exposes the temporary/risky state.
- **Correction** identifies a later full or partial change when one exists.
- **Current disposition** states what Junho Plate should do now. No correction means the current contract and official docs control.
- “Partial” is deliberate: it credits only the named issue and does not promote the surrounding implementation.

## Deliberate delay register

| Pattern | Introduction | Correction | Current disposition |
|---|---|---|---|
| **deliberate delay** in SSR/deferred lesson | [cc8309573fa3c202fefeacede5f54019f65f9caa](https://github.com/nomadcoders/wemake/commit/cc8309573fa3c202fefeacede5f54019f65f9caa) adds a long loader delay; [874adeb6b1dc31c78d4654569abc003d3dc3937e](https://github.com/nomadcoders/wemake/commit/874adeb6b1dc31c78d4654569abc003d3dc3937e) shifts delay into query/deferred teaching paths | [5a98ef76c289ac8fc8052d9f2454d53e9c3baaab](https://github.com/nomadcoders/wemake/commit/5a98ef76c289ac8fc8052d9f2454d53e9c3baaab) disables the lesson delays while introducing a separate empty client-loader transition | Never preserve artificial latency in production. Test pending behavior deterministically. |
| Delayed raw login action | [b4025d60d9e1859b5f6b0278846e4c73b0c282a6](https://github.com/nomadcoders/wemake/commit/b4025d60d9e1859b5f6b0278846e4c73b0c282a6) adds delay, raw FormData, and a fake branch | [0eff204384cfa735eaa3325b6b5b94230301e9af](https://github.com/nomadcoders/wemake/commit/0eff204384cfa735eaa3325b6b5b94230301e9af) removes the delay and validates auth actions; partial because other auth-side-effect choices remain | Use action pending state; do not simulate latency in application code. |
| Delayed optimistic mutation | [a1befc3516d1bebaf2071971bef8d51485e245bf](https://github.com/nomadcoders/wemake/commit/a1befc3516d1bebaf2071971bef8d51485e245bf) adds a real optimistic toggle with an artificial delay and unvalidated input | [d13c78798176354cea7a00ec69a145b5c15417dc](https://github.com/nomadcoders/wemake/commit/d13c78798176354cea7a00ec69a145b5c15417dc) removes the delay in a broad `legacy-risk` integration; validation, atomicity, and failure mapping remain unresolved | Treat the removal as partial only; apply current validation and mutation rules. |

[6d58ab9afa611d77f1b5add657dfc370fb674529](https://github.com/nomadcoders/wemake/commit/6d58ab9afa611d77f1b5add657dfc370fb674529) removes stale timestamp text and narrows pathname revalidation, so its `correction` classification is limited to those observed changes. It retains rather than introduces the pre-existing delayed hard-coded reply, and it is not a correction for that delay or the larger messaging risks.

## Debug logging register

| Pattern | Introduction | Correction | Current disposition |
|---|---|---|---|
| Loader **debug logging** and untyped demo data | [27b4717b8257a2f61c1ca17458c3996c182cf35f](https://github.com/nomadcoders/wemake/commit/27b4717b8257a2f61c1ca17458c3996c182cf35f) | [c14569ea751224d0f6cf0f4cc64efe49613482f2](https://github.com/nomadcoders/wemake/commit/c14569ea751224d0f6cf0f4cc64efe49613482f2) fixes only typing; [c9b8baec70fa8939a9c064be37db6022c940d75b](https://github.com/nomadcoders/wemake/commit/c9b8baec70fa8939a9c064be37db6022c940d75b) removes the demo/log path | Use structured server reporting for real failures; remove lesson logs. |
| Fetcher log and fake success | [4169ccfec4a752b672d88115cad4db27c0d41180](https://github.com/nomadcoders/wemake/commit/4169ccfec4a752b672d88115cad4db27c0d41180), then [ccd8ec5edb517dc0e61cb5c9c110ab1dabc821f5](https://github.com/nomadcoders/wemake/commit/ccd8ec5edb517dc0e61cb5c9c110ab1dabc821f5) | [a1befc3516d1bebaf2071971bef8d51485e245bf](https://github.com/nomadcoders/wemake/commit/a1befc3516d1bebaf2071971bef8d51485e245bf) replaces the fake step with a real mutation, but remains delayed/unvalidated | Never cite the first two as an action result contract; the third still needs current safeguards. |

## Empty client loader

**Introduction.** [5a98ef76c289ac8fc8052d9f2454d53e9c3baaab](https://github.com/nomadcoders/wemake/commit/5a98ef76c289ac8fc8052d9f2454d53e9c3baaab) adds an empty client loader to an analytics route while removing the earlier deferred lesson.

**Correction.** [1583d3724b064506fb7fc7e8e5b31acaf7b642cb](https://github.com/nomadcoders/wemake/commit/1583d3724b064506fb7fc7e8e5b31acaf7b642cb) removes that client loader. The correction is behaviorally useful for this narrow issue but the commit is `legacy-risk` because it also depends on an untracked view without `security_invoker` evidence.

**Current disposition.** Do not add `clientLoader` without a browser-only or explicit hydration responsibility. Removing an empty hook does not validate unrelated database choices.

## Pre-validation assertion register

| Pattern | Introduction | Correction | Current disposition |
|---|---|---|---|
| Screen non-null **pre-validation assertion** over query data | [67d3b45a935dc1b3f92aa96117f0cd24f6462ab7](https://github.com/nomadcoders/wemake/commit/67d3b45a935dc1b3f92aa96117f0cd24f6462ab7) | [9068f40f7ee0a98066e2ea08acd661536cb2d0f0](https://github.com/nomadcoders/wemake/commit/9068f40f7ee0a98066e2ea08acd661536cb2d0f0) removes assertions through a type overlay; partial/static only | Validate/map runtime data and separately repair view migration/security. |
| Raw message FormData cast | [70224a3e386ef06b28a0fc28d2490b64fa2cb708](https://github.com/nomadcoders/wemake/commit/70224a3e386ef06b28a0fc28d2490b64fa2cb708) | No audited correction at the pinned head | Parse with Zod before application/database use; do not inherit the cast. |
| Optimistic route input trusted before parsing | [a1befc3516d1bebaf2071971bef8d51485e245bf](https://github.com/nomadcoders/wemake/commit/a1befc3516d1bebaf2071971bef8d51485e245bf) | Delay is later removed, but validation has no clean correction | The optimistic UI does not authorize or validate the mutation. |

## Later correction chains

| Incomplete implementation | Introduction | Later correction | Completeness |
|---|---|---|---|
| Reply mutation without complete interaction | [5034ee6cd1700da4fe979f936c69acf284f4fb91](https://github.com/nomadcoders/wemake/commit/5034ee6cd1700da4fe979f936c69acf284f4fb91) | [9821875b81b37db6b0793371cec6891ad0ced095](https://github.com/nomadcoders/wemake/commit/9821875b81b37db6b0793371cec6891ad0ced095) | Complete for the stated reply-flow scope. |
| Fake/raw auth action | [b4025d60d9e1859b5f6b0278846e4c73b0c282a6](https://github.com/nomadcoders/wemake/commit/b4025d60d9e1859b5f6b0278846e4c73b0c282a6) | [0eff204384cfa735eaa3325b6b5b94230301e9af](https://github.com/nomadcoders/wemake/commit/0eff204384cfa735eaa3325b6b5b94230301e9af) | Complete for validated login/signup action; partial for the broader auth feature because logout remains side-effecting loader/GET behavior. |
| Singleton Supabase client chain | [594f62ec2d6c14387a689027be8f5b5bf0f67338](https://github.com/nomadcoders/wemake/commit/594f62ec2d6c14387a689027be8f5b5bf0f67338) | [0acd28f36d82fb9542f36bf577873e759d77ec8a](https://github.com/nomadcoders/wemake/commit/0acd28f36d82fb9542f36bf577873e759d77ec8a) | Partial: request scoping improves, but ordinary cookie-header propagation and database security remain incomplete. |
| Fake nested loaders and empty action | [b669fde2192fbc54880d24c19dac0d9e8b6bebfe](https://github.com/nomadcoders/wemake/commit/b669fde2192fbc54880d24c19dac0d9e8b6bebfe) | No single clean correction; later queries/reviews resolve pieces | Never use the transitional route as a complete exemplar. |
| Unsafe recursive bot trigger | [c24587b2f8b30b27340c0f721ae2f4cf7270a495](https://github.com/nomadcoders/wemake/commit/c24587b2f8b30b27340c0f721ae2f4cf7270a495) | [21ceb5d55c608772ed374a651eaf1639eaec6d5c](https://github.com/nomadcoders/wemake/commit/21ceb5d55c608772ed374a651eaf1639eaec6d5c) | Partial: recursion guard only; migration, privileges, hard-coded identity, and broad revalidation remain. |

## Legacy pattern register

- **Standalone functions and triggers.** [9d47cced558de6ee96e170aef703dc94e9967cb6](https://github.com/nomadcoders/wemake/commit/9d47cced558de6ee96e170aef703dc94e9967cb6), [4e5a4462194077b46c9b57407a1eb495e6956085](https://github.com/nomadcoders/wemake/commit/4e5a4462194077b46c9b57407a1eb495e6956085), [d810dfe7153af1fec9a11fdeedac85a11036ce12](https://github.com/nomadcoders/wemake/commit/d810dfe7153af1fec9a11fdeedac85a11036ce12), and [d99414c7984e5aa992402c351acf9b118eea2449](https://github.com/nomadcoders/wemake/commit/d99414c7984e5aa992402c351acf9b118eea2449) lack complete migration, safe search-path, or privilege evidence. [3e23c51baff7b984c48d2c665cedbcc6e79fd88f](https://github.com/nomadcoders/wemake/commit/3e23c51baff7b984c48d2c665cedbcc6e79fd88f) corrects relation qualification only.
- **Standalone views.** [67d3b45a935dc1b3f92aa96117f0cd24f6462ab7](https://github.com/nomadcoders/wemake/commit/67d3b45a935dc1b3f92aa96117f0cd24f6462ab7) and related view history are counterexamples where generated types do not establish migration tracking or `security_invoker`.
- **RLS without policy evidence.** [0a47c0a69e9e0d9cfead7483145f56c1ea4c0e02](https://github.com/nomadcoders/wemake/commit/0a47c0a69e9e0d9cfead7483145f56c1ea4c0e02) changes only a settings-page path. It cannot support a current RLS claim.
- **Non-atomic room creation.** [09e731982f319eedc61e9708f113813831aea6ce](https://github.com/nomadcoders/wemake/commit/09e731982f319eedc61e9708f113813831aea6ce) separates related writes and uses insecurely evidenced standalone function SQL.
- **Realtime duplication.** [b568063272e4032a0529b3c2c9c2cd1079f145de](https://github.com/nomadcoders/wemake/commit/b568063272e4032a0529b3c2c9c2cd1079f145de) copies loader data, subscribes broadly with stale/raw handling, and suppresses revalidation despite having cleanup.
- **Privileged side-effecting loader.** [a0d678874d1de875a6a89456c2b4221522a81ee6](https://github.com/nomadcoders/wemake/commit/a0d678874d1de875a6a89456c2b4221522a81ee6) combines remote effect, admin authority, loader/GET semantics, and missing consent/auth/audit boundaries.
- **Payment confirmation variants.** [287411fe3fe9ba96ba398ef4f644d5f0534233e0](https://github.com/nomadcoders/wemake/commit/287411fe3fe9ba96ba398ef4f644d5f0534233e0) and [ae7a5dfdb2a88b3d88994dc570e6831ee617b3ac](https://github.com/nomadcoders/wemake/commit/ae7a5dfdb2a88b3d88994dc570e6831ee617b3ac) remain sibling legacy-risk branches with side-effecting loader, trusted query data, and embedded-secret risk. Neither is a correction of the other.

## Current rule

Use Wemake to understand why a responsibility moved and where a risk appeared. Use the approved Junho Plate contract, security/data integrity, installed-version official docs, and current database policy to decide what to implement. Teaching history never overrides those sources.
