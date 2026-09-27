"""Behavioral contracts for the Probe intent-event index."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "record_intent_event.py"


class IntentIndexTests(unittest.TestCase):
    def test_recorder_exists_before_behavior_contracts_run(self) -> None:
        self.assertTrue(SCRIPT.is_file(), f"missing intent recorder: {SCRIPT}")

    def run_recorder(self, workspace: Path, event: dict[str, object]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(workspace)],
            input=json.dumps(event, ensure_ascii=False),
            capture_output=True,
            text=True,
        )

    def sample_event(self) -> dict[str, object]:
        return {
            "id": "I-001",
            "time": "2026-09-27T17:00:00+09:00",
            "phase": 3,
            "kind": "prompt",
            "original": "Admin preview와 고객 renderer를 하나로 만들어줘",
            "normalized_ko": "동일한 발행 view model을 공유 renderer로 표시한다.",
            "retrieval_en": "Share one renderer for admin preview and customer output.",
            "done_condition": "동일 fixture의 의미상 출력이 일치한다.",
            "verification": "npm run test:preview-parity",
            "result": "PASS",
            "evidence": ["tests/preview-parity.test.ts:18"],
            "supersedes": [],
            "source": "contemporaneous",
        }

    def test_records_jsonl_and_searchable_korean_english_index(self) -> None:
        if not SCRIPT.is_file():
            self.skipTest("RED: recorder not implemented")
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            completed = self.run_recorder(workspace, self.sample_event())
            self.assertEqual(0, completed.returncode, completed.stderr)

            event_path = workspace / ".junho-probe" / "intent" / "events.jsonl"
            index_path = workspace / ".junho-probe" / "INTENT-INDEX.md"
            stored = json.loads(event_path.read_text(encoding="utf-8").strip())
            index = index_path.read_text(encoding="utf-8")

            self.assertEqual("I-001", stored["id"])
            self.assertIn("동일한 발행 view model", index)
            self.assertIn("Share one renderer", index)
            self.assertIn("npm run test:preview-parity", index)
            self.assertIn("tests/preview-parity.test.ts:18", index)

    def test_redacts_likely_secrets_before_persistence(self) -> None:
        if not SCRIPT.is_file():
            self.skipTest("RED: recorder not implemented")
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            event = self.sample_event()
            event["original"] = "Use token sk-proj-abcdefghijklmnopqrstuvwxyz123456"
            completed = self.run_recorder(workspace, event)
            self.assertEqual(0, completed.returncode, completed.stderr)
            combined = "\n".join(
                path.read_text(encoding="utf-8")
                for path in (workspace / ".junho-probe").rglob("*")
                if path.is_file()
            )
            self.assertNotIn("sk-proj-abcdefghijklmnopqrstuvwxyz123456", combined)
            self.assertIn("[REDACTED]", combined)

    def test_same_id_is_idempotent_but_conflicting_rewrite_is_rejected(self) -> None:
        if not SCRIPT.is_file():
            self.skipTest("RED: recorder not implemented")
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            event = self.sample_event()
            first = self.run_recorder(workspace, event)
            same = self.run_recorder(workspace, event)
            changed = dict(event)
            changed["result"] = "FAIL"
            conflict = self.run_recorder(workspace, changed)

            self.assertEqual(0, first.returncode, first.stderr)
            self.assertEqual(0, same.returncode, same.stderr)
            self.assertNotEqual(0, conflict.returncode)
            lines = (workspace / ".junho-probe" / "intent" / "events.jsonl").read_text(
                encoding="utf-8"
            ).splitlines()
            self.assertEqual(1, len(lines))


if __name__ == "__main__":
    unittest.main()

