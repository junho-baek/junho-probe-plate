from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "query_wiki.py"
HOOK = SKILL_DIR / "scripts" / "claude_hook.py"


class QueryWikiTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_cli(self, command: str, payload: dict, *, check: bool = True):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), command],
            input=json.dumps(payload, ensure_ascii=False),
            text=True,
            capture_output=True,
            check=check,
        )

    def events(self) -> list[dict]:
        path = self.root / ".junho-probe/query-wiki/events.jsonl"
        return [json.loads(line) for line in path.read_text().splitlines() if line]

    def test_receive_redacts_secrets_before_any_persistence(self) -> None:
        secret = "sk-proj-abcdefghijklmnopqrstuvwxyz0123456789"
        result = self.run_cli(
            "receive",
            {
                "source": "claude-code",
                "session_id": "session-1",
                "prompt": f"이 키로 실행해 OPENAI_API_KEY={secret}",
            },
        )
        query_id = json.loads(result.stdout)["query_id"]

        persisted = "\n".join(
            path.read_text(errors="replace")
            for path in self.root.rglob("*")
            if path.is_file()
        )
        self.assertNotIn(secret, persisted)
        self.assertIn("[REDACTED]", persisted)
        self.assertEqual(query_id, self.events()[0]["query_id"])

    def test_json_style_api_key_is_redacted_in_all_artifacts(self) -> None:
        secret = "ordinary-secret-value-that-must-not-persist"
        self.run_cli(
            "receive",
            {
                "source": "api",
                "session_id": "json-secret",
                "prompt": f'설정은 {{"api_key": "{secret}"}} 입니다',
            },
        )
        persisted = "\n".join(
            path.read_text(errors="replace")
            for path in self.root.rglob("*")
            if path.is_file()
        )
        self.assertNotIn(secret, persisted)
        self.assertIn("[REDACTED]", persisted)

    def test_receive_retry_while_open_is_idempotent(self) -> None:
        payload = {
            "source": "claude-code",
            "session_id": "session-2",
            "prompt": "같은 요청",
            "event_key": "turn-001",
        }
        first = json.loads(self.run_cli("receive", payload).stdout)
        second = json.loads(self.run_cli("receive", payload).stdout)

        self.assertEqual(first["query_id"], second["query_id"])
        self.assertEqual(1, len(self.events()))

    def test_complete_appends_and_preserves_received_event(self) -> None:
        received = json.loads(
            self.run_cli(
                "receive",
                {"source": "api", "session_id": "session-3", "prompt": "위키 설계"},
            ).stdout
        )
        before = (self.root / ".junho-probe/query-wiki/events.jsonl").read_bytes()

        self.run_cli(
            "complete",
            {
                "source": "api",
                "session_id": "session-3",
                "query_id": received["query_id"],
                "assistant_summary": "2단 위키 구조를 설계했다.",
                "evidence": ["tests/test_query_wiki.py"],
            },
        )

        after = (self.root / ".junho-probe/query-wiki/events.jsonl").read_bytes()
        self.assertTrue(after.startswith(before))
        self.assertEqual(["query_received", "query_completed"], [e["type"] for e in self.events()])
        index = (self.root / ".junho-probe/query-wiki/QUERY-INDEX.md").read_text()
        self.assertIn("완료", index)
        self.assertIn(received["query_id"], index)

    def test_complete_without_matching_receive_fails(self) -> None:
        result = self.run_cli(
            "complete",
            {"source": "api", "session_id": "missing", "assistant_summary": "없음"},
            check=False,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("open query", result.stderr.lower())

    def test_finish_rejects_second_terminal_event(self) -> None:
        query_id = json.loads(
            self.run_cli(
                "receive",
                {"source": "api", "session_id": "terminal-once", "prompt": "한 번만 완료"},
            ).stdout
        )["query_id"]
        payload = {
            "source": "api",
            "session_id": "terminal-once",
            "query_id": query_id,
            "assistant_summary": "완료",
        }
        self.run_cli("complete", payload)
        second = self.run_cli("complete", payload, check=False)
        conflicting = self.run_cli(
            "fail",
            {"source": "api", "session_id": "terminal-once", "query_id": query_id, "error": "늦은 실패"},
            check=False,
        )
        self.assertNotEqual(0, second.returncode)
        self.assertNotEqual(0, conflicting.returncode)
        self.assertEqual(1, len([event for event in self.events() if event["type"] == "query_completed"]))
        self.assertFalse(any(event["type"] == "query_failed" for event in self.events()))

    def test_capture_does_not_create_probe_intent_evidence(self) -> None:
        self.run_cli(
            "receive",
            {"source": "api", "session_id": "session-4", "prompt": "버튼 색을 바꿔줘"},
        )
        self.assertFalse((self.root / ".junho-probe/intent/events.jsonl").exists())

    def test_promote_creates_bilingual_topic_with_traceability(self) -> None:
        query_id = json.loads(
            self.run_cli(
                "receive",
                {"source": "api", "session_id": "session-5", "prompt": "자동 위키 설계"},
            ).stdout
        )["query_id"]
        self.run_cli(
            "complete",
            {
                "source": "api",
                "session_id": "session-5",
                "query_id": query_id,
                "assistant_summary": "설계와 테스트를 마쳤다.",
                "evidence": [".junho-probe/query-wiki/events.jsonl"],
            },
        )
        self.run_cli(
            "promote",
            {
                "query_id": query_id,
                "slug": "automatic-query-wiki",
                "title_ko": "자동 쿼리 위키",
                "title_en": "Automatic Query Wiki",
                "summary": "모든 질의를 안전하게 기록하고 중요한 판단만 승격한다.",
                "key_points": ["원문은 append-only 사건으로 저장", "중요 판단만 Probe 의도 증거 후보"],
                "evidence": [".junho-probe/query-wiki/events.jsonl"],
                "open_questions": ["Codex 호스트 훅 지원 여부"],
                "materiality": "architecture_decision",
                "materiality_reason": "이후 모든 에이전트의 기록 경계를 결정한다.",
                "actor_role": "producer",
                "approved_by": "producer",
                "promotion_status": "verified",
            },
        )

        topic = self.root / ".junho-probe/query-wiki/topics/automatic-query-wiki.md"
        body = topic.read_text()
        self.assertIn("# 자동 쿼리 위키 | Automatic Query Wiki", body)
        self.assertIn(query_id, body)
        self.assertIn("## 근거", body)
        self.assertIn("## 열린 질문", body)
        promoted = [event for event in self.events() if event["type"] == "query_promoted"][0]
        self.assertEqual("모든 질의를 안전하게 기록하고 중요한 판단만 승격한다.", promoted["snapshot"]["summary"])
        self.assertEqual("architecture_decision", promoted["snapshot"]["materiality"])

    def test_open_query_can_be_candidate_but_not_verified(self) -> None:
        query_id = json.loads(
            self.run_cli(
                "receive",
                {"source": "api", "session_id": "still-open", "prompt": "아직 작업 중"},
            ).stdout
        )["query_id"]
        payload = {
            "query_id": query_id,
            "slug": "still-open",
            "title_ko": "진행 중",
            "title_en": "Still Open",
            "summary": "완료되지 않은 자동 분류 후보다.",
            "key_points": ["아직 검증되지 않았다."],
            "evidence": [],
            "open_questions": ["작업 완료 후 유지할 주제인가"],
            "materiality": "open_question",
            "actor_role": "producer",
            "promotion_status": "candidate",
        }
        self.run_cli("promote", payload)
        topic = self.root / ".junho-probe/query-wiki/topics/still-open.md"
        self.assertIn("candidate", topic.read_text())

        verified = self.run_cli(
            "promote",
            {
                **payload,
                "evidence": [".junho-probe/query-wiki/events.jsonl"],
                "materiality_reason": "아직 열린 질의다.",
                "approved_by": "producer",
                "promotion_status": "verified",
            },
            check=False,
        )
        self.assertNotEqual(0, verified.returncode)

    def test_judge_can_propose_but_cannot_directly_promote(self) -> None:
        query_id = json.loads(
            self.run_cli(
                "receive",
                {"source": "api", "session_id": "judge", "prompt": "아키텍처 결정"},
            ).stdout
        )["query_id"]
        self.run_cli(
            "complete",
            {"source": "api", "session_id": "judge", "query_id": query_id, "assistant_summary": "완료"},
        )
        payload = {
            "query_id": query_id,
            "slug": "judge-proposal",
            "title_ko": "판정 제안",
            "title_en": "Judge Proposal",
            "summary": "Judge가 승격을 제안했다.",
            "key_points": ["제안과 승격은 다르다."],
            "evidence": [".junho-probe/query-wiki/events.jsonl"],
            "open_questions": [],
            "materiality": "architecture_decision",
            "materiality_reason": "재사용할 경계를 설명한다.",
            "actor_role": "judge",
        }
        self.run_cli("propose", payload)
        self.assertFalse((self.root / ".junho-probe/query-wiki/topics/judge-proposal.md").exists())
        rejected = self.run_cli(
            "promote",
            {**payload, "approved_by": "judge", "promotion_status": "verified"},
            check=False,
        )
        self.assertNotEqual(0, rejected.returncode)
        self.assertTrue(any(event["type"] == "query_promotion_proposed" for event in self.events()))

    def test_promote_requires_materiality_reason_and_existing_evidence(self) -> None:
        query_id = json.loads(
            self.run_cli(
                "receive",
                {"source": "api", "session_id": "weak-promotion", "prompt": "오탈자 수정"},
            ).stdout
        )["query_id"]
        self.run_cli(
            "complete",
            {"source": "api", "session_id": "weak-promotion", "query_id": query_id, "assistant_summary": "완료"},
        )
        base = {
            "query_id": query_id,
            "slug": "weak-promotion",
            "title_ko": "약한 승격",
            "title_en": "Weak Promotion",
            "summary": "근거가 약하다.",
            "key_points": [],
            "open_questions": [],
            "materiality": "architecture_decision",
            "actor_role": "producer",
            "approved_by": "producer",
            "promotion_status": "verified",
        }
        no_reason = self.run_cli("promote", {**base, "evidence": ["missing.txt"]}, check=False)
        no_evidence = self.run_cli(
            "promote",
            {**base, "materiality_reason": "중요하다고 주장", "evidence": ["missing.txt"]},
            check=False,
        )
        self.assertNotEqual(0, no_reason.returncode)
        self.assertNotEqual(0, no_evidence.returncode)

        candidate = self.run_cli(
            "promote",
            {
                **base,
                "promotion_status": "candidate",
                "evidence": [],
            },
        )
        self.assertEqual(0, candidate.returncode)

    def test_session_id_cannot_escape_state_directory(self) -> None:
        self.run_cli(
            "receive",
            {"source": "api", "session_id": "../../escape", "prompt": "경로 안전"},
        )
        self.assertFalse((self.root / "escape").exists())
        state_files = list((self.root / ".junho-probe/query-wiki/state").glob("*.json"))
        self.assertEqual(1, len(state_files))
        self.assertNotIn("..", state_files[0].name)

    def test_internal_recursion_guard_skips_capture(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), "receive"],
            input=json.dumps(
                {"source": "judge", "session_id": "internal", "prompt": "위키를 다시 위키화"},
                ensure_ascii=False,
            ),
            text=True,
            capture_output=True,
            env={**os.environ, "JUNHO_QUERY_WIKI_INTERNAL": "1"},
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual({"skipped": True, "reason": "internal_recursion_guard"}, json.loads(result.stdout))
        self.assertFalse((self.root / ".junho-probe/query-wiki/events.jsonl").exists())

    def test_concurrent_receives_produce_valid_unique_jsonl(self) -> None:
        def receive(index: int) -> None:
            self.run_cli(
                "receive",
                {
                    "source": "api",
                    "session_id": f"parallel-{index}",
                    "event_key": f"turn-{index}",
                    "prompt": f"병렬 요청 {index}",
                },
            )

        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(receive, range(20)))

        events = self.events()
        self.assertEqual(20, len(events))
        self.assertEqual(20, len({event["query_id"] for event in events}))

    def test_claude_hook_maps_prompt_and_stop_events(self) -> None:
        env = {**os.environ, "JUNHO_QUERY_WIKI_ROOT": str(self.root)}
        prompt_event = {
            "hook_event_name": "UserPromptSubmit",
            "session_id": "claude-session",
            "transcript_path": "/tmp/transcript.jsonl",
            "cwd": str(self.root),
            "prompt": "의도 기록을 시작해줘",
        }
        prompt_result = subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(prompt_event, ensure_ascii=False),
            text=True,
            capture_output=True,
            env=env,
        )
        self.assertEqual(0, prompt_result.returncode, prompt_result.stderr)

        stop_result = subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(
                {
                    "hook_event_name": "Stop",
                    "session_id": "claude-session",
                    "cwd": str(self.root),
                    "last_assistant_message": "위키 기록을 마쳤습니다.",
                },
                ensure_ascii=False,
            ),
            text=True,
            capture_output=True,
            env=env,
        )
        self.assertEqual(0, stop_result.returncode, stop_result.stderr)
        self.assertEqual(["query_received", "query_completed"], [e["type"] for e in self.events()])

    def test_skill_contract_explains_two_tiers_and_truth_boundary(self) -> None:
        body = (SKILL_DIR / "SKILL.md").read_text()
        required = [
            "query capture is not Intent evidence",
            "append-only",
            "topic promotion",
            "Claude Code",
            "Codex",
            "Cloudflare",
            "recursion guard",
        ]
        for phrase in required:
            self.assertIn(phrase, body)


if __name__ == "__main__":
    unittest.main()
