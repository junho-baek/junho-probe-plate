# Probe scoring rubric — this suite's scoring conventions

**Authority**: [probe-official-rubric.md](../../junho-probe-skill/references/probe-official-rubric.md)
(from <https://www.getcofa.com/ko/probe>, checked 2026-09-27) is the single source of truth for official wording.

**What this file is**: the numeric and judgment layer this suite adds on top of that document.
Official axis weights, totals, and the contents of the official meets/fails examples are **unpublished**.
Everything below that is not a verbatim official quote is labeled
`Unofficial — this suite's own convention. Official weights, totals, and example contents are unpublished.`
Never present any figure or example from this file as an official Probe standard.

**Scope**: applies when the grader is Probe. For an event with its own published criteria, score against that
event's criteria instead; this file is not a universal scoring authority.

Do **not** restate here what the authority document already contains. Read it there:

| Already in the authority document — read it there | Section |
| --- | --- |
| The three axes, their definitions, and their evidence channels | 공식 — 세 축과 평가 근거 채널 |
| The 3 / 6 / 3 criteria and their official wording | 공식 — 세부 rubric |
| The four common tests applied to every criterion | 공식 — 모든 답변에 공통 적용되는 판정 기준 |
| The five met signals and the five fail signals | 공식 — 충족으로 보는 신호 / 공식 — 미충족으로 보는 신호 |
| The evaluation frame (real API, real compute, time **and** token budget) | 공식 — 평가 환경과 절차 |

There are **three** axes. There is no fourth axis.

---

## Unofficial — evidence scale, 0-5

> Unofficial — this suite's own convention. Official weights, totals, and example contents are unpublished.

| Score | Evidence level |
| ---: | --- |
| 0 | No behavior, contradictory behavior, or material integrity problem |
| 1 | Claimed in prose only |
| 2 | Defined in a prompt, plan, or document |
| 3 | Demonstrated by code, execution, or an observable artifact |
| 4 | Demonstrated on happy and failure/boundary paths |
| 5 | Evidence exposed a problem and caused a justified revision |

Do not infer a 3-5 from polished prose. Require observable evidence.

## Unofficial — axis maxima

> Unofficial — this suite's own convention. Official weights, totals, and example contents are unpublished.

| Axis | Criteria | Max under the 0-5 scale |
| --- | ---: | ---: |
| 기술 관리 / Technique | 3 | 15 |
| 의도 관리 / Intent | 6 | 30 |
| 인지 관리 / Cognition | 3 | 15 |

Report `sum/max` per axis and stop. Never synthesize a 100-point total. If a single figure is unavoidable,
label it `unofficial convention of this skill: NN/60` and never call it a Probe score.

**Axis subtotals are produced by `$junho-probe-audit` only.** No other skill in this suite reports a score.

---

# Unofficial readings of the official criteria

Each block below quotes the official criterion verbatim, then gives this suite's own meets/fails reading.

> Unofficial — this suite's own convention. Official weights, totals, and example contents are unpublished.
> The official rubric states that meets/fails examples exist per criterion; their **contents are not published**.
> The readings below are this suite's inventions, not reconstructions of the official examples.

## 기술 관리 / Technique — channel: artifact and code

1. **기능 · 실행성** — 실제 환경에서 깨끗하게 돌아가는가

*Unofficial reading:*
- Meets: the user flow was executed end to end against the real dependency, with output captured.
- Fails: it builds but the core path was never run, or it only ran against a mock stand-in for the real API.

2. **격리 · 구조화** — 유지 · 확장 가능한 구조로 만들었는가

*Unofficial reading:*
- Meets: boundaries are separated so one concern can change alone; non-deterministic AI judgment is isolated from deterministic enforcement.
- Fails: one undifferentiated file or function where domain rules, I/O, prompts, and secrets are interleaved.

3. **보안 위생** — 시크릿 · 민감정보가 코드 · 로그로 새지 않는가

*Unofficial reading:*
- Meets: credentials come from the environment, are absent from the repo and the transcript, and logs redact sensitive fields.
- Fails: a key pasted into source, a prompt, or a committed config; or a log line printing personal data.

## 의도 관리 / Intent — channel: behavior (prompts, tool config, verification runs, files written at the time)

1. **Output 목표 구체화** — AI에게 맡긴 일이 어떤 상태가 되면 끝나는지를 정의하는가

*Unofficial reading:*
- Meets: the prompt states completion conditions and acceptance criteria that can be checked.
- Fails: whole-cloth delegation with no stated end state.

2. **문제 상황 · 제약 정의** — AI가 추측하지 않도록 맥락과 경계를 제공하는가

*Unofficial reading:*
- Requirements work — who decides, who is affected, which ambiguity was surfaced and closed, which non-goals,
  assumptions, and input/output contracts were stated — is scored **here**, not as a separate axis.
- Meets: an ambiguity was raised as an open question and then closed with a recorded decision; constraints and non-goals appear in the prompt before the code.
- Fails: an unknown silently assumed, or a goal restated with no constraint, data contract, or boundary.

3. **의도 갱신 · 맥락 유지** — 새 정보와 실패가 생겼을 때 지시와 기록을 갱신하는가

*Unofficial reading:*
- Meets: after a failure or discovery, the standing instruction file and the next prompt both changed to match.
- Fails: the same stale instruction re-sent after a run already contradicted it.

4. **작업 분해 · 위임 설계** — 큰 문제를 점검 가능한 실행 단위로 쪼개 맡기는가

*Unofficial reading:*
- Meets: tasks map one-to-one onto acceptance criteria and are sized to the remaining time and token budget.
- Fails: a single sprawling request, or subtasks with no way to check them individually.

5. **재사용 가능한 작업 체계** — 반복 작업과 맥락 전달을 문서 · 도구로 고정하는가

*Unofficial reading:*
- The official met-signal names 의도 문서 (CLAUDE.md); this suite accepts `AGENTS.md` as the same artifact.
- Also scored here: domain language staying consistent across prompt, code, and test, and traceability from a
  recorded decision through to code, test, and demo claim.
- Meets: a fresh session, given only that document, can state the goal, the constraints, and how to verify.
- Fails: context lives only in one chat history; or tools and MCP servers are added ad hoc so the signal blurs instead of being fixed.

6. **검증 루프 설계 · 통제** — AI 결과를 그대로 믿지 않고 검증 → 수정 → 재검증으로 닫는가

*Unofficial reading:*
- The loop closes only when **the same verification runs again and now passes**. A new, easier check does not close it.
- Meets: a failing check, the fix, and a re-run of that same check passing — all three visible.
- Fails: the AI's completion report accepted without a run, or a failure followed by a substituted check.

## 인지 관리 / Cognition — channel: post-hoc Q&A

Official channel: 사후 Q&A. **Documents do not raise these scores** — no README, decision log, or
retrospective adds a cognition point.

*Unofficial — how this suite scores it:* cognition is only scorable by **running a quiz**. Generate 5-10
questions from the actual project folder with `$junho-probe-quiz`, ask them with documents closed, and score
the answers. A rehearsal checklist is not evidence; an unanswered quiz is **missing** evidence for cognition,
not a pass.

1. **AI 의사결정 · 근거 이해** — AI가 택한 구조와 기술이 무엇이고 왜인지 설명하는가

*Unofficial reading:*
- Meets: names the chosen structure, the rejected alternative, and the reason, consistent with the code.
- Fails: textbook generalities about good architecture that never touch this submission.

2. **AI 산출물 구조 이해** — AI가 만든 것의 실제 구성과 연결을 설명하는가

*Unofficial reading:*
- Meets: traces one real request through the actual modules and data contracts that exist in the repo.
- Fails: citing a file, module, or API that does not exist in the submission.

3. **AI 산출물 동작 · 리스크 예측** — 정상 · 비정상 경로의 동작과 깨질 조건을 예측하는가

*Unofficial reading:*
- Meets: names a specific break condition, and it is confirmed by testing it during the audit.
- Fails: "it should handle errors" with no named condition, or a prediction the audit immediately falsifies.

---

## Unofficial — score consequences of the official signals

> Unofficial — this suite's own convention. Official weights, totals, and example contents are unpublished.

The signal wording is official and lives in the authority document (공식 — 미충족으로 보는 신호). The score
consequences below are **not** official: the official rubric attaches no numbers to these signals.

| Official fail signal (see authority document) | Unofficial consequence in this suite |
| --- | --- |
| 통짜 위임 | Intent 1 ≤ 1 |
| 검증 없이 수용 | Intent 6 ≤ 1 |
| 교과서 일반론 | that Cognition criterion ≤ 1 |
| 없는 파일 · API 인용 | that criterion 0, plus an integrity note |
| 도구 · MCP 남발로 흐려진 신호 | Intent 5 ≤ 2 when tooling was added faster than it was justified |

On the last one: every added tool, agent, or MCP server with no recorded purpose and no verification run
behind it dilutes Intent evidence. Volume is not evidence.

The four common tests are official; the consequence this suite attaches to them is not — a criterion that
fails one of them **cannot exceed 2**.

## Unofficial — score caps and integrity penalties

> Unofficial — this suite's own convention. Official weights, totals, and example contents are unpublished.
> The official rubric publishes no cap table. These caps exist only in this suite.

Caps are per axis, against that axis's own maximum. No total is produced.

| Condition | Cap |
| --- | --- |
| No runnable core path | Technique max **6/15**, criterion 1 ≤ 2; route to `$junho-probe-build` |
| Only AI-authored tests, no executed user flow | Technique max **9/15** |
| No problem/constraint definition beyond a restated goal | Intent max **18/30** |
| No closed verification loop (no re-pass of the same verification) | Intent max **18/30**, criterion 6 ≤ 2 |
| Cannot explain own artifact in Q&A, or answers are generic rather than artifact-grounded | Cognition max **6/15** |
| Answers contradict the submission, or cite files/APIs that do not exist | that criterion 0, Cognition max **6/15** |
| Mock data or simulated integration presented as production/real | Integrity failure: cap **every** axis at half its maximum and state the misrepresentation explicitly |
| Fabricated logs, metrics, citations, or execution claims | Integrity failure: do not report axis subtotals as a normal result; report the integrity finding instead |
| Secret or credential leak, privacy exposure, or a serious unapproved side effect | Critical safety finding regardless of scores, and Technique criterion 3 = 0 |

Do not penalize an honest failed attempt that produced useful evidence and a sound revision.
Separate absence of evidence from negative evidence, and say which one a low score rests on.

A scope cut recorded at the time to stay inside the time or token budget is Intent evidence, not a deduction.

## Grey areas — official statement vs. this suite's inference

**Official**: "기준마다 **grey area**와 충족 · 미충족 예가 정의돼 **채점이 재현 가능**하다."

*Unofficial inference:* because the grey areas are pre-defined rather than negotiated, borderline placement
should not be expected to be scored generously. If evidence sits on the line, treat it as not a pass and move
it clearly onto the meets side.

## Unofficial — optional lens, not scored

Stakeholder mapping, domain-language glossaries, and decision→demo traceability are useful reading lenses but
are not Probe axes. When they produce real evidence, score that evidence under Intent 2 or Intent 5 — never
separately, and never as a fourth axis.

The output contract for an audit lives in one place only: [../SKILL.md](../SKILL.md) (`## Audit output`).
