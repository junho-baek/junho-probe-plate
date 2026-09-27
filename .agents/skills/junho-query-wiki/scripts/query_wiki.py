#!/usr/bin/env python3
"""Append-only query journal with rebuildable Markdown projections."""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
import re
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any, Iterator


VERSION = 1
MAX_PROMPT_CHARS = 16_000
MAX_RESPONSE_CHARS = 8_000
SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}"),
)
ASSIGNMENT_PATTERN = re.compile(
    r"(?i)\b([A-Z0-9_]*(?:API[_-]?KEY|TOKEN|SECRET|PASSWORD|PASSWD))"
    r"\s*([:=])\s*([^\s,;\"']+)"
)
QUOTED_ASSIGNMENT_PATTERN = re.compile(
    r"(?i)([\"'](?:api[_-]?key|token|secret|password|passwd)[\"']\s*:\s*[\"'])"
    r"([^\"']+)([\"'])"
)
MATERIALITIES = {
    "objective",
    "constraint",
    "architecture_decision",
    "domain_rule",
    "verification",
    "failure_pattern",
    "operating_procedure",
    "open_question",
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def redact_text(value: str) -> str:
    redacted = QUOTED_ASSIGNMENT_PATTERN.sub(
        lambda match: f"{match.group(1)}[REDACTED]{match.group(3)}", value
    )
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    redacted = ASSIGNMENT_PATTERN.sub(lambda match: f"{match.group(1)}{match.group(2)}[REDACTED]", redacted)
    return redacted


def redact(value: Any) -> Any:
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, dict):
        return {str(key): redact(item) for key, item in value.items()}
    return value


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def clipped(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 1] + "…"


