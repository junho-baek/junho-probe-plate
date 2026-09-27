# Cloudflare Harness Integration

Cloudflare에서 완전 자동 기록을 원하면 스킬 프롬프트가 아니라 **harness lifecycle**에 기록기를 둔다.

1. 사용자 메시지를 모델에 보내기 직전에 `query_received`를 Durable Object의 SQL에 append한다.
2. tool loop와 최종 응답을 같은 `query_id`로 연결한다.
3. 응답 성공 시 `query_completed`, 예외 또는 취소 시 `query_failed`를 `finally`에서 append한다.
4. 별도 exporter가 동일 이벤트 스키마를 `.junho-probe/query-wiki/events.jsonl`로 내보낸 뒤 `rebuild-index`를 실행한다.
5. Judge agent는 승격 후보를 제안할 수 있지만, Probe Intent 점수는 실제 동시대 행동 증거가 있을 때만 별도로 기록한다.

`onChatResponse`는 응답 이후 비동기 분류와 주제 승격 후보 생성에 적합하다. 그러나 수신 이벤트는 모델 호출 전에 harness가 먼저 기록해야 누락 구간을 줄일 수 있다.

재귀 방지를 위해 exporter와 Judge가 만든 내부 요청에는 `JUNHO_QUERY_WIKI_INTERNAL=1` 또는 같은 의미의 metadata를 붙이고 캡처 대상에서 제외한다.
