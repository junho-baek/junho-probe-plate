"""Static contracts for independent three-axis auditing."""

from __future__ import annotations

import unittest
from pathlib import Path


SKILLS = Path(__file__).resolve().parents[2]
AUDIT = SKILLS / "junho-probe-audit" / "SKILL.md"


class AuditContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = AUDIT.read_text(encoding="utf-8")

    def test_intent_uses_raw_behavior_and_treats_index_as_projection(self) -> None:
        for term in (
            ".junho-probe/intent/events.jsonl",
            ".junho-probe/INTENT-INDEX.md",
            "searchable projection",
            "source: contemporaneous",
            "source: reconstructed",
            "cannot retroactively raise Intent",
        ):
            self.assertIn(term, self.audit)

    def test_technique_accepts_plate_evidence_but_not_plate_assertion(self) -> None:
        for term in (
            "$junho-plate-review",
            "executable evidence",
            "Plate scorecard",
            "does not prove",
        ):
            self.assertIn(term, self.audit)

    def test_judge_is_independent_and_read_only(self) -> None:
        for term in (
            "independent Judge",
            "read-only",
            "must not grade its own output",
            "deterministic gates",
        ):
            self.assertIn(term, self.audit)

    def test_independence_has_operational_provenance_and_no_score_shopping(self) -> None:
        for term in (
            "artifact revision or SHA-256",
            "Judge identity or context ID",
            "Evidence state: verified | missing | negative | contradictory",
            "score-shopping",
        ):
            self.assertIn(term, self.audit)


if __name__ == "__main__":
    unittest.main()
