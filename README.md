# 준호 Probe Plate

AI 협업 평가에서 **기술(Technique)·의도(Intent)·인지(Cognition)**를 서로 다른 증거 채널로 관리하고,
마지막에는 실제 코드와 행동 기록을 함께 설명할 수 있게 만드는 개인 하네스입니다.

이 저장소는 두 층으로 구성됩니다.

- **Junho Plate**: AI가 빠르게 만든 코드의 라스트 마일을 기술적으로 조입니다.
- **Junho Probe**: 목표·제약·위임·검증 행동을 기록하고, 제출 뒤 자기 산출물을 설명할 수 있는지 검증합니다.

## 왜 둘을 합쳤나

Probe의 세 축은 서로 대신할 수 없습니다.

| 축 | 허용되는 주 증거 | 이 저장소의 도구 |
| --- | --- | --- |
| 기술 | 실제 코드, 빌드, 테스트, 실행 결과 | `junho-plate*`, `junho-probe-build` |
| 의도 | 당시 프롬프트, 도구 설정, 실패와 재검증 | `junho-probe-coach`, intent event index |
| 인지 | 문서를 닫고 수행한 사후 Q&A | `junho-probe-quiz` |

잘 쓴 README는 인지 점수를 대신하지 않고, Plate scorecard는 실행 증거를 대신하지 않으며,
사후 회고는 당시 의도 행동을 소급해 만들지 않습니다.

## 포함된 스킬

### Plate

- `junho-plate`: 기술 품질 coordinator
- `junho-plate-feature`: 최소 수직 기능 구현
- `junho-plate-refactor`: 동작 보존 리팩터링
- `junho-plate-review`: 증거 기반 읽기 전용 리뷰

### Probe

- `junho-probe-skill`: Phase router와 3축 상태 관리
- `junho-probe-coach`: 문제·제약·완료 조건·위임 설계
- `junho-probe-build`: bounded task 실행과 검증 루프
- `junho-probe-audit`: 독립 Judge 방식의 3축 감사
- `junho-probe-quiz`: 코드와 의도 이벤트를 함께 묻는 closed-book 인지 퀴즈
- `junho-probe-demo`: 사실 경계가 있는 데모 준비

## 설치

다른 프로젝트에 복사 설치합니다. 복사 방식이라 웹 IDE에서도 별도 전역 설정 없이 사용할 수 있습니다.

```bash
./scripts/install-skills.sh /absolute/path/to/project
```

Claude Code용 `.claude/skills` 링크도 함께 만들려면 다음처럼 실행합니다.

```bash
./scripts/install-skills.sh /absolute/path/to/project --claude-links
```

## 가장 짧은 사용법

### 전체 루프

```text
$junho-probe-skill 이 과제를 실제 행사 rubric 기준으로 시작해줘. 먼저 문제·제약·완료 조건을 고정하고, 기술·의도·인지 증거를 서로 섞지 말아줘.
```

### 기술

```text
$junho-plate-review 현재 변경을 읽기 전용으로 리뷰해줘. production build, API·Admin·Customer 소유권, shared preview renderer, 타입 경계, 순수 함수 테스트, secret hygiene를 실제 증거로 확인해줘.
```

### 의도

```text
$junho-probe-coach 지금 결정을 contemporaneous intent event로 기록해줘. 원문, 한국어 정규화 의도, 영문 검색 gloss, 완료 조건, 검증 명령, 결과, supersedes를 남겨줘.
```

### 인지

```text
$junho-probe-quiz SET 모드로 실제 코드와 intent event를 함께 읽고 closed-book 질문을 내줘. 답은 공개하지 말고 file:line과 event ID를 검증해줘.
```

### 독립 감사

```text
$junho-probe-audit Producer와 분리된 read-only Judge로 감사해줘. artifact revision을 고정하고 Plate 결과를 재검증하며, reconstructed intent는 점수 증거에서 제외하고 cognition은 quiz verdict만 사용해줘.
```

더 많은 명령은 [3축 실행 명령](docs/COMMANDS.md)에 있습니다.

## Agent 기본 패턴

Cloudflare Workers에서 지속 상태·연결·스케줄·서버 도구 실행이 필요한 agentic workload라면
Cloudflare Agents SDK를 우선 검토합니다. 생성은 Producer, 평가는 독립 Judge, 안전·스키마·권한·발행은
결정론적 gate가 최종 책임집니다. 단순 정적·로컬 작업에는 불필요한 agent runtime을 강제하지 않습니다.

상세 구조는 [Cloudflare agent 패턴](docs/CLOUDFLARE_AGENT_PATTERN.md)에 있습니다.

## 검증

```bash
python3 -m unittest discover -s .agents/skills/junho-plate/tests -p 'test_*.py'
python3 .agents/skills/junho-plate/scripts/validate_evidence.py
python3 -m unittest discover -s .agents/skills/junho-probe-skill/tests -p 'test_*.py'
git diff --check
```

## 문서

- [핵심 원칙](docs/CORE_PRINCIPLES.md)
- [3축 운영 모델](docs/THREE_AXIS_MODEL.md)
- [의도 이벤트 스키마](docs/INTENT_EVENT_SCHEMA.md)
- [인지 퀴즈 설계](docs/COGNITION_QUIZ.md)
- [Cloudflare agent 패턴](docs/CLOUDFLARE_AGENT_PATTERN.md)
- [3축 실행 명령](docs/COMMANDS.md)
- [출처와 재배포 경계](docs/ORIGINS_AND_BOUNDARIES.md)
- [코드리뷰 피드백을 Plate 규칙으로 변환한 근거](.agents/skills/junho-plate/references/review-feedback-evidence.md)

## Supaplate 경계

이 저장소에는 Supaplate 원본 코드·템플릿·fixture·builder를 재배포하지 않습니다. 비공개 저장소라는
사실만으로 제3자 소스의 재배포 권리가 생기지는 않습니다. 여기에는 코드리뷰에서 얻은 교훈을 일반화한
Junho Plate 규칙, 합성 테스트, Probe 하네스만 저장합니다.
