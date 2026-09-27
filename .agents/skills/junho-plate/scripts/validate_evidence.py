#!/usr/bin/env python3
"""Validate Junho Plate's evidence-bearing guardrail catalog."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "references" / "rule-catalog.json"
LATER_REFERENCE_PATHS = (
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
REQUIRED_KEYS = (
    "id", "statement", "scope", "pass", "warn", "fail", "hard_blocker",
    "exceptions", "detection", "remediation", "validation", "wemake_commits",
    "plate_evidence", "official_docs", "confidence",
)
EVIDENCE_FIELDS = ("wemake_commits", "plate_evidence", "official_docs")
ALLOWED_PREFIXES = (
    "ARCH", "RR7", "SUPA", "DB", "TS", "ZOD", "UI", "ERR", "TEST", "SEC", "BUILD", "AGENT",
)
PREFIX_TOTALS = {
    "ARCH": 8, "RR7": 6, "SUPA": 5, "DB": 5, "TS": 3,
    "ZOD": 3, "UI": 7, "ERR": 3, "TEST": 2, "SEC": 3,
    "BUILD": 2, "AGENT": 2,
}
ALLOWED_CONFIDENCE = ("normative", "plate-convention", "wemake-derived", "heuristic")
CANONICAL_HEURISTIC_FAIL = "N/A: heuristic evidence alone cannot independently produce FAIL."
BASE_ACTIONS = frozenset(("search", "inspect", "run", "trace", "query", "compile", "test", "check"))
OBSERVABLE_TARGETS = frozenset((
    "import", "graph", "module", "file", "function", "handler", "route", "action", "loader", "client",
    "credential", "secret", "policy", "table", "migration", "schema", "query", "mutation", "boundary",
    "value", "type", "input", "output", "state", "subscription", "cleanup", "path", "export", "view",
    "transaction", "rpc", "operation", "effect", "trigger", "catalog", "rule", "outcome", "test",
    "assertion", "behavior", "repository", "screen", "component", "server", "browser", "typescript", "algorithm",
    "data", "request", "response", "grant", "role", "authorization", "identity", "consent", "retry",
    "fallback", "index", "error", "catch", "permission", "bundle", "edge",
    "artifact", "dependency", "stylesheet", "renderer", "entrypoint", "agent", "workflow", "judge", "trace",
))
STYLE_UNITS = frozenset(("line", "file", "function", "prop", "statement", "component"))
STYLE_MEASURES = frozenset(("count", "length", "size", "limit", "quota", "threshold"))
EXTREME_MEASURES = frozenset(("maximum", "minimum", "max", "min"))
COMPARATIVE_CUES = frozenset(("fewer", "more", "less", "shorter", "longer", "most", "least", "exceed", "exceeds", "exceeded", "below", "above", "under", "over", "capped", "cap", "contains", "has", "exactly", "total", "exist", "exists"))
QUALITATIVE_STYLE_PAIRS = (("too", "long"), ("too", "short"), ("too", "many"), ("too", "few"), ("excessive", ""), ("oversized", ""))
NUMBER_WORDS = frozenset((
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
    "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
    "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "dozen",
))
RELATION_WORDS = frozenset(("for", "against", "before", "after", "without", "with"))
GENERIC_CLAIM_WORDS = frozenset(("all", "well", "works", "work", "correct", "valid", "compliance", "correctness", "appropriately", "carefully", "missing", "things", "thing", "look", "looks", "good", "fine", "okay", "ok"))
TOKEN_PATTERN = re.compile(r"[a-z]+|\d+")
REQUIRED_RULES = {
    "ARCH-001": "domain framework independence", "ARCH-002": "dependency direction",
    "ARCH-003": "feature public boundaries", "ARCH-004": "proportional layering",
    "ARCH-005": "application ports and use cases",
    "ARCH-006": "infrastructure responsibility purity", "RR7-001": "loader-owned server data",
    "RR7-002": "action/Form/fetcher mutations", "RR7-003": "generated route types",
    "RR7-004": "server auth and authorization", "RR7-005": "status/ErrorBoundary mapping",
    "RR7-006": "no duplicated router state", "SUPA-001": "browser/server/admin clients",
    "SUPA-002": "repository error mapping", "SUPA-003": "map raw responses at infrastructure",
    "SUPA-004": "generated database types", "SUPA-005": "realtime subscription lifecycle",
    "DB-001": "migration-tracked schema changes", "DB-002": "RLS and minimum grants",
    "DB-003": "function search_path/privileges", "DB-004": "view security_invoker review",
    "DB-005": "atomic multi-write boundary", "TS-001": "no explicit any",
    "TS-002": "no unjustified suppression/assertion", "TS-003": "no server code through client barrels",
    "ZOD-001": "validate trust boundaries", "ZOD-002": "infer input types from schema",
    "ZOD-003": "do not repeatedly parse trusted data", "UI-001": "no nested component definitions",
    "UI-002": "explicit UI props/view models", "UI-003": "index is explicit public API only",
    "UI-004": "screen composes presentation only", "UI-005": "framework-native state ownership",
    "ERR-001": "classify empty/domain/external/system", "ERR-002": "no swallowed errors or fake success",
    "ERR-003": "visible, bounded, idempotent fallback", "TEST-001": "risk-value-proportional tests",
    "TEST-002": "no tests for tests' sake", "SEC-001": "server-only secrets",
    "SEC-002": "server-side authorization", "SEC-003": "consent for remote/destructive effects",
    "ARCH-007": "runtime surface ownership", "ARCH-008": "scoped starter residue cleanup",
    "UI-006": "preview and customer renderer parity", "UI-007": "stylesheet ownership and scoping",
    "BUILD-001": "production artifact smoke verification",
    "BUILD-002": "runtime dependency cost justification",
    "AGENT-001": "Cloudflare agent runtime by default",
    "AGENT-002": "independent judge evidence boundary",
}


def tokens(value: str) -> list[str]:
    """Normalize bounded English input for the validator's vocabulary checks."""
    raw_words = TOKEN_PATTERN.findall(value.lower())
    normalized: list[str] = []
    for word in raw_words:
        y_singular = f"{word[:-3]}y" if word.endswith("ies") else ""
        regular_singular = word[:-1] if word.endswith("s") else ""
        if y_singular in OBSERVABLE_TARGETS:
            normalized.append(y_singular)
        elif regular_singular in OBSERVABLE_TARGETS or regular_singular in STYLE_UNITS:
            normalized.append(regular_singular)
        else:
            normalized.append(word)
    return normalized


