"""Contracts for authority-aware, one-slice Plate refactoring."""

from __future__ import annotations

import unittest
from pathlib import Path


SKILLS_ROOT = Path(__file__).resolve().parents[2]
SKILL = SKILLS_ROOT / "junho-plate-refactor" / "SKILL.md"
OPENAI = SKILLS_ROOT / "junho-plate-refactor" / "agents" / "openai.yaml"
FIXTURE = SKILLS_ROOT / "junho-plate" / "tests" / "fixtures" / "tangled-slice"
PROMPTS = SKILLS_ROOT / "junho-plate" / "tests" / "prompts"


class RefactorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = SKILL.read_text(encoding="utf-8")
        cls.metadata = OPENAI.read_text(encoding="utf-8")

    def test_frontmatter_and_core_fail_closed_contract(self) -> None:
        frontmatter = self.skill.split("---", 2)[1]
        self.assertIn("name: junho-plate-refactor", frontmatter)
        for term in (
            "Plate",
            "Supaplate",
            "one existing feature slice",
            "without requesting plan or file-list approval",
        ):
            self.assertIn(term.casefold(), frontmatter.casefold())
        self.assertIn("whether or not it derives", frontmatter.casefold())
        for path in (
            "../junho-plate/SKILL.md",
            "../junho-plate/scripts/detect_plate.py",
            "../junho-plate/references/rule-catalog.json",
        ):
            self.assertIn(path, self.skill)
        self.assertRegex(self.skill, r"(?is)Fail closed without edits.*missing")
        self.assertRegex(self.skill, r"(?is)Mutation is allowed for `CONFIRMED` and `COMPATIBLE`")
        self.assertIn("never ask Plate provenance for a compatible project", self.skill)
        self.assertIn("continue for `CONFIRMED` or `COMPATIBLE`", self.skill)

    def test_explicit_change_request_executes_without_redundant_approval(self) -> None:
        self.assertRegex(
            self.skill,
            r"(?is)explicit change request.*mutation authority.*refactor it.*fix everything in that scorecard/table.*do not ask.*approve the same scope again",
        )
        self.assertIn("working file list is an audit trail, not a consent mechanism", self.skill)
        self.assertIn("Do not ask for plan approval, filename approval, or a second confirmation", self.skill)
        self.assertRegex(
            self.skill,
            r"(?is)scope notification, not an approval request.*Do not stop.*continue into implementation in the same turn",
        )
        for obsolete_gate in (
            "first turn is always read-only",
            "valid approval is a later response",
            "STOP and ask exactly one recommended approval question",
        ):
            self.assertNotIn(obsolete_gate, self.skill)

    def test_review_or_direction_request_remains_read_only(self) -> None:
        self.assertRegex(self.skill, r"(?is)how would you refactor this.*direction.*review/audit/explanation.*read-only")
        for prohibited in (
            "edit files", "format or autofix", "install dependencies", "update lockfiles",
            "generate route/database types", "create or apply migrations", "update snapshots",
            "create commits", "push", "remote database", "deploy",
        ):
            self.assertIn(prohibited, self.skill)
        self.assertRegex(self.skill, r"(?is)scorecard before the proposal.*exactly one contextual question")

    def test_assessment_reports_behavior_files_dependencies_and_exclusions(self) -> None:
        for field in (
            "Target slice:", "Preserve:", "Working files:",
            "Inspection-only dependencies:", "Explicitly excluded:", "Planned validation:",
        ):
            self.assertIn(field, self.skill)
        self.assertIn("| Rule ID | Status | Evidence | Risk | Recommendation | Blocking |", self.skill)
        self.assertRegex(self.skill, r"(?is)no `FAIL` and no actionable `WARN`.*do not manufacture")
        self.assertRegex(
            self.skill,
            r"(?is)ARCH-006.*exact destination model/domain, application, or presentation files.*Working files.*in-place editing is incomplete",
        )
        self.assertRegex(
            self.skill,
            r"(?is)UI-002.*screen that can prepare the presentation contract.*component/view-model files.*Working files.*component-only patch",
        )

    def test_authorized_execution_is_ordered_and_proportional(self) -> None:
        ordered = (
            "Capture the current observable behavior",
            "Add the smallest characterization test",
            "Repair trust-boundary input and unsafe types",
            "Make the route a React Router 7 adapter",
            "Extract an application operation or port",
            "Add domain code only for a real business invariant",
            "Isolate Supabase, Drizzle, and external APIs",
            "Make screen, component, and index presentation-only",
            "Classify errors and remove hidden fallback",
            "Run proportional type generation, typecheck, relevant tests, and build checks",
            "Re-run the same scorecard",
        )
        positions = [self.skill.index(item) for item in ordered]
        self.assertEqual(positions, sorted(positions))
        self.assertRegex(self.skill, r"(?is)characterization test only when a named regression risk.*cheaper check insufficient")
        self.assertIn("This order does not require every layer", self.skill)

    def test_route_tree_refactor_requires_a_real_outlet_boundary(self) -> None:
        for term in (
            "canonical Outlet admission table",
            "Do not introduce an Outlet-bearing parent merely to shorten a screen",
            "stable parent shell",
            "real child routes",
            "child-specific loader/action ownership",
            "resource authorization",
        ):
            self.assertIn(term, self.skill)

    def test_refactor_extracts_mixed_responsibilities_without_class_ceremony(self) -> None:
        for term in (
            "Move reusable factories, ordering, state transitions, and fallback product policy out of infrastructure",
            "read-modify-write coordination",
            "filesystem, Supabase, Drizzle, database, network, and vendor modules limited to I/O",
            "move CSS/Tailwind tokens to presentation",
            "Apply `ARCH-006` by change reason, not file size or function count",
            "plain functions",
            "Do not manufacture a class, generic repository base, or one-call wrapper",
        ):
            self.assertIn(term, self.skill)

    def test_refactor_moves_varying_content_into_screen_owned_semantic_props(self) -> None:
        for term in (
            "screen map route/application data into explicit semantic props or a cohesive named view model",
            "varying copy, status, options, pricing, CTA, and visual variants",
            "Apply `UI-002` by meaning, not prop count",
            "Remove item-specific literals from reusable components",
            "display-label parsing and index-based semantics",
            "semantic-to-CSS mapping in presentation",
            "raw persistence records",
        ):
            self.assertIn(term, self.skill)

    def test_in_slice_expansion_is_autonomous_but_material_boundaries_require_authority(self) -> None:
        self.assertRegex(self.skill, r"(?is)Before every edit.*requested slice.*necessary adjacent dependency")
        self.assertRegex(
            self.skill,
            r"(?is)newly discovered file.*same behavior-preserving slice.*announce.*continue without approval",
        )
        for boundary in (
            "explicitly excluded or unrelated feature",
            "change a public API",
            "material product/permission/data decision",
            "require external state",
        ):
            self.assertIn(boundary, self.skill)
        self.assertIn("one feature slice per run", self.skill)
        for gate in (
            "supabase db push", "deployment", "paid-service creation",
            "data conversion or deletion", "commit", "push", "public API breakage",
        ):
            self.assertIn(gate, self.skill)

    def test_completion_requires_zero_fail_and_green_relevant_checks(self) -> None:
        for term in (
            "`FAIL = 0`", "hard blockers", "every retained `WARN`", "type, test, and build checks pass",
            "preserved behaviors", "inside the reported working scope", "no hidden fallback",
        ):
            self.assertIn(term, self.skill)
        self.assertRegex(self.skill, r"(?is)If any condition is false.*incomplete work truthfully")

    def test_refactor_closes_review_derived_delivery_gaps_without_overarchitecture(self) -> None:
        for term in (
            "ARCH-007",
            "ARCH-008",
            "UI-006",
            "UI-007",
            "BUILD-001",
            "BUILD-002",
            "AGENT-001",
            "AGENT-002",
            "checkpoint candidate",
        ):
            self.assertIn(term, self.skill)
        self.assertIn("Do not require separate processes or deployments", self.skill)
        self.assertRegex(self.skill, r"(?is)commit.*only.*explicit.*authority")

    def test_exactly_one_contextual_question_contract_has_precedence(self) -> None:
        self.assertIn("End every user-facing turn with exactly one contextual question", self.skill)
        precedence = (
            "remote migration is ready",
            "material boundary decision is required",
            "successful local refactor",
            "no issue exists",
            "read-only assessment",
        )
        positions = [self.skill.index(item) for item in precedence]
        self.assertEqual(positions, sorted(positions))

    def test_skill_does_not_copy_catalog_schema_or_rule_bodies(self) -> None:
        for forbidden in ("wemake_commits", "plate_evidence", "official_docs", '"hard_blocker"', '"remediation"'):
            self.assertNotIn(forbidden, self.skill)
        self.assertLess(self.skill.count("PASS:"), 2)
        self.assertLess(self.skill.count("FAIL:"), 2)

    def test_metadata_is_explicit_only(self) -> None:
        self.assertIn("$junho-plate-refactor", self.metadata)
        self.assertIn("allow_implicit_invocation: false", self.metadata)
        self.assertIn("avoiding redundant plan approval", self.metadata)

    def test_fixture_and_prompts_encode_behavior_without_priming_findings(self) -> None:
        source = "\n".join(path.read_text(encoding="utf-8") for path in FIXTURE.rglob("*") if path.is_file())
        for signal in (
            "useEffect", "useState<any[]>", "fetch(\"/tasks\"", "function TaskRow",
            "supabase.from", "search", "toggleTask", 'export * from "../../core/supabase/server"',
            'billing/internal/billing-policy',
        ):
            self.assertIn(signal, source)

        prompt_names = (
            "refactor-assess.md", "refactor-approved.md", "refactor-no-findings.md",
            "refactor-scope-expansion.md",
        )
        for name in prompt_names:
            prompt = (PROMPTS / name).read_text(encoding="utf-8")
            self.assertNotRegex(prompt, r"(?i)must fix|expected finding|should detect|rule id")
        assessment = (PROMPTS / "refactor-assess.md").read_text(encoding="utf-8")
        self.assertRegex(assessment, r"(?is)review.*do not change files")
        execution = (PROMPTS / "refactor-approved.md").read_text(encoding="utf-8")
        self.assertIn("Fix every item in the guardrail scorecard you just showed me", execution)


if __name__ == "__main__":
    unittest.main()
