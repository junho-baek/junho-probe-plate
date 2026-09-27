"""Static and behavioral contracts for the Junho Plate coordinator."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
OPENAI = ROOT / "agents" / "openai.yaml"
DETECTOR = ROOT / "scripts" / "detect_plate.py"
PROMPTS = ROOT / "tests" / "prompts"
FIXTURES = ROOT / "tests" / "fixtures"


class CoordinatorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = SKILL.read_text(encoding="utf-8")
        cls.metadata = OPENAI.read_text(encoding="utf-8")

    def test_frontmatter_triggers_all_coordinator_work(self) -> None:
        frontmatter = self.skill.split("---", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^name: junho-plate$")
        description = re.search(r"(?m)^description: (.+)$", frontmatter)
        self.assertIsNotNone(description)
        normalized = description.group(1).casefold()
        for term in ("plate", "supaplate", "review", "refactor", "feature"):
            self.assertIn(term, normalized)
        self.assertIn("whether or not they derive", normalized)

    def test_detection_is_executable_and_fail_closed(self) -> None:
        self.assertIn("scripts/detect_plate.py <project-root>", self.skill)
        for state in ("CONFIRMED", "COMPATIBLE", "UNSUPPORTED"):
            self.assertIn(state, self.skill)
        self.assertNotIn("`AMBIGUOUS`", self.skill)
        self.assertRegex(self.skill, r"(?is)COMPATIBLE.*continue without a provenance question")
        self.assertRegex(self.skill, r"(?is)UNSUPPORTED.*Make no framework-specific edit.*exactly one contextual")
        self.assertRegex(self.skill, r"(?is)missing Supabase, Drizzle, Zod.*not refusal reasons")
        self.assertRegex(self.skill, r"(?is)references/.*missing or unreadable.*refuse to invent rules")

    def test_required_order_and_scope_authority_are_explicit(self) -> None:
        ordered = (
            "Detect project compatibility",
            "Inspect installed versions",
            "Establish requested scope and authority",
            "Load only relevant canonical references",
            "Classify the work as review, refactor, or feature",
            "Apply the shared hard gates",
            "Hand off to the exact sibling workflow",
            "Verify the child result",
            "End with exactly one contextual question",
        )
        positions = [self.skill.index(item) for item in ordered]
        self.assertEqual(positions, sorted(positions))
        for term in ("package.json", "lockfile", "declared ranges", "resolved versions"):
            self.assertIn(term, self.skill)
        self.assertRegex(self.skill, r"(?is)review or audit is read-only")

    def test_routes_with_host_neutral_names_without_copying_child_workflows(self) -> None:
        for sibling in (
            "junho-plate-review",
            "junho-plate-refactor",
            "junho-plate-feature",
        ):
            self.assertIn(f"`{sibling}`", self.skill)
        for term in (
            "host-neutral identifiers",
            "current host's native skill mechanism",
            "Codex",
            "Claude Code",
            "Skill tool",
            "manual user commands",
        ):
            self.assertIn(term.casefold(), self.skill.casefold())
        self.assertNotRegex(self.skill, r"\$junho-plate(?:-review|-refactor|-feature)?")
        self.assertIn("Do not copy or perform a child skill's detailed workflow", self.skill)
        self.assertNotIn("Rule ID | Status | Evidence", self.skill)

    def test_shared_skill_frontmatter_is_portable(self) -> None:
        for skill_name in (
            "junho-plate",
            "junho-plate-review",
            "junho-plate-refactor",
            "junho-plate-feature",
        ):
            skill_file = ROOT.parent / skill_name / "SKILL.md"
            frontmatter = skill_file.read_text(encoding="utf-8").split("---", 2)[1]
            keys = {
                line.split(":", 1)[0]
                for line in frontmatter.splitlines()
                if line.strip()
            }
            self.assertEqual({"name", "description"}, keys, skill_name)

    def test_shared_hard_gates_and_closing_contract_are_explicit(self) -> None:
        for prefix in ("SEC-*", "DB-*", "SUPA-*", "TS-*", "ZOD-*"):
            self.assertIn(prefix, self.skill)
        self.assertRegex(self.skill, r"(?is)never downgrade or bypass.*secret exposure")
        self.assertRegex(self.skill, r"(?is)Every response.*ends with exactly one question")
        self.assertIn("If there is nothing to fix", self.skill)

    def test_delivery_and_surface_references_are_routed_only_when_applicable(self) -> None:
        self.assertIn("delivery-build-rules.md", self.skill)
        for term in (
            "production build",
            "deployable artifact",
            "preview parity",
            "runtime dependency",
            "Cloudflare Agents SDK",
        ):
            self.assertIn(term.casefold(), self.skill.casefold())
        self.assertRegex(
            self.skill,
            r"(?is)Cloudflare Agents SDK.*supported.*task constraints.*installed capabilities",
        )

    def test_openai_metadata_is_explicit_and_coordinator_only(self) -> None:
        for key in ("display_name", "short_description", "default_prompt"):
            self.assertRegex(self.metadata, rf'(?m)^  {key}: "[^"]+"$')
        self.assertIn("$junho-plate", self.metadata)
        self.assertRegex(self.metadata, r"(?m)^  allow_implicit_invocation: true$")

    def test_prompt_fixtures_are_natural_and_detector_results_are_stable(self) -> None:
        scenarios = {
            "detect-confirmed-review.md": ("confirmed-plate", "CONFIRMED"),
            "detect-compatible-refactor.md": ("compatible-stack", "COMPATIBLE"),
            "detect-unsupported-feature.md": ("unsupported-project", "UNSUPPORTED"),
        }
        for prompt_name, (fixture_name, expected_status) in scenarios.items():
            with self.subTest(prompt=prompt_name):
                prompt = (PROMPTS / prompt_name).read_text(encoding="utf-8")
                self.assertIn(f"junho-plate/tests/fixtures/{fixture_name}", prompt)
                self.assertNotRegex(prompt, r"(?i)expected|must output|should detect|test fixture")
                completed = subprocess.run(
                    [sys.executable, str(DETECTOR), str(FIXTURES / fixture_name)],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(expected_status, json.loads(completed.stdout)["status"])


if __name__ == "__main__":
    unittest.main()
