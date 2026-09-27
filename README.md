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
- `junho-query-wiki`: 모든 사용자 질의를 append-only로 기록하고 중요한 판단을 candidate/verified 주제로 승격

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

## 병렬 터미널 운영

이 하네스의 권장 방식은 한 에이전트가 한 번에 여러 역할을 흉내 내는 것이 아닙니다. 사용자는
**구현 터미널을 계속 운전**하고, 고정된 commit을 읽는 Plate 리팩터링·기술 검증·코드리뷰·인지
퀴즈 터미널을 별도로 열어 병렬로 돌립니다.

```text
사용자 ──> A. Intent + Producer ──> 작은 checkpoint commit ──> 다음 구현을 즉시 계속
                         ├──> B. Plate Refactor ──> 별도 branch의 후보 commit
                         ├──> C. Technique Verify ──> 실행 증거만 보고
                         ├──> D. Technical Review ──> read-only finding
                         └──> E. Cognition Quiz ──> closed-book 질문과 판정

모든 사용자 질의 ──> Query Wiki
실제 동시대 목표·제약·검증 행동만 ──> Probe Intent event
```

### 운영 원칙

- A만 현재 제품 worktree를 쓴다. 사용자는 A에서 의도 기반 구현을 빠르게 이어간다.
- B는 별도 branch와 worktree만 쓴다. A의 움직이는 파일을 직접 고치지 않는다.
- C·D·E는 같은 `CHECKPOINT_SHA`를 본다. 서로의 결론을 미리 공유하지 않는다.
- B의 refactor commit은 자동 병합하지 않는다. A가 잠시 멈춘 checkpoint에서 검증 뒤 cherry-pick한다.
- C의 테스트 실패는 고치지 않고 그대로 보고한다. 수정은 A 또는 다음 B wave가 맡는다.
- E의 SET 모드는 답을 공개하지 않는다. 사용자가 직접 답한 뒤 JUDGE 모드로 판정한다.
- Query Wiki의 모든 질의 기록은 검색·회고 재료다. Producer의 실제 행동으로 연결되지 않은 기록은 Intent 점수가 아니다.

### 0. 기준 checkpoint와 격리 worktree 만들기

먼저 A에서 현재 slice를 작은 commit으로 고정합니다. 관련 파일만 선택적으로 stage합니다.

```bash
git status --short
git add <이번-slice의-파일들>
git commit -m "checkpoint: <observable slice>"
```

그다음 아래 블록을 한 번 실행합니다. B·C·D·E가 모두 같은 commit을 보게 하는 것이 목적입니다.

```bash
TASK_ROOT="$(pwd)"
TASK_PARENT="$(dirname "$TASK_ROOT")"
TASK_NAME="$(basename "$TASK_ROOT")"
RUN_TAG="$(date +%Y%m%d-%H%M%S)"
CHECKPOINT_SHA="$(git rev-parse HEAD)"

PLATE_TREE="${TASK_PARENT}/${TASK_NAME}-plate-${RUN_TAG}"
VERIFY_TREE="${TASK_PARENT}/${TASK_NAME}-verify-${RUN_TAG}"
REVIEW_TREE="${TASK_PARENT}/${TASK_NAME}-review-${RUN_TAG}"
QUIZ_TREE="${TASK_PARENT}/${TASK_NAME}-quiz-${RUN_TAG}"

git worktree add -b "quality/plate-${RUN_TAG}" "$PLATE_TREE" "$CHECKPOINT_SHA"
git worktree add --detach "$VERIFY_TREE" "$CHECKPOINT_SHA"
git worktree add --detach "$REVIEW_TREE" "$CHECKPOINT_SHA"
git worktree add --detach "$QUIZ_TREE" "$CHECKPOINT_SHA"

echo "$TASK_ROOT"
echo "$PLATE_TREE"
echo "$VERIFY_TREE"
echo "$REVIEW_TREE"
echo "$QUIZ_TREE"
```

새 터미널은 기존 shell 변수를 자동으로 상속하지 않습니다. 위에서 출력한 절대 경로를 각 터미널의
`-C` 값에 넣거나, 같은 terminal multiplexer 세션에서 환경 변수를 상속해 실행합니다. A~E는 한 wave
동안 계속 열어두고 후속 요청을 같은 역할로만 보냅니다.

### A. 구현용 터미널 — Intent + Producer

이 터미널은 대화형으로 계속 유지합니다. 새 요구가 들어올 때마다 Query Wiki를 기록하되, 먼저 다음
bounded task의 목적·범위·완료 조건·검증 명령을 갱신하고 구현합니다.

```bash
codex -C "$TASK_ROOT" -s workspace-write --approve-for-me \
  '$junho-probe-skill 과제를 이어서 수행해줘. 너는 foreground Producer다. 사용자 요청마다 $junho-query-wiki로 query lifecycle을 기록하고, 실제 목표·제약·선택·실패·검증 변경만 contemporaneous Intent event로 남겨라. 한 번에 하나의 bounded vertical slice만 구현하고 같은 검증을 실패→수정→재통과로 닫아라. Plate·review·quiz 결과를 기다리지 말고 다음 독립 slice를 진행하되 checkpoint 병합 순간에는 멈춰라.'
```

Codex host에서 lifecycle hook이 없으면 Query Wiki는 에이전트가 start/finish protocol을 호출하는
best-effort입니다. Claude Code에서는 `junho-query-wiki/references/claude-hooks.example.json`을
`.claude/settings.json`에 병합하면 `UserPromptSubmit`, `Stop`, `StopFailure`를 자동 기록할 수 있습니다.

