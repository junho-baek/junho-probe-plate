#!/usr/bin/env python3
"""Initialize a non-destructive Junho Probe evidence workspace."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import re
import shutil
import sys

EXIT_OK = 0
EXIT_NO_TEMPLATES = 2
EXIT_SKIPPED = 3

UNSPECIFIED_EVENT = "UNSPECIFIED"

# Every *.md in the template directory is copied. This list only drives the
# missing-template warning, so a template that has not landed yet is visible
# instead of silently absent.
EXPECTED_TEMPLATES = (
    "STATUS.md",
    "RUBRIC.md",
    "PROBE-CANVAS.md",
    "DECISIONS.md",
    "EVALS.md",
    "DEMO.md",
    "INTENT-INDEX.md",
)

STATUS_FILE = "STATUS.md"
EVENT_LINE = re.compile(r"^- Event:.*$", re.MULTILINE)
TASK_LINE = re.compile(r"^- Task:.*$", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create .junho-probe evidence files without overwriting existing work."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Workspace root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--event",
        default=UNSPECIFIED_EVENT,
        help=(
            "Event identifier inserted into STATUS.md, e.g. 'SK-hynix-AI-hackathon-2026'. "
            "State it: it is how a stale workspace from an earlier event is detected."
        ),
    )
    parser.add_argument(
        "--task-title",
        default="Untitled challenge",
        help="Task title inserted into STATUS.md.",
    )
    parser.add_argument(
        "--directory",
        default=".junho-probe",
        help="Evidence directory name under the workspace root.",
    )
    return parser.parse_args()


def apply_event(content: str, event: str) -> str:
    """Return STATUS.md content with a filled `- Event:` field.

    Substitutes the {{EVENT}} marker when the template carries one; otherwise
    fills an empty `- Event:` line, or inserts one after `- Task:`.
    """
    if "{{EVENT}}" in content:
        return content.replace("{{EVENT}}", event)

    line = f"- Event: {event}"
    if EVENT_LINE.search(content):
        return EVENT_LINE.sub(lambda _match: line, content, count=1)

    task = TASK_LINE.search(content)
    if task:
        return f"{content[: task.end()]}\n{line}{content[task.end() :]}"
    return f"{line}\n{content}"


def read_existing_event(status_path: Path) -> str | None:
    """Return the event recorded in an existing STATUS.md, if any."""
    try:
        text = status_path.read_text(encoding="utf-8")
    except OSError:
        return None
    match = EVENT_LINE.search(text)
    if not match:
        return None
    return match.group(0).split(":", 1)[1].strip() or None


def warn_skipped(skipped: list[Path], target_dir: Path, event: str) -> None:
    """Report skipped files loudly. A silent skip inherits an old event's state."""
    rule = "=" * 72
    print(rule, file=sys.stderr)
    print(
        f"WARNING: {len(skipped)} file(s) already existed and were NOT touched.",
        file=sys.stderr,
    )
    for path in skipped:
        print(f"  KEPT {path.name}", file=sys.stderr)

    existing_event = read_existing_event(target_dir / STATUS_FILE)
    if existing_event and existing_event != event:
        print(
            f"  STATUS.md records event '{existing_event}', but this run declares '{event}'.",
            file=sys.stderr,
        )

    print(
        f"Confirm these files belong to event '{event}'. If they do not, they are stale\n"
        f"state from an earlier event: run this script in a different directory, or move\n"
        f"or remove {target_dir} and run it again. Do not build on inherited state.",
        file=sys.stderr,
    )
    print(rule, file=sys.stderr)


def main() -> int:
    args = parse_args()
    skill_dir = Path(__file__).resolve().parent.parent
    template_dir = skill_dir / "assets" / "templates"
    target_dir = args.root.expanduser().resolve() / args.directory

    if not template_dir.is_dir():
        print(f"Template directory not found: {template_dir}", file=sys.stderr)
        return EXIT_NO_TEMPLATES

    if args.event == UNSPECIFIED_EVENT:
        print(
            "WARNING: no --event given; STATUS.md will record "
            f"'{UNSPECIFIED_EVENT}'. Pass --event so a stale workspace is detectable.",
            file=sys.stderr,
        )

    target_dir.mkdir(parents=True, exist_ok=True)
    replacements = {
        "{{TASK_TITLE}}": args.task_title,
        "{{EVENT}}": args.event,
        "{{CREATED_AT}}": datetime.now().astimezone().isoformat(timespec="minutes"),
    }

    sources = sorted(template_dir.glob("*.md"))
    missing = [name for name in EXPECTED_TEMPLATES if not (template_dir / name).is_file()]
    if missing:
        print(
            f"WARNING: expected template(s) absent from {template_dir}: "
            f"{', '.join(missing)}",
            file=sys.stderr,
        )

    created: list[Path] = []
    skipped: list[Path] = []

    for source in sources:
        destination = target_dir / source.name
        if destination.exists():
            skipped.append(destination)
            continue

        content = source.read_text(encoding="utf-8")
        for marker, value in replacements.items():
            content = content.replace(marker, value)
        if source.name == STATUS_FILE:
            content = apply_event(content, args.event)
        destination.write_text(content, encoding="utf-8")
        shutil.copymode(source, destination)
        created.append(destination)

    print(f"Probe workspace: {target_dir}")
    print(f"Event: {args.event}")
    for path in created:
        print(f"CREATED {path.name}")
    for path in skipped:
        print(f"SKIPPED {path.name} (already exists)")

    if skipped:
        warn_skipped(skipped, target_dir, args.event)
        print(
            f"SUMMARY event={args.event} created={len(created)} "
            f"skipped={len(skipped)} STALE_STATE_POSSIBLE"
        )
        return EXIT_SKIPPED

    print(f"SUMMARY event={args.event} created={len(created)} skipped=0 CLEAN")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
