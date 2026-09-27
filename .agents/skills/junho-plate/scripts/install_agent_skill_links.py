#!/usr/bin/env python3
"""Expose the canonical Junho Plate skills to another Agent Skills host."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


SKILL_NAMES = (
    "junho-plate",
    "junho-plate-review",
    "junho-plate-refactor",
    "junho-plate-feature",
)


class InstallError(RuntimeError):
    """Raised when installing links would be unsafe or incomplete."""


def default_source_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _validated_sources(source_root: Path) -> dict[str, Path]:
    sources: dict[str, Path] = {}
    errors: list[str] = []

    for skill_name in SKILL_NAMES:
        source = source_root / skill_name
        if not (source / "SKILL.md").is_file():
            errors.append(f"missing source SKILL.md: {source / 'SKILL.md'}")
            continue
        sources[skill_name] = source.resolve(strict=True)

    if errors:
        raise InstallError("\n".join(errors))
    return sources


def _link_problem(destination: Path, source: Path) -> str | None:
    if not os.path.lexists(destination):
        return "missing"
    if not destination.is_symlink():
        return f"destination exists and is not a symlink: {destination}"
    try:
        resolved = destination.resolve(strict=True)
    except FileNotFoundError:
        return f"destination is a broken symlink: {destination}"
    if resolved != source:
        return f"destination points elsewhere: {destination} -> {resolved}"
    return None


def install_links(
    source_root: Path,
    destination_root: Path,
    *,
    check: bool = False,
) -> list[Path]:
    sources = _validated_sources(source_root)

    if os.path.lexists(destination_root) and not destination_root.is_dir():
        raise InstallError(
            f"destination root exists and is not a directory: {destination_root}"
        )

    missing: list[tuple[Path, Path]] = []
    conflicts: list[str] = []
    for skill_name, source in sources.items():
        destination = destination_root / skill_name
        problem = _link_problem(destination, source)
        if problem == "missing":
            missing.append((destination, source))
        elif problem is not None:
            conflicts.append(problem)

    if check and missing:
        conflicts.extend(f"destination link is missing: {path}" for path, _ in missing)
    if conflicts:
        raise InstallError("\n".join(conflicts))

    if not check:
        destination_root.mkdir(parents=True, exist_ok=True)
        for destination, source in missing:
            destination.symlink_to(source, target_is_directory=True)

    return [destination_root / skill_name for skill_name in SKILL_NAMES]


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Create non-overwriting links from one canonical Junho Plate source "
            "to another Agent Skills discovery directory."
        )
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=default_source_root(),
        help="Directory containing all four Junho Plate skill folders.",
    )
    parser.add_argument(
        "--destination-root",
        type=Path,
        required=True,
        help="Agent Skills discovery directory, such as ~/.claude/skills.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify exact links without creating anything.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        links = install_links(
            args.source_root,
            args.destination_root,
            check=args.check,
        )
    except InstallError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    action = "verified" if args.check else "installed"
    print(f"{action} {len(links)} Junho Plate skill links in {args.destination_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
