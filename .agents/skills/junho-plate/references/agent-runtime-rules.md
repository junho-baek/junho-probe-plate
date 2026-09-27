# Junho Plate Agent Runtime Rules

This guide covers `AGENT-001` and `AGENT-002`. It is a default profile for agentic product work, not permission to install infrastructure that the task or environment does not support.

## AGENT-001: Cloudflare agent runtime by default

When Cloudflare Workers and the Agents SDK are supported by task constraints and installed capabilities, prefer:

- `Agent` for durable identity, state, connections, and real-time interaction;
- Cloudflare Workflows for retryable multi-step work, long-running jobs, and approval waits;
- sub-agents or agents-as-tools for independently owned parallel agent state;
- a narrow runtime adapter when the event or deployment target requires another provider.

Do not replace a compatible existing Agents SDK boundary with an ad-hoc in-process loop. Also do not force Cloudflare into an incompatible web IDE, prohibited network environment, or time-boxed task merely to satisfy this preference.

## AGENT-002: independent judge evidence boundary

Use multiple agents only when independent perspectives create material evidence. Separate roles:

| Role | May do | Must not do |
|---|---|---|
| Producer | create a bounded candidate and attach evidence | approve its own output from confidence |
| Judge | read immutable candidate artifacts, criteria, traces, and test results | silently mutate the candidate under review |
| Repairer | apply an accepted, bounded finding | broaden scope without authority |
| Deterministic gate | run tests, schemas, policies, and build checks | be replaced by an LLM verdict |

Preserve disagreement and judge rationale as evidence. A Judge result is advisory where deterministic verification exists. One producer plus deterministic checks is better than ornamental multi-agent complexity.

For durable orchestration, let a Workflow own step order, retries, and approvals. For short interactive work, an Agent may coordinate tools or sub-agents directly. Keep agent state and candidate artifacts addressable so the Judge evaluates the same result that may later ship.

## Official documentation evidence

| Product | Version or access date | Direct official URL | Supported Rule IDs |
|---|---|---|---|
| Cloudflare Agents SDK | Accessed 2026-09-27 | [Agents](https://developers.cloudflare.com/agents/) | AGENT-001 |
| Cloudflare Agents SDK | Accessed 2026-09-27 | [Using Agents with Workflows](https://developers.cloudflare.com/agents/concepts/workflows/) | AGENT-001, AGENT-002 |
| Cloudflare Agents SDK | Accessed 2026-09-27 | [Sub-agents](https://developers.cloudflare.com/agents/runtime/execution/sub-agents/) | AGENT-002 |

