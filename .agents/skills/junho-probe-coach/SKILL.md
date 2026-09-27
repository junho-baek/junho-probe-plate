---
name: junho-probe-coach
description: Analyze a raw Probe-style challenge and generate one bounded, evidence-driven prompt for Phases 0-3. Use for intake under time and token budgets, capturing this event's own scoring rubric, submission checklist, and demo format, resolving ambiguity, defining intent and metrics, scoring opportunities, designing a thin end-to-end slice, and emitting prompt packets mapped to the intent-management criteria with evidence, without writing product code or axis scores.
---

# Junho Probe Coach

Operate only in Phases 0-3. Generate the smallest prompt that passes the current gate. Do not write product code.
Event-independent: use for any AI-native evaluation, Probe-scored or not.

## The rubric is a branch, not a constant

Which criteria apply depends on the event. Phase 0 records *this* event's scoring criteria into
`.junho-probe/RUBRIC.md`, with verbatim quotation, source, and date confirmed.

- **Event scored by Probe** — `.junho-probe/RUBRIC.md` cites
  [probe-official-rubric.md](../junho-probe-skill/references/probe-official-rubric.md) as its source, and
  the three-axis channel model below applies.
- **Event scored by anything else** (organizer's own published criteria) — `.junho-probe/RUBRIC.md` quotes
  those criteria and governs. The Probe rubric then serves only as a method reference for evidence
  discipline, never as the scoring authority.

## Scoring channel — applies when the event is scored by Probe

Official Probe axes are three, each scored from a different channel: technique from code and outputs,
intent from behavior, cognition from post-hoc Q&A. This skill owns **intent**, read from behavior —
the automatically collected prompts, tool settings, and verification traces.

- The prompt you emit *is* the evidence; a retrospective write-up cannot add intent score.
- Cognition cannot be supplemented by documents; it is explained aloud in Q&A.
- Technique cannot be supplemented by narration; code and run results are the evidence.

For the six official intent criteria this skill reports **met / not met plus the evidence that shows it**,
and nothing numeric. Axis subtotals are produced by `$junho-probe-audit` only. The 0-5 evidence scale and
axis subtotals that audit uses are *unofficial* — this suite's own convention; official axis weights and
totals are unpublished, so never invent them. "Communication management" is not an official axis:
requirement discovery and stakeholder ambiguity are scored as official intent criterion 2, and the
remainder is an optional lens carrying no score. Anything here not quoted from the rubric is unofficial.
Do not present it as official, and do not reword official text.

When `.junho-probe/RUBRIC.md` records a non-Probe rubric, map this skill's output to that rubric's own
criteria instead; the evidence discipline above is unchanged.

## Never (official Probe unmet signals)

English gloss for reading speed. The official wording is Korean in
`../junho-probe-skill/references/probe-official-rubric.md` — quote it from there, not from here.

- Wholesale delegation of the kind "just build something good".
- Accepting the AI's completion report without verification.
- Textbook generalities in place of this challenge's own artifacts.
- Citing a file or API that does not exist.
- Tool and MCP sprawl.

Convention, not official text: because intent is read from behavior, any server, tool, or skill call this
gate does not require muddies that signal. Add none by default; if one is required, state why the gate
needs it.

## Load shared state

Read, when present: `.junho-probe/RUBRIC.md` (this event's criteria — read it before any other state),
`.junho-probe/STATUS.md`, `.junho-probe/PROBE-CANVAS.md`, `.junho-probe/DECISIONS.md`,
the intent document a fresh session would resume from (`CLAUDE.md` or `AGENTS.md`), the exact problem and
rules, and provided API/data documentation.

If the shared workspace is absent, invoke `$junho-probe-skill` or run the sibling router's initializer.

Domain reference, not rubric: load [oliveyoung-checks.md](references/oliveyoung-checks.md) **only when the
challenge's own source text names consumer retail, H&B, or beauty commerce.** Do not load it for
manufacturing, semiconductor, industrial, or B2B-operations challenges. When the source text names neither,
skip it.

## Apply the evidence boundary

- Put only quoted requirements and inspected artifacts under known facts.
- Preserve numbers, units, nouns, and qualifiers.
- Keep assumptions and unknowns separate.
- Do not infer fields, APIs, baselines, or business impact.
- Reason from evidence, not from authority or convention.
- Ask for clarification only when ambiguity changes the solution or creates unsafe claims.

Treat these as blocking:

- duration could mean build time, SLA, freshness, timeout, or forecast horizon
- quantity lacks unit or grain
- recommend, allocate, reserve, and execute are mixed
- inventory semantics or freshness are unknown
- capacity lacks resource and time window
- KPI lacks baseline, measurement window, or observable proxy

## Select the phase

### Phase 0: Intake

Produce:

- exact source problem
- explicit rules and provided resources
- repository and runnable command observations
- **time budget** remaining and **token budget** remaining, both as stated numbers
- **`.junho-probe/RUBRIC.md` — this event's scoring criteria.** Verbatim quotation of the criteria text,
  the source (URL or document name), and the date confirmed. If the event is scored by Probe, cite the
  sibling rubric and say so; otherwise quote the organizer's own published criteria, which then govern.
  If nothing is published, write "not published", plus what you looked at and when — never invent axes,
  weights, or totals.
- **submission checklist.** Every required deliverable, its format, its deadline, and its submission
  channel, each quoted verbatim from the event rules. Mark anything the rules leave unstated as unstated.
- **demo / presentation format and length limit**, quoted from the rules — medium, whether live or
  recorded, and the stated time limit. If unstated, record "unstated" and the length you will assume.
- fact, assumption, unknown, and blocking-question lists

Gate:

- source text preserved
- critical units and verbs resolved or explicitly blocked
- build constraints and expected deliverable known
- time budget and token budget both recorded, and planned scope fits inside both
- `.junho-probe/RUBRIC.md` exists, quotes its criteria verbatim, and names source and confirmation date
- submission checklist recorded: every deliverable with format, deadline, and channel
- demo format and length limit recorded, or explicitly marked unstated with the assumed length

### Phase 1: Intent

Define:

```text
[user] in [situation] tries to [target behavior], but [root cause]
causes [user/business loss].
```

Also define:

- one primary user
- one business beneficiary or decision-maker
- current workflow in 5-7 steps
- one largest disconnect
- target metric and measurement plan
- constraints, assumptions, unknowns, and non-goals

Ask "why?" up to three times. Classify root cause as information, judgment, process, connection, or motivation.

Write or update the intent document (`CLAUDE.md` or `AGENTS.md`) so a session with no history can resume:
goal, done-state, constraints, non-goals, verification commands, current phase. Re-update it whenever new
information or a failure changes the intent — that is the evidence for intent criteria 3 and 5.

Gate:

- concrete moment and loss named
- root cause contains no solution language
- metric is observable or labeled as a hypothesis
- intent document exists and matches the current intent

### Phase 2: Opportunity

Generate at most three options. Score 1-5:

- impact
- frequency
- demo provability
- implementation feasibility
- differentiation without a generic chatbot

List fatal constraints separately; totals cannot override them. Select one decisive moment and record
rejected alternatives with the reason for rejection.

Gate:

- exactly one opportunity selected
- choice fits available data, time budget, and token budget
- a before/after fits the demo length recorded in Phase 0
- rejected alternatives and reasons recorded

### Phase 3: Thin-slice design

Define:

```text
input -> interpretation/decision -> result -> user action -> business value
```

Specify:

- one happy path
- one meaningful failure path
- code-enforced invariants
- AI judgment boundary
- human approval boundary
- data/API trust boundary
- at most three vertical build tasks
- binary acceptance test and evidence target for every task
- per task, the named verification that closes the loop: run the verification, fix the failure, then
  **re-pass the same verification**, keeping both runs as evidence

Gate:

- real input reaches an observable output
- AI cannot bypass critical invariants
- no task depends on invented data or API behavior
- every task names the verification it must re-pass after a fix
- build sequence is ready for `$junho-probe-build`

## Prompt packet

Emit one ready-to-copy prompt:

```text
MODE AND PHASE

OBJECTIVE

KNOWN FACTS

ASSUMPTIONS AND UNKNOWNS

CONSTRAINTS

NON-GOALS

INPUTS TO INSPECT

REQUESTED ACTION

OUTPUT CONTRACT

ACCEPTANCE CRITERIA

VERIFICATION

EVIDENCE TO RECORD

STOP CONDITIONS
```

The packet carries the intent evidence. Under a Probe-scored event, each official intent criterion is met
by named slots; under a non-Probe rubric, map the same slots onto that rubric's criteria.

| Official intent criterion | Satisfied by |
| --- | --- |
| 1. Output goal concretized (done-state) | `OUTPUT CONTRACT` + binary `ACCEPTANCE CRITERIA` |
| 2. Problem situation and constraints defined (no guessing) | `KNOWN FACTS`, `CONSTRAINTS` (incl. time budget, token budget, submission deadline, demo length), `NON-GOALS`, `ASSUMPTIONS AND UNKNOWNS` |
| 3. Intent update and context maintenance | intent document + `PROBE-CANVAS.md` / `DECISIONS.md` / `STATUS.md`, re-emitted when a failure changes the plan |
| 4. Task decomposition and delegation design | `MODE AND PHASE` (one phase) + `REQUESTED ACTION` scoped to one of Phase 3's at most three vertical tasks |
| 5. Reusable work system | `CLAUDE.md` or `AGENTS.md` a fresh session resumes from, plus this packet template |
| 6. Verification loop design and control | `VERIFICATION` (named command, re-passed after the fix) + `EVIDENCE TO RECORD` + `STOP CONDITIONS` |

An empty slot is a missing intent criterion, not a stylistic gap. Report each criterion as met / not met
with the evidence; emit no score — axis subtotals come from `$junho-probe-audit` alone.

Lint before emitting:

- every known fact has an exact source
- no number or unit changed meaning
- assumptions are not requirements
- criteria do not require unavailable fields or APIs
- nothing contradicts the actual submission
- every criterion is stated against this challenge's own artifacts, not general practice
- nothing non-existent is invented: no unobserved file, API, field, or baseline
- every inference rests on cited evidence, not authority
- no tool or MCP server is requested that this gate does not need
- a shorter clarification prompt would not be safer
- only one phase is included

Default to at most 1,200 words. Exceed only for an explicitly exhaustive or safety-critical request.

After the prompt, add only:

- `Why this prompt now`: at most three bullets
- `Gate to advance`: one sentence
- `Evidence expected`: at most three items, each naming the criterion in `.junho-probe/RUBRIC.md` it feeds
  (no score)

## Update shared state

When executing analysis rather than only generating a prompt:

- update `PROBE-CANVAS.md`
- append material choices and rejected alternatives to `DECISIONS.md`
- update Phase and gate in `STATUS.md`
- keep the intent document (`CLAUDE.md` or `AGENTS.md`) current
- keep `.junho-probe/RUBRIC.md` current when the organizer publishes a clarification, re-quoting verbatim
  and updating the confirmation date
- do not mark a gate PASS without cited evidence
- record the emitted material prompt or changed harness/skill with `../junho-probe-skill/scripts/record_intent_event.py`; preserve its original text, normalized Korean intent, English retrieval gloss, done condition, literal verification, result/evidence, and any prior event it supersedes

When Phase 3 passes, set next skill to `$junho-probe-build`.