def require_text(payload: dict[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


class QueryWiki:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.base = self.root / ".junho-probe" / "query-wiki"
        self.events_path = self.base / "events.jsonl"
        self.index_path = self.base / "QUERY-INDEX.md"
        self.log_path = self.base / "log.md"
        self.state_dir = self.base / "state"
        self.topics_dir = self.base / "topics"
        self.lock_path = self.base / ".lock"
        for directory in (self.base, self.state_dir, self.topics_dir):
            directory.mkdir(parents=True, exist_ok=True)
            self._chmod(directory, 0o700)

    @staticmethod
    def _chmod(path: Path, mode: int) -> None:
        try:
            path.chmod(mode)
        except OSError:
            pass

    @contextlib.contextmanager
    def locked(self) -> Iterator[None]:
        with self.lock_path.open("a+", encoding="utf-8") as handle:
            self._chmod(self.lock_path, 0o600)
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def state_path(self, source: str, session_id: str) -> Path:
        return self.state_dir / f"{digest(source + chr(0) + session_id)}.json"

    def read_state(self, source: str, session_id: str) -> dict[str, Any] | None:
        path = self.state_path(source, session_id)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def write_state(self, source: str, session_id: str, state: dict[str, Any]) -> None:
        path = self.state_path(source, session_id)
        self.atomic_write(path, json.dumps(redact(state), ensure_ascii=False, indent=2) + "\n", 0o600)

    @staticmethod
    def atomic_write(path: Path, content: str, mode: int = 0o600) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        file_descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(file_descriptor, "w", encoding="utf-8") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            temporary.chmod(mode)
            os.replace(temporary, path)
        finally:
            if temporary.exists():
                temporary.unlink()

    def append_event(self, event: dict[str, Any]) -> None:
        safe_event = redact(event)
        line = json.dumps(safe_event, ensure_ascii=False, separators=(",", ":")) + "\n"
        with self.events_path.open("a", encoding="utf-8") as handle:
            self._chmod(self.events_path, 0o600)
            handle.write(line)
            handle.flush()
            os.fsync(handle.fileno())

    def read_events(self) -> list[dict[str, Any]]:
        if not self.events_path.exists():
            return []
        events: list[dict[str, Any]] = []
        for line_number, line in enumerate(self.events_path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(f"invalid JSONL at line {line_number}: {error}") from error
        return events

    def rebuild_index(self) -> None:
        queries: dict[str, dict[str, Any]] = {}
        order: list[str] = []
        for event in self.read_events():
            query_id = event.get("query_id")
            if not isinstance(query_id, str):
                continue
            if event.get("type") == "query_received":
                if query_id not in queries:
                    order.append(query_id)
                queries[query_id] = {
                    "received_at": event.get("timestamp", ""),
                    "source": event.get("source", ""),
                    "prompt_excerpt": event.get("prompt_excerpt", ""),
                    "status": "진행 중",
                    "topics": [],
                }
            elif query_id in queries and event.get("type") == "query_completed":
                queries[query_id]["status"] = "완료"
            elif query_id in queries and event.get("type") == "query_failed":
                queries[query_id]["status"] = "실패"
            elif query_id in queries and event.get("type") == "query_interrupted":
                queries[query_id]["status"] = "중단"
            elif query_id in queries and event.get("type") == "query_promoted":
                slug = event.get("slug")
                if isinstance(slug, str) and slug not in queries[query_id]["topics"]:
                    queries[query_id]["topics"].append(slug)

        completed = sum(1 for item in queries.values() if item["status"] == "완료")
        lines = [
            "# 쿼리 인덱스 | Query Index",
            "",
            "> 이 문서는 `events.jsonl`에서 재생성되는 검색용 투영입니다. 쿼리 기록 자체는 Probe 의도 점수가 아닙니다.",
            "",
            f"- 전체 질의: {len(queries)}",
            f"- 완료: {completed}",
            "",
            "| 시각 | Query ID | 출처 | 상태 | 요청 요약 | 승격 주제 |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for query_id in reversed(order):
            item = queries[query_id]
            topics = ", ".join(f"[마크다운](topics/{slug}.md)" for slug in item["topics"]) or "-"
            lines.append(
                "| {time} | `{query_id}` | {source} | {status} | {prompt} | {topics} |".format(
                    time=self.escape_cell(str(item["received_at"])),
                    query_id=self.escape_cell(query_id),
                    source=self.escape_cell(str(item["source"])),
                    status=item["status"],
                    prompt=self.escape_cell(str(item["prompt_excerpt"])),
                    topics=topics,
                )
            )
        self.atomic_write(self.index_path, "\n".join(lines) + "\n", 0o600)

    @staticmethod
    def escape_cell(value: str) -> str:
        return value.replace("|", "\\|").replace("\n", " ").replace("\r", " ")

    def receive(self, raw_payload: dict[str, Any]) -> dict[str, Any]:
        payload = redact(raw_payload)
        source = require_text(payload, "source")
        session_id = require_text(payload, "session_id")
        prompt = clipped(require_text(payload, "prompt"), MAX_PROMPT_CHARS)
        prompt_hash = digest(prompt)
        event_key = str(payload.get("event_key", "")).strip()
        event_key_hash = digest(event_key) if event_key else ""

        with self.locked():
            state = self.read_state(source, session_id)
            if state and state.get("status") == "open":
                same_key = bool(event_key_hash) and state.get("event_key_hash") == event_key_hash
                same_prompt = state.get("prompt_sha256") == prompt_hash
                if same_key or (not event_key_hash and same_prompt):
                    return {"query_id": state["query_id"], "deduplicated": True}
                self.append_event(
                    {
                        "version": VERSION,
                        "type": "query_interrupted",
                        "query_id": state["query_id"],
                        "timestamp": utc_now(),
                        "reason": "superseded_by_new_query",
                    }
                )

            query_id = f"Q-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
            event = {
                "version": VERSION,
                "type": "query_received",
                "query_id": query_id,
                "timestamp": utc_now(),
                "source": source,
                "session_hash": digest(session_id),
                "prompt": prompt,
                "prompt_excerpt": clipped(" ".join(prompt.split()), 180),
                "prompt_sha256": prompt_hash,
                "event_key_hash": event_key_hash or None,
            }
            self.append_event(event)
            self.write_state(
                source,
                session_id,
                {
                    "query_id": query_id,
                    "status": "open",
                    "prompt_sha256": prompt_hash,
                    "event_key_hash": event_key_hash,
                },
            )
            self.rebuild_index()
            return {"query_id": query_id, "deduplicated": False}

    def resolve_open_query(self, payload: dict[str, Any]) -> tuple[str, str, str, dict[str, Any]]:
        source = require_text(payload, "source")
        session_id = require_text(payload, "session_id")
        state = self.read_state(source, session_id)
        requested = str(payload.get("query_id", "")).strip()
        query_id = requested or (str(state.get("query_id")) if state else "")
        if not query_id:
            raise ValueError("no open query for source/session")
        if not state or state.get("status") != "open":
            raise ValueError(f"no open query matching {query_id}")
        received_ids = {
            event.get("query_id") for event in self.read_events() if event.get("type") == "query_received"
        }
        if query_id not in received_ids:
            raise ValueError(f"no open query matching {query_id}")
        if state and state.get("query_id") != query_id:
            raise ValueError(f"no open query matching {query_id}")
        return source, session_id, query_id, state or {}

    def finish(self, raw_payload: dict[str, Any], *, failed: bool) -> dict[str, Any]:
        payload = redact(raw_payload)
        with self.locked():
            source, session_id, query_id, state = self.resolve_open_query(payload)
            event_type = "query_failed" if failed else "query_completed"
            event: dict[str, Any] = {
                "version": VERSION,
                "type": event_type,
                "query_id": query_id,
                "timestamp": utc_now(),
                "source": source,
            }
            if failed:
                event["error"] = clipped(str(payload.get("error", "unknown failure")), 2_000)
            else:
                event["assistant_summary"] = clipped(
                    str(payload.get("assistant_summary", "")).strip(), MAX_RESPONSE_CHARS
                )
                evidence = payload.get("evidence", [])
                event["evidence"] = evidence if isinstance(evidence, list) else []
            self.append_event(event)
            self.write_state(source, session_id, {**state, "status": "failed" if failed else "completed"})
            self.rebuild_index()
            return {"query_id": query_id, "status": "failed" if failed else "completed"}

    def promotion_snapshot(self, raw_payload: dict[str, Any], *, proposal: bool = False) -> dict[str, Any]:
        payload = redact(raw_payload)
        query_id = require_text(payload, "query_id")
        slug = require_text(payload, "slug")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise ValueError("slug must contain lowercase letters, digits, and single hyphens")
        title_ko = require_text(payload, "title_ko")
        title_en = require_text(payload, "title_en")
        summary = require_text(payload, "summary")
        events = self.read_events()
        if not any(event.get("type") == "query_received" and event.get("query_id") == query_id for event in events):
            raise ValueError(f"unknown query_id: {query_id}")

        def string_list(field: str) -> list[str]:
            value = payload.get(field, [])
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                raise ValueError(f"{field} must be a list of strings")
            return [item.strip() for item in value if item.strip()]

        key_points = string_list("key_points")
        evidence = string_list("evidence")
        open_questions = string_list("open_questions")
        materiality = str(payload.get("materiality", "open_question")).strip()
        if materiality not in MATERIALITIES:
            raise ValueError(f"materiality must be one of: {', '.join(sorted(MATERIALITIES))}")
        actor_role = str(payload.get("actor_role", "producer")).strip()
        promotion_status = "proposal" if proposal else str(payload.get("promotion_status", "candidate")).strip()
        if promotion_status not in {"proposal", "candidate", "verified"}:
            raise ValueError("promotion_status must be proposal, candidate, or verified")
        if not proposal and promotion_status == "verified":
            if actor_role == "judge":
                raise ValueError("Judge may propose or create a candidate, but cannot verify its own promotion")
            approved_by = str(payload.get("approved_by", "")).strip()
            if approved_by not in {"human", "producer"}:
                raise ValueError("verified promotion requires approved_by human or producer")
            require_text(payload, "materiality_reason")
            terminal_types = [
                event.get("type")
                for event in events
                if event.get("query_id") == query_id and event.get("type") in {"query_completed", "query_failed"}
            ]
            if terminal_types != ["query_completed"]:
                raise ValueError("verified promotion requires one completed query")
            if not evidence:
                raise ValueError("verified promotion requires at least one evidence path")
            for evidence_ref in evidence:
                candidate = (self.root / evidence_ref).resolve()
                try:
                    candidate.relative_to(self.root)
                except ValueError as error:
                    raise ValueError(f"evidence escapes project root: {evidence_ref}") from error
                if not candidate.exists():
                    raise ValueError(f"evidence path does not exist: {evidence_ref}")
        return {
            "query_id": query_id,
            "slug": slug,
            "title_ko": title_ko,
            "title_en": title_en,
            "summary": summary,
            "key_points": key_points,
            "evidence": evidence,
            "open_questions": open_questions,
            "materiality": materiality,
            "materiality_reason": str(payload.get("materiality_reason", "")).strip(),
            "actor_role": actor_role,
            "approved_by": str(payload.get("approved_by", "")).strip(),
            "promotion_status": promotion_status,
        }

    def propose(self, raw_payload: dict[str, Any]) -> dict[str, Any]:
        snapshot = self.promotion_snapshot(raw_payload, proposal=True)
        with self.locked():
            self.append_event(
                {
                    "version": VERSION,
                    "type": "query_promotion_proposed",
                    "query_id": snapshot["query_id"],
                    "timestamp": utc_now(),
                    "snapshot": snapshot,
                }
            )
        return {"query_id": snapshot["query_id"], "status": "proposal"}

    def promote(self, raw_payload: dict[str, Any]) -> dict[str, Any]:
        snapshot = self.promotion_snapshot(raw_payload)
        query_id = snapshot["query_id"]
        slug = snapshot["slug"]
        with self.locked():
            topic_path = self.topics_dir / f"{slug}.md"
            query_ids = [query_id]
            if topic_path.exists():
                query_ids.extend(re.findall(r"`(Q-[^`]+)`", topic_path.read_text(encoding="utf-8")))
            query_ids = list(dict.fromkeys(query_ids))
            lines = [
                f"# {snapshot['title_ko']} | {snapshot['title_en']}",
                "",
                f"> 마지막 갱신: {utc_now()}",
                f"> 지식 상태: `{snapshot['promotion_status']}` · 중요도: `{snapshot['materiality']}`",
                "",
                "## 요약",
                "",
                snapshot["summary"],
                "",
                "## 핵심 판단",
                "",
                *([f"- {item}" for item in snapshot["key_points"]] or ["- 아직 정리된 핵심 판단이 없습니다."]),
                "",
                "## 근거",
                "",
                *([f"- `{item}`" for item in snapshot["evidence"]] or ["- 아직 연결된 검증 근거가 없습니다."]),
                "",
                "## 관련 질의",
                "",
                *[f"- `{item}`" for item in query_ids],
                "",
                "## 열린 질문",
                "",
                *([f"- {item}" for item in snapshot["open_questions"]] or ["- 없음"]),
                "",
            ]
            self.atomic_write(topic_path, "\n".join(lines), 0o600)
            self.append_event(
                {
                    "version": VERSION,
                    "type": "query_promoted",
                    "query_id": query_id,
                    "timestamp": utc_now(),
                    "slug": slug,
                    "topic_path": str(topic_path.relative_to(self.root)),
                    "snapshot": snapshot,
                }
            )
            log_entry = (
                f"- {utc_now()} `{query_id}` → [**{snapshot['title_ko']}**](topics/{slug}.md) "
                f"`{snapshot['promotion_status']}`\n"
            )
            if not self.log_path.exists():
                self.atomic_write(self.log_path, "# 위키 갱신 로그 | Wiki Update Log\n\n" + log_entry, 0o600)
            else:
                with self.log_path.open("a", encoding="utf-8") as handle:
                    handle.write(log_entry)
                    handle.flush()
                    os.fsync(handle.fileno())
            self.rebuild_index()
        return {"query_id": query_id, "topic": str(topic_path.relative_to(self.root))}


def load_payload() -> dict[str, Any]:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        raise ValueError(f"stdin must contain one JSON object: {error}") from error
    if not isinstance(payload, dict):
        raise ValueError("stdin must contain one JSON object")
    return payload


def main() -> int:
    if os.environ.get("JUNHO_QUERY_WIKI_INTERNAL") == "1" and os.environ.get("JUNHO_QUERY_WIKI_WRITER") != "1":
        print(json.dumps({"skipped": True, "reason": "internal_recursion_guard"}))
        return 0
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "command", choices=("receive", "complete", "fail", "propose", "promote", "rebuild-index")
    )
    args = parser.parse_args()
    try:
        wiki = QueryWiki(args.root)
        if args.command == "rebuild-index":
            with wiki.locked():
                wiki.rebuild_index()
            result = {"index": str(wiki.index_path)}
        else:
            payload = load_payload()
            if args.command == "receive":
                result = wiki.receive(payload)
            elif args.command == "complete":
                result = wiki.finish(payload, failed=False)
            elif args.command == "fail":
                result = wiki.finish(payload, failed=True)
            elif args.command == "propose":
                result = wiki.propose(payload)
            else:
                result = wiki.promote(payload)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"query-wiki error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
