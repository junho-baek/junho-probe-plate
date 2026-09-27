# 준호 Probe Plate | Junho Probe Plate

AI 협업 평가에서 **의도(Intent)·기술(Technique)·인지(Cognition)**를 서로 다른 증거 채널로 관리하기 위한 개인 하네스 저장소입니다.

현재 포함된 묶음:

- `junho-plate`: React Router 7 프로젝트의 기술 품질 coordinator
- `junho-plate-feature`: 최소 수직 기능 구현
- `junho-plate-refactor`: 동작 보존 리팩터링
- `junho-plate-review`: 증거 기반 읽기 전용 리뷰

## Plate 핵심 원칙

- 파일 길이보다 책임과 변경 이유로 경계를 나눕니다.
- API·Admin·Customer는 별도 배포를 강제하지 않되 소유권과 진입점을 분명히 합니다.
- Admin preview와 고객 화면은 같은 renderer 또는 rendering core를 사용합니다.
- dev server가 아니라 실제 production build 산출물을 smoke test합니다.
- dependency는 보호하는 경계나 실제 consumer가 있을 때만 유지합니다.
- Git checkpoint는 제안하되 commit은 명시적인 권한이 있을 때만 생성합니다.
- 호환되는 agent workload는 Cloudflare Agents SDK를 기본으로 검토합니다.
- Producer와 Judge를 분리하고, Judge는 결정론적 테스트나 정책 gate를 대체하지 않습니다.

## 사용 예시

```text
$junho-plate 이 기능 슬라이스를 기술 기준으로 리뷰해줘.
$junho-plate-feature 이 요구사항을 최소 수직 슬라이스로 구현해줘.
$junho-plate-refactor 방금 scorecard의 FAIL과 actionable WARN을 수정해줘.
$junho-plate-review Admin preview와 고객 renderer의 parity를 읽기 전용으로 점검해줘.
```

## 검증

```bash
python3 -m unittest discover -s .agents/skills/junho-plate/tests -p 'test_*.py'
python3 .agents/skills/junho-plate/scripts/validate_evidence.py
```

현재 Plate 계약 테스트 기준은 166개이며 환경 의존 테스트 4개는 조건부 skip입니다.

## 출처와 재배포 경계

이 저장소는 Supaplate 원본 코드, 템플릿, fixture 또는 builder를 포함하지 않습니다. Plate/Supaplate는 구조적 배경이며, 이 저장소에는 사용자 소유 프로젝트에 적용할 파생 규칙과 합성 테스트만 저장합니다. 상세 경계는 `junho-plate/references/plate-detection.md`와 `wemake-rule-evidence.md`에 기록되어 있습니다.

