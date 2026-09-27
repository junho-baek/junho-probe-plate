# 의도 이벤트 스키마

의도 기록은 LLM 위키처럼 검색 가능해야 하지만 회고문으로 과거 행동을 꾸며서는 안 됩니다.

## 저장 구조

```text
.junho-probe/
  intent/events.jsonl     # append-only source of truth
  INTENT-INDEX.md         # 한글·영문 검색용 projection
```

## 필드

| 필드 | 의미 |
| --- | --- |
| `id` | 변경되지 않는 이벤트 식별자 |
| `time` | 실제 기록 시각 |
| `phase` | Probe 작업 단계 |
| `kind` | prompt, harness, skill, tool, verification, decision |
| `original` | 사용자가 실제로 입력한 원문 또는 실제 명령 |
| `normalized_ko` | 검색 가능한 한국어 의도 |
| `retrieval_en` | 다국어 검색을 위한 영문 gloss |
| `done_condition` | 어떤 상태가 되면 끝나는가 |
| `verification` | 문자 그대로 실행할 검증 |
| `result` | PASS, FAIL, BLOCKED 등 실제 결과 |
| `evidence` | 파일·라인·명령·로그 위치 |
| `supersedes` | 이전 이벤트를 삭제하지 않고 갱신하는 연결 |
| `source` | `contemporaneous` 또는 `reconstructed` |

## 기록 예시

```bash
python3 .agents/skills/junho-probe-skill/scripts/record_intent_event.py --root . <<'JSON'
{
  "id": "I-014",
  "time": "2026-09-27T17:00:00+09:00",
  "phase": 4,
  "kind": "verification",
  "original": "Admin preview와 customer renderer parity를 검증한다",
  "normalized_ko": "동일 fixture가 공유 renderer에서 같은 의미 결과를 내야 한다.",
  "retrieval_en": "Verify preview and customer renderer parity with one fixture.",
  "done_condition": "parity 테스트와 production build가 모두 통과한다.",
  "verification": "npm run test:preview-parity && npm run build",
  "result": "PASS",
  "evidence": ["tests/preview-parity.test.ts:18"],
  "supersedes": ["I-009"],
  "source": "contemporaneous"
}
JSON
```

비밀값은 기록 전에 제거합니다. 같은 ID의 동일 이벤트는 멱등적으로 처리하지만 내용이 다른 덮어쓰기는
거절합니다.

