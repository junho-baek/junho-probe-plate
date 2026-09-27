---
name: junho-probe-build
description: Generate or execute one bounded implementation task in Phase 4 of a Probe-style evaluation. Use for thin vertical-slice coding, scoped AI delegation, targeted tests, changed-file inspection, isolation and secret-leak checks, re-running the same verification after a fix, and contemporaneous intent-document, decision, and eval updates without expanding scope. The event's own rubric in `.junho-probe/RUBRIC.md` governs, and axis subtotals come from the audit skill, not from here.
---

# Junho Probe Build

Operate only in Phase 4. Execute one bounded task at a time.

## Which rubric governs, and this phase's channel

`.junho-probe/RUBRIC.md` is this event's authority — read it first. When it names Probe as the grader its basis is [probe-official-rubric.md](../junho-probe-skill/references/probe-official-rubric.md) and the channels below apply. When it names any other grader, that event's criteria govern and the Probe material here is a method reference for evidence discipline only.

- **Technique** (code and artifacts): all three criteria are decided here — 기능 · 실행성, 격리 · 구조화, 보안 위생. Prose cannot compensate.
- **Intent** (behavior, collected automatically): criteria 3 (의도 갱신 · 맥락 유지) and 6 (검증 루프 설계 · 통제) are decided here, by real prompts, tool settings, and verification traces. A later write-up cannot compensate.
- **Cognition** (사후 Q&A): not produced here and **not compensable by documents**. Implement only what you can later explain — structure, why, and where it breaks; `$junho-probe-quiz` sets the questions.

This skill assigns no score. Axis subtotals — and the 0-5 evidence scale and caps behind them, which are this suite's own unofficial convention, not official Probe wording — come from `$junho-probe-audit` only.

## Preflight

Read:

- `.junho-probe/STATUS.md`
- `.junho-probe/PROBE-CANVAS.md`
- `.junho-probe/DECISIONS.md`
- `.junho-probe/EVALS.md`
- the intent document (`CLAUDE.md` or `AGENTS.md`) and current worktree state

Require Phase 3 evidence:

- user and decision
- selected thin slice
- data/API contract
- code-enforced invariants
- AI and approval boundaries
- one happy and one failure criterion
- no more than three ordered build tasks

If missing, stop and route to `$junho-probe-coach`. Never invent the missing contract.

If an intent document that a fresh session could resume from does not exist, create the minimal one before the first task: goal, constraints, boundaries, verification commands, current state. Official satisfied-signal: 새 세션이 이어받을 수 있는 의도 문서 (CLAUDE.md).

## Choose behavior

- If asked for a prompt, emit one implementation prompt and do not edit code.
- If asked to implement, perform the task, verify it, and update evidence.
- If a previous task failed, reproduce before changing code and generate one recovery task.

## Bounded task contract

Each task must contain:

```text
OBJECTIVE
one observable outcome

ALLOWED SCOPE
exact files or component boundary

KNOWN CONTRACT
confirmed inputs, outputs, invariants, and dependencies

NON-GOALS
explicitly excluded work

REQUESTED CHANGE
small ordered actions

ACCEPTANCE CRITERIA
binary checks, including isolation/structure and security-hygiene checks

VERIFICATION
exact commands and user-flow checks, named literally so the same ones can be re-run

EVIDENCE
what to record in DECISIONS.md, EVALS.md, and the intent document

STOP CONDITIONS
missing authority, data, dependency, or unexpected scope
```

Do not include another phase or multiple independent features.

## Execute safely

1. Inspect relevant files and existing conventions.
2. Preserve unrelated user changes.
3. Implement the smallest vertical change.
4. Add the smallest decisive tests.
5. Inspect changed files.
6. Run specified verification.
7. Compare actual results with acceptance criteria.
8. Accept, revise, or reject the AI-produced result.
9. Update evidence before claiming completion.

Prohibited — official unmet-signals, verbatim (English after the dash is a gloss, not a quotation):

- '알아서 잘 만들어줘'식의 **통짜 위임** — wholesale delegation
- AI의 완료 보고를 **검증 없이 수용** — accepting a completion report unverified
- **도구 · MCP 남발**로 흐려진 신호 — tool and MCP sprawl

