---
name: junho-query-wiki
description: Use when every user query should be captured safely as a searchable project wiki while keeping raw conversation history, durable topic knowledge, and Probe Intent evidence explicitly separate.
---

# Junho Query Wiki

모든 사용자 질의를 잊지 않되, 모든 문장을 평가 증거나 영구 지식으로 과장하지 않는 자동 기록 하네스다.

## Non-negotiable truth boundary

**query capture is not Intent evidence.** 질의가 기록됐다는 사실은 Probe 의도 점수를 올리지 않는다. 목표·제약·완료 조건·대안·검증 루프를 실제 작업 전에 명시하고 그 행동이 transcript와 산출물에 남았을 때만 `junho-probe-skill`의 별도 Intent event 후보가 된다.

## Two-tier model

### Tier 1 — automatic append-only journal

모든 외부 사용자 질의는 `.junho-probe/query-wiki/events.jsonl`에 다음 lifecycle event로 남긴다.

- `query_received`: 비밀정보를 제거한 요청, 출처, 익명 session hash
- `query_completed`: 같은 `query_id`에 연결된 응답 요약과 검증 근거
- `query_failed`: 실패 원인
- `query_interrupted`: 완료 기록 없이 다음 요청이 시작된 경우

JSONL은 append-only 정본이다. 과거 행을 고치거나 삭제해 성공한 흐름처럼 재작성하지 않는다. `QUERY-INDEX.md`는 언제든 재생성할 수 있는 검색용 투영이다.

### Tier 2 — non-blocking topic promotion

구현 루프를 멈추지 않도록 topic promotion에는 두 상태가 있다.

- `candidate`: 에이전트가 자동으로 만들 수 있는 임시 지식. 완료·근거를 강제하지 않는다.
- `verified`: 완료된 질의, 존재하는 근거 파일, 중요도 이유, Producer 또는 사람의 승인이 모두 있는 지식.

다음 중 하나에 해당해 보이면 먼저 `candidate`로 올린다.

- 이후 세션도 알아야 할 목표·제약·도메인 규칙
- 선택한 대안과 기각한 대안
- 반복 사용할 검증법·실패 패턴·운영 절차
- 서로 모순되거나 아직 답이 없는 중요한 판단

사소한 문구 수정, 일회성 상태 질문, 중복 요청은 원칙적으로 인덱스에만 둔다. 자동 분류가 틀려도 구현을 막지 않고 candidate로 표시한다. 주제 문서는 한영 병기 H1, 요약, 핵심 판단, 근거, 관련 질의, 열린 질문을 유지한다.

## Start/finish protocol

### Start every external turn

```bash
python3 .agents/skills/junho-query-wiki/scripts/query_wiki.py \
  --root "$PWD" receive <<'JSON'
{"source":"harness","session_id":"SESSION","prompt":"사용자 요청"}
JSON
```

반환된 `query_id`를 현재 turn metadata에 보존한다.

### Finish the same turn

검증 근거는 실제 파일·테스트·명령만 넣는다.

```bash
python3 .agents/skills/junho-query-wiki/scripts/query_wiki.py \
  --root "$PWD" complete <<'JSON'
{"source":"harness","session_id":"SESSION","query_id":"Q-...","assistant_summary":"무엇을 결정하고 검증했는지","evidence":["path/to/test"]}
JSON
```

예외·중단이면 `complete` 대신 `fail`을 호출한다. 완료 이벤트를 사후에 꾸며 넣지 않는다.

### Promote a candidate without blocking implementation

```bash
python3 .agents/skills/junho-query-wiki/scripts/query_wiki.py \
  --root "$PWD" promote <<'JSON'
{
  "query_id":"Q-...",
  "slug":"automatic-query-wiki",
  "title_ko":"자동 쿼리 위키",
  "title_en":"Automatic Query Wiki",
  "summary":"질의를 안전하게 기록하고 중요한 판단만 승격한다.",
  "key_points":["자동 기록과 평가 증거를 분리한다."],
  "evidence":[],
  "open_questions":["호스트 lifecycle hook 지원 범위"],
  "materiality":"architecture_decision",
  "actor_role":"producer",
  "promotion_status":"candidate"
}
JSON
```

완료 뒤 근거가 확인되면 같은 slug를 `promotion_status: "verified"`로 다시 승격한다. 이때만 `materiality_reason`, 실제 존재하는 `evidence` 경로, `approved_by: "producer" | "human"`을 요구한다. Judge는 `propose` 또는 candidate 생성까지만 하며 자기 제안을 verified로 승인하지 않는다.

