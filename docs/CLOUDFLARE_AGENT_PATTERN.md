# Cloudflare agent 패턴

## 선택 기준

Cloudflare Workers 환경에서 다음이 필요할 때 Agents SDK를 우선 검토합니다.

- durable agent identity와 state
- WebSocket 같은 live connection
- scheduling 또는 alarm
- 서버 측 tool 실행
- 여러 요청에 걸친 agent lifecycle

장시간 다단계 실행, retry, approval pause가 핵심이면 Workflows를 함께 검토합니다. 서로 격리된 상태로
병렬 후보를 만들 때는 sub-agent 또는 agent-as-tool 패턴이 적합할 수 있습니다. 정적 페이지나 짧은
로컬 변환에는 agent runtime을 강제하지 않습니다.

공식 문서:

- <https://developers.cloudflare.com/agents/>
- <https://developers.cloudflare.com/agents/runtime/agents-api/>
- <https://developers.cloudflare.com/agents/concepts/workflows/>
- <https://developers.cloudflare.com/agents/runtime/execution/sub-agents/>

## Producer → Judge → Gate

```text
bounded contract
  -> Producer candidate
  -> immutable revision or SHA-256
  -> independent read-only Judge
  -> deterministic tests and policy gates
  -> accept, revise, or reject
```

### Producer

- 허용된 파일·상태만 변경합니다.
- 목표, 비목표, 완료 조건, 검증을 받습니다.
- 후보와 실행 증거를 제출합니다.

### Judge

- 후보 revision과 rubric을 고정한 뒤 시작합니다.
- 후보를 수정하지 않습니다.
- 자신의 산출물을 스스로 채점하지 않습니다.
- Judge context ID와 시작 시각을 남깁니다.
- 코드·검증·intent event의 모순을 찾습니다.

### Deterministic gate

- schema, safety, authorization, publication, invariant의 최종 책임자입니다.
- 두 agent가 동의해도 실패한 gate를 우회하지 않습니다.
- Judge의 서술은 실행 검증을 대체하지 않습니다.

## 병렬화 규칙

독립 후보는 파일 또는 state ownership을 분리한 뒤 병렬화합니다. 공유 상태를 수정하거나 통합 순서가
있는 작업은 순차 실행합니다. agent 수와 도구 수는 평가 증거가 아닙니다.

