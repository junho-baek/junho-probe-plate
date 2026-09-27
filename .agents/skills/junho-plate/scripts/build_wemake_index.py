#!/usr/bin/env python3
"""Build a deterministic, reviewable Git history index for Wemake."""
from __future__ import annotations

import argparse
from datetime import datetime
import html
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
from typing import Any, Callable, Iterable

SOURCE_URL = "https://github.com/nomadcoders/wemake"
CLASSIFICATIONS = {"foundation", "pattern-introduction", "pattern-refinement", "teaching-transition", "correction", "product-polish", "legacy-risk"}
RECORD_FIELDS = ("number", "hash", "author_date", "subject", "changed_paths", "technical_topics", "architecture_stage", "rule_ids", "classification", "audit_note")
HUMAN_FIELDS = ("technical_topics", "architecture_stage", "rule_ids", "classification", "audit_note")
LOWER_SHA = re.compile(r"^[0-9a-f]{40}$")
NUMBER = re.compile(r"^\d{3}$")
UNAUDITED_MARKER = re.compile(r"\b(?:UNREVIEWED|TODO|TBD|FIXME|PLACEHOLDER)\b", re.IGNORECASE)
DEFAULT_OUTPUT_MODE = 0o644


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def canonical_source_url(origin: str) -> str:
    value = origin.strip()
    if value.endswith(".git"):
        value = value[:-4]
    if value in {"git@github.com:nomadcoders/wemake", "ssh://git@github.com/nomadcoders/wemake"}:
        value = SOURCE_URL
    if value != SOURCE_URL:
        raise ValueError("origin must be https://github.com/nomadcoders/wemake")
    return value


def resolve_revision(repo: Path, revision: str) -> str:
    resolved = git(repo, "rev-parse", "--verify", f"{revision}^{{commit}}").strip()
    if not LOWER_SHA.fullmatch(resolved):
        raise ValueError("revision did not resolve to a full lowercase commit hash")
    return resolved


def collect_git_records(repo: Path, revision: str) -> list[dict[str, Any]]:
    resolved = resolve_revision(repo, revision)
    hashes = [item for item in git(repo, "rev-list", "--reverse", resolved).splitlines() if item]
    records = []
    for number, commit_hash in enumerate(hashes, 1):
        author_date, subject = git(repo, "show", "-s", "--format=%aI%x00%s", commit_hash).rstrip("\n").split("\x00", 1)
        parents = git(repo, "show", "-s", "--format=%P", commit_hash).split()
        if len(parents) > 1:
            paths = sorted(set(item for item in git(repo, "diff-tree", "--root", "-m", "--no-commit-id", "--name-only", "-r", commit_hash).splitlines() if item))
        else:
            paths = sorted(item for item in git(repo, "show", "--format=", "--name-only", commit_hash).splitlines() if item)
        if not paths:
            raise ValueError(f"commit {commit_hash} has no changed paths")
        records.append({"number": f"{number:03d}", "hash": commit_hash, "author_date": author_date, "subject": subject, "changed_paths": paths, "technical_topics": [], "architecture_stage": "", "rule_ids": [], "classification": "UNREVIEWED", "audit_note": ""})
    return records


def is_annotated(record: dict[str, Any]) -> bool:
    return record.get("classification") != "UNREVIEWED" or any(bool(record.get(field)) for field in ("technical_topics", "architecture_stage", "rule_ids", "audit_note"))


