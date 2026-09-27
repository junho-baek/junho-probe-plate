"""Contracts for the strictly read-only Junho Plate review workflow."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


SKILLS_ROOT = Path(__file__).resolve().parents[2]
SKILL_PATH = SKILLS_ROOT / "junho-plate-review" / "SKILL.md"
OPENAI_PATH = SKILLS_ROOT / "junho-plate-review" / "agents" / "openai.yaml"
FIXTURES = SKILLS_ROOT / "junho-plate" / "tests" / "fixtures"
PROMPT = SKILLS_ROOT / "junho-plate" / "tests" / "prompts" / "review-read-only.md"


class ReviewContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = SKILL_PATH.read_text(encoding="utf-8")
        cls.metadata = OPENAI_PATH.read_text(encoding="utf-8")

    def test_frontmatter_is_specific_to_read_only_plate_review(self) -> None:
        frontmatter = self.skill.split("---", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^name: junho-plate-review$")
        for term in ("Plate", "Supaplate", "read-only", "review", "audit"):
            self.assertIn(term.casefold(), frontmatter.casefold())
        self.assertIn("whether or not it derives", frontmatter.casefold())

    def test_compatible_rr7_projects_do_not_require_plate_provenance(self) -> None:
        self.assertIn("Continue for `CONFIRMED` and `COMPATIBLE`", self.skill)
        self.assertIn("Never ask a compatible project's Plate provenance", self.skill)
        self.assertNotIn("`AMBIGUOUS`", self.skill)

    def test_canonical_sibling_references_are_explicit(self) -> None:
        for name in (
            "rule-catalog.json",
            "architecture-rules.md",
            "rr7-rules.md",
            "supabase-rules.md",
            "typescript-zod-rules.md",
            "component-rules.md",
            "testing-fallback-rules.md",
        ):
            self.assertIn(f"../junho-plate/references/{name}", self.skill)
        self.assertIn("../junho-plate/scripts/detect_plate.py", self.skill)

    def test_read_only_boundary_covers_every_mutation_surface(self) -> None:
        for term in (
            "files", "formatting", "autofix", "dependencies", "lockfiles",
            "migrations", "generated", "caches", "Git state", "external services",
            "database rows", "--fix", "--write",
        ):
            self.assertIn(term.casefold(), self.skill.casefold())
        self.assertRegex(self.skill, r"(?is)git status --short.*before and after")
        self.assertRegex(self.skill, r"(?is)If no safe alternative exists.*not run")

    def test_scope_is_one_slice_plus_necessary_adjacent_dependencies(self) -> None:
        self.assertIn("one feature slice and necessary adjacent dependencies", self.skill)
        for term in ("route", "schemas", "application/domain", "ports/adapters", "screen/components", "public index"):
            self.assertIn(term, self.skill)
        self.assertIn("Do not turn one feature review into a whole-repository", self.skill)

    def test_scorecard_contract_has_statuses_evidence_and_blocking(self) -> None:
        self.assertIn("| Rule ID | Status | Evidence | Risk | Recommendation | Blocking |", self.skill)
        for status in ("PASS", "WARN", "FAIL", "N/A"):
            self.assertIn(f"`{status}`", self.skill)
        for blocking in ("`Hard`", "`Soft`"):
            self.assertIn(blocking, self.skill)
        self.assertIn("file:line", self.skill)
        self.assertIn("Never create an overall numeric score", self.skill)
        self.assertIn("specific reason and future trigger for every WARN", self.skill)

    def test_route_family_review_distinguishes_every_layout_shape(self) -> None:
        for term in (
            "canonical Outlet admission table",
            "screen composition",
            "ordinary Layout component",
            "nested parent route",
            "pathless layout route",
            "route prefix",
            "do not treat screen length alone as evidence",
        ):
            self.assertIn(term, self.skill)

    def test_review_reports_mixed_infrastructure_responsibility_as_soft_fail(self) -> None:
        for term in (
            "ARCH-006",
            "node:fs",
            "all exported and reusable behavior",
            "`Soft` `FAIL`",
            "entity factories",
            "read-modify-write use-case orchestration",
            "product fallback policy",
            "CSS/Tailwind presentation tokens",
            "storage-specific serialization",
            "trivial policy-free projection",
        ):
            self.assertIn(term, self.skill)

    def test_review_checks_screen_owned_semantic_props_for_varying_components(self) -> None:
        for term in (
            "UI-002",
            "compare at least two plausible items or states",
            "description, release copy, options, selected/disabled state, badges, pricing, CTA",
            "item-specific literals",
            "persistence/data record as its public contract",
            "localized display labels",
            "array position as real selection state",
            "stable component-owned chrome",
            "semantic-variant-to-CSS mapping",
        ):
            self.assertIn(term, self.skill)

    def test_priority_completion_and_closing_are_strict(self) -> None:
        priorities = (
            "Security and authorization",
            "Data integrity and database policy",
            "Type safety and input validation",
            "React Router/framework ownership",
            "Architecture and dependency direction",
            "Components and state ownership",
            "Error, fallback, and justified tests",
            "Optional polish",
        )
        positions = [self.skill.index(item) for item in priorities]
        self.assertEqual(positions, sorted(positions))
        self.assertRegex(self.skill, r"(?is)Do not claim.*ready or complete.*Hard.*type/test failure")
        self.assertRegex(self.skill, r"(?is)no applicable `FAIL` or `WARN`.*no change is recommended")
        self.assertRegex(self.skill, r"(?is)End the response with exactly one contextual question")

    def test_review_checks_runtime_surfaces_preview_css_build_and_dependency_cost(self) -> None:
        for term in (
            "ARCH-007",
            "ARCH-008",
            "UI-006",
            "UI-007",
            "BUILD-001",
            "BUILD-002",
            "AGENT-001",
            "AGENT-002",
            "built artifact",
        ):
            self.assertIn(term, self.skill)
        self.assertIn("Do not require separate processes or deployments", self.skill)

    def test_metadata_disallows_implicit_invocation(self) -> None:
        self.assertIn("$junho-plate-review", self.metadata)
        self.assertRegex(self.metadata, r"(?m)^  allow_implicit_invocation: false$")

    def test_synthetic_fixtures_encode_clean_and_violation_cases(self) -> None:
        clean = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (FIXTURES / "review-clean").rglob("*.ts*")
        )
        violations = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (FIXTURES / "review-violations").rglob("*.ts*")
        )
        for clean_term in ("noteSchema.parse", "<Form", "NoteScreen", "NoteCardProps"):
            self.assertIn(clean_term, clean)
        for violation_term in (
            "supabase.from", "useEffect", ": any", "function NoteRow",
            'export * from "./queries/note.server"', "return []",
            'formData.get("title") as string',
        ):
            self.assertIn(violation_term, violations)

        prompt = PROMPT.read_text(encoding="utf-8")
        self.assertIn("checksum_command:", prompt.split("---", 2)[1])
        natural_request = prompt.split("---", 2)[2]
        self.assertIn("review-violations", natural_request)
        self.assertNotRegex(natural_request, r"(?i)expected|must find|should report")


if __name__ == "__main__":
    unittest.main()
