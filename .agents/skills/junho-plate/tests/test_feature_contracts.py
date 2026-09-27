"""Contracts for proactive, proportional Plate feature implementation."""

from __future__ import annotations

import unittest
from pathlib import Path


SKILLS_ROOT = Path(__file__).resolve().parents[2]
SKILL = SKILLS_ROOT / "junho-plate-feature" / "SKILL.md"
OPENAI = SKILLS_ROOT / "junho-plate-feature" / "agents" / "openai.yaml"
FIXTURE = SKILLS_ROOT / "junho-plate" / "tests" / "fixtures" / "clean-slice"
PROMPTS = SKILLS_ROOT / "junho-plate" / "tests" / "prompts"


class FeatureContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = SKILL.read_text(encoding="utf-8")
        cls.metadata = OPENAI.read_text(encoding="utf-8")

    def test_frontmatter_and_entry_fail_closed_contract(self) -> None:
        frontmatter = self.skill.split("---", 2)[1]
        self.assertIn("name: junho-plate-feature", frontmatter)
        for term in ("Plate", "Supaplate", "Proactively", "complete", "vertical feature slice"):
            self.assertIn(term.casefold(), frontmatter.casefold())
        self.assertIn("whether or not it derives", frontmatter.casefold())
        for path in (
            "../junho-plate/SKILL.md",
            "../junho-plate/scripts/detect_plate.py",
            "../junho-plate/references/rule-catalog.json",
        ):
            self.assertIn(path, self.skill)
        for state in ("CONFIRMED", "COMPATIBLE", "UNSUPPORTED"):
            self.assertIn(state, self.skill)
        self.assertNotIn("`AMBIGUOUS`", self.skill)
        self.assertRegex(self.skill, r"(?is)COMPATIBLE.*Never ask Plate provenance")

    def test_entry_order_reuses_existing_design_and_auto_starts(self) -> None:
        ordered = (
            "Locate `../junho-plate/SKILL.md`",
            "Detect RR7 compatibility and inspect actual declared and resolved package versions",
            "Confirm that the request authorizes implementation",
            "Inspect existing domains, features, routes, schema, migrations, and public APIs",
            "Identify only unresolved decisions that materially change behavior or authority",
            "Choose the minimum justified layer set",
            "Begin implementation immediately",
        )
        positions = [self.skill.index(item) for item in ordered]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("Do not stop for plan approval", self.skill)
        self.assertIn("Do not ask for plan approval", self.skill)

    def test_only_material_decisions_pause_implementation(self) -> None:
        for decision in (
            "product behavior has multiple materially different outcomes",
            "authentication or authorization policy is missing",
            "existing data must be transformed or deleted",
            "public API compatibility would break",
            "paid or external service must be created",
            "feature requires out-of-scope refactoring",
        ):
            self.assertIn(decision, self.skill)
        self.assertRegex(self.skill, r"(?is)Ask one decision at a time.*recommend the safest likely default first.*stop without partial edits")

    def test_layer_matrix_is_proportional_and_rejects_ceremony(self) -> None:
        for shape in ("Static/presentation", "Server read/write", "Domain-complex"):
            self.assertIn(shape, self.skill)
        for forbidden_default in (
            "Never require a `domain/` directory", "class repository", "abstract factory",
            "one-call wrapper", "generic base service", "fixed file count",
        ):
            self.assertIn(forbidden_default, self.skill)
        self.assertIn("The sequence is not a requirement to create every named file or layer", self.skill)

    def test_framework_ownership_and_generated_route_types_are_explicit(self) -> None:
        for route_type in ("Route.LoaderArgs", "Route.ActionArgs", "Route.ComponentProps"):
            self.assertIn(route_type, self.skill)
        ownership = (
            ("Server reads", "`loader`"),
            ("Navigating writes", "`action` + `Form`"),
            ("Non-navigating writes", "`action` + `fetcher`"),
            ("Shareable filters and pagination", "URL search params"),
            ("Navigation or submission pending", "`useNavigation` or `fetcher.state`"),
            ("Ephemeral open, focus, selection, or draft", "`useState`"),
            ("External subscription, widget, timer, or browser API", "`useEffect` with cleanup"),
        )
        for state, owner in ownership:
            self.assertIn(f"| {state} | {owner} |", self.skill)
        for antipattern in (
            "copy loader data into state", "fetch loader-owned data in an effect",
            "watch action results in an effect", "derived-state effects",
            "reconstruct React Router pending state",
        ):
            self.assertIn(antipattern, self.skill)

    def test_route_tree_design_applies_outlet_admission_before_registration(self) -> None:
        for term in (
            "Apply the canonical Outlet admission table",
            "smallest honest route-tree shape",
            "Keep one screen's visual arrangement in screen composition",
            "stable parent responsibility across real child routes",
            "child-specific reads, mutations, validation, and authorization",
        ):
            self.assertIn(term, self.skill)

    def test_trust_authority_component_and_public_boundaries_are_complete(self) -> None:
        for boundary in ("params", "URL search params", "FormData", "environment values", "external responses"):
            self.assertIn(boundary, self.skill)
        self.assertRegex(self.skill, r"(?is)Parse them with Zod.*`z.infer`")
        self.assertRegex(self.skill, r"(?is)Authenticate and authorize.*on the server.*before execution")
        for term in (
            "raw response/error shapes in infrastructure", "raw nested Supabase join",
            "Define components at module scope", "explicit `index.ts` re-exports only",
            "separate server entrypoint",
        ):
            self.assertIn(term, self.skill)

    def test_screen_builds_semantic_view_models_for_varying_components(self) -> None:
        for term in (
            "screen prepare a presentation-ready named view model",
            "varying description, release copy, options, selected/disabled state, badges, pricing, CTA",
            "semantic visual variants",
            "item-specific literals",
            "raw persistence-record props",
            "localized-label parsing",
            "index-based semantic state",
            "semantic variants to CSS classes",
        ):
            self.assertIn(term, self.skill)

    def test_database_errors_and_tests_are_risk_driven(self) -> None:
        for term in (
            "local migrations", "owner/resource RLS", "minimum grants", "server-only",
            "safe function `search_path`", "view `security_invoker`", "generated type synchronization",
            "transaction/RPC",
        ):
            self.assertIn(term, self.skill)
        for error_class in ("normal empty state", "expected domain failure", "recoverable external failure", "unexpected system error"):
            self.assertIn(error_class, self.skill)
        self.assertIn("ErrorBoundary", self.skill)
        self.assertIn("material failure it prevents and why a cheaper", self.skill)
        for rejected in ("coverage-driven tests", "blanket E2E", "snapshots", "library re-tests", "mock-heavy"):
            self.assertIn(rejected, self.skill)

    def test_self_repair_completion_and_external_authority_are_strict(self) -> None:
        self.assertIn("automatically repair every in-scope `FAIL`", self.skill)
        for completion in (
            "`FAIL = 0`", "no unresolved hard blocker", "reason for every `WARN`",
            "passing relevant typegen/typecheck/test/build checks", "no unauthorized external effect",
        ):
            self.assertIn(completion, self.skill)
        for gate in (
            "remote Supabase migrations", "deploy", "paid service", "destructive data",
            "break a public API", "commit", "push", "unrelated feature",
        ):
            self.assertIn(gate, self.skill)
        self.assertRegex(self.skill, r"(?is)unrelated debt.*`junho-plate-refactor` candidate.*do not silently")

    def test_delivery_checks_use_real_artifact_and_preserve_git_authority(self) -> None:
        for term in (
            "BUILD-001",
            "built artifact",
            "preview and customer renderer",
            "stylesheet ownership",
            "runtime dependency",
            "AGENT-001",
            "AGENT-002",
            "checkpoint candidate",
        ):
            self.assertIn(term, self.skill)
        self.assertRegex(self.skill, r"(?is)commit.*only.*explicit.*authority")

    def test_closing_has_exactly_one_contextual_question_precedence(self) -> None:
        self.assertIn("End every user-facing turn with exactly one contextual question", self.skill)
        precedence = (
            "material decision is unresolved",
            "local migration work is complete",
            "check is blocked",
            "Otherwise recommend one adjacent feature slice",
        )
        positions = [self.skill.index(item) for item in precedence]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("Never append “anything else?”", self.skill)

    def test_metadata_is_explicit_only(self) -> None:
        self.assertIn("$junho-plate-feature", self.metadata)
        self.assertIn("allow_implicit_invocation: false", self.metadata)

    def test_fixture_and_natural_prompts_cover_proactivity_cases(self) -> None:
        self.assertTrue((FIXTURE / "app/routes.ts").is_file())
        self.assertTrue((FIXTURE / "drizzle/migrations/0000_base.sql").is_file())
        prompt_names = (
            "feature-tasks.md", "feature-permission-ambiguity.md",
            "feature-unrelated-debt.md", "feature-static-page.md",
        )
        for name in prompt_names:
            prompt = (PROMPTS / name).read_text(encoding="utf-8")
            self.assertNotRegex(
                prompt,
                r"(?i)loader|action|fetcher|zod|repository|expected file|must implement|rule id",
            )
        tasks = (PROMPTS / "feature-tasks.md").read_text(encoding="utf-8")
        for requirement in (
            "authenticated users", "/tasks", "/tasks/:taskId", "URL parameter `q`",
            "navigates to its detail page", "stays on the list", "only their own rows",
            "local database migration", "do not apply it remotely or deploy",
        ):
            self.assertIn(requirement, tasks)


if __name__ == "__main__":
    unittest.main()
