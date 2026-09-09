#!/usr/bin/env python3
"""Hermes pre-run gate for Trend Brain candidate analysis.

The script intentionally performs no LLM or provider call. It asks the internal
Trend Brain API whether semantic-analysis candidates are waiting, then emits the
Hermes cron wakeAgent contract on stdout.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_API_URL = "http://127.0.0.1:8787"
DEFAULT_TIMEOUT_SECONDS = 5.0


def parse_pending_count(payload: Any) -> int:
    if not isinstance(payload, dict):
        raise ValueError("response must be a JSON object")
    value = payload.get("pending_count")
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError("pending_count must be a non-negative integer")
    return value


def build_gate_output(pending_count: int) -> dict[str, Any]:
    if pending_count == 0:
        return {"wakeAgent": False}
    return {
        "wakeAgent": True,
        "context": {
            "pending_candidates": pending_count,
            "source": "trend-brain-internal-api",
        },
    }


def fetch_pending_count(api_url: str, token: str, timeout: float) -> int:
    endpoint = f"{api_url.rstrip('/')}/internal/v1/candidates/pending-count"
    headers = {"Accept": "application/json", "User-Agent": "trend-brain-hermes-gate/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(endpoint, headers=headers, method="GET")
    with urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return parse_pending_count(payload)


def main() -> int:
    api_url = os.environ.get("TRND_INTERNAL_API_URL", DEFAULT_API_URL)
    token = os.environ.get("TRND_INTERNAL_API_TOKEN", "")
    try:
        timeout = float(os.environ.get("TRND_INTERNAL_API_TIMEOUT_SECONDS", DEFAULT_TIMEOUT_SECONDS))
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        pending_count = fetch_pending_count(api_url, token, timeout)
        print(json.dumps(build_gate_output(pending_count), separators=(",", ":")))
        return 0
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError, OSError) as exc:
        # Do not print the URL because it may be misconfigured with a credential.
        print(f"Trend Brain pending check failed: {type(exc).__name__}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
