#!/usr/bin/env python3
"""Classify React Router 7 compatibility and optional Plate provenance."""

from __future__ import annotations

import argparse
import codecs
import json
import sys
from pathlib import Path
from typing import Any


DEPENDENCY_MAPS = ("dependencies", "devDependencies")
MAX_READABLE_TEXT_BYTES = 64 * 1024
SERVER_SOURCE_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}
SUPABASE_DIRECTORY_SERVER_STEMS = {
    "server",
    "server-client",
    "supabase.server",
    "supa-client.server",
    "supabase-client.server",
    "supa-admin-client.server",
    "supabase-admin-client.server",
}
CONVENTIONAL_SERVER_CLIENT_STEMS = {
    "supa-client.server",
    "supabase-client.server",
    "supa-admin-client.server",
    "supabase-admin-client.server",
}
REACT_ROUTER_FRAMEWORK_PACKAGES = {"react-router", "@react-router/dev"}


def _read_package(root: Path) -> dict[str, Any]:
    package_path = root / "package.json"
    if not package_path.is_file():
        raise FileNotFoundError(f"package.json not found in {root}")
    try:
        package = json.loads(package_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid package.json in {root}: {error.msg}") from error
    if not isinstance(package, dict):
        raise ValueError(f"invalid package.json in {root}: expected a JSON object")
    return package


def _dependencies(package: dict[str, Any]) -> dict[str, str]:
    dependencies: dict[str, str] = {}
    for map_name in DEPENDENCY_MAPS:
        if map_name not in package:
            continue
        values = package[map_name]
        if not isinstance(values, dict):
            raise ValueError(f"invalid package.json: {map_name} must be an object")
        for name, version in values.items():
            if not isinstance(name, str):
                raise ValueError(f"invalid package.json: {map_name} dependency names must be strings")
            if not isinstance(version, str):
                raise ValueError(
                    f"invalid package.json: {map_name} version for {name} must be a string"
                )
            if name not in dependencies:
                dependencies[name] = version
    return dependencies


def _declares_react_router_seven(version: str) -> bool:
    value = version.strip()
    if value.startswith("workspace:"):
        value = value[len("workspace:"):]
    if value.startswith(("^", "~")):
        value = value[1:]
    if value.startswith("v"):
        value = value[1:]

    suffix_present = False
    if "+" in value:
        if value.count("+") != 1:
            return False
        value, build = value.split("+", 1)
        if not _valid_semver_suffix(build, reject_numeric_leading_zero=False):
            return False
        suffix_present = True
    if "-" in value:
        value, prerelease = value.split("-", 1)
        if not _valid_semver_suffix(prerelease, reject_numeric_leading_zero=True):
            return False
        suffix_present = True

    segments = value.split(".")
    if not 1 <= len(segments) <= 3 or segments[0] != "7":
        return False
    wildcard_seen = False
    for segment in segments:
        if segment.casefold() in {"x", "*"}:
            wildcard_seen = True
        elif segment.isascii() and segment.isdigit():
            if len(segment) > 1 and segment.startswith("0"):
                return False
            if wildcard_seen:
                return False
        else:
            return False
    if suffix_present and (wildcard_seen or len(segments) != 3):
        return False
    return True


def _valid_semver_suffix(value: str, *, reject_numeric_leading_zero: bool) -> bool:
    identifiers = value.split(".")
    for identifier in identifiers:
        if not identifier or not all(
            character.isascii() and (character.isalnum() or character == "-")
            for character in identifier
        ):
            return False
        if (
            reject_numeric_leading_zero
            and identifier.isdigit()
            and len(identifier) > 1
            and identifier.startswith("0")
        ):
            return False
    return True


def _read_bounded_utf8(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        with path.open("rb", buffering=0) as file:
            content = file.read(MAX_READABLE_TEXT_BYTES + 1)
    except OSError:
        return None
    truncated = len(content) > MAX_READABLE_TEXT_BYTES
    prefix = content[:MAX_READABLE_TEXT_BYTES]
    try:
        if truncated:
            decoder = codecs.getincrementaldecoder("utf-8")(errors="strict")
            text = decoder.decode(prefix, final=False)
        else:
            text = prefix.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return None
    if _contains_binary_controls(text):
        return None
    return text


def _is_readable_utf8(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        with path.open("r", encoding="utf-8") as file:
            while content := file.read(64 * 1024):
                if _contains_binary_controls(content):
                    return False
    except (OSError, UnicodeDecodeError):
        return False
    return True


def _contains_binary_controls(content: str) -> bool:
    allowed_controls = {"\t", "\n", "\r", "\f"}
    return any(
        character not in allowed_controls
        and (ord(character) < 32 or 127 <= ord(character) <= 159)
        for character in content
    )


def _has_readable_server_marker(root: Path) -> bool:
    core_directory = root / "app" / "core"
    supabase_directory = core_directory / "supabase"
    for stem in sorted(SUPABASE_DIRECTORY_SERVER_STEMS):
        for suffix in sorted(SERVER_SOURCE_SUFFIXES):
            if _is_readable_utf8(supabase_directory / f"{stem}{suffix}"):
                return True

    lib_directory = core_directory / "lib"
    for stem in sorted(CONVENTIONAL_SERVER_CLIENT_STEMS):
        for suffix in sorted(SERVER_SOURCE_SUFFIXES):
            candidate = lib_directory / f"{stem}{suffix}"
            text = _read_bounded_utf8(candidate)
            if (
                text is not None
                and "supabase" in text.casefold()
                and _is_readable_utf8(candidate)
            ):
                return True
    return False


def _is_positive_supaplate_text(text: str) -> bool:
    for line in text.splitlines():
        normalized = line.strip().casefold()
        if normalized in {"# supaplate", "supaplate-provenance: true"}:
            return True
    return False


def _has_supaplate_provenance(root: Path, package: dict[str, Any]) -> bool:
    package_name = package.get("name")
    if isinstance(package_name, str):
        normalized_name = package_name.casefold()
        if normalized_name == "supaplate" or (
            normalized_name.startswith("@")
            and normalized_name.count("/") == 1
            and normalized_name.rsplit("/", 1)[1] == "supaplate"
        ):
            return True
    if package.get("supaplateProvenance") is True:
        return True
    try:
        children = sorted(root.iterdir())
    except OSError:
        return False
    for child in children:
        name = child.name.casefold()
        if not child.is_file() or not name.startswith(("readme", "license", "licence")):
            continue
        text = _read_bounded_utf8(child)
        if text is not None and _is_positive_supaplate_text(text):
            return True
    return False


def inspect_project(project_root: str | Path, user_confirmed: bool = False) -> dict[str, object]:
    """Return a JSON-safe, evidence-based Plate classification for *project_root*."""
    root = Path(project_root)
    if not root.exists():
        raise FileNotFoundError(f"project root does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"project root is not a directory: {root}")

    package = _read_package(root)
    dependencies = _dependencies(package)
    evidence = ["project-inspected"]
    missing: list[str] = []

    router_packages = sorted(name for name in dependencies if name in REACT_ROUTER_FRAMEWORK_PACKAGES)
    router_seven_packages = [
        name for name in router_packages if _declares_react_router_seven(dependencies[name])
    ]
    if router_seven_packages:
        evidence.append("react-router-framework-mode")
    else:
        missing.append("missing-react-router-framework-mode")

    supabase_packages = sorted(
        name for name in dependencies if name in {"@supabase/supabase-js", "@supabase/ssr"}
    )
    if supabase_packages:
        evidence.append("supabase")
    else:
        missing.append("missing-supabase")

    if "drizzle-orm" in dependencies:
        evidence.append("drizzle")
    else:
        missing.append("missing-drizzle")

    if _is_readable_utf8(root / "app" / "routes.ts"):
        evidence.append("app-routes")
    else:
        missing.append("missing-app-routes")

    if (root / "app" / "features").is_dir():
        evidence.append("app-features-directory")
    else:
        missing.append("missing-app-features-directory")

    if _has_readable_server_marker(root):
        evidence.append("server-side-supabase-marker")
    else:
        missing.append("missing-server-side-supabase-marker")

    provenance_found = _has_supaplate_provenance(root, package)
    if provenance_found:
        evidence.append("supaplate-provenance")
    elif user_confirmed:
        evidence.append("user-confirmed-provenance")
    else:
        evidence.append("generic-or-unverified-origin")

    if user_confirmed and "user-confirmed-provenance" not in evidence:
        evidence.append("user-confirmed-provenance")

    if router_seven_packages and (provenance_found or user_confirmed):
        status = "CONFIRMED"
    elif router_seven_packages:
        status = "COMPATIBLE"
    else:
        status = "UNSUPPORTED"

    optional_names = [
        name
        for name in ("drizzle-orm", "react", "typescript", "zod")
        if name in dependencies
    ]
    relevant_names = sorted(set(router_packages + supabase_packages + optional_names))
    versions = {name: dependencies[name] for name in relevant_names}
    return {"status": status, "evidence": evidence, "missing": missing, "versions": versions}


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.exit(2, f"error: {message}\n")


def main(argv: list[str] | None = None) -> int:
    parser = _ArgumentParser(
        description="Inspect React Router 7 compatibility and optional Plate provenance."
    )
    parser.add_argument("project_root")
    parser.add_argument("--user-confirmed", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = inspect_project(args.project_root, user_confirmed=args.user_confirmed)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
