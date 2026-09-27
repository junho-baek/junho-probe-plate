from __future__ import annotations

import json
from pathlib import Path


SKILLS_ROOT = Path(__file__).resolve().parents[2]
CORE_ROOT = SKILLS_ROOT / "junho-plate"
REFERENCES_ROOT = CORE_ROOT / "references"


def read_text(relative_path: str) -> str:
    return (SKILLS_ROOT / relative_path).read_text(encoding="utf-8")


def read_json(relative_path: str):
    return json.loads(read_text(relative_path))


def assert_no_placeholders(test_case, text: str, source: str) -> None:
    banned = (
        "TO" + "DO",
        "T" + "BD",
        "FIX" + "ME",
        "<" + "placeholder>",
        "fill " + "this in",
    )
    for token in banned:
        test_case.assertNotIn(token, text, f"{source} contains {token}")
