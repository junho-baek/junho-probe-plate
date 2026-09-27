---
name: junho-probe-skill
description: Route Probe-style AI-native evaluation work through the Junho Probe skill suite while preserving evidence and phase gates. Use as the primary entry point when starting or resuming a challenge, recording the event's own scoring rubric, checking the current phase, initializing the .junho-probe workspace and the root intent document, deciding whether to invoke coach, build, audit, quiz, or demo, or compressing the workflow as time or token budget runs out.
---

# Junho Probe Router

Route work through this loop:

> intent -> bounded delegation -> observable result -> verification -> revised decision

Do not solve the child phase inside this router.

This suite targets AI-native evaluation in general, not one event. Anything specific to a single event — its domain, dataset, deliverable list, judges, or schedule — belongs in a scoped reference or in shared state, never in these routing rules. Name no event here.

## The rubric is a branch, not a constant

Phase gates and evidence discipline hold for every event. **Scoring criteria do not.** Establish them in Phase 0 and record them in `.junho-probe/RUBRIC.md`:

- the criteria **quoted verbatim** from the event's own published material
- the **source URL**, or the exact document handed to participants
- the **date checked**
- **who scores, from which channel** — automated process, human judges, or both

Then branch:

| Scorer | Scoring authority | Status of `references/probe-official-rubric.md` |
| --- | --- | --- |
| Probe (getcofa.com) | the official Probe rubric, copied into `RUBRIC.md` as its basis | authoritative — quote its 「공식」 sections verbatim |
| any other event | that event's own criteria, as recorded in `RUBRIC.md` | reference only — a lens for preparation, never cited as a criterion |

If an event publishes no rubric, write that fact into `RUBRIC.md` and mark every criterion you work from as an assumption. Never present this suite's axes, scales, or subtotals as an event's official criteria.

## Three axes and evidence channels

This frame is the Probe rubric's. Use it as the scoring structure only when Probe scores; otherwise map the event's own criteria in `RUBRIC.md` and keep these axes as a preparation lens.

| Axis | Scored from |
| --- | --- |
| Technique (기술 관리) | artifacts and code |
| Intent (의도 관리) | behavior — automatically collected prompts, tool configuration, verification runs |
| Cognition (인지 관리) | post-hoc Q&A |

Channels do not substitute for one another: cognition cannot be covered by documents, intent cannot be covered by a written retrospective, technique cannot be covered by explanation.

There are **three** axes. "Communication management" is not one of them — requirement discovery and stakeholder ambiguity are scored under Intent criterion 2 (problem situation and constraints).

Scoring mechanics — the 0-5 evidence scale, per-axis maxima, caps, penalties — are **this suite's own unofficial conventions**, not published rubric text. Official weights and totals are unpublished. Only `$junho-probe-audit` applies these conventions; this router does not score and does not restate them.

Read `references/probe-official-rubric.md` before quoting any criterion, and never paraphrase official wording as if it were official.

## Initialize shared state

Run the initializer at the start of every challenge — including in a directory that already holds a
`.junho-probe/`. It never overwrites, and it is the only thing that detects a stale workspace left by
an earlier event: it warns loudly, lists every file it kept, and signals a mismatch between the
recorded event and `--event`. Skipping it because `STATUS.md` already exists is exactly how an old
event's state gets inherited in silence.

```bash
python3 <skill-dir>/scripts/init_probe_workspace.py \
  --root <workspace-root> \
  --task-title "<exact task title>"
```

Shared state in `.junho-probe/`:

- `RUBRIC.md`: the event's own criteria verbatim, source URL, date checked, who scores from which channel
- `STATUS.md`: current phase, gate, next action, blockers — plus the per-event constraints every child skill reads: **remaining time**, **remaining token budget**, the event's **submission checklist**, and the event's **demo or presentation length**
- `PROBE-CANVAS.md`: problem, constraints, assumptions, selected slice
- `DECISIONS.md`: material decisions and rejected alternatives
- `EVALS.md`: criteria, execution results, claim-to-evidence map
- `DEMO.md`: reproducible demo and defense
- `INTENT-INDEX.md`: searchable material behavior index; original prompt, normalized Korean intent, English retrieval gloss, done condition, verification, result, evidence, and supersedes links

The init script fills all six templates, `RUBRIC.md` included, and does not overwrite existing files. Filling `RUBRIC.md` with this event's own published criteria is yours to do in Phase 0. Every per-event number — time budget, token budget, demo length, submission items — lives in `STATUS.md` or `RUBRIC.md`; no skill hardcodes it.

Separate from those files, maintain an **intent document at the repository root** — `CLAUDE.md`, or `AGENTS.md` when that is what the toolchain reads. The init script does not create it: create it in Phase 0 and update it whenever intent, constraints, or verification commands change. It is a first-class deliverable, because a new session must be able to take over from it alone. Keep in it the goal and done condition, constraints and non-goals, how to run and verify, the current slice, and open unknowns.

Keep entries concise and contemporaneous. Mark reconstructed history explicitly.

## Index intent as behavior, not retrospective decoration

For each material prompt, harness or skill change, tool choice, verification, or revised decision, pipe one JSON object to:

```bash
python3 <skill-dir>/scripts/record_intent_event.py --root <workspace-root>
```

The event preserves the redacted **original prompt**, a **normalized Korean intent**, an **English retrieval gloss**, the done condition, literal verification, result, evidence, and any event it `supersedes`. The canonical append-only record is `.junho-probe/intent/events.jsonl`; `INTENT-INDEX.md` is its searchable Markdown view.

