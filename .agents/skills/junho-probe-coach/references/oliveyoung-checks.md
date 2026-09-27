# Olive Young domain checks

Load only when the challenge's own text names consumer retail, health & beauty, or beauty commerce.
Do not load it for manufacturing, semiconductor, industrial, or B2B-operations challenges: the generic
operations nouns used below — inventory, logistics, recommendation — occur there too and are not on
their own a reason to load this file.

## Cross-domain questions

- Who makes the operational or purchase decision?
- Which data is authoritative, delayed, inferred, or user-generated?
- What is the most expensive failure: stockout, overstock, delay, wrong recommendation, compliance issue, or lost conversion?
- Which recommendation may be automated, and which action requires approval?
- Does the result lead to a real next action or stop at text?

## Inventory and fulfillment

Distinguish:

- `on_hand`
- `reserved`
- `available_to_promise`
- safety stock
- stale or in-transit stock

Check:

- available-to-promise never becomes negative
- allocation never exceeds inventory or node capacity
- duplicate events and requests are idempotent
- stale inventory produces a warning or fallback
- order, inventory, and fulfillment state transitions are auditable
- simulation is not presented as an actual WMS/OMS mutation

Relevant trade-offs:

- stockout versus overstock
- delivery SLA versus fulfillment cost
- split shipment versus customer promise
- local availability versus network-wide optimization

## Recommendation and search

Separate:

- retrieval
- ranking
- grounding evidence
- availability filter
- explanation
- safety or compliance constraints

Check:

- unavailable products are filtered or explicitly handled
- product facts, ingredients, price, promotion, and inventory are grounded
- uncertain claims are not stated as facts
- recommendations include a next purchase or comparison action
- the system has a fallback when the model or retrieval fails

## UGC and discovery commerce

Distinguish:

- content engagement signal
- purchase-intent signal
- product-content match
- creator or content trust
- inventory-aware exposure

Check:

- views are not automatically treated as demand
- content-product mismatches can be reviewed or reversed
- cold-start products and popularity bias are acknowledged
- out-of-stock content has a substitution or suppression policy
- channel-specific assumptions are not generalized without evidence

## S&OP and demand signals

Treat forecasts as uncertain decisions, not facts. Record:

- signal source and freshness
- forecast horizon
- confidence or scenario range
- promotion and event effects
- lead time and capacity
- decision owner and approval

Prefer scenario comparison over unsupported accuracy claims:

```text
baseline
trend spike
supply delay
promotion uplift
```

Show the consequence of each scenario on stockout risk, inventory, SLA, or opportunity rather than inventing financial impact.
