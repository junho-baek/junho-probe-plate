# 출처와 재배포 경계

## Probe

Probe의 공개 3축 정의와 평가 흐름은 Cofa의 공개 페이지를 기준으로 정리했습니다.

- <https://www.getcofa.com/ko/probe>

이 저장소의 0~5 evidence scale, cap, 명령 문법, intent event schema, 교차 증거 퀴즈는 공식 Probe
채점표가 아니라 Junho Probe의 운영 규칙입니다. 공식 rubric과 개인 convention을 문서에서 구분합니다.

## Junho Plate

Junho Plate는 COFATHON 결과물에 대한 코드리뷰에서 받은 다음 교훈을 일반화했습니다.

- surface와 책임 분리
- UI와 비즈니스 규칙 분리
- shared renderer로 preview parity 보장
- 서버부터 UI까지 이어지는 타입 경계
- production build 산출물 검증
- 사용하지 않는 starter surface 정리
- 순수 함수 격리와 테스트
- public API 중심의 index
- Git checkpoint와 인간 오너십

개별 프로젝트 코드나 제3자의 비공개 구현은 규칙의 증거로 재배포하지 않습니다.

## Supaplate

Supaplate는 Junho Plate의 구조적 배경 중 하나지만, 이 저장소에는 Supaplate 원본 코드·template·fixture·
builder를 포함하지 않습니다. 비공개 GitHub 저장소도 제3자 라이선스 의무를 없애지 않습니다.

원본을 보관해야 한다면 다음 중 하나를 사용합니다.

1. 권한이 확인된 별도 private mirror
2. 원본 remote URL과 허용된 commit SHA만 기록한 manifest
3. 라이선스가 허용하는 설치 스크립트

현재 `vendor/`는 이 경계를 설명하는 manifest 자리만 제공합니다.