def has_base_action(words: list[str]) -> bool:
    return bool(BASE_ACTIONS.intersection(words))


def has_observable_target(words: list[str]) -> bool:
    return bool(OBSERVABLE_TARGETS.intersection(words))


def meaningful(words: list[str]) -> list[str]:
    return [word for word in words if word not in GENERIC_CLAIM_WORDS and word not in {"the", "a", "an", "it", "its", "and"}]


def has_assertion_condition(words: list[str]) -> bool:
    """A confirm/verify clause must name a predicate beyond generic reassurance."""
    for index, word in enumerate(words):
        if word in {"confirm", "verify"} and len(meaningful(words[index + 1:])) >= 2:
            return True
    return False


def has_relation_condition(words: list[str]) -> bool:
    """Temporal relations need an object; other relations need two evidence tokens."""
    for index, word in enumerate(words):
        if word not in RELATION_WORDS:
            continue
        evidence = meaningful(words[index + 1:])
        if word in {"before", "after"} and evidence:
            return True
        if word not in {"before", "after"} and len(evidence) >= 2:
            return True
    return False


def is_observable_validation(value: str) -> bool:
    """Require a base action, named target, and substantive assertion or relation."""
    if not isinstance(value, str):
        return False
    words = tokens(value)
    return has_base_action(words) and has_observable_target(words) and (
        has_assertion_condition(words) or has_relation_condition(words)
    )


def is_number(word: str) -> bool:
    return word.isdigit() or word in NUMBER_WORDS


def has_qualitative_style_pair(words: list[str]) -> bool:
    if not STYLE_UNITS.intersection(words):
        return False
    for first, second in QUALITATIVE_STYLE_PAIRS:
        if second and any(words[index:index + 2] == [first, second] for index in range(len(words) - 1)):
            return True
        if not second and first in words:
            return True
    return False


def style_windows(words: list[str], distance: int = 5) -> list[list[str]]:
    windows: list[list[str]] = []
    for index, word in enumerate(words):
        if word not in STYLE_UNITS:
            continue
        if index + 1 < len(words) and is_number(words[index + 1]) and not STYLE_MEASURES.intersection(words[index + 2:index + 6]):
            continue
        end = index + distance + 1
        for boundary in words[index + 1:end]:
            if boundary in {"confirm", "verify"}:
                end = index + 1 + words[index + 1:end].index(boundary)
                break
        windows.append(words[max(0, index - distance):end])
    return windows


