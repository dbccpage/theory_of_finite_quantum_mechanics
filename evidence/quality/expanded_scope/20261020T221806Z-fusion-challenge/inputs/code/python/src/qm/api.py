"""The Python application delegates mathematical computation to Rust or pure-Python fallback.

Clean Architecture: Provides fail-soft access to computational suites and claim ledgers.
If the native PyO3 compiled extension `_native` is uncompiled or unavailable,
pure-Python fallbacks seamlessly serve schema fixtures, suite catalogs, and claim records.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
import logging
from fractions import Fraction
from importlib.resources import files
from typing import Any

logger = logging.getLogger(__name__)

_native: Any = None
_NATIVE_AVAILABLE: bool = False

try:
    from . import _native as _compiled_native

    _native = _compiled_native
    _NATIVE_AVAILABLE = True
except (ImportError, AttributeError):
    _native = None
    _NATIVE_AVAILABLE = False
    logger.debug("Native PyO3 extension '_native' is uncompiled; using pure-Python fallback.")


def is_native_available() -> bool:
    """Return whether the native PyO3 acceleration module is compiled and loaded."""
    return _NATIVE_AVAILABLE


def _encode(value: Any) -> Any:
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    raise TypeError(f"Unsupported input type: {type(value).__name__}")


def list_suites() -> list[str]:
    """List available computational suite identifiers."""
    if _NATIVE_AVAILABLE and _native is not None:
        return _native.list_suites()
    try:
        fixture = files("src.qm.data").joinpath("defaults.json")
        data = json.loads(fixture.read_text(encoding="utf-8"))
        return sorted(data.keys())
    except Exception as exc:
        logger.warning("Could not read defaults.json for suite list: %s", exc)
        return []


def claims(paper: str = "qm122") -> dict[str, Any]:
    """Return the structured claim ledger for the specified foundation paper."""
    if paper != "qm122":
        raise ValueError(f"UNKNOWN_PAPER:{paper}")
    if _NATIVE_AVAILABLE and _native is not None:
        return json.loads(_native.qm122_claims_json())
    fixture = files("src.qm.data").joinpath("quantum_claims.json")
    return json.loads(fixture.read_text(encoding="utf-8"))


def run_suite(name: str, request: Any = None) -> Any:
    """Execute a computational suite by name with typed or default parameters."""
    if request is None:
        fixture = files("src.qm.data").joinpath("defaults.json")
        request = json.loads(fixture.read_text(encoding="utf-8")).get(name)
    return run_json(name, json.dumps(request, default=_encode, allow_nan=False))


def run_json(name: str, request_text: str) -> Any:
    """Preserve raw numeric tokens and the native duplicate-key contract."""
    if _NATIVE_AVAILABLE and _native is not None:
        return json.loads(_native.run_suite_json(name, request_text))
    raise RuntimeError(
        f"Native acceleration engine '_native' is uncompiled for suite '{name}'. "
        f"Use pure-Python algorithms in 'finite_qm.use_cases' or compile the PyO3 crate."
    )
