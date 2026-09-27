"""Static contracts for intent indexing and three-axis routing."""

from __future__ import annotations

import unittest
from pathlib import Path


SKILLS = Path(__file__).resolve().parents[2]
ROUTER = SKILLS / "junho-probe-skill" / "SKILL.md"
COACH = SKILLS / "junho-probe-coach" / "SKILL.md"
BUILD = SKILLS / "junho-probe-build" / "SKILL.md"
COMMANDS = SKILLS / "junho-probe-skill" / "references" / "command-examples.md"


class ProbeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.router = ROUTER.read_text(encoding="utf-8")
        cls.coach = COACH.read_text(encoding="utf-8")
        cls.build = BUILD.read_text(encoding="utf-8")

    def test_router_indexes_material_intent_events_without_retroactive_score_claims(self) -> None:
        for term in (
            "INTENT-INDEX.md",
            "record_intent_event.py",
            "original prompt",
            "normalized Korean intent",
            "English retrieval gloss",
            "contemporaneous",
            "reconstructed",
            "cannot retroactively raise Intent",
        ):
            self.assertIn(term, self.router)

    def test_coach_and_build_record_material_prompt_and_verification_events(self) -> None:
        for skill in (self.coach, self.build):
            for term in (
                "record_intent_event.py",
                "done condition",
                "verification",
                "supersedes",
            ):
                self.assertIn(term, skill)

    def test_command_reference_covers_each_axis_and_full_loop(self) -> None:
        self.assertTrue(COMMANDS.is_file(), f"missing command reference: {COMMANDS}")
        text = COMMANDS.read_text(encoding="utf-8")
        for term in (
            "$junho-probe-coach",
            "$junho-plate-review",
            "$junho-probe-quiz",
            "$junho-probe-audit",
            "$junho-probe-skill",
            "Cloudflare Agents SDK",
            "Judge",
        ):
            self.assertIn(term, text)

    def test_build_defines_cloudflare_producer_judge_and_policy_boundaries(self) -> None:
        for term in (
            "Cloudflare Agents SDK",
            "Producer",
            "Judge",
            "immutable",
            "deterministic",
            "must not grade its own output",
        ):
            self.assertIn(term, self.build)


if __name__ == "__main__":
    unittest.main()
