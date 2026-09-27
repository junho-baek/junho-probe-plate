"""Substantive contracts for the canonical human-reference set.

These checks prevent a path-only evidence validator from accepting empty or
decorative Markdown. They intentionally verify durable decisions and evidence
provenance rather than exact prose or formatting.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"
CATALOG = REFERENCES / "rule-catalog.json"
WEMAKE_INDEX = REFERENCES / "wemake-commit-index.json"
HUMAN_REFERENCES = (
    "plate-detection.md",
    "architecture-rules.md",
    "rr7-rules.md",
    "supabase-rules.md",
    "typescript-zod-rules.md",
    "component-rules.md",
    "delivery-build-rules.md",
    "agent-runtime-rules.md",
    "review-feedback-evidence.md",
    "testing-fallback-rules.md",
    "wemake-rule-evidence.md",
    "wemake-key-diffs.md",
    "wemake-transitional-antipatterns.md",
)
WEMAKE_REFERENCES = (
    "wemake-rule-evidence.md",
    "wemake-key-diffs.md",
    "wemake-transitional-antipatterns.md",
)
WEMAKE_COMMIT_URL = re.compile(
    r"https://github\.com/nomadcoders/wemake/commit/([0-9a-f]{40})(?![0-9a-f])"
)
MARKDOWN_URL = re.compile(r"\[[^\]]+\]\((https://[^)]+)\)")


def read_reference(name: str) -> str:
    return (REFERENCES / name).read_text(encoding="utf-8")


class HumanReferenceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        cls.index = json.loads(WEMAKE_INDEX.read_text(encoding="utf-8"))
        cls.index_hashes = {record["hash"] for record in cls.index["records"]}

    def test_detection_contract_is_compatibility_first_and_version_aware(self) -> None:
        text = read_reference("plate-detection.md")
        for value in (
            "CONFIRMED",
            "COMPATIBLE",
            "UNSUPPORTED",
            "--user-confirmed",
            "declared ranges",
            "react-router `^7.5.1`",
            "@supabase/supabase-js `^2.49.1`",
            "2.49.4",
            "Zod `^3.24.2`",
            "3.24.3",
            "package 1.0",
        ):
            self.assertIn(value, text)
        self.assertRegex(text, r"(?is)Both `CONFIRMED` and `COMPATIBLE` permit automatic routing")
        self.assertRegex(text, r"(?is)--user-confirmed.*does not override.*React Router")
        self.assertRegex(text, r"(?is)React Router 7 without provenance yields `COMPATIBLE`.*without a provenance question")
        self.assertRegex(text, r"(?is)Missing Supabase, Drizzle, Zod.*does not block routing")
        self.assertRegex(text, r"(?is)UNSUPPORTED.*missing RR7 compatibility")
        hierarchy = (
            "Eligibility",
            "Installed capabilities",
            "Project structure",
            "Origin",
        )
        positions = [text.index(item) for item in hierarchy]
        self.assertEqual(positions, sorted(positions), "detection evidence hierarchy changed")

    def test_architecture_contract_is_directional_proportional_and_nonceremonial(self) -> None:
        text = read_reference("architecture-rules.md")
        for arrow in (
            "routes -> application -> domain",
            "infrastructure -> ports",
            "domain -> React/RR7/Supabase/Drizzle",
            "screen/component -> Supabase/Drizzle",
        ):
            self.assertIn(arrow, text)
        for layout in ("Static", "Server-backed", "Domain-complex"):
            self.assertIn(layout, text)
        self.assertRegex(text, r"(?is)class.*repositor.*use case.*wrapper.*not mandatory")
        precedence = (
            "Approved Junho Plate contract",
            "Security and data integrity",
            "Installed-version official documentation",
            "Plate/Supaplate structure",
            "Audited Wemake evidence",
            "Heuristics",
        )
        positions = [text.index(item) for item in precedence]
        self.assertEqual(positions, sorted(positions), "conflict precedence changed")

    def test_infrastructure_purity_separates_change_reasons_without_ceremony(self) -> None:
        text = read_reference("architecture-rules.md")
        for term in (
            "ARCH-006: infrastructure responsibility purity",
            "node:fs",
            "Entity or block factories, ordering, state transitions",
            "Read → change → write coordination",
            "CSS classes, Tailwind tokens",
            "Product fallback or seed policy",
            "Storage-specific serialization",
            "Do not fail a module for importing several infrastructure utilities",
            "skill-content-file.repository.server.ts",
            "skill-content.model.ts",
            "update-skill-content.server.ts",
            "Do not introduce a class, generic repository base, or port",
        ):
            with self.subTest(term=term):
                self.assertIn(term.casefold(), text.casefold())

    def test_framework_references_cover_the_approved_ownership_boundaries(self) -> None:
        required_terms = {
            "rr7-rules.md": (
                "loader", "action", "Form", "fetcher", "Route types", "SSR",
                "URL search params", "layout data", "pending", "status", "ErrorBoundary",
                "effect-based fetch", "action-result watcher", "duplicated loader state",
                "client-only auth",
            ),
            "supabase-rules.md": (
                "browser client", "server client", "admin client", "service role", "RLS",
                "minimum grants", "migrations", "generated database types", "search_path",
                "security_invoker", "repository error mapping", "atomic", "Realtime cleanup",
                "Drizzle ownership",
            ),
            "typescript-zod-rules.md": (
                "unknown -> Zod -> z.infer -> application input -> domain value",
                "any", "@ts-ignore", "assertion", "trust boundary", "parse once",
                "Zod 3.24.3", "https://v3.zod.dev/?id=basic-usage",
            ),
            "component-rules.md": (
                "route", "screen", "component", "index", "cohesive view model",
                "prop count", "smell", "ephemeral UI", "external synchronization",
                "public API", "presentation composition",
            ),
            "testing-fallback-rules.md": (
                "real failure", "cheaper check", "coverage quota", "snapshots",
                "visible", "bounded", "justified", "fake success", "hidden recovery",
            ),
            "delivery-build-rules.md": (
                "BUILD-001", "BUILD-002", "production artifact", "built artifact",
                "runtime dependency", "checkpoint candidate", "explicit mutation authority",
            ),
            "agent-runtime-rules.md": (
                "AGENT-001", "AGENT-002", "Cloudflare Agents SDK", "Workflows",
                "Producer", "Judge", "immutable candidate", "deterministic gate",
            ),
        }
        for name, terms in required_terms.items():
            text = read_reference(name)
            for term in terms:
                with self.subTest(name=name, term=term):
                    self.assertIn(term.casefold(), text.casefold())

    def test_screen_prepares_semantic_props_and_components_only_render_them(self) -> None:
        text = read_reference("component-rules.md")
        for term in (
            "Let the screen prepare the correct presentation contract",
            "Any value that can vary by product, route, permission, release state, or selected option",
            "Final display copy or an explicit message model",
            'variant: "sale" | "default"',
            "cta: { label, to }",
            "selected, disabled",
            'artTone: "forest" | "neutral"',
            'discount === "무료"',
            'children.includes("%")',
            "index === 0",
            "ProductSummaryViewModel",
            "The failure is hidden item-specific content or policy, not every JSX literal",
        ):
            with self.subTest(term=term):
                self.assertIn(term.casefold(), text.casefold())

    def test_rr7_outlet_admission_distinguishes_route_and_visual_layouts(self) -> None:
        rr7 = read_reference("rr7-rules.md")
        components = read_reference("component-rules.md")

        for term in (
            "Nested parent, layout route, and Outlet admission",
            "screen composition and ordinary presentation components",
            "ordinary `Layout` component",
            "nested parent route that renders `<Outlet />`",
            "pathless React Router layout route that renders `<Outlet />`",
            "route prefix",
            "manual pathname branching",
            "A long screen, one JSX wrapper, or a hypothetical future child is not enough",
            "Do not copy loader data into outlet context",
            "does not replace resource-level authorization",
            "Do not issue a `FAIL` merely because a feature has no layout route",
        ):
            with self.subTest(reference="rr7-rules.md", term=term):
                self.assertIn(term.casefold(), rr7.casefold())

        self.assertRegex(rr7, r"(?is)parent loader.*only data required across.*child loader/action own child-specific")
        self.assertRegex(rr7, r"(?is)/skills/:slug.*index child.*reviews.*curriculum.*purchase")

        for term in (
            "Screen layout versus route layout",
            "screen composition",
            "Layout component",
            "pathless layout route with `<Outlet />`",
            "Do not add a route layout merely because a screen is long",
            "pathname conditionals",
        ):
            with self.subTest(reference="component-rules.md", term=term):
                self.assertIn(term.casefold(), components.casefold())

    def test_catalog_evidence_is_concrete_and_zod_links_match_installed_major(self) -> None:
        for rule in self.catalog:
            for item in rule["plate_evidence"]:
                self.assertNotIn("Contract-derived", item, f"mislabeled Plate evidence: {rule['id']}")
                is_pinned_observation = (
                    "8449384cdfad30f20337bad6536b0c7d46a3dde5" in item
                    and "path category" in item.lower()
                )
                is_review_contract = item.startswith("Junho Plate review-derived contract:")
                self.assertTrue(
                    is_pinned_observation or is_review_contract,
                    f"unsupported Plate evidence kind: {rule['id']}",
                )
                for self_negating_claim in (
                    "does not establish domain independence",
                    "does not prove an explicit public api",
                    "names do not prove the absence of explicit any",
                ):
                    self.assertNotIn(
                        self_negating_claim,
                        item.casefold(),
                        f"self-negating evidence: {rule['id']}",
                    )
            if rule["confidence"] == "heuristic":
                continue
            has_official = any(url.startswith("https://") for url in rule["official_docs"])
            has_wemake = any(commit in self.index_hashes for commit in rule["wemake_commits"])
            has_plate = any(
                "8449384cdfad30f20337bad6536b0c7d46a3dde5" in item
                and "path category" in item.lower()
                for item in rule["plate_evidence"]
            )
            has_review_contract = any(
                item.startswith("Junho Plate review-derived contract:")
                for item in rule["plate_evidence"]
            )
            self.assertTrue(
                has_official or has_wemake or has_plate or has_review_contract,
                f"{rule['id']} lacks concrete evidence",
            )
        catalog_text = CATALOG.read_text(encoding="utf-8")
        self.assertNotIn("https://zod.dev/?id=", catalog_text)
        self.assertIn("https://v3.zod.dev/?id=basic-usage", catalog_text)

    def test_catalog_confidence_matches_its_concrete_source_kind(self) -> None:
        for rule in self.catalog:
            with self.subTest(rule=rule["id"]):
                if rule["confidence"] == "normative":
                    self.assertTrue(rule["official_docs"], "normative rule needs a primary source")
                elif rule["confidence"] == "plate-convention":
                    self.assertTrue(rule["plate_evidence"], "Plate convention needs documented evidence")
                elif rule["confidence"] == "wemake-derived":
                    self.assertTrue(rule["wemake_commits"], "Wemake-derived rule needs an audited commit")

    def test_corrected_rules_use_their_actual_source_kind(self) -> None:
        rules = {rule["id"]: rule for rule in self.catalog}
        microsoft = "https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice"
        for identifier in ("ARCH-001", "ARCH-002"):
            self.assertEqual("normative", rules[identifier]["confidence"])
            self.assertIn(microsoft, rules[identifier]["official_docs"])

        ts = rules["TS-001"]
        self.assertEqual("normative", ts["confidence"])
        self.assertEqual([], ts["plate_evidence"])
        self.assertEqual(2, len(ts["official_docs"]))

        consent = rules["SEC-003"]
        self.assertEqual("wemake-derived", consent["confidence"])
        self.assertEqual([], consent["official_docs"])
        self.assertEqual(
            ["a0d678874d1de875a6a89456c2b4221522a81ee6"],
            consent["wemake_commits"],
        )

    def test_catalog_wemake_hashes_link_back_to_the_same_rule_id(self) -> None:
        records = {record["hash"]: record for record in self.index["records"]}
        for rule in self.catalog:
            for commit in rule["wemake_commits"]:
                with self.subTest(rule=rule["id"], commit=commit):
                    self.assertRegex(commit, r"^[0-9a-f]{40}$")
                    self.assertIn(commit, records)
                    self.assertIn(rule["id"], records[commit]["rule_ids"])

    def test_every_rule_id_is_present_in_human_guidance_and_evidence_index(self) -> None:
        guides = "\n".join(read_reference(name) for name in (
            "architecture-rules.md",
            "rr7-rules.md",
            "supabase-rules.md",
            "typescript-zod-rules.md",
            "component-rules.md",
            "testing-fallback-rules.md",
            "delivery-build-rules.md",
            "agent-runtime-rules.md",
        ))
        evidence_index = read_reference("wemake-rule-evidence.md")
        for rule in self.catalog:
            with self.subTest(rule=rule["id"]):
                self.assertIn(rule["id"], guides)
                self.assertIn(f"| {rule['id']} |", evidence_index)

    def test_current_documentation_citations_have_metadata_and_rule_ids(self) -> None:
        evidence = read_reference("wemake-rule-evidence.md")
        self.assertIn("Product | Version or access date | Direct official URL | Supported Rule IDs", evidence)
        all_reference_text = "\n".join(read_reference(name) for name in HUMAN_REFERENCES)
        catalog_urls = {url for rule in self.catalog for url in rule["official_docs"]}
        for url in catalog_urls:
            with self.subTest(url=url):
                self.assertIn(f"]({url})", all_reference_text)
        for url in MARKDOWN_URL.findall(all_reference_text):
            if any(domain in url for domain in (
                "reactrouter.com", "react.dev", "supabase.com",
                "typescriptlang.org", "postgresql.org", "zod.dev",
                "learn.microsoft.com",
            )):
                self.assertRegex(
                    all_reference_text,
                    rf"(?m)^\| [^|]+ \| (?:[^|]*\d[^|]*|Accessed 2026-08-04) \| \[[^\]]+\]\({re.escape(url)}\) \| [A-Z0-9]+-\d{{3}}",
                    f"official citation lacks version/access date and Rule IDs: {url}",
                )

    def test_wemake_references_use_only_indexed_full_hashes_and_no_source_fences(self) -> None:
        for name in WEMAKE_REFERENCES:
            text = read_reference(name)
            self.assertNotIn("```", text, f"source-like code fence in {name}")
            hashes = set(WEMAKE_COMMIT_URL.findall(text))
            self.assertTrue(hashes, f"no full Wemake evidence hash in {name}")
            self.assertLessEqual(hashes, self.index_hashes, f"unknown Wemake hash in {name}")

    def test_wemake_key_diffs_cover_every_approved_transition(self) -> None:
        text = read_reference("wemake-key-diffs.md")
        for transition in (
            "Route config and layout",
            "Generated Route types",
            "Zod and ErrorBoundary",
            "Query and screen",
            "Supabase SSR",
            "loader and action",
            "Auth and RLS",
            "Form and fetcher",
            "Optimistic UI",
            "Realtime and function security",
        ):
            with self.subTest(transition=transition):
                self.assertIn(transition, text)

    def test_wemake_transitions_distinguish_risk_from_current_recommendation(self) -> None:
        text = read_reference("wemake-transitional-antipatterns.md")
        for term in (
            "deliberate delay", "debug logging", "empty client loader",
            "pre-validation assertion", "later correction", "legacy pattern",
            "teaching-transition", "legacy-risk", "not a current recommendation",
            "Introduction", "Correction",
        ):
            self.assertIn(term.casefold(), text.casefold())

    def test_license_boundary_forbids_redistribution(self) -> None:
        combined = "\n".join(read_reference(name) for name in HUMAN_REFERENCES)
        self.assertIn("user-owned local React Router 7 projects", combined)
        self.assertIn("Operate only on user-owned local projects", combined)
        self.assertRegex(
            combined,
            r"(?i)never package or redistribute Supaplate source, snippets, templates, fixtures, or builders",
        )

    def test_human_references_contain_no_unfinished_markers(self) -> None:
        banned = ("TO" + "DO", "T" + "BD", "FIX" + "ME", "<" + "placeholder>", "fill " + "this in")
        for name in HUMAN_REFERENCES:
            text = read_reference(name)
            for marker in banned:
                with self.subTest(name=name, marker=marker):
                    self.assertNotIn(marker, text)


if __name__ == "__main__":
    unittest.main()
