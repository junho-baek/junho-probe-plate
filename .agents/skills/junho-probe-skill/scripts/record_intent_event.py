#!/usr/bin/env python3
"""Append one redacted, searchable intent event and rebuild its Markdown index."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = (
    "id",
    "time",
    "phase",
    "kind",
    "original",
    "normalized_ko",
    "retrieval_en",
    "done_condition",
    "verification",
    "result",
    "evidence",
    "supersedes",
    "source",
)
ALLOWED_KINDS = {"prompt", "harness", "skill", "tool", "verification", "decision"}
ALLOWED_SOURCES = {"contemporaneous", "reconstructed"}
SECRET_PATTERNS = (
    re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bgh[opsu]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}\b", re.IGNORECASE),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    return parser.parse_args()


def redact_text(value: str) -> str:
    for pattern in SECRET_PATTERNS:
        value = pattern.sub("[REDACTED]", value)
    return value


def redact(value: Any) -> Any:
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, dict):
        return {key: redact(item) for key, item in value.items()}
    return value


def validate(event: Any) -> list[str]:
    if not isinstance(event, dict):
        return ["input must be one JSON object"]
    errors: list[str] = []
    missing = [field for field in REQUIRED_FIELDS if field not in event]
    if missing:
        errors.append(f"missing field(s): {', '.join(missing)}")
        return errors
    for field in REQUIRED_FIELDS:
        value = event[field]
        if field in {"evidence", "supersedes"}:
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                errors.append(f"{field} must be an array of strings")
        elif field == "phase":
            if not isinstance(value, (int, str)) or str(value).strip() == "":
                errors.append("phase must be a nonempty integer or string")
        elif not isinstance(value, str) or not value.strip():
            errors.append(f"{field} must be a nonempty string")
    if event.get("kind") not in ALLOWED_KINDS:
        errors.append(f"kind must be one of: {', '.join(sorted(ALLOWED_KINDS))}")
    if event.get("source") not in ALLOWED_SOURCES:
        errors.append(f"source must be one of: {', '.join(sorted(ALLOWED_SOURCES))}")
    if isinstance(event.get("id"), str) and not re.fullmatch(r"I-\d{3,}", event["id"]):
        errors.append("id must use I-NNN form")
    return errors


def canonicalize(event: dict[str, Any]) -> dict[str, Any]:
    cleaned = redact({field: event[field] for field in REQUIRED_FIELDS})
    cleaned["phase"] = str(cleaned["phase"])
    cleaned["prompt_sha256"] = hashlib.sha256(
        cleaned["original"].encode("utf-8")
    ).hexdigest()
    return cleaned


def read_events(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    events: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"events line {number} is not an object")
        events.append(value)
    return events


def cell(value: Any) -> str:
    if isinstance(value, list):
        value = ", ".join(str(item) for item in value) or "—"
    return str(value).replace("\n", " ").replace("|", "\\|")


def render_index(events: list[dict[str, Any]]) -> str:
    lines = [
        "# Intent index | 의도 인덱스",
        "",
        "Material prompts, harness/skill changes, tool choices, verification, and revised decisions.",
        "`reconstructed` entries improve retrieval but cannot retroactively raise Intent evidence.",
        "",
        "| ID | Time | Phase | Kind | Original prompt | Normalized Korean intent | English retrieval gloss | Done condition | Verification | Result | Evidence | Supersedes | Source |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for event in events:
        columns = (
            event["id"],
            event["time"],
            event["phase"],
            event["kind"],
            event["original"],
            event["normalized_ko"],
            event["retrieval_en"],
            event["done_condition"],
            event["verification"],
            event["result"],
            event["evidence"],
            event["supersedes"],
            event["source"],
        )
        lines.append("| " + " | ".join(cell(value) for value in columns) + " |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    try:
        raw = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        print(f"ERROR: invalid JSON input: {error.msg}", file=sys.stderr)
        return 2
    errors = validate(raw)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 2

    event = canonicalize(raw)
    probe_dir = args.root.expanduser().resolve() / ".junho-probe"
    intent_dir = probe_dir / "intent"
    events_path = intent_dir / "events.jsonl"
    index_path = probe_dir / "INTENT-INDEX.md"
    intent_dir.mkdir(parents=True, exist_ok=True)

    try:
        events = read_events(events_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: cannot read existing intent events: {error}", file=sys.stderr)
        return 2

    by_id = {existing.get("id"): existing for existing in events}
    existing = by_id.get(event["id"])
    if existing is not None and existing != event:
        print(f"ERROR: conflicting event id {event['id']}; append a new event and use supersedes", file=sys.stderr)
        return 3
    if existing is None:
        events.append(event)
        with events_path.open("a", encoding="utf-8") as output:
            output.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")

    index_path.write_text(render_index(events), encoding="utf-8")
    print(f"RECORDED {event['id']} source={event['source']} index={index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

