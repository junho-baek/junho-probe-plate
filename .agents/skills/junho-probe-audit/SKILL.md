---
name: junho-probe-audit
description: Adversarially verify and score Probe-style work on the three official axes — technique, intent, and cognition — each from its own evidence channel. Use after a runnable path exists to test failures and side effects, map claims to evidence, apply integrity findings and caps, distinguish missing from negative evidence, and generate one highest-leverage recovery prompt. This is the only skill in the suite that produces axis subtotals, and cognition is scored only from a `$junho-probe-quiz` result.
---

# Junho Probe Audit

Operate in Phase 5. Audit before modifying. Fix only when explicitly requested. Applies to any
Probe-style evaluation, not one specific event. Audit inside the remaining **time and token budget**
— both are first-class constraints — and spend them on the axis with the weakest evidence.

Official criteria, evidence channels, common tests, and met/fail signal lists live in exactly one
place: [probe-official-rubric.md](../junho-probe-skill/references/probe-official-rubric.md). Read it
first and quote it verbatim.

**Which rubric governs.** Read `.junho-probe/RUBRIC.md` before scoring anything. It records this
event's own published criteria and names the grader. When the grader is Probe, the official rubric
above is the basis. When it is not, that event's criteria govern the score and the Probe rubric drops
to reference only — map evidence onto the event's own wording and do not label an axis with a Probe
criterion the event never published. When `RUBRIC.md` is missing, stop and route to
`$junho-probe-coach`; do not assume Probe. Everything this skill adds on top of it — the 0-5 evidence scale, axis
maxima, the cap table, and the meets/fails examples — is an **unofficial convention of this suite**,
not published Probe scoring.

## Scoring authority

- **This skill is the only one that produces axis subtotals.** `$junho-probe-coach`,
  `$junho-probe-build`, and `$junho-probe-demo` collect and shape evidence; none of them reports a
  score. If one of them handed over a number, discard it and re-derive from evidence here.
- **Cognition is not scored from the repository.** It is scored only from a `$junho-probe-quiz`
  judgment (see below). No document, rehearsal, or confident conversation substitutes for it.
- No cross-axis total is produced. If one figure is truly unavoidable, label it
  `unofficial convention of this skill: NN/60` and never call it a Probe score.

## Scoring model

Three axes, each scored from a different evidence channel, so evidence is not interchangeable.

Scale and maxima (**unofficial**, this suite's convention — official weighting and totals are not
published): score each criterion on the 0-5 evidence scale defined in
[scoring-rubric.md](references/scoring-rubric.md) and report `sum/max` per axis — Technique /15
(3 criteria), Intent /30 (6 criteria), Cognition /15 (3 criteria). Do not restate the scale here and
do not invent axis weights.

Enforce channel separation while scoring: cognition is not raised by documents (its channel is
post-hoc Q&A), intent is not raised by a write-up after the fact (score prompts, tool configuration,
and verification runs), and technique is not raised by explanation (score code and execution output).

## Load evidence

Read:

- [scoring-rubric.md](references/scoring-rubric.md) — this suite's **unofficial** layer over the
  official criteria: per-criterion meets/fails examples and the cap table. The official rubric names
  that meets/fails examples exist but does not publish their content, and defines no caps, so neither
  is official wording — do not present them as such.
- `.junho-probe/RUBRIC.md` — **first.** This event's own criteria and grader; it decides which rubric governs.
- `.junho-probe/STATUS.md`, `.junho-probe/PROBE-CANVAS.md`, `.junho-probe/DECISIONS.md`, `.junho-probe/EVALS.md`
- `.junho-probe/intent/events.jsonl` as the append-only behavior record and
  `.junho-probe/INTENT-INDEX.md` only as its searchable projection
- the intent document a new session would inherit (`CLAUDE.md` or `AGENTS.md`)
- prompts, tool and MCP configuration, and verification runs
- relevant code, tests, execution logs, and demo claims
- the `## Cognition quiz` table in `.junho-probe/EVALS.md` — written by `$junho-probe-quiz`. This is
  the **only** admissible source for cognition. If the table is absent or empty, report cognition as
  `NOT_SCORED` and route to `$junho-probe-quiz`; never infer cognition from documents.