Conventions for staying clear of them (this skill's, not official wording):

- every delegation carries objective, scope, contract, and acceptance criteria
- only an executed verification with its output counts; “implemented successfully”, a green summary, or a diff that looks right does not
- add no tool, MCP server, agent, or framework this task's acceptance criteria do not require; extra tooling dilutes the behavior signal Intent is read from, so use the smallest tool that produces the evidence

Do not launch parallel work against shared state or integration-ordered tasks.

## Agent-runtime contract

For an agentic feature on Cloudflare Workers, prefer the **Cloudflare Agents SDK** when the work
needs durable agent identity or state, live connections, scheduling, or server-side tool execution.
Use Workflows for durable multi-step execution, retries, and approval pauses. Do not force this
runtime onto a static, local-only, or otherwise incompatible task; record why the smaller runtime
is sufficient.

When several agents generate or verify work, separate their authority:

1. A **Producer** receives a bounded contract and writes one candidate inside its owned scope.
2. The candidate and its evidence become **immutable** input to a read-only **Judge**.
3. The Judge must not grade its own output, modify the candidate, share hidden mutable state with
   the Producer, or replace executable verification with an opinion.
4. A **deterministic** policy or test gate remains the final authority for safety, schema,
   authorization, and publication. Agent agreement is supporting evidence, never the gate.
5. If candidates can run independently, isolate their state and file ownership before parallel
   execution. Keep integration-ordered work sequential.

Record the selected runtime, rejected alternative, ownership boundary, Judge rubric, and literal
verification command as contemporaneous intent events. If no independent Judge is warranted,
record that choice instead of adding ceremonial multi-agent complexity.

## Verification minimum

Require:

- actual end-to-end path when the task completes the slice
- one relevant failure or boundary case
- domain invariants cannot be bypassed
- approval and side-effect boundaries remain intact
- exact commands and exit status recorded
- mock and real integration boundaries labeled

### Re-pass the same verification

When a verification fails: fix the cause, then **re-run the identical command or check that failed and record that it now passes**. Log the failing run and the passing run of the same verification, in order.

Switching to a different, easier, or narrower verification after a failure does not count as a pass. Neither does declaring it fixed without a re-run. A pass recorded against a verification other than the one that failed is a FAIL.

### Security hygiene (official criterion 보안 위생; the checks below are this skill's)

Check on every task and record the result even when nothing changed. A leak found here is a task FAIL, not a follow-up.

- no secrets, keys, tokens, or credentials in source, config, tests, or fixtures; real values stay in the environment or an ignored `.env`, and ignore rules actually exclude the files that exist
- no secrets or personal data in **logs**, including debug prints and request/response dumps
- no secrets, raw payloads, or stack internals in **error messages** returned to a user or client
- untrusted input is not interpolated into commands, queries, or file paths

### Isolation and structure (official criterion 격리 · 구조화; the checks below are this skill's)

Acceptance criteria must include:

- the change stays inside ALLOWED SCOPE; no unrelated file is edited
- one responsibility per module; domain logic is not embedded in UI, route handlers, or scripts
- external calls, side effects, and approval gates sit behind named boundaries a test can substitute
- dependency direction is one-way, with no new cycle and no duplicated logic left unjustified

## Evidence update

Append to `EVALS.md`:

- criterion
- verification method
- PASS, FAIL, or BLOCKED
- command, log, response, screenshot, or file evidence
- for a fixed failure: the failing run and the passing re-run of the same verification
- follow-up

Append to `DECISIONS.md` for material choices:

- observation
- decision
- rejected alternative
- evidence
- remaining risk
- next gate

Update the **intent document** (`CLAUDE.md` or `AGENTS.md`) whenever new information, a failure, or a rejected result changes what a fresh session would need to know: revised constraint, new boundary, the verification command that is now authoritative, a known-broken path. Update `STATUS.md` with the current task, gate state, and next action. Both belong in the same turn as the discovery — Intent criterion 3 is scored from when they happened.

Record each material implementation prompt, harness or skill choice, failed verification, revised decision, and accepted result through `../junho-probe-skill/scripts/record_intent_event.py`. Include the original text, normalized Korean intent, English retrieval gloss, done condition, literal verification, result/evidence, and the event it supersedes. Record it in the same turn as `source: contemporaneous`; later reconstruction cannot create historical Intent evidence.

Before claiming anything, apply the official common judgment criteria (verbatim) to every line written:

- 실제 제출물과 **모순되지 않는가** — no contradiction with the submitted artifact
- 일반론이 아닌 **본인 산출물 기준**인가 — specific to your own artifact
- **없는 것을 지어내지 않는가** — no invented file, command, API, or result
- 권위가 아닌 **증거로 추론하는가** — inferred from evidence, not from what a tool asserted

## Result report

```text
Result: PASS | FAIL | BLOCKED
Changed:
Verified (command + re-passed same check):
Security hygiene:
Isolation/structure:
Evidence:
Rejected or revised:
Intent doc / STATUS updated:
Remaining risk:
Next task or routed skill:
```

If all Phase 4 acceptance criteria pass, route to `$junho-probe-audit`. If verification fails, remain in Phase 4 and issue one recovery task.

## Time and token budget compression

Time and token budget are both first-class constraints — official Probe work happens 시간과 토큰 budget 안에서. Track both; compress when either runs short. The event’s actual numbers live in `.junho-probe/STATUS.md`, never here.

Token discipline, every task:

- read only what ALLOWED SCOPE names; prefer targeted search over whole-file dumps and re-reads
- cite evidence by path, line range, and command instead of pasting long logs into evidence files
- do not buy convenience with extra tools, MCP servers, or agents; they cost tokens and blur the signal

Unofficial (this skill's convention), applied to whichever budget is scarcer:

- two failed attempts on the same task: stop, record the failure and the reproduction in `EVALS.md`, update the intent document, issue one recovery task
- less than 25% remaining: reject new features; finish the smallest working path
- less than 10% remaining: change code only if the core demo cannot run; otherwise route to audit or demo
