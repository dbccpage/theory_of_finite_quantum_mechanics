"""Native-only boundary; no Python mathematical fallback."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


class NativeUnavailable(RuntimeError):
    """The declared native experimental executable is unavailable."""


class NativeRefusal(RuntimeError):
    """The native input contract refused a supplied request."""

    def __init__(self, payload: dict):
        self.payload = payload
        super().__init__(str(payload.get("refused", "native request refused")))


def executable() -> Path:
    configured = os.environ.get("WDP_QUESTION_ENCODING_BINARY")
    if not configured:
        raise NativeUnavailable("Set WDP_QUESTION_ENCODING_BINARY to the built omega_wdp example.")
    path = Path(configured)
    if not path.is_file():
        raise NativeUnavailable(f"Native example not found: {path}")
    return path


def invoke(request: dict, *, timeout: int = 60) -> dict:
    try:
        result = subprocess.run(
            [str(executable())], input=json.dumps(request, separators=(",", ":")),
            capture_output=True, text=True, timeout=timeout, check=False,
        )
    except OSError as error:
        raise NativeUnavailable("Could not execute the native example.") from error
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise NativeRefusal({"refused": "INVALID_REQUEST_OR_RESPONSE", "detail": result.stderr[:1000]}) from error
    if type(payload) is not dict:
        raise NativeRefusal({"refused": "INVALID_NATIVE_RESPONSE"})
    if result.returncode != 0 or "refused" in payload:
        raise NativeRefusal(payload)
    return payload
