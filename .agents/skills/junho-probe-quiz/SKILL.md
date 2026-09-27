---
name: junho-probe-quiz
description: Read a real project folder and set 5-10 cognition questions spread across the three official Probe cognition criteria, then judge answers against the artifact. Use to rehearse or examine post-hoc Q&A readiness, anchor every question to a verified file:line, expose cognition gaps where the builder cannot explain their own output, and hand verdicts to the audit skill instead of scoring here.
---

# Junho Probe Quiz

A cognition examiner, not a rehearsal checklist. It **reads the project** and sets questions the
builder must answer out loud, the way post-hoc Q&A is actually taken — question by question.

Usable from Phase 4 onward, as soon as an artifact exists to read. Two modes:

- **SET** — investigate the project and issue the question list
- **JUDGE** — take answers and rule each one met or unmet against the artifact

Do not run in SET mode against a folder you have not read.

## Scoring basis, and which rubric governs

Default authority: `../junho-probe-skill/references/probe-official-rubric.md`. Read its 「공식」
section before setting questions, and quote official wording verbatim.

**The grader is not always Probe.** If the event's grader is something else, that event's rubric
governs, not this file:

- If `.junho-probe/RUBRIC.md` exists, read it first and treat it as the authority for this event.
- Map each question onto that event's own cognition-equivalent criteria, using its wording.
- If it defines no cognition-equivalent criterion, still run SET and JUDGE, but emit findings as
  **cognition gaps only** — do not attach Probe criterion labels to a non-Probe event.

Everything below that names a Probe criterion applies when Probe (or a Probe-style rubric) is the
grader.

## Why questions, and not a document

Official: cognition management is scored from **사후 Q&A**. The three criteria, verbatim:

1. **AI 의사결정 · 근거 이해** — AI가 택한 구조와 기술이 무엇이고 왜인지 설명하는가
2. **AI 산출물 구조 이해** — AI가 만든 것의 실제 구성과 연결을 설명하는가
3. **AI 산출물 동작 · 리스크 예측** — 정상 · 비정상 경로의 동작과 깨질 조건을 예측하는가

No document raises any of them. A quiz is the only faithful rehearsal, because the real thing is
answered live, one question at a time, **closed-book**, with the repository and intent index closed.
SET must not reveal the answer; it may name anchors for examiner traceability, but must not summarize
what those anchors prove before the person answers.

## Investigate the project first

Given a project root, establish the following from the files, never from assumption:

- the real file tree and which modules are load-bearing
- the entry point and the path one request travels end to end
- the data contract: schema, fixture, or config the code actually reads
- the verification commands that exist and whether they pass
- the boundaries: external calls, mock-versus-real seams, approval points, secret handling
- material behavior records in `.junho-probe/intent/events.jsonl`, using
  `.junho-probe/INTENT-INDEX.md` only as a searchable projection

```bash
git -C <root> ls-files | head -200
rg -n "^(export )?(async )?function |^(export )?(default )?class |^def " <root> --glob '!node_modules'
sed -n '1,80p' <root>/<entry file>
```

Anything you could not establish is not a question topic. It is a gap (see below).

The append-only JSONL is the intent source of truth. Verify each event ID, source, result, evidence,
and `supersedes` edge there before using it. `source: reconstructed` can help retrieval but cannot be
treated as contemporaneous behavior or used to claim that an action occurred during the build.

## Set the questions

Issue **5-10 questions** spread evenly across the three criteria — at least one each, at least two
each once you pass six. That count and spread are *this skill's convention*, not official; official
only states that Q&A is drawn 고루 across outputs, intent, and cognition. Fit the count to the
remaining time and token budget: fewer, anchored questions beat more, loose ones.

Every question must be specific to this artifact. Reject open prompts like "explain the
architecture" or "what are the risks" — an official miss signal is **교과서 일반론** answers, and a
general question invites one.

Each question carries five fields:

| Field | Requirement |
| --- | --- |
| `question` | Names a concrete module, function, file, input, or failure. Answerable in under a minute. |
| `criterion` | Exactly one of the three official cognition criteria above. |
| `answer_anchor` | Supply one or more verified `file:line` anchors the answer rests on. **Verify every one before writing it.** |
| `intent_anchor` | A verified intent event ID, or `N/A — <reason>` when no event is relevant. |
| `failing_answer` | Only the failure shape: a generality, absent citation, or unverified number. It must not disclose the expected answer. |

Shape questions by criterion:

- **의사결정 · 근거** — which option was chosen at this specific seam, why that one, and which
  alternative was rejected on what evidence
- **구조 이해** — which file owns which responsibility, where data crosses between them, where the
  human approval boundary sits, and the exact path of one named request