Use `source: contemporaneous` only when recording the behavior in the same work turn. Use `source: reconstructed` for history recovered later. A reconstructed entry can improve retrieval and cognition preparation but **cannot retroactively raise Intent**. Never rewrite an existing event ID; append a new event and link it through `supersedes`. Redact secrets and personal data before persistence.

Record material transitions, not every conversational sentence. An event is material when it changes objective, constraints, scope, delegation, tool/harness selection, done condition, verification, acceptance, or the next prompt.

Invocation examples for each axis and the full loop live in `references/command-examples.md`.

## Preserve universal integrity

These hold whoever scores. When Probe scores, the first two lists are also official rubric text; check them in every child skill.

Official common judgment criteria — they apply to all three axes. The English below is a reading
gloss; the official wording is Korean in `references/probe-official-rubric.md`. Quote from there,
never from this gloss:

1. Does not contradict the actual submission.
2. Grounded in your own artifacts, not in generalities.
3. Invents nothing that does not exist.
4. Reasons from evidence, not authority.

Official unmet signals — treat each as a blocking defect, not a style note. Gloss again; the Korean
original in `references/probe-official-rubric.md` is what you quote:

1. Wholesale delegation of the kind "just build something good".
2. Accepting an AI completion report without verification.
3. Answers filled with textbook generalities.
4. Explanations citing files or APIs that do not exist.
5. Signal blurred by tool and MCP sprawl.

Suite conventions (not official rubric text):

- Preserve original nouns, numbers, units, and qualifiers when restating a claim.
- Claim no integration, performance, accuracy, or impact without evidence for it.
- Cite commands, tests, diffs, logs, screenshots, responses, or file paths.
- Add a tool or MCP server only when it produces evidence a child skill actually consumes; remove the rest before scoring.
- Separate fact, inference, assumption, and unknown.
- Record concise rationale, not private chain-of-thought, and one rejected alternative per material decision.
- Close every verification loop as verify -> fix -> **re-pass the same verification**.
- Require one happy path and one meaningful failure path.
- Freeze features before sacrificing verification or reproducibility.

## Determine the current phase

Read `STATUS.md`, then verify its claim against the shared artifacts. First confirm that its task title and `RUBRIC.md` describe the event you are actually in — state left behind by an earlier event is worse than no state, so reset it rather than inherit it. Do not advance because a document merely says `PASS`.

| Phase | Gate | Route |
| ---: | --- | --- |
| 0 | exact problem, rules, constraints, unknowns preserved; `RUBRIC.md` written with source and date | `$junho-probe-coach` |
| 1 | concrete user, moment, loss, metric defined | `$junho-probe-coach` |
| 2 | one opportunity selected and alternatives rejected | `$junho-probe-coach` |
| 3 | thin slice, invariants, boundaries, tests defined | `$junho-probe-coach` |
| 4 | one bounded build task at a time | `$junho-probe-build` |
| 5 | adversarial verification; axis subtotals from evidence | `$junho-probe-audit` |
| 5 (cognition) | cognition scored by a quiz generated from the project folder, then answered | `$junho-probe-quiz` |
| 6 | reproducible demo and public defense | `$junho-probe-demo` |

Cognition is the one axis this suite cannot score from artifacts, so it is scored the way it is actually examined: as a quiz. Route cognition scoring to `$junho-probe-quiz`, which reads the project folder and sets 5-10 questions to answer under Q&A conditions.

If the routed skill is available, read its `SKILL.md` completely and follow it. The suite is installed as sibling directories:

- `../junho-probe-coach/SKILL.md`
- `../junho-probe-build/SKILL.md`
- `../junho-probe-audit/SKILL.md`
- `../junho-probe-quiz/SKILL.md`
- `../junho-probe-demo/SKILL.md`

If it is unavailable, emit the exact `$skill-name` invocation and stop.

## Enforce transitions

Do not enter Phase 4 unless Phase 1-3 artifacts confirm:

- concrete user and target decision
- meaning and unit of critical metrics
- available data/API contracts
- selected thin slice
- critical invariants and non-goals
- acceptance and failure criteria
- a root intent document a new session could resume from

Do not enter Phase 5 until at least one end-to-end path runs.

Do not enter Phase 6 until claims are mapped to direct evidence and critical failures are either fixed or disclosed.

If a gate fails, keep the current phase and route a recovery task to the same skill.

## Route by explicit request

Respect an explicit child skill unless its entry gate is unsupported.

- "문제를 해석해", "아이디어 골라", "프롬프트 짜줘" -> coach
- "구현해", "다음 작업 실행해" -> build, only after Phase 3
- "검증해", "채점해", "감점 요소 찾아" -> audit
- "퀴즈", "예상 질문 뽑아", "Q&A 준비", "인지 점검" -> quiz, only once the project folder holds readable work
- "발표", "데모", "토론 준비" -> demo, only after audit evidence

When refusing a premature route, name the missing evidence and route the smallest recovery prompt.

## Emergency routing

Time and token budget are both first-class constraints; the tighter of the two decides. Read both from `STATUS.md`.

- Less than 25% of remaining time **or** token budget: route to audit, freeze features, preserve the smallest working path.
- Less than 10% of either: route to demo unless the core path cannot run.
- Core path broken: route one recovery task to build, then return to audit.

## Router output

Emit:

```text
Current phase:
Gate status: PASS | FAIL | BLOCKED
Scoring authority (from RUBRIC.md):
Evidence inspected:
Budget left (time / tokens):
Routed skill:
Reason:
Exact next invocation:
```

Then continue with the child skill only if its instructions have been loaded. Do not duplicate the child skill's full output in the routing preface.
