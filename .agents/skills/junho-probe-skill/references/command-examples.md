# Junho Probe Plate invocation examples | 3축 발동 예시

Use the event's rubric first. These commands select evidence workflows; they do not create official weights.

## Intent | 의도 관리

```text
$junho-probe-coach 이 과제를 Phase 0부터 분석하고, 완료조건·제약·비목표·검증을 포함한 다음 프롬프트를 만들어줘. material prompt는 INTENT-INDEX에 contemporaneous event로 기록해줘.
```

## Technique | 기술 관리

```text
$junho-plate-review 현재 기능 슬라이스의 실행성·격리/구조화·보안 위생을 file:line 증거로 점검해줘. production artifact, surface ownership, preview parity도 해당하면 검사해줘.
```

수정 권한까지 줄 때만 다음을 사용합니다.

```text
$junho-plate-refactor 방금 scorecard의 FAIL과 actionable WARN을 동작 보존 방식으로 수정하고 동일 검증을 재통과해줘.
```

## Cognition | 인지 관리

```text
$junho-probe-quiz SET 이 프로젝트의 코드와 INTENT-INDEX를 함께 읽고, 기술 구조와 당시 판단이 결합된 폐쇄형 사후 Q&A를 내줘. 답은 아직 주지 마.
```

답변 뒤에는 다음처럼 판정합니다.

```text
$junho-probe-quiz JUDGE 내 답변을 실제 file:line과 intent event에 대조해 met/partial/unmet으로 판정해줘.
```

## Three-axis full loop | 3축 전체 루프

```text
$junho-probe-skill 이 과제를 시작해줘. 이벤트 rubric을 먼저 기록하고 Intent는 행동 index, Technique는 Junho Plate, Cognition은 artifact-grounded quiz로 분리해 끝까지 라우팅해줘.
```

```text
$junho-probe-audit code/artifact, intent events, quiz verdict를 각 채널에서만 읽어 3축을 점검하고 가장 큰 회복 프롬프트 하나를 만들어줘.
```

## Agent workload | Cloudflare Agents SDK + Judge

```text
$junho-probe-build 이 agent 기능을 Cloudflare Agents SDK 기본 경로로 구현해줘. Producer와 read-only Judge를 분리하고, Judge가 immutable candidate를 검토하게 하며 결정론적 테스트와 policy gate는 최종 권한으로 유지해줘.
```

