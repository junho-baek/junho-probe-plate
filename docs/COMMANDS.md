# 3축 실행 명령

## 시작

```text
$junho-probe-skill 이 저장소를 Probe 방식으로 시작해줘. 행사 원문과 rubric 출처를 먼저 고정하고, 남은 시간·토큰·제출 조건을 STATUS에 기록해줘. 기술·의도·인지 증거를 서로 대신하지 마.
```

## 의도: 문제와 완료 조건

```text
$junho-probe-coach 요구사항을 사용자·결정·입력·출력·불변식·비목표·mock/live 경계로 분해해줘. 모호한 부분은 추측하지 말고 open question으로 남긴 뒤, 최대 3개의 검증 가능한 task로 만들어줘.
```

## 의도: 프롬프트와 하네스 기록

```text
$junho-probe-coach 방금 프롬프트, 선택한 harness/skill, 완료 조건, literal verification, 결과를 intent event로 append해줘. 한국어 정규화와 영문 retrieval gloss를 함께 만들고 이전 결정을 바꿨다면 supersedes를 연결해줘.
```

## 기술: 구현

```text
$junho-probe-build OBJECTIVE·ALLOWED SCOPE·KNOWN CONTRACT·NON-GOALS·ACCEPTANCE CRITERIA·VERIFICATION·STOP CONDITIONS가 있는 bounded task 하나만 구현해줘. 실패하면 같은 검증을 수정 후 다시 실행해줘.
```

## 기술: Plate 리뷰

```text
$junho-plate-review 현재 변경을 읽기 전용으로 검토해줘. 실제 production build, runtime surface ownership, preview/customer renderer parity, 타입 경계, dependency 정당성, unused starter residue, 순수 함수 테스트, 보안 위생을 rule ID와 file:line으로 보고해줘.
```

## 기술: Plate 수정

```text
$junho-plate-refactor 직전 scorecard의 FAIL과 actionable WARN만 수정해줘. 동작을 보존하고 같은 검증을 재실행해. 새 기능과 무관한 cleanup은 하지 마.
```

## Agent orchestration

```text
$junho-probe-build 이 agentic slice가 Cloudflare Agents SDK가 필요한지 먼저 판정해줘. 필요하면 Producer와 read-only Judge를 분리하고 후보 revision을 고정해. 안전·스키마·권한·발행은 deterministic gate가 최종 결정하게 해줘.
```

## 인지 퀴즈

```text
$junho-probe-quiz SET 모드. 실제 코드와 intent JSONL을 읽고 5~10개 closed-book 문항을 한 번에 설계해줘. 각 문항은 검증된 file:line과 관련 event ID를 가지며 답은 공개하지 마. agent 구현이 있으면 Producer·Judge·gate 경계를 반드시 물어봐.
```

```text
$junho-probe-quiz JUDGE 모드. 내 답을 코드와 intent event에 대조해 met·partial·unmet으로 판정해줘. 일반론, 존재하지 않는 API, 코드나 당시 결정과의 모순을 명시해줘.
```

## 최종 감사

```text
$junho-probe-audit 고정된 artifact revision을 독립 read-only Judge로 감사해줘. Plate scorecard는 결정적 검증을 재실행하고, Intent는 raw contemporaneous evidence만 사용하며, Cognition은 quiz verdict만 사용해. 세 축 subtotal과 가장 작은 recovery prompt 하나만 줘.
```