def has_asserted_style_metric(words: list[str]) -> bool:
    """Recognize numeric style criteria inside a confirm/verify clause in any word order."""
    for index, word in enumerate(words):
        if word not in {"confirm", "verify"}:
            continue
        clause = words[index + 1:]
        for boundary, candidate in enumerate(clause):
            if candidate in {"confirm", "verify"}:
                clause = clause[:boundary]
                break
        has_number = any(is_number(candidate) for candidate in clause)
        has_number_then_style_unit = any(
            is_number(clause[position]) and clause[position + 1] in STYLE_UNITS
            for position in range(len(clause) - 1)
        )
        explicit_count_context = {"only", "exactly", "total", "declared", "there", "contains", "has"}
        has_modified_number_then_style_unit = any(
            is_number(clause[position])
            and any(candidate in STYLE_UNITS for candidate in clause[position + 1:position + 5])
            for position in range(len(clause))
        ) and bool(explicit_count_context.intersection(clause))
        has_number_of_style_unit = "number" in clause and bool(STYLE_UNITS.intersection(clause))
        has_named_measure = bool((STYLE_MEASURES | {"number"}).intersection(clause))
        pre_assertion_style_target = bool(STYLE_UNITS.intersection(words[:index]))
        if has_number and (has_number_then_style_unit or has_modified_number_then_style_unit or has_number_of_style_unit):
            return True
        if has_number and pre_assertion_style_target and has_named_measure:
            return True
    return False


def has_style_metric(words: list[str]) -> bool:
    """Bind numbers and comparisons to the same local style-unit condition."""
    if has_asserted_style_metric(words):
        return True
    windows = style_windows(words)
    if not windows:
        return False
    if has_qualitative_style_pair(words):
        return True
    for window in windows:
        has_number = any(is_number(word) for word in window)
        has_cue = bool((STYLE_MEASURES | COMPARATIVE_CUES).intersection(window))
        if has_number and has_cue:
            return True
        if {"limit", "quota", "threshold"}.intersection(window):
            return True
        if bool(EXTREME_MEASURES.intersection(window)) and bool(STYLE_MEASURES.intersection(window)):
            return True
    if any(
        {words[index], words[index + 1]} <= {"count", "length", "size", "limit", "quota", "threshold"}
        for index in range(len(words) - 1)
    ):
        return True
    for index, word in enumerate(words):
        if word not in {"count", "length", "size"}:
            continue
        named_style_target = index > 0 and words[index - 1] in {"its", "file", "function", "component"}
        numeric_value = any(is_number(candidate) for candidate in words[index + 1:index + 4])
        if named_style_target and numeric_value:
            return True
    return False


def has_forbidden_snapshot(words: list[str]) -> bool:
    """Allow database snapshots, but reject UI/test snapshot approval or presence rules."""
    if "snapshot" not in words and "snapshots" not in words:
        return False
    context = {"test", "component", "ui", "visual", "approval"}
    criteria = {"present", "missing", "required", "approved", "baseline"}
    if context.intersection(words):
        return True
    if {"transaction", "database", "isolation"}.intersection(words):
        return False
    return bool(criteria.intersection(words))


def has_forbidden_coverage_or_ratio(value: str, words: list[str]) -> bool:
    """Reject test/code measurement, not ordinary authorization coverage or data ratios."""
    percent = "%" in value or bool({"percent", "percentage"}.intersection(words))
    coverage = bool({"coverage", "covered"}.intersection(words))
    ratio = "ratio" in words
    test_or_code_context = bool(
        {"test", "suite", "code", "line", "branch", "statement", "function", "component"}.intersection(words)
    )
    quota_context = bool({"quota", "threshold", "target", "score"}.intersection(words))
    return (
        (percent and (test_or_code_context or coverage or ratio))
        or (coverage and (test_or_code_context or quota_context))
        or (ratio and (test_or_code_context or quota_context))
    )


def has_forbidden_complexity(words: list[str]) -> bool:
    """Reject code/style complexity metrics while allowing domain/schema descriptions."""
    if "complexity" not in words:
        return False
    named_metric = bool({"cyclomatic", "cognitive", "score", "threshold", "quota"}.intersection(words))
    code_context = bool({"code", "function", "component", "algorithm", "test"}.intersection(words))
    quantified = any(is_number(word) for word in words) or bool(COMPARATIVE_CUES.intersection(words))
    return named_metric or code_context or quantified


def has_forbidden_hard_blocker_metric(value: str) -> bool:
    """Reject style/test metrics while permitting ordinary inspection evidence."""
    if not isinstance(value, str):
        return False
    words = tokens(value)
    return (
        has_forbidden_snapshot(words)
        or has_forbidden_coverage_or_ratio(value, words)
        or has_forbidden_complexity(words)
        or has_style_metric(words)
    )