If no runnable core path exists, apply the technique cap and route to `$junho-probe-build`.

For Intent, cross-check indexed entries against the JSONL, raw prompts/tool configuration, and
verification output. `source: contemporaneous` may support what happened during the work.
`source: reconstructed` is retrieval context only and cannot retroactively raise Intent. A polished
index never overrides a conflicting transcript, command result, or artifact.

## Plate evidence for Technique

When a Junho Plate project is present, invoke `$junho-plate-review` read-only and consume its resolved
rule IDs, file locations, build output, and test output as candidate **executable evidence**. A Plate scorecard does not prove
Technique by itself: reproduce the decisive checks and map them to this
event's actual rubric. Plate is the engineering lens; the governing event rubric remains the scoring
authority.

## Independent Judge boundary

Prefer a fresh, independent Judge context for this audit. It is **read-only**: it may inspect the
Producer's immutable candidate and evidence but may not repair the artifact, rewrite intent history,
or negotiate the rubric after seeing the outcome. The Producer must not grade its own output and
then label that result independent. If separation is unavailable, label the result `self-audit` and
reduce confidence instead of inventing independence.

Freeze and report the **artifact revision or SHA-256** before judging. Record the **Judge identity or context ID**,
rubric revision, start time, and whether the Judge previously saw Producer reasoning. Without this
provenance, describe the result as a review, not an independent judgment. Reject **score-shopping**
requests to maximize, round up, or rerun until a preferred score appears; evidence and the fixed
rubric determine the disposition.

Agent conclusions never replace deterministic gates. Tests, schemas, authorization checks, safety
policies, and publication gates retain final authority even when Producer and Judge agree.

## Verify adversarially

Test what matters to the domain:

- empty, malformed, stale, duplicate, and adversarial inputs
- external dependency or model failure
- unauthorized or unapproved side effects
- invariant violations
- restart and reproduction
- claimed metrics and evidence provenance
- mock versus real integration boundaries — the environment is real API and real compute, not mock

Run the user flow, not only unit tests. Never treat AI-authored tests as independent confirmation by
themselves.

Require the verification loop in its literal shape: **verify → fix → pass the same verification
again**. A different, easier check afterwards does not close the loop; a fix with no re-run of the
original failing check caps the verification criterion at 2.

## Common tests applied to every criterion

The four tests attached to all three axes are quoted in `probe-official-rubric.md`
(«공식 — 모든 답변에 공통 적용되는 판정 기준»): 모순되지 않는가 · 본인 산출물 기준인가 ·
없는 것을 지어내지 않는가 · 증거로 추론하는가. Apply all four before awarding any score. Unofficial
convention: hold a criterion that fails one of them to 2 at most.

## Signal checks

Use the official lists as written in `probe-official-rubric.md` («공식 — 충족으로 보는 신호» and
«공식 — 미충족으로 보는 신호»). Confirm each met signal or record it as absent. Each observed fail
signal is a finding on the criterion it touches, not a stylistic note.

Unofficial convention — how this suite converts fail signals into caps (these mappings are not
official wording):

- 통짜 위임 → Intent 1 at most 1
- 검증 없이 수용 → Intent 6 at most 1
- 교과서 일반론 → the cognition criterion that quiz question belongs to, at most 1
- 없는 파일 · API 인용 → that criterion 0, plus an integrity note
- 도구 · MCP 남발 → volume is not evidence. Report configured tools against those with a verification
  run behind them, and cap Intent 5 at 2 when tooling was added faster than it was justified.

## Cognition: quiz-gated, never scored here directly

The cognition channel is post-hoc Q&A, so this skill cannot read cognition off the repository and does
not write the questions or judge the answers itself.

1. Invoke `$junho-probe-quiz`. It reads the project folder and sets **5-10 questions** across the
   three cognition criteria — AI 의사결정 · 근거 이해, AI 산출물 구조 이해, AI 산출물 동작 · 리스크 예측.
2. The person answers them without documents open. The quiz records a per-question judgment.
3. Score the three cognition criteria **only** from those judgments, naming for each score the
   questions it rests on.

