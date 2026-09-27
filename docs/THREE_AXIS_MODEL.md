# 3축 운영 모델

## 흐름

```text
rubric 고정
  -> 문제·제약·완료 조건 정의
  -> bounded task와 intent event 기록
  -> Plate 기술 gate
  -> 실제 E2E와 실패 경로 검증
  -> immutable artifact 고정
  -> closed-book cognition quiz
  -> independent Judge audit
```

## 기술

기술 축의 질문은 “코드가 예쁜가”가 아니라 다음에 가깝습니다.

- 실제 환경에서 핵심 경로가 실행되는가
- 한 책임을 바꿀 때 다른 surface를 불필요하게 읽거나 수정하지 않아도 되는가
- 타입과 런타임 데이터 경계가 이어지는가
- preview와 실제 고객 결과가 같은 renderer를 통과하는가
- production artifact가 만들어지고 실행되는가
- 시크릿과 민감정보가 코드·로그·오류에 남지 않는가

Plate scorecard는 조사 결과입니다. 점수의 직접 증거는 재현된 명령, 테스트, 실행 결과입니다.

## 의도

의도 축은 최종 설명문이 아니라 행동의 시간 순서입니다.

```text
prompt/harness 선택
  -> 완료 조건
  -> 실제 검증
  -> 결과
  -> 실패하면 지시 갱신
  -> 동일 검증 재통과
```

`.junho-probe/intent/events.jsonl`이 원본이며 `INTENT-INDEX.md`는 검색용 투영입니다. 행사 중 기록은
`contemporaneous`, 나중에 복원한 회고는 `reconstructed`로 구분합니다.

## 인지

인지 축은 기술 지식 퀴즈만도, 의사결정 회고만도 아닙니다. 실제 코드와 당시 의도를 연결해 설명하는
능력을 봅니다. 따라서 질문은 `file:line`과 intent event ID를 함께 가질 수 있습니다.

- 구조 선택과 기각한 대안
- 요청·데이터의 end-to-end 흐름
- 정상·비정상 경로와 깨질 조건
- 프롬프트 또는 하네스 변경이 산출물에 미친 결과
- 실패→수정→동일 검증 재통과
- Producer·Judge·deterministic gate의 권한 경계

SET은 답을 공개하지 않고, 응답 뒤 JUDGE가 코드와 이벤트를 다시 대조합니다.