def validate_existing_records(records: Any) -> None:
    if not isinstance(records, list):
        raise ValueError("existing records must be a list")
    hashes: set[str] = set()
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("existing record must be an object")
        missing = set(RECORD_FIELDS) - set(record)
        if missing:
            raise ValueError(f"existing record missing {sorted(missing)[0]}")
        if set(record) != set(RECORD_FIELDS):
            raise ValueError("existing record has unsupported fields")
        if not isinstance(record["number"], str) or not NUMBER.fullmatch(record["number"]):
            raise ValueError("existing record has malformed number")
        if not isinstance(record["hash"], str) or not LOWER_SHA.fullmatch(record["hash"]):
            raise ValueError("existing record has malformed hash")
        if record["hash"] in hashes:
            raise ValueError("existing records contain duplicate hash")
        hashes.add(record["hash"])
        if not isinstance(record["author_date"], str) or not record["author_date"]:
            raise ValueError("existing record has malformed author date")
        try:
            datetime.fromisoformat(record["author_date"].replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError("existing record has malformed author date") from error
        if not isinstance(record["subject"], str) or not record["subject"].strip():
            raise ValueError("existing record has malformed subject")
        paths = record["changed_paths"]
        if not isinstance(paths, list) or not paths or any(not isinstance(item, str) or not item.strip() for item in paths) or paths != sorted(paths) or len(paths) != len(set(paths)):
            raise ValueError("existing record has malformed changed paths")
        for field in ("technical_topics", "rule_ids"):
            values = record[field]
            if not isinstance(values, list) or any(not isinstance(item, str) or not item or item != item.strip() for item in values) or len(values) != len(set(values)):
                raise ValueError(f"existing record has malformed {field}")
        for field in ("architecture_stage", "classification", "audit_note"):
            if not isinstance(record[field], str) or record[field] != record[field].strip():
                raise ValueError(f"existing record has malformed {field}")


def merge_records(drafts: list[dict[str, Any]], existing: list[dict[str, Any]]) -> list[dict[str, Any]]:
    validate_existing_records(existing)
    draft_hashes = {record["hash"] for record in drafts}
    if any(is_annotated(record) and record["hash"] not in draft_hashes for record in existing):
        raise ValueError("annotated hash is absent from requested revision")
    prior = {record["hash"]: record for record in existing}
    merged = []
    for draft in drafts:
        result = dict(draft)
        if draft["hash"] in prior:
            result.update({field: prior[draft["hash"]][field] for field in HUMAN_FIELDS})
        else:
            result.update({"technical_topics": [], "architecture_stage": "", "rule_ids": [], "classification": "UNREVIEWED", "audit_note": ""})
        merged.append(result)
    return merged


def make_payload(records: list[dict[str, Any]], source_url: str, pinned_head: str, verified_at: str) -> dict[str, Any]:
    return {"source_url": source_url, "pinned_head": pinned_head, "verified_at": verified_at, "record_count": len(records), "records": records}


def load_rule_ids(path: Path) -> set[str]:
    with path.open(encoding="utf-8") as file:
        catalog = json.load(file)
    if not isinstance(catalog, list):
        raise ValueError("rule catalog must be a list")
    return {item["id"] for item in catalog if isinstance(item, dict) and isinstance(item.get("id"), str)}


def validate_payload(payload: Any, rule_ids: set[str], require_audited: bool) -> None:
    if not isinstance(payload, dict) or set(payload) != {"source_url", "pinned_head", "verified_at", "record_count", "records"}:
        raise ValueError("index has malformed top-level fields")
    if not isinstance(payload["records"], list):
        raise ValueError("index records must be a list")
    if payload["source_url"] != SOURCE_URL:
        raise ValueError("index source URL is malformed")
    if not isinstance(payload["pinned_head"], str) or not LOWER_SHA.fullmatch(payload["pinned_head"]):
        raise ValueError("index pinned head is malformed")
    if not isinstance(payload["verified_at"], str):
        raise ValueError("index verified date is malformed")
    try:
        datetime.fromisoformat(payload["verified_at"])
    except ValueError as error:
        raise ValueError("index verified date is malformed") from error
    if type(payload["record_count"]) is not int or payload["record_count"] != len(payload["records"]):
        raise ValueError("index record count does not match records")
    validate_existing_records(payload["records"])
    if payload["records"] and payload["pinned_head"] != payload["records"][-1]["hash"]:
        raise ValueError("index pinned head does not match final record")
    for index, record in enumerate(payload["records"], 1):
        if record["number"] != f"{index:03d}":
            raise ValueError("record numbers are not sequential")
        pristine = record["classification"] == "UNREVIEWED" and not record["technical_topics"] and not record["architecture_stage"] and not record["rule_ids"] and not record["audit_note"]
        audited = record["classification"] in CLASSIFICATIONS and bool(record["technical_topics"]) and bool(record["architecture_stage"].strip()) and bool(record["rule_ids"]) and bool(record["audit_note"].strip()) and all(item.strip() for item in record["technical_topics"]) and all(item.strip() for item in record["rule_ids"])
        if not pristine and not audited:
            raise ValueError("record annotations are neither pristine nor audited")
        if audited and not set(record["rule_ids"]).issubset(rule_ids):
            raise ValueError("record uses an unknown rule id")
        if audited:
            annotation_values = [*record["technical_topics"], record["architecture_stage"], *record["rule_ids"], record["classification"], record["audit_note"]]
            if any(UNAUDITED_MARKER.search(value) for value in annotation_values):
                raise ValueError("record contains an unaudited marker")
        if require_audited:
            if not audited:
                raise ValueError("record classification is not audited")


def table_text(value: Any) -> str:
    if isinstance(value, list):
        value = ", ".join(str(item) for item in value)
    return html.escape(str(value), quote=False).replace("|", "\\|").replace("\n", "<br>")


def render_markdown(payload: dict[str, Any]) -> str:
    lines = ["# Wemake Commit Evidence Index", "", f"- Source: {payload['source_url']}", f"- Pinned head: `{payload['pinned_head']}`", f"- Verified: {payload['verified_at']}", f"- Records: {payload['record_count']}", "", "Each row is based on the commit's changed paths and its reviewed diff context. `teaching-transition` records a deliberately incomplete instructional step; `legacy-risk` records behavior that is not a current recommendation. The index is evidence of this pinned history, not a claim that every intermediate commit is production-ready guidance.", "", "| # | Full SHA | Subject | Key paths | Topics / stage | Rule IDs | Classification | Audit note |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for record in payload["records"]:
        stage = f"{', '.join(record['technical_topics'])}; {record['architecture_stage']}"
        values = (record["number"], record["hash"], record["subject"], record["changed_paths"], stage, record["rule_ids"], record["classification"], record["audit_note"])
        lines.append("| " + " | ".join(table_text(value) for value in values) + " |")
    return "\n".join(lines) + "\n"


def read_existing(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        with path.open(encoding="utf-8") as file:
            payload = json.load(file)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("existing JSON is malformed") from error
    rules = load_rule_ids(Path(__file__).resolve().parents[1] / "references" / "rule-catalog.json")
    validate_payload(payload, rules, require_audited=False)
    return payload["records"]


def validate_output_paths(json_path: Path, markdown_path: Path) -> tuple[Path, Path]:
    json_destination = json_path.resolve(strict=False)
    markdown_destination = markdown_path.resolve(strict=False)
    equivalent = json_destination == markdown_destination
    if not equivalent and json_destination.exists() and markdown_destination.exists():
        equivalent = os.path.samefile(json_destination, markdown_destination)
    if equivalent:
        raise ValueError("JSON and Markdown destinations must be distinct")
    return json_destination, markdown_destination


def output_paths_are_equivalent(json_destination: Path, markdown_destination: Path) -> bool:
    try:
        return json_destination.exists() and markdown_destination.exists() and os.path.samefile(json_destination, markdown_destination)
    except FileNotFoundError:
        return False


class _EquivalentOutputPathsError(OSError):
    pass


def _destination_mode(destination: Path) -> int:
    if not destination.exists():
        return DEFAULT_OUTPUT_MODE
    destination_stat = destination.stat()
    if not stat.S_ISREG(destination_stat.st_mode):
        raise OSError(f"output destination is not a file: {destination}")
    return stat.S_IMODE(destination_stat.st_mode)


def _prepare_text(
    destination: Path,
    text: str,
    prefix: str,
    *,
    fsync: Callable[[int], None] = os.fsync,
    chmod: Callable[[str, int], None] = os.chmod,
) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        mode = _destination_mode(destination)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=destination.parent, prefix=prefix, delete=False) as file:
            temporary = Path(file.name)
            file.write(text)
            file.flush()
            chmod(str(temporary), mode)
            fsync(file.fileno())
        return temporary
    except BaseException:
        _unlink_if_present(temporary)
        raise


def _prepare_backup(
    destination: Path,
    prefix: str,
    *,
    fsync: Callable[[int], None] = os.fsync,
    chmod: Callable[[str, int], None] = os.chmod,
) -> tuple[bool, Path | None]:
    if not destination.exists():
        return False, None
    mode = _destination_mode(destination)
    backup: Path | None = None
    try:
        with destination.open("rb") as source, tempfile.NamedTemporaryFile("wb", dir=destination.parent, prefix=prefix, delete=False) as file:
            backup = Path(file.name)
            while True:
                chunk = source.read(1024 * 1024)
                if not chunk:
                    break
                file.write(chunk)
            file.flush()
            chmod(str(backup), mode)
            fsync(file.fileno())
        return True, backup
    except BaseException:
        _unlink_if_present(backup)
        raise


def _unlink_if_present(path: Path | None) -> None:
    if path is not None:
        try:
            path.unlink()
        except FileNotFoundError:
            pass


def write_output_pair(
    json_path: Path,
    json_text: str,
    markdown_path: Path,
    markdown_text: str,
    *,
    replace: Callable[[str, str], None] = os.replace,
    equivalent_after_json: Callable[[Path, Path], bool] = output_paths_are_equivalent,
) -> None:
    json_destination, markdown_destination = validate_output_paths(json_path, markdown_path)
    prepared_json: Path | None = None
    prepared_markdown: Path | None = None
    json_backup: Path | None = None
    markdown_backup: Path | None = None
    json_existed = False
    markdown_existed = False
    try:
        prepared_json = _prepare_text(json_destination, json_text, ".wemake-json-")
        prepared_markdown = _prepare_text(markdown_destination, markdown_text, ".wemake-markdown-")
        json_existed, json_backup = _prepare_backup(json_destination, ".wemake-json-backup-")
        markdown_existed, markdown_backup = _prepare_backup(markdown_destination, ".wemake-markdown-backup-")
        json_replaced = False
        markdown_replaced = False
        try:
            replace(str(prepared_json), str(json_destination))
            json_replaced = True
            if equivalent_after_json(json_destination, markdown_destination):
                raise _EquivalentOutputPathsError("JSON and Markdown destinations became equivalent after JSON publish")
            replace(str(prepared_markdown), str(markdown_destination))
            markdown_replaced = True
        except OSError as error:
            rollback_error: OSError | None = None
            for destination, existed, backup, replaced in (
                (json_destination, json_existed, json_backup, json_replaced),
                (markdown_destination, markdown_existed, markdown_backup, markdown_replaced),
            ):
                if not replaced:
                    continue
                try:
                    if existed and backup is not None:
                        os.replace(backup, destination)
                    elif not existed:
                        _unlink_if_present(destination)
                except OSError as restore_error:
                    rollback_error = restore_error
            if rollback_error is not None:
                raise OSError("failed to publish output pair and restore prior outputs") from rollback_error
            if isinstance(error, _EquivalentOutputPathsError):
                raise OSError("JSON and Markdown destinations became equivalent; prior outputs restored") from error
            raise OSError("failed to publish output pair; prior outputs restored") from error
    finally:
        for temporary in (prepared_json, prepared_markdown, json_backup, markdown_backup):
            _unlink_if_present(temporary)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Wemake commit evidence index")
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--json", required=True, dest="json_path", type=Path)
    parser.add_argument("--markdown", required=True, type=Path)
    parser.add_argument("--source-url", default=None)
    args = parser.parse_args(argv)
    try:
        validate_output_paths(args.json_path, args.markdown)
        origin_url = canonical_source_url(git(args.repo, "remote", "get-url", "origin"))
        if args.source_url is not None and canonical_source_url(args.source_url) != origin_url:
            raise ValueError("source URL must be https://github.com/nomadcoders/wemake")
        source_url = origin_url
        pinned_head = resolve_revision(args.repo, args.revision)
        records = merge_records(collect_git_records(args.repo, pinned_head), read_existing(args.json_path))
        payload = make_payload(records, source_url, pinned_head, "2026-08-04")
        rules = load_rule_ids(Path(__file__).resolve().parents[1] / "references" / "rule-catalog.json")
        validate_payload(payload, rules, require_audited=all(is_annotated(record) for record in records))
        write_output_pair(
            args.json_path,
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            args.markdown,
            render_markdown(payload),
        )
    except (OSError, UnicodeDecodeError, subprocess.CalledProcessError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
