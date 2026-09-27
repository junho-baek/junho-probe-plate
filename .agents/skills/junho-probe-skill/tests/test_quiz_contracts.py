"""Static contracts for artifact-and-intent-grounded cognition quizzes."""

from __future__ import annotations

import unittest
from pathlib import Path


SKILLS = Path(__file__).resolve().parents[2]
QUIZ = SKILLS / "junho-probe-quiz" / "SKILL.md"
AGENT = SKILLS / "junho-probe-quiz" / "agents" / "openai.yaml"


class QuizContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.quiz = QUIZ.read_text(encoding="utf-8")
        cls.agent = AGENT.read_text(encoding="utf-8")

    def test_set_mode_reads_artifact_and_intent_events(self) -> None:
        for term in (
            ".junho-probe/INTENT-INDEX.md",
            ".junho-probe/intent/events.jsonl",
            "intent_anchor",
            "cross-evidence",
            "at least two",
        ):
            self.assertIn(term, self.quiz)

    def test_questions_cover_intent_technique_fusion_and_agent_boundaries(self) -> None:
        for term in (
            "rejected alternative",
            "prompt or harness change",
            "same verification",
            "Producer",
            "Judge",
            "deterministic gate",
        ):
            self.assertIn(term, self.quiz)
        self.assertIn("must include at least one agent-boundary question", self.quiz)

    def test_multi_module_questions_allow_multiple_anchors_without_answer_leakage(self) -> None:
        for term in (
            "one or more verified `file:line` anchors",
            "must not disclose the expected answer",
        ):
            self.assertIn(term, self.quiz)

    def test_judgment_rejects_conflict_with_code_or_intent_record(self) -> None:
        for term in (
            "code contradicts",
            "intent event contradicts",
            "closed-book",
            "must not reveal the answer",
        ):
            self.assertIn(term, self.quiz)

    def test_agent_prompt_names_both_evidence_channels(self) -> None:
        for term in ("file:line", "intent event", "cross-evidence"):
            self.assertIn(term, self.agent)


if __name__ == "__main__":
    unittest.main()
