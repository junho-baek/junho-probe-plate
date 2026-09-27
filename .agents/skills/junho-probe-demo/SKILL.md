---
name: junho-probe-demo
description: Turn verified evidence into a reproducible demo at the event's own presentation length, plus the grounded material a post-hoc Q&A answer needs. Use after auditing to build the Before-Trigger-Magic-After-Impact narrative, map every claim to direct evidence, document exact reproduction steps, disclose limitations, and verify that every file and API you name really exists. Cognition Q&A itself is set and judged by $junho-probe-quiz, and axis subtotals only by $junho-probe-audit.
---

# Junho Probe Demo

Operate in Phase 6. Tell only the story the artifact supports.

Which rubric governs: read `.junho-probe/RUBRIC.md` first — it records this event's own published
criteria and names the grader. When the grader is Probe,
`../junho-probe-skill/references/probe-official-rubric.md`
(source: <https://www.getcofa.com/ko/probe>, checked 2026-09-27) is the basis. When it is another
grader, that event's criteria govern and the Probe rubric is reference only.
Event-independent: use for any graded AI-native evaluation, not one specific hackathon.

Scope boundary:

- **Cognition is scored from post-hoc Q&A**, which arrives as a quiz over your own project. This skill
  does not set, answer, or score it — `$junho-probe-quiz` does. Nothing written in `DEMO.md` earns
  cognition credit.
- Nothing said here recovers technique (read from code) or intent (read from the automatically
  collected behavior record).
- Axis subtotals are produced only by `$junho-probe-audit`. Do not compute a score here.

So this phase produces exactly two things: **the demo narrative**, and **the grounded material** a
quiz answer will draw on — real files, real paths, real verification output. Work inside the
remaining **time and token budget**.

## Load verified evidence

Read:

- `.junho-probe/RUBRIC.md` — this event's own criteria and grader
- `.junho-probe/STATUS.md` — including the **presentation length** recorded in Phase 0
- `.junho-probe/PROBE-CANVAS.md`
- `.junho-probe/DECISIONS.md`
- `.junho-probe/EVALS.md`
- `.junho-probe/DEMO.md`
- the intent document a fresh session would inherit (`CLAUDE.md` or `AGENTS.md`)
- the actual runnable artifact and its reproduction commands

If the core path cannot run or the largest claim lacks evidence, route back to
`$junho-probe-audit` or `$junho-probe-build`.

## Build the flow at the event's presentation length

Use the presentation length the event specifies, as recorded in `STATUS.md` in Phase 0. Only when the
event specifies none, default to 60-90 seconds and label it as this suite's default, not a rule.

Structure:

```text
Before -> Trigger -> Magic moment -> After -> Business impact
```

Show:

- one concrete user and moment
- one input
- one previously disconnected decision or action
- one observable result
- one next user action
- one verified metric or explicitly labeled validation hypothesis

Do not add another feature for presentation value, and do not add a tool or MCP server for the demo
either — signal blurred by tool and MCP sprawl is an official miss signal.

## Map claims

For every material statement, record:

| Claim | Evidence | Status | Limitation |
| --- | --- | --- | --- |

Allowed status: verified fact, supported inference, hypothesis.

Remove unsupported or contradictory claims. Do not present simulation, mock data, or a heuristic
as a real integration or measured outcome.

## Prepare reproduction

Provide:

- exact setup command
- exact run command
- fixture or safe input
- happy-path steps
- one failure-path step
- expected output
- fallback if an external dependency fails

Re-run the documented path from the documented starting state before finalizing the script. Where a
defect was fixed, hold the record showing it failed, was fixed, and then **passed the same
verification again** — not a different or weakened check.

## Assemble quiz material, then hand off

Post-hoc Q&A is drawn **across outputs, intent, and cognition**, over your own project folder.
Assemble the material and invoke `$junho-probe-quiz` to set the questions and judge the answers.

Each item below must resolve to a real path, symbol, or captured command output — not recalled
reasoning:

- **Structure map** — which file or module owns which responsibility, where data crosses between
  them, where the human approval boundary sits.
- **Decision record** — which structure and technologies were chosen, on what evidence, and which AI
  proposal or alternative was rejected and why (from `DECISIONS.md`).
- **Behavior notes** — the normal path step by step, and the abnormal path (bad input, dependency
  down, empty result), with the observed output for each.
- **Risk and hypothesis list** — what breaks first and under what condition; which claims are still
  hypotheses and what would falsify them.
- **Intent trail** — the completion condition given to the AI, how it was checked, how instructions
  and the intent document changed when new information or a failure arrived, and which verification
  loop closed the result.

## Check every claim before finalizing

Apply the four criteria that attach to all three axes: does the statement contradict the actual
submission, is it grounded in **your own artifact** rather than general principles, does it invent
anything that does not exist, does it reason from evidence rather than authority.

Then run the existence check — **citing a file or API that does not exist is an official miss
signal.** List every path, command, function, endpoint, and config key appearing in the script or the
quiz material and resolve each against the artifact:

```bash
test -e <path> || echo "MISSING: <path>"
grep -rn "<symbol>" <artifact dir> || echo "UNGROUNDED: <symbol>"
```

Correct or delete whatever does not resolve. Also reject two shapes outright: textbook generalities
standing in for your artifact, and an AI completion report used as the evidence.

## Update `DEMO.md`

Write:

- the script, at the recorded presentation length
- reproduction commands
- claim-to-evidence table
- known limitations
- quiz material (structure map, decision record, behavior notes, risk and hypothesis list, intent
  trail)

Set `STATUS.md` to Phase 6 PASS only after the demo has been run from the documented starting state
and the existence check is clean.

## Final output

```text
Presentation length (event-specified | suite default):
Exact run path:
Largest verified claim:
Explicit hypothesis:
Known limitation:
Existence check: CLEAN | unresolved names listed
Quiz material: READY | gaps listed
Handoff: $junho-probe-quiz
Final gate: PASS | FAIL | BLOCKED
```
