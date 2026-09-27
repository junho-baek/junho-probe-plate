#!/usr/bin/env python3
"""Claude Code hook adapter for junho-query-wiki.

The adapter is intentionally fail-open: observability must not block the user's work.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    if os.environ.get("JUNHO_QUERY_WIKI_INTERNAL") == "1":
        return 0
    try:
        hook = json.load(sys.stdin)
        if not isinstance(hook, dict):
            raise ValueError("hook input must be an object")
        event_name = hook.get("hook_event_name")
        root = Path(os.environ.get("JUNHO_QUERY_WIKI_ROOT") or hook.get("cwd") or os.getcwd())
        script = Path(__file__).with_name("query_wiki.py")
        source = "claude-code"
        session_id = str(hook.get("session_id", "")).strip()
        if not session_id:
            raise ValueError("missing session_id")

        if event_name == "UserPromptSubmit":
            command = "receive"
            payload = {
                "source": source,
                "session_id": session_id,
                "prompt": str(hook.get("prompt", "")),
            }
        elif event_name == "Stop":
            command = "complete"
            payload = {
                "source": source,
                "session_id": session_id,
                "assistant_summary": str(hook.get("last_assistant_message", "")),
            }
        elif event_name == "StopFailure":
            command = "fail"
            payload = {
                "source": source,
                "session_id": session_id,
                "error": str(hook.get("error", hook.get("error_message", "Claude stopped with an error"))),
            }
        else:
            return 0

        environment = {**os.environ, "JUNHO_QUERY_WIKI_WRITER": "1"}
        environment.pop("JUNHO_QUERY_WIKI_INTERNAL", None)
        result = subprocess.run(
            [sys.executable, str(script), "--root", str(root), command],
            input=json.dumps(payload, ensure_ascii=False),
            text=True,
            capture_output=True,
            env=environment,
        )
        if result.returncode != 0:
            print(result.stderr.strip() or "query-wiki hook failed", file=sys.stderr)
        return 0
    except Exception as error:  # hooks must never break the user's agent turn
        print(f"query-wiki hook warning: {error}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