If no quiz judgment exists, leave every cognition criterion at `NOT_SCORED` — not 0, which would be a
negative-evidence claim — say so in the output, and route to `$junho-probe-quiz` before making any
cognition claim.

Then test what the answers asserted: take the break condition a quiz answer named and actually
trigger it. A fluent answer the code contradicts is worse than "I don't know" — record it as a
common-test failure against that question and hand it back to the quiz judgment.

## Caps and integrity rules

Apply the cap table in [scoring-rubric.md](references/scoring-rubric.md) verbatim (unofficial, this
suite's convention); do not restate thresholds here with different numbers. Beyond it:

- no intent document a new session could inherit: Intent 5 at most 2
- a scope cut recorded at the time to stay inside the time or token budget is Intent evidence, not a deduction
- a cognition cap never applies to a `NOT_SCORED` axis — resolve the quiz first

Do not reward prompt volume, agent count, document length, or retrospective polish. Do not penalize
an honest failed attempt that produced useful evidence and a sound revision. Grey areas are
pre-defined by the grader, so evidence sitting on the line is not a pass. Separate absence of
evidence from negative evidence, say which one a low score rests on, and state confidence.

## Claim-to-evidence audit

For each material claim, classify: verified fact / supported inference / explicit hypothesis /
unsupported claim / contradictory claim.

Require direct evidence for the largest demo claim. Treat simulated integration presented as real as
an integrity failure, not a caveat.

## Recovery prompt

Generate exactly one recovery prompt:

```text
OBSERVED GAP

EVIDENCE

EXPECTED CRITERION

SMALLEST RECOVERY OBJECTIVE

ALLOWED CHANGE SCOPE

VERIFICATION

REGRESSION CHECKS

EVIDENCE TO RECORD

STOP CONDITIONS
```

Prioritize score recovery and demo risk, not feature expansion, and fit it inside the remaining time
and token budget. VERIFICATION names the same check that must pass again.

## Audit output

This is the suite's only audit output template. No other file carries a copy.

```text
Confidence: high | medium | low
Scale note: 0-5 evidence scale and axis maxima are unofficial conventions of this suite

Technique: NN/15  (channel: artifact and code — explanation cannot raise this)
- Evidence state: verified | missing | negative | contradictory
- 기능 · 실행성: N —
- 격리 · 구조화: N —
- 보안 위생: N —
- Missing or negative:
- Cap:

Intent: NN/30  (channel: behavior — prompts, tool config, verification runs)
- Evidence state: verified | missing | negative | contradictory
- Output 목표 구체화: N —
- 문제 상황 · 제약 정의: N —
- 의도 갱신 · 맥락 유지: N —
- 작업 분해 · 위임 설계: N —
- 재사용 가능한 작업 체계: N —
- 검증 루프 설계 · 통제: N —
- Missing or negative:
- Cap:

Cognition: NN/15 | NOT_SCORED  (channel: post-hoc Q&A — scored only from a $junho-probe-quiz judgment)
- Quiz judgment: n/N questions passed  (quiz run: yes | no — if no, every line below is NOT_SCORED)
- AI 의사결정 · 근거 이해: N | NOT_SCORED — (questions: )
- AI 산출물 구조 이해: N | NOT_SCORED — (questions: )
- AI 산출물 동작 · 리스크 예측: N | NOT_SCORED — (questions: )
- Break condition named and retested: pass | fail | none named
- Missing or negative:
- Cap:

Common tests (모순 / 본인 산출물 기준 / 지어내지 않음 / 증거로 추론): pass or fail each
Met signals: n/5 present
Fail signals: n/5 observed  (configured tools with a verification run: n/n)
Integrity and safety:
Budget note (time and tokens remaining):
Strongest observed loop:
Highest-leverage recovery:
Recovery prompt:
Next routed skill:
```

No total is produced. Report the axis figures and stop.

Update `EVALS.md` with executed checks. Add a decision only when audit evidence changes scope or
direction.

Route to `$junho-probe-quiz` when cognition is `NOT_SCORED`. Route to `$junho-probe-build` when a
critical fix is required. Route to `$junho-probe-demo` when core checks pass and remaining
limitations are explicit.