## Automatic capture by environment

### Claude Code

Claude Code는 `UserPromptSubmit`, `Stop`, `StopFailure` hooks를 제공한다. `references/claude-hooks.example.json`을 프로젝트 `.claude/settings.json`에 병합하면 요청 수신과 종료를 자동 연결할 수 있다. 프로젝트 설정은 팀과 공유되므로 명령을 검토한 뒤 커밋한다.

### Codex

Codex skill text만으로는 모든 turn의 전후 lifecycle 실행을 보장할 수 없다. Codex 호스트가 공식 hook을 제공하지 않는 환경에서는 다음 우선순위를 따른다.

1. API/서비스 harness middleware에서 모델 호출 직전과 `finally`에 기록
2. 프로젝트 runner 또는 wrapper가 turn metadata와 함께 기록
3. 둘 다 불가능할 때 이 스킬의 start/finish protocol을 에이전트가 협조적으로 실행

3번은 자동화 보장이 아니라 best-effort다. 누락을 숨기지 말고 인덱스 coverage gap으로 남긴다.

### Cloudflare Agents SDK

Cloudflare에서는 build-your-own harness가 prompt 구성, tool loop, 상태 저장, lifecycle을 소유하도록 하고 Durable Object SQL에 같은 event schema를 append한다. 응답 후 Judge는 topic promotion 후보를 만들 수 있으나 수신 이벤트는 모델 호출 전에 기록한다. 자세한 경계는 `references/cloudflare-harness.md`를 따른다.

## Security and privacy

- 원문보다 먼저 redaction을 수행한다. API key, GitHub token, Bearer token, password assignment를 저장하지 않는다.
- session ID는 파일명이나 이벤트에 원문으로 쓰지 않고 SHA-256으로 익명화한다.
- 이벤트·투영·상태 파일은 가능한 경우 사용자 전용 권한으로 만든다.
- 전체 응답은 무제한 저장하지 않는다. 완료 기록은 최대 길이로 자르고 실제 검증 근거를 우선한다.
- 민감한 원문 보존이 꼭 필요하면 이 스킬 밖의 승인된 암호화 저장소를 사용한다.

## Recursion and noise control

**recursion guard:** `JUNHO_QUERY_WIKI_INTERNAL=1`인 내부 exporter, Judge, 위키 재생성 요청은 core와 adapter 모두 기록하지 않는다. 위키를 만들기 위한 질의가 다시 위키 질의를 생성하는 루프를 막는다.

- 같은 open query의 동일 hook 재시도는 중복 기록하지 않는다.
- topic page를 query마다 만들지 않는다.
- 자동 요약이 사실을 추가하지 않게 파일·명령·테스트 경로만 evidence로 인정한다.
- Judge의 “중요해 보인다”는 분류는 proposal 또는 candidate일 뿐 Intent 점수가 아니다.

## Relationship to Probe axes

| 기록 | Technique | Intent | Cognition |
| --- | --- | --- | --- |
| 모든 query lifecycle | 관측 가능성 보조 | 점수 아님 | 회고 재료 |
| material Probe event | 검증 명령과 연결 가능 | 동시대 행동 증거 | 설명 근거 |
| topic promotion | 구조·운영 지식 | 결정 맥락 유지 | 퀴즈와 teach-back 입력 |

의도 점수를 노릴 때는 관련 query ID를 `.junho-probe/intent/events.jsonl`의 `evidence_refs`에 연결하되, 실제 산출물과 검증이 없는 질의를 승격하지 않는다.

## Verification

```bash
python3 -m unittest discover \
  -s .agents/skills/junho-query-wiki/tests -v
```

## Done when

- 모든 지원 환경에서 자동화 수준과 한계를 사실대로 표시했다.
- 외부 질의가 `query_received` 뒤 `completed`, `failed`, `interrupted` 중 하나로 연결된다.
- 비밀정보가 JSONL, 상태, Markdown 어디에도 남지 않는다.
- append-only 정본과 재생성 가능한 투영이 분리되어 있다.
- candidate 승격은 구현을 막지 않고, verified 승격만 완료·근거·승인을 강제한다.
- topic promotion의 전체 snapshot이 append-only 이벤트에 남아 원 질의와 과거 판단을 역추적할 수 있다.
- query 기록을 Probe Intent 점수로 잘못 세지 않는다.
