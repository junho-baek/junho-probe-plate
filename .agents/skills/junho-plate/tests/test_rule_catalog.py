"""Behavioral checks for the evidence-bearing guardrail catalog."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "junho-plate" / "scripts" / "validate_evidence.py"
CATALOG_PATH = ROOT / "junho-plate" / "references" / "rule-catalog.json"


def load_validator():
    if not VALIDATOR_PATH.is_file():
        raise AssertionError(f"validator is missing: {VALIDATOR_PATH}")
    spec = importlib.util.spec_from_file_location("validate_evidence", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("validator module cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RuleCatalogTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator()

    def load_catalog(self):
        with CATALOG_PATH.open(encoding="utf-8") as source:
            return json.load(source)

    def assert_invalid(self, catalog, expected_fragment):
        errors = self.validator.validate_catalog(catalog)
        self.assertTrue(errors, "catalog should be rejected")
        self.assertIn(expected_fragment, "\n".join(errors))

    def test_catalog_has_the_complete_evidence_bearing_rule_set(self):
        catalog = self.load_catalog()
        self.assertEqual([], self.validator.validate_catalog(catalog))
        self.assertEqual(49, len(catalog))
        self.assertEqual(self.validator.PREFIX_TOTALS, {
            "ARCH": 8, "RR7": 6, "SUPA": 5, "DB": 5, "TS": 3,
            "ZOD": 3, "UI": 7, "ERR": 3, "TEST": 2, "SEC": 3,
            "BUILD": 2,
            "AGENT": 2,
        })
        actual = {rule["id"]: rule["statement"] for rule in catalog}
        self.assertEqual(self.validator.REQUIRED_RULES, actual)
        self.assertTrue(all(
            rule["wemake_commits"] or rule["plate_evidence"] or rule["official_docs"]
            for rule in catalog
        ))
        self.assertTrue(all(
            url and url.startswith("https://")
            for rule in catalog
            for url in rule["official_docs"]
        ))

    def test_catalog_uses_honest_direct_evidence_for_affected_rules(self):
        rules = {rule["id"]: rule for rule in self.load_catalog()}
        expected = {
            "SUPA-002": (
                "plate-convention",
                ["https://supabase.com/docs/guides/api/handling-errors-in-supabase-js"],
            ),
            "SUPA-003": ("plate-convention", []),
            "SUPA-004": (
                "normative",
                ["https://supabase.com/docs/guides/api/rest/generating-types"],
            ),
            "DB-001": (
                "normative",
                ["https://supabase.com/docs/guides/deployment/database-migrations"],
            ),
            "TS-001": (
                "normative",
                [
                    "https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#any",
                    "https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html#any",
                ],
            ),
            "ARCH-001": (
                "normative",
                ["https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice"],
            ),
            "ARCH-002": (
                "normative",
                ["https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice"],
            ),
            "ARCH-006": (
                "plate-convention",
                [],
            ),
            "SEC-003": (
                "wemake-derived",
                [],
            ),
        }
        for identifier, (confidence, official_docs) in expected.items():
            with self.subTest(identifier=identifier):
                self.assertEqual(confidence, rules[identifier]["confidence"])
                self.assertEqual(official_docs, rules[identifier]["official_docs"])
                joined = " ".join(rules[identifier]["official_docs"])
                self.assertNotIn("secure-data", joined)
                self.assertNotIn("noImplicitAny", joined)

    def test_ui_002_enforces_screen_owned_semantic_component_contracts(self):
        rules = {rule["id"]: rule for rule in self.load_catalog()}
        rule = rules["UI-002"]
        self.assertFalse(rule["hard_blocker"])
        for term in (
            "screen maps route or application data",
            "hardcodes product or route-specific copy",
            "imports a persistence record",
            "parsing display strings",
            "CSS tokens carried by data models",
            "index-based semantic state",
            "presentation-ready named view model",
            "semantic visual variants",
            "two representative screen view models",
        ):
            self.assertIn(term.casefold(), " ".join(str(value) for value in rule.values()).casefold())

    def test_review_derived_rules_are_explicit_and_observable(self):
        rules = {rule["id"]: rule for rule in self.load_catalog()}
        expected = {
            "ARCH-007": "runtime surface ownership",
            "ARCH-008": "scoped starter residue cleanup",
            "UI-006": "preview and customer renderer parity",
            "UI-007": "stylesheet ownership and scoping",
            "BUILD-001": "production artifact smoke verification",
            "BUILD-002": "runtime dependency cost justification",
            "AGENT-001": "Cloudflare agent runtime by default",
            "AGENT-002": "independent judge evidence boundary",
        }
        for identifier, statement in expected.items():
            with self.subTest(identifier=identifier):
                self.assertIn(identifier, rules)
                self.assertEqual(statement, rules[identifier]["statement"])
                self.assertFalse(rules[identifier]["hard_blocker"])
                self.assertTrue(self.validator.is_observable_validation(rules[identifier]["validation"]))

    def test_validator_rejects_schema_identity_and_evidence_tampering(self):
        catalog = self.load_catalog()

        malformed = [dict(rule) for rule in catalog]
        malformed[0].pop("validation")
        self.assert_invalid(malformed, "exactly")

        bad_type = [dict(rule) for rule in catalog]
        bad_type[0]["hard_blocker"] = "true"
        self.assert_invalid(bad_type, "boolean")

        blank_field = [dict(rule) for rule in catalog]
        blank_field[0]["scope"] = " "
        self.assert_invalid(blank_field, "nonempty string")

        duplicate = [dict(rule) for rule in catalog]
        duplicate[1]["id"] = duplicate[0]["id"]
        self.assert_invalid(duplicate, "duplicate id")

        bad_prefix = [dict(rule) for rule in catalog]
        bad_prefix[0]["id"] = "NOPE-001"
        self.assert_invalid(bad_prefix, "unknown prefix")

        bad_confidence = [dict(rule) for rule in catalog]
        bad_confidence[0]["confidence"] = "guessed"
        self.assert_invalid(bad_confidence, "confidence")

        no_evidence = [dict(rule) for rule in catalog]
        for field in self.validator.EVIDENCE_FIELDS:
            no_evidence[0][field] = []
        self.assert_invalid(no_evidence, "evidence")

    def test_validator_rejects_unsafe_hard_blocker_and_heuristic_claims(self):
        catalog = self.load_catalog()

        generic_blocker = [dict(rule) for rule in catalog]
        generic_blocker[0]["hard_blocker"] = True
        generic_blocker[0]["validation"] = "Review the implementation carefully."
        self.assert_invalid(generic_blocker, "observable validation")

        heuristic_blocker = [dict(rule) for rule in catalog]
        heuristic_blocker[0]["confidence"] = "heuristic"
        heuristic_blocker[0]["hard_blocker"] = True
        self.assert_invalid(heuristic_blocker, "heuristic")

        heuristic_fail = [dict(rule) for rule in catalog]
        heuristic_fail[0]["confidence"] = "heuristic"
        heuristic_fail[0]["hard_blocker"] = False
        heuristic_fail[0]["fail"] = "FAIL: component is large."
        self.assert_invalid(heuristic_fail, "canonical nonblocking representation")

        metric_blocker = [dict(rule) for rule in catalog]
        metric_blocker[0]["hard_blocker"] = True
        metric_blocker[0]["validation"] = "FAIL when a file exceeds 300 lines."
        self.assert_invalid(metric_blocker, "metric criterion")

        observable_inspection = [dict(rule) for rule in catalog]
        observable_inspection[0]["validation"] = (
            "Inspect the file and confirm the function imports no framework module."
        )
        self.assertEqual([], self.validator.validate_catalog(observable_inspection))

    def test_observable_validation_requires_a_target_and_expected_condition(self):
        rejected = (
            "Check compliance.",
            "Verify correctness.",
            "Inspect appropriately.",
            "Review the import graph.",
            "Inspect the server handler.",
            "Inspect the server handler and confirm.",
            "Confirm the file.",
            "Inspect the file for missing.",
            "Inspect the server handler and confirm all is well.",
            "Inspect the server handler and verify it works.",
            "Inspect the server handler and confirm it is valid.",
            "Inspect the server handler and confirm things look good.",
        )
        accepted = (
            "Inspect the domain import graph and confirm no React edge reaches domain code.",
            "Inspect the server handler and confirm authorization precedes the protected mutation.",
            "Search browser output and confirm no service-role secret is serialized.",
            "Search TypeScript source and confirm explicit any is absent from maintained contracts.",
            "Inspect the table and confirm RLS policy protects its operations.",
            "Inspect the server handler for authorization before mutation.",
            "Search the browser bundle for serialized service-role secrets.",
            "Run the authorization test and verify denial occurs before mutation.",
            "Inspect the function for unsafe assertions.",
            "Inspect the file for explicit any.",
            "Search the dependency graph for forbidden upward edges.",
            "Inspect queries and confirm unauthorized rows are never returned.",
            "Inspect policies and confirm anonymous users are denied.",
        )
        for value in rejected:
            with self.subTest(value=value):
                self.assertFalse(self.validator.is_observable_validation(value))
        for value in accepted:
            with self.subTest(value=value):
                self.assertTrue(self.validator.is_observable_validation(value))

    def test_hard_blockers_reject_metric_criteria_without_rejecting_inspection(self):
        catalog = self.load_catalog()
        forbidden = (
            "Inspect the component and confirm its snapshot is present.",
            "Run the test suite and confirm at least 80 percent of lines are covered.",
            "Inspect the file and confirm it contains at most 10 exported functions.",
            "Inspect the function and confirm its length is less than 40 statements.",
            "Inspect the file and confirm it is no longer than 300 lines.",
            "Inspect the algorithm and confirm complexity is at most 10.",
            "Inspect the algorithm and confirm complexity score is below 10.",
            "Inspect the algorithm and confirm cyclomatic complexity is under 10.",
            "Inspect the algorithm and confirm cognitive complexity is under 10.",
            "Inspect the file and confirm it has fewer than ten functions.",
            "Inspect the component and confirm it has no more than a dozen props.",
            "Inspect the function and confirm it is shorter than forty statements.",
            "Inspect the file and confirm it does not exceed three hundred lines.",
            "Inspect the file and confirm it is below the configured line limit.",
            "Inspect the function and confirm it is within the configured length limit.",
            "Inspect the component and confirm it has ten props or fewer.",
            "Inspect the file and confirm it is capped at three hundred lines.",
            "Inspect the file and confirm its maximum length is 300 lines.",
            "Inspect the function and confirm it is too long.",
            "Inspect the function and confirm it is too short.",
            "Inspect the component and confirm it has too many props.",
            "Inspect the component and confirm it has too few props.",
            "Inspect the files and confirm there are too many.",
            "Run the test and confirm 80% of branches execute.",
            "Inspect the file and confirm it contains 300 lines.",
            "Inspect the component and confirm exactly 10 props exist.",
            "Inspect the function and confirm its length is 40.",
            "Inspect the file and confirm its size is 2 MB.",
            "Inspect the file and confirm its count is 10.",
            "Inspect the component snapshot of database results and confirm the baseline is approved.",
            "Inspect the test transaction snapshot and confirm the required baseline is present.",
            "Inspect the function and confirm the length is 40.",
            "Inspect the component and confirm the number of props is 10.",
            "Inspect the component and confirm 10 props are declared.",
            "Inspect the file and confirm there are 10 functions.",
            "Inspect the file and confirm file 2 contains 300 lines.",
            "Inspect the route and confirm only 2 privileged functions are declared.",
            "Inspect the component and confirm only 10 public props are declared.",
            "Inspect the repository and confirm only 10 source files are declared.",
        )
        for criterion in forbidden:
            with self.subTest(criterion=criterion):
                self.assertTrue(self.validator.has_forbidden_hard_blocker_metric(criterion))
                tampered = [dict(rule) for rule in catalog]
                tampered[0]["validation"] = criterion
                self.assert_invalid(tampered, "metric criterion")

        allowed = [dict(rule) for rule in catalog]
        allowed[0]["validation"] = (
            "Inspect the file and confirm its function imports no framework module."
        )
        self.assertEqual([], self.validator.validate_catalog(allowed))

        for validation in (
            "Inspect the transaction snapshot and confirm protected rows remain isolated.",
            "Inspect the 2 privileged functions and confirm authorization precedes mutation.",
            "Inspect the function and confirm minimum privileges are granted.",
            "Inspect the 2 privileged functions and confirm grants exceed user permissions.",
            "Inspect the transaction snapshot and confirm required rows remain atomic.",
            "Inspect the database transaction snapshot and confirm a protected row is present.",
            "Inspect the route and confirm function 2 enforces authorization.",
            "Inspect the browser bundle and confirm file 2 contains no secrets.",
            "Inspect authorization coverage and confirm every protected route checks permission.",
            "Inspect schema complexity and confirm migration behavior remains deterministic.",
            "Inspect the data ratio and confirm the protected invariant is preserved.",
        ):
            with self.subTest(validation=validation):
                self.assertFalse(self.validator.has_forbidden_hard_blocker_metric(validation))
                allowed = [dict(rule) for rule in catalog]
                allowed[0]["validation"] = validation
                self.assertEqual([], self.validator.validate_catalog(allowed))

    def test_future_reference_contract_is_exact_and_deterministic(self):
        expected = (
            "references/architecture-rules.md",
            "references/rr7-rules.md",
            "references/supabase-rules.md",
            "references/typescript-zod-rules.md",
            "references/component-rules.md",
            "references/delivery-build-rules.md",
            "references/agent-runtime-rules.md",
            "references/review-feedback-evidence.md",
            "references/testing-fallback-rules.md",
            "references/plate-detection.md",
            "references/wemake-commit-index.json",
            "references/wemake-commit-index.md",
            "references/wemake-rule-evidence.md",
            "references/wemake-key-diffs.md",
            "references/wemake-transitional-antipatterns.md",
        )
        self.assertTrue(
            hasattr(self.validator, "LATER_REFERENCE_PATHS"),
            "validator must export LATER_REFERENCE_PATHS",
        )
        self.assertEqual(expected, self.validator.LATER_REFERENCE_PATHS)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            errors = self.validator.validate_later_references(root=root)
        self.assertEqual(
            [f"later reference is missing: {root / relative}" for relative in expected],
            errors,
        )

    def test_heuristic_fail_uses_only_the_canonical_nonblocking_representation(self):
        catalog = self.load_catalog()
        accepted = [dict(rule) for rule in catalog]
        accepted[0]["confidence"] = "heuristic"
        accepted[0]["hard_blocker"] = False
        accepted[0]["fail"] = "N/A: heuristic evidence alone cannot independently produce FAIL."
        self.assertEqual([], self.validator.validate_catalog(accepted))

        contradictory = [dict(rule) for rule in accepted]
        contradictory[0]["fail"] = (
            "FAIL: independently reject it. This cannot independently produce FAIL."
        )
        self.assert_invalid(contradictory, "canonical nonblocking representation")

    def test_file_validation_reports_json_errors_without_traceback(self):
        with tempfile.TemporaryDirectory() as temporary:
            malformed_path = Path(temporary) / "bad-catalog.json"
            malformed_path.write_text("{not json", encoding="utf-8")
            errors = self.validator.validate_catalog_file(malformed_path)
        self.assertEqual(1, len(errors))
        self.assertIn("invalid JSON", errors[0])

    def test_file_and_cli_validation_report_unreadable_catalogs_without_traceback(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            invalid_utf8 = root / "invalid-utf8.json"
            invalid_utf8.write_bytes(b"[\xff]")
            cases = ((invalid_utf8, "UTF-8"), (root, "cannot read catalog"))
            for path, expected in cases:
                with self.subTest(path=path):
                    try:
                        errors = self.validator.validate_catalog_file(path)
                    except Exception as error:  # pragma: no cover - regression guard
                        self.fail(f"validate_catalog_file raised {type(error).__name__}")
                    self.assertEqual(1, len(errors))
                    self.assertIn(expected, errors[0])
                    completed = subprocess.run(
                        [sys.executable, str(VALIDATOR_PATH), "--rules-only", "--catalog", str(path)],
                        check=False,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(1, completed.returncode)
                    self.assertIn(expected, completed.stdout)
                    self.assertNotIn("Traceback", completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
