"""Exact transport to omega_functional through the packaged Rust executable.

No functional is evaluated in this module. An unavailable executable or an
invalid response is an error; there is no Python arithmetic fallback.
"""

from __future__ import annotations

import json
import subprocess
from fractions import Fraction
from typing import Callable


class FunctionalEvaluationError(RuntimeError):
    """The native evaluator was unavailable, refused, or broke its protocol."""


class NativeUnavailableError(FunctionalEvaluationError):
    """The native evaluator is not built, missing, or cannot be executed."""


class NativeTimeoutError(FunctionalEvaluationError):
    """The native evaluator exceeded its runtime budget."""


class NativeProtocolError(FunctionalEvaluationError):
    """The native evaluator returned invalid JSON or violated protocol."""


class CertificateMismatchError(FunctionalEvaluationError):
    """The native evaluator completed verification and found an inconsistency."""


def encode(value: int | Fraction) -> str:
    if type(value) not in (int, Fraction):
        raise TypeError("functional inputs must be exact integers or Fractions")
    return str(value)


def decode(value: object) -> Fraction:
    if type(value) is not str:
        raise FunctionalEvaluationError("native rationals must be strings")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise FunctionalEvaluationError("invalid native rational") from error
    if str(result) != value:
        raise FunctionalEvaluationError("noncanonical native rational")
    return result


def _unique_fields(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise FunctionalEvaluationError("duplicate response field")
        result[key] = value
    return result


def evaluate(request: dict, *, tick: Callable[[], None] | None = None) -> dict:
    from native_wdp import find_binary, NativeWdpUnavailable

    try:
        binary = find_binary("evaluate_wdp_functionals", "WDP_FUNCTIONALS_BIN")
    except NativeWdpUnavailable as error:
        raise NativeUnavailableError(str(error)) from error
    if binary is None:
        raise NativeUnavailableError("evaluate_wdp_functionals is not built")
    if tick is not None:
        tick()
    try:
        with subprocess.Popen(
            [str(binary)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True,
        ) as process:
            try:
                pending_input = json.dumps(request, allow_nan=False)
                for _ in range(3000):
                    if tick is not None:
                        tick()
                    try:
                        stdout, _stderr = process.communicate(pending_input, timeout=0.01)
                        break
                    except subprocess.TimeoutExpired:
                        pending_input = None
                else:
                    raise NativeTimeoutError("native evaluator exceeded 30 seconds")
            except BaseException:
                process.kill()
                process.communicate()
                raise
        if tick is not None:
            tick()
    except OSError as error:
        raise NativeUnavailableError(f"cannot execute native evaluator: {error}") from error
    try:
        response = json.loads(stdout, object_pairs_hook=_unique_fields)
    except json.JSONDecodeError as error:
        raise NativeProtocolError("native evaluator returned invalid JSON") from error
    if (process.returncode != 0 or type(response) is not dict
            or response.get("schema") != "wdp-functionals-v1"
            or response.get("authority_effect") != "None"):
        raise NativeProtocolError("invalid native evaluator response")
    if response.get("status") == "REFUSE":
        raise CertificateMismatchError(str(response.get("reason", "native refusal")))
    if (response.get("status") != "PASS" or type(response.get("result")) is not dict
            or json.dumps(response.get("request"), sort_keys=True) != json.dumps(request, sort_keys=True)):
        raise NativeProtocolError("native result is not bound to the submitted request")
    return response["result"]


def representative_mass(values, weights=None, *, tick=None) -> Fraction:
    values = tuple(values)
    weights = (1,) * len(values) if weights is None else tuple(weights)
    result = evaluate({"operation": "representative_mass",
                       "residual": [encode(x) for x in values],
                       "weights": [encode(x) for x in weights]}, tick=tick)
    return decode(result.get("value"))


def closure(d0, c0_dim: int, d1, residual, *, tick=None) -> Fraction:
    result = evaluate({"operation": "closure", "c0_dim": c0_dim,
                       "d0": [[encode(x) for x in row] for row in d0],
                       "d1": [[encode(x) for x in row] for row in d1],
                       "residual": [encode(x) for x in residual]}, tick=tick)
    return decode(result.get("value"))


def squared_l2(values) -> Fraction:
    return decode(evaluate({"operation": "squared_l2", "residual": [encode(x) for x in values]}).get("value"))


def polyhedral_gauge(facets, values) -> Fraction:
    return decode(evaluate({"operation": "polyhedral_gauge",
                            "facets": [[encode(x) for x in row] for row in facets],
                            "residual": [encode(x) for x in values]}).get("value"))


def dual_bound(matrix, columns, delta, weights, dual) -> Fraction:
    """Canonical signed pairing after exact dual feasibility and annihilation checks."""
    return decode(evaluate({"operation": "dual_bound", "columns": columns,
                            "matrix": [[encode(x) for x in row] for row in matrix],
                            "delta": [encode(x) for x in delta], "weights": [encode(x) for x in weights],
                            "dual": [encode(x) for x in dual]}).get("value"))