### B. Plate 리팩터링 터미널 — 별도 writer

B는 현재 동작을 보존하면서 구조만 조입니다. `PLATE_TREE` 밖을 고치지 않고, 한 wave에서 하나의
명확한 경계만 리팩터링한 뒤 검증과 commit을 남깁니다.

```bash
codex -C "$PLATE_TREE" -s workspace-write --approve-for-me \
  '$junho-plate-refactor 이 worktree의 checkpoint만 대상으로 동작 보존 리팩터링을 수행해줘. 우선순위는 public API 목차화, UI와 비즈니스 로직 분리, API·Admin·Customer 소유권, shared renderer, end-to-end 타입 경계, 순수 함수 격리와 테스트다. 한 번에 가장 영향 큰 경계 하나만 수정하고 기존 검증과 추가한 최소 테스트를 실행해라. 다른 worktree나 branch는 건드리지 말고 결과를 하나의 후보 commit으로 남겨라.'
```

B의 결과는 후보일 뿐입니다. A가 다음 checkpoint에 잠시 멈춘 뒤 commit과 diff를 확인하고 C의 동일
검증이 통과할 때만 가져옵니다.

```bash
git -C "$PLATE_TREE" log -1 --oneline
git cherry-pick <검증된-plate-commit-sha>
```

### C. 기술 검증 터미널 — 실행 증거 전용

C는 격리 worktree에서 실제 명령을 실행할 수 있으므로 `workspace-write`를 주되, 소스 수정은 금지합니다.
시작·종료 Git 상태를 비교하고 typecheck, unit, build, E2E, secret 검사를 프로젝트에 존재하는 명령으로
실행합니다. 실패를 고쳐 성공처럼 만들지 않습니다.

```bash
codex -C "$VERIFY_TREE" -s workspace-write --approve-for-me \
  '기술 검증 전용 터미널이다. 코드를 수정하거나 dependency를 설치하지 마라. 시작과 종료에 git status --short를 기록하고, package scripts와 문서에서 실제 검증 명령을 찾아 typecheck, unit test, production build, 핵심 E2E, secret hygiene를 실행해라. 존재하지 않는 명령은 만들지 말고 NOT_RUN으로 표시해라. 각 항목을 PASS, FAIL, BLOCKED로 나누고 literal command, exit status, 핵심 출력, 현재 HEAD SHA를 보고해라. 실패는 수정하지 마라.'
```

### D. 기술 코드리뷰 터미널 — read-only Plate Judge

D는 실행 성공 여부와 별개로 코드의 구조·소유권·타입·보안 경계를 봅니다. 자동 수정 없이
`file:line` 근거가 있는 finding만 냅니다.

```bash
codex -C "$REVIEW_TREE" -s read-only \
  '$junho-plate-review 기준으로 현재 HEAD와 부모 commit의 diff를 읽기 전용 리뷰해줘. scope를 실제 변경 slice에 고정하고 API·Admin·Customer 소유권, public API, UI/비즈니스 분리, shared preview renderer, 타입 경계, 순수 함수 테스트, secret hygiene를 확인해라. 수정하지 말고 실제 file:line 근거가 있는 FAIL/WARN만 우선순위순으로 보고해라.'
```

### E. 인지 퀴즈 터미널 — closed-book examiner

E는 구현을 돕는 터미널이 아닙니다. 고정된 code와 실제 intent event를 함께 읽고 답을 공개하지 않은 채
질문을 냅니다. 사용자는 A와 문서를 닫고 자기 말로 답합니다.

```bash
codex -C "$QUIZ_TREE" -s read-only \
  '$junho-probe-quiz SET 모드로 현재 HEAD의 실제 코드와 .junho-probe/intent/events.jsonl을 조사해 5~10개 closed-book 질문을 내줘. AI 의사결정·근거 이해, 산출물 구조 이해, 정상·비정상 동작과 리스크 예측을 고르게 묻고, 답은 공개하지 마라. 모든 질문의 file:line과 event ID는 먼저 검증하고 reconstructed event는 당시 행동 증거로 쓰지 마라.'
```

같은 E 터미널에서 직접 답한 뒤 다음 요청으로 판정합니다.

```text
$junho-probe-quiz JUDGE 모드로 방금 내 답을 현재 HEAD와 대조해 met/partial/unmet으로 판정해줘. 틀린 답을 대신 고쳐 쓰지 말고, 내가 설명하지 못한 구조·결정·파손 조건만 cognition gap으로 남겨줘.
```

### Wave 결과를 합치는 순서

1. A는 다음 독립 slice를 계속 구현하고 작은 checkpoint를 만든다.
2. C의 FAIL은 먼저 A에서 재현하고 같은 명령으로 닫는다.
3. D의 finding은 사용자 영향·보안·데이터·타입·구조 순으로 다음 bounded task 후보가 된다.
4. B의 commit은 A가 잠시 멈춘 시점에만 cherry-pick하고 C의 검증을 다시 통과시킨다.
5. E의 cognition gap은 답을 외우는 문서가 아니라 코드 명료화, 결정 근거 복원, 다음 퀴즈 입력으로 사용한다.
6. 새 checkpoint마다 B·C·D·E를 새 SHA로 다시 띄운다. 움직이는 working tree를 평가하지 않는다.

시간이 부족하면 C와 D를 우선하고 E의 문항 수를 줄입니다. B는 구현을 막는 hard finding이 없으면
뒤로 미뤄도 됩니다. 병렬화의 목적은 에이전트 수를 늘리는 것이 아니라 **사용자의 의도→구현
critical path에서 품질 점검 대기시간을 제거하는 것**입니다.

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