- **동작 · 리스크** — step-by-step behavior on the normal path, then on one abnormal path (empty,
  malformed, dependency down), and the first condition under which this breaks

### Cross-evidence questions: cognition about both behavior and artifact

When contemporaneous intent events exist, include **at least two** cross-evidence questions. Each
must join one verified event ID to one verified `file:line`; it is not enough to quiz the event log
or the code alone. Prefer the highest-signal shapes:

- explain a chosen structure and its **rejected alternative**, then show where the choice exists
- show how a **prompt or harness change** altered the actual artifact or verification result
- trace a failed check, the fix, and the **same verification** passing afterwards
- explain a data path or ownership boundary and the constraint that caused it
- for agentic work, distinguish **Producer**, independent **Judge**, and the **deterministic gate**;
  state what each may read, write, and decide, and what breaks if one agent grades itself

If the inspected artifact actually implements agent orchestration, SET **must include at least one agent-boundary question**
covering Producer, Judge, and deterministic enforcement. If it does not,
do not invent those roles merely to satisfy this suite convention.

These remain cognition questions, not an extra score axis. They test whether the person understands
the relationship between their recorded intent and the technical artifact that resulted.

## Verify before issuing

An official miss signal is **없는 파일 · API를 인용**하는 설명. The examiner must not commit that
error itself. Before emitting the list, resolve every anchor and every name you used:

```bash
test -e <file> || echo "MISSING: <file>"
awk 'NR==<line>{print;found=1} END{if(!found) print "NO SUCH LINE: <file>:<line>"}' <file>
rg -n "<symbol>" <root> --glob '!node_modules' || echo "UNGROUNDED: <symbol>"
```

If an anchor does not resolve, **drop that question** and set another. Do not soften it into a vague
question to keep the count.

Resolve every `intent_anchor` against the JSONL as well. If an event is absent, conflicting, or only
reconstructed, either drop the claimed behavior or label the exact limitation. Never manufacture a
prompt history from a polished retrospective.

## Judge answers

When answers arrive, rule each question independently. Every ruling cites `file:line` — a ruling
without one is not a ruling.

Apply the four official common criteria, verbatim, to every answer:

- 실제 제출물과 **모순되지 않는가**
- 일반론이 아닌 **본인 산출물 기준**인가
- **없는 것을 지어내지 않는가**
- 권위가 아닌 **증거로 추론하는가**

Verdicts: `met` · `partial` · `unmet`. An answer failing any of the four common criteria cannot be
`met`. A fluent answer the code contradicts is worse than "I don't know": rule it `unmet` and record
the contradiction, because contradicting the submission is the strongest official deduction. The
same rule applies when an intent event contradicts the answer: cite the event ID, its source, and the
conflicting artifact anchor. An intent index entry alone never overrides the real code or executed
verification.
"I don't know" is `unmet` without an integrity note.

## Report cognition gaps

A question nobody can answer is the finding, not a failed quiz. For each, record what could not be
explained, the anchor it should have rested on, and the route:

- structure or behavior unexplainable because the code is genuinely unclear → `$junho-probe-build`
  for the smallest restructuring that makes it explainable
- decision or rejected alternative unexplainable because it was never recorded → record it in
  `.junho-probe/DECISIONS.md` now, and mark it reconstructed rather than contemporaneous
- a topic you could not establish from the files at all → name it as an investigation gap, not a
  question

Do not invent an answer on the builder's behalf. Do not write a document and call the gap closed —
documents cannot raise cognition.

## No score is produced here

This skill produces questions, verdicts, and gaps. **Axis subtotals are computed only by
`$junho-probe-audit`.** Hand the verdict table to it and stop; do not total, weight, or scale
anything here.

## Output

```text
Mode: SET | JUDGE
Rubric in force: official Probe | .junho-probe/RUBRIC.md (<event>)
Project root:
Investigated: <files read> / verification command and its result

Questions (n, anchors verified):
1. [의사결정 · 근거] <question>
   answer_anchor: <file>:<line>
   intent_anchor: <event ID> | N/A — <reason>
   failing answer: <shape>
2. [구조 이해] ...
3. [동작 · 리스크] ...

Dropped for unresolved anchor: <question topic> — <missing path or symbol>

Verdicts (JUDGE only):
| # | Criterion | Verdict | Artifact evidence (file:line) | Intent evidence (event ID) | Common-criteria failure |
| - | --- | --- | --- | --- | --- |

Cognition gaps:
- <what could not be explained> — <anchor it needed> — route: $junho-probe-build | DECISIONS.md

Handoff: verdict table -> $junho-probe-audit (scoring)
```