def validate_catalog(catalog: Any) -> list[str]:
    """Return deterministic, human-readable catalog validation errors."""
    errors: list[str] = []
    if not isinstance(catalog, list):
        return ["catalog root must be a JSON array"]
    if len(catalog) != 49:
        errors.append(f"catalog must contain exactly 49 rules; found {len(catalog)}")

    identifiers: list[str] = []
    for position, rule in enumerate(catalog, start=1):
        label = f"rule {position}"
        if not isinstance(rule, dict):
            errors.append(f"{label} must be an object")
            continue
        if set(rule) != set(REQUIRED_KEYS):
            errors.append(f"{label} must have exactly the required field set")
            continue
        identifier = rule["id"]
        if not isinstance(identifier, str) or not re.fullmatch(r"[A-Z][A-Z0-9]*-\d{3}", identifier):
            errors.append(f"{label} id must use PREFIX-NNN form")
        else:
            identifiers.append(identifier)
            prefix = identifier.split("-", 1)[0]
            if prefix not in ALLOWED_PREFIXES:
                errors.append(f"{label} has unknown prefix {prefix}")
        for field in REQUIRED_KEYS:
            value = rule[field]
            if field == "hard_blocker":
                if type(value) is not bool:
                    errors.append(f"{label} hard_blocker must be a boolean")
            elif field in EVIDENCE_FIELDS or field == "exceptions":
                if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
                    errors.append(f"{label} {field} must be an array of nonempty strings")
            elif not isinstance(value, str) or not value.strip():
                errors.append(f"{label} {field} must be a nonempty string")
        if isinstance(rule["confidence"], str) and rule["confidence"] not in ALLOWED_CONFIDENCE:
            errors.append(f"{label} has unknown confidence {rule['confidence']}")
        if all(isinstance(rule[field], list) and not rule[field] for field in EVIDENCE_FIELDS):
            errors.append(f"{label} needs evidence in at least one evidence array")
        if rule["hard_blocker"] is True:
            validation = rule["validation"]
            if not isinstance(validation, str) or not validation.strip() or not is_observable_validation(validation):
                errors.append(f"{label} hard blocker needs observable validation")
            if has_forbidden_hard_blocker_metric(validation):
                errors.append(f"{label} hard blocker cannot use a metric criterion")
        if rule["confidence"] == "heuristic":
            if rule["hard_blocker"] is True:
                errors.append(f"{label} heuristic rule cannot be a hard blocker")
            fail_text = rule["fail"]
            if fail_text != CANONICAL_HEURISTIC_FAIL:
                errors.append(f"{label} heuristic FAIL must use the canonical nonblocking representation")

    duplicates = sorted(identifier for identifier, count in Counter(identifiers).items() if count > 1)
    if duplicates:
        errors.append(f"duplicate id(s): {', '.join(duplicates)}")
    if len(identifiers) == len(catalog):
        actual_rules = {rule["id"]: rule["statement"] for rule in catalog if isinstance(rule, dict) and "id" in rule and "statement" in rule}
        if actual_rules != REQUIRED_RULES:
            errors.append("catalog ids and statements must match the required rule set")
        totals = Counter(identifier.split("-", 1)[0] for identifier in identifiers if "-" in identifier)
        if dict(totals) != PREFIX_TOTALS:
            errors.append("catalog prefix totals do not match the required coverage")
    return errors


def validate_catalog_file(path: Path = CATALOG_PATH) -> list[str]:
    try:
        with path.open(encoding="utf-8") as source:
            return validate_catalog(json.load(source))
    except FileNotFoundError:
        return [f"catalog is missing: {path}"]
    except json.JSONDecodeError as error:
        return [f"invalid JSON in {path}: {error.msg}"]
    except UnicodeDecodeError:
        return [f"catalog is not valid UTF-8: {path}"]
    except IsADirectoryError:
        return [f"cannot read catalog {path}: path is a directory"]
    except OSError as error:
        detail = error.strerror or type(error).__name__
        return [f"cannot read catalog {path}: {detail}"]


def validate_later_references(root: Path = ROOT) -> list[str]:
    """Keep future human-reference and Wemake checks explicit and separable."""
    expected = tuple(root / relative for relative in LATER_REFERENCE_PATHS)
    return [f"later reference is missing: {path}" for path in expected if not path.is_file()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rules-only", action="store_true", help="validate only rule-catalog.json")
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH, help="catalog path to validate")
    args = parser.parse_args(argv)
    errors = validate_catalog_file(args.catalog)
    if not errors and not args.rules_only:
        errors.extend(validate_later_references())
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("49 unique rules; all twelve prefixes covered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
