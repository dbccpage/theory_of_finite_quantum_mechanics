"""Native Rust bridge for Witnessed Difference Programme (WDP).

# Executable finite evidence; AuthorityEffect: None.

Provides an exact rational interface to the native Rust binaries:
- solve_wdp_obstruction
- solve_genesis_observer

Boundary contract:
- All operations carry AuthorityEffect: None.
- Exact rational arithmetic is strictly enforced; floats and bools in numeric
  contexts are rejected by the exact rational float firewall.
- Typed errors: NativeWdpUnavailable, NativeWdpRefusal, NativeWdpTimeout, NativeWdpProtocolError.
- Functional evaluation requires the native owner; unavailable execution refuses.
"""

from __future__ import annotations

import json
import os
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Mapping, Optional, Sequence, Tuple

from witnessed_difference.obstruction import MatrixQuotientCertificate, verify_matrix_certificate
from witnessed_difference.native_functionals import decode, FunctionalEvaluationError, _unique_fields
from witnessed_difference.outcomes import Refused
from witnessed_difference.ports import GenesisDescentResult, WdpObstructionSolution
from witnessed_difference.rop import Err, Ok, Refusal, Result

RUST_DIR = Path(__file__).resolve().parent / "rust"
NATIVE_TIMEOUT_SECONDS = 30


class NativeWdpError(RuntimeError):
    """Base class for native boundary failures."""


class NativeWdpUnavailable(NativeWdpError):
    code = "WDP_NATIVE_UNAVAILABLE"


class NativeWdpRefusal(NativeWdpError):
    code = "WDP_NATIVE_REFUSAL"


class NativeWdpTimeout(NativeWdpError):
    code = "WDP_NATIVE_TIMEOUT"


class NativeWdpProtocolError(NativeWdpError):
    code = "WDP_NATIVE_PROTOCOL"


def _exact_rat_str(value: int | Fraction) -> str:
    if isinstance(value, bool) or type(value) not in (int, Fraction):
        raise TypeError(f"Exact rational required, got {type(value).__name__}: {value!r}")
    return str(value)


def _repository_root(start: Path) -> Optional[Path]:
    for candidate in (start, *start.parents):
        marker = candidate / ".git"
        if marker.is_file() or marker.is_dir():
            return candidate
    return None


def find_binary(binary_name: str, env_var: Optional[str] = None) -> Optional[Path]:
    """Return the configured executable, then a paper build, then a package-local one.

    Release wins over debug in each home. The workspace ``target`` directory is
    last: this package's binaries are not emitted there.
    """
    if env_var:
        env_val = os.environ.get(env_var)
        if env_val:
            candidate = Path(env_val)
            if candidate.is_file():
                return candidate
            raise NativeWdpUnavailable(f"{env_var} is not an existing file: {candidate}")
    names = (f"{binary_name}.exe", binary_name)
    directories: list[Path] = []
    configured_target = os.environ.get("CARGO_TARGET_DIR")
    if configured_target:
        directories.extend([Path(configured_target) / "release", Path(configured_target) / "debug"])
    repo_root = _repository_root(RUST_DIR)
    if repo_root is not None:
        directories.extend([
            repo_root / "target_paper_rust" / "release",
            repo_root / "target_paper_rust" / "debug",
        ])
    directories.extend([
        RUST_DIR / "target" / "release",
        RUST_DIR / "target" / "debug",
    ])
    if repo_root is not None:
        directories.extend([
            repo_root / "target" / "release",
            repo_root / "target" / "debug",
        ])
    for directory in directories:
        for name in names:
            candidate = directory / name
            if candidate.is_file():
                return candidate
    return None


def _boundary_refusal(
    require_native: bool,
    error: NativeWdpError,
    *,
    code: str,
    locus: str,
    cause: Optional[BaseException] = None,
) -> Err[Refusal]:
    """Raise the native error when the caller demanded it; otherwise return Err."""
    if require_native:
        if cause is None:
            raise error
        raise error from cause
    return Err(
        Refusal(
            code=code,
            message=str(error),
            locus=locus,
            details=(("authority_effect", "None"),),
        )
    )


def solve_native_obstruction(
    vertices: Sequence[str],
    edges: Sequence[Tuple[str, str]],
    cochain: Mapping[Tuple[str, str], int | Fraction],
    require_native: bool = False,
) -> Result[WdpObstructionSolution, Refusal]:
    """Solve exact potential and dual obstruction certificate."""
    vertices = tuple(vertices)
    edges = tuple(tuple(edge) for edge in edges)
    if (any(type(vertex) is not str or "," in vertex for vertex in vertices)
            or len(set(vertices)) != len(vertices)
            or any(len(edge) != 2 or any(vertex not in vertices for vertex in edge) for edge in edges)
            or len(set(edges)) != len(edges) or set(cochain) != set(edges)):
        return _boundary_refusal(require_native, NativeWdpProtocolError("invalid graph carrier or cochain keys"),
                                 code="WDP_NATIVE_INPUT", locus="native_wdp.solve_native_obstruction")
    serialized_cochain: dict[str, str] = {}
    for (u, v), val in cochain.items():
        serialized_cochain[f"{u},{v}"] = _exact_rat_str(val)

    binary = find_binary("solve_wdp_obstruction", "WDP_OBSTRUCTION_BIN")
    if binary is None:
        if require_native:
            raise NativeWdpUnavailable("solve_wdp_obstruction binary not found and require_native=True")
        return _boundary_refusal(False, NativeWdpUnavailable("solve_wdp_obstruction is not built"),
                                 code="WDP_NATIVE_UNAVAILABLE", locus="native_wdp.solve_native_obstruction")

    req = {
        "vertices": list(vertices),
        "edges": [list(e) for e in edges],
        "cochain": serialized_cochain,
    }

    try:
        proc = subprocess.run(
            [str(binary)],
            input=json.dumps(req),
            text=True,
            capture_output=True,
            check=False,
            timeout=NATIVE_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as err:
        return _boundary_refusal(
            require_native,
            NativeWdpTimeout(f"solve_wdp_obstruction exceeded {NATIVE_TIMEOUT_SECONDS}s"),
            code="WDP_NATIVE_TIMEOUT",
            locus="native_wdp.solve_native_obstruction",
            cause=err,
        )
    except OSError as err:
        unavailable = NativeWdpUnavailable(f"Cannot execute {binary}: {err}")
        return _boundary_refusal(
            require_native,
            unavailable,
            code=unavailable.code,
            locus="native_wdp.solve_native_obstruction",
            cause=err,
        )

    try:
        payload = json.loads(proc.stdout, object_pairs_hook=_unique_fields)
        if type(payload) is not dict:
            raise NativeWdpProtocolError("native response must be an object")
    except (json.JSONDecodeError, FunctionalEvaluationError, NativeWdpProtocolError) as err:
        protocol = NativeWdpProtocolError(
            f"Non-JSON response from {binary} (exit {proc.returncode}): {proc.stdout[:200]!r}"
        )
        return _boundary_refusal(
            require_native,
            protocol,
            code=protocol.code,
            locus="native_wdp.solve_native_obstruction",
            cause=err,
        )

    if payload.get("status") == "REFUSE":
        if require_native:
            raise NativeWdpRefusal(payload.get("reason", "unspecified refusal"))
        return Err(Refusal(
            code=payload.get("code", "WDP_NATIVE_REFUSAL"),
            message=payload.get("reason", "unspecified refusal"),
            locus="native_wdp.solve_native_obstruction",
            details=(("authority_effect", "None"),),
        ))

    if proc.returncode != 0 or payload.get("status") != "PASS":
        return _boundary_refusal(
            require_native,
            NativeWdpProtocolError(
                f"Unexpected native response (exit {proc.returncode}): {payload!r}"
            ),
            code="WDP_NATIVE_UNEXPECTED",
            locus="native_wdp.solve_native_obstruction",
        )

    try:
        required = {"status", "phi1", "is_exact", "potential", "residual", "dual_witness", "authority_effect"}
        if set(payload) != required or type(payload["is_exact"]) is not bool or payload["authority_effect"] != "None":
            raise FunctionalEvaluationError("incomplete certificate or invalid metadata")
        def mapping(name, keys):
            raw = payload[name]
            if type(raw) is not dict or set(raw) != set(keys):
                raise FunctionalEvaluationError("native coordinate set does not match the input")
            return {key: decode(value) for key, value in raw.items()}
        names = [f"{u},{v}" for u, v in edges]
        potential = mapping("potential", vertices)
        residual = mapping("residual", names)
        dual = mapping("dual_witness", names)
        value = decode(payload["phi1"])
        if payload["is_exact"] != (value == 0):
            raise FunctionalEvaluationError("native exactness flag disagrees with its value")
        positions = {vertex: i for i, vertex in enumerate(vertices)}
        rows = []
        for u, v in edges:
            row = [Fraction(0)] * len(vertices)
            row[positions[u]] -= 1
            row[positions[v]] += 1
            rows.append(tuple(row))
        certificate = MatrixQuotientCertificate(
            tuple(rows), len(vertices), tuple(Fraction(cochain[edge]) for edge in edges),
            (Fraction(1),) * len(edges), tuple(potential[v] for v in vertices),
            tuple(residual[name] for name in names), value, tuple(dual[name] for name in names),
        )
        checked = verify_matrix_certificate(certificate)
        if isinstance(checked, Refused):
            raise FunctionalEvaluationError(checked.detail)
    except (FunctionalEvaluationError, KeyError, TypeError, ValueError) as error:
        return _boundary_refusal(require_native, NativeWdpProtocolError(str(error)),
                                 code="WDP_NATIVE_PROTOCOL", locus="native_wdp.solve_native_obstruction", cause=error)
    return Ok(WdpObstructionSolution(
        phi1=value, is_exact=payload["is_exact"], potential=potential,
        residual={edge: residual[name] for edge, name in zip(edges, names)},
        dual_witness={edge: dual[name] for edge, name in zip(edges, names)},
        authority_effect="None", backend="rust",
    ))


def solve_native_genesis_descent(
    memory_transitions: Sequence[Sequence[int]],
    memory_initial: int,
    transducer_transitions: Sequence[Sequence[int]],
    transducer_emit: Sequence[Sequence[Sequence[int]]],
    transducer_initial: int,
    prefix_words: Sequence[int],
    final_words: Sequence[Sequence[int]],
    require_native: bool = False,
) -> Result[GenesisDescentResult, Refusal]:
    """Construct a finite descent map or collision, using Rust when available.

    With require_native=False, a missing binary selects exact Python descent
    search. This constructs a finite map/collision; it evaluates no Phi or
    Gamma functional. Functional evaluation has no Python fallback.
    """
    from original_genesis_observer import HistoryMemory, WordTransducer
    try:
        mem = HistoryMemory(memory_transitions, memory_initial)
        trans = WordTransducer(transducer_transitions, transducer_emit, transducer_initial, prefix_words, final_words)
        if len(mem.transitions[0]) != len(trans.transitions[0]):
            raise ValueError("alphabet mismatch")
    except (ValueError, TypeError) as error:
        return _boundary_refusal(require_native, NativeWdpProtocolError(str(error)),
                                 code="WDP_NATIVE_INPUT", locus="native_wdp.solve_native_genesis_descent", cause=error)
    binary = find_binary("solve_genesis_observer", "WDP_GENESIS_BIN")
    if binary is None:
        if require_native:
            raise NativeWdpUnavailable("solve_genesis_observer binary not found and require_native=True")
        from original_genesis_observer import HistoryMemory, WordTransducer
        mem = HistoryMemory(memory_transitions, memory_initial)
        trans = WordTransducer(
            transducer_transitions,
            transducer_emit,
            transducer_initial,
            prefix_words,
            final_words,
        )
        res = trans.descent(mem)
        if res[0] == "map":
            return Ok(GenesisDescentResult(
                kind="map",
                prefix=tuple(prefix_words),
                certificate=str(res[1:]),
                authority_effect="None",
                backend="python_fallback",
            ))
        return Ok(GenesisDescentResult(
            kind="collision",
            collision_first=tuple(res[1]),
            collision_second=tuple(res[2]),
            authority_effect="None",
            backend="python_fallback",
        ))

    req = {
        "memory_transitions": [list(row) for row in memory_transitions],
        "memory_initial": memory_initial,
        "transducer_transitions": [list(row) for row in transducer_transitions],
        "transducer_emit": [[list(w) for w in row] for row in transducer_emit],
        "transducer_initial": transducer_initial,
        "prefix_words": list(prefix_words),
        "final_words": [list(w) for w in final_words],
    }

    try:
        proc = subprocess.run(
            [str(binary)],
            input=json.dumps(req),
            text=True,
            capture_output=True,
            check=False,
            timeout=NATIVE_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as err:
        return _boundary_refusal(
            require_native,
            NativeWdpTimeout(f"solve_genesis_observer exceeded {NATIVE_TIMEOUT_SECONDS}s"),
            code="WDP_NATIVE_TIMEOUT",
            locus="native_wdp.solve_native_genesis_descent",
            cause=err,
        )
    except OSError as err:
        unavailable = NativeWdpUnavailable(f"Cannot execute {binary}: {err}")
        return _boundary_refusal(
            require_native,
            unavailable,
            code=unavailable.code,
            locus="native_wdp.solve_native_genesis_descent",
            cause=err,
        )

    try:
        payload = json.loads(proc.stdout, object_pairs_hook=_unique_fields)
        if type(payload) is not dict:
            raise NativeWdpProtocolError("native response must be an object")
    except (json.JSONDecodeError, FunctionalEvaluationError, NativeWdpProtocolError) as err:
        protocol = NativeWdpProtocolError(
            f"Non-JSON response from {binary} (exit {proc.returncode}): {proc.stdout[:200]!r}"
        )
        return _boundary_refusal(
            require_native,
            protocol,
            code=protocol.code,
            locus="native_wdp.solve_native_genesis_descent",
            cause=err,
        )

    if payload.get("status") == "REFUSE":
        if require_native:
            raise NativeWdpRefusal(payload.get("reason", "unspecified refusal"))
        return Err(Refusal(
            code=payload.get("code", "WDP_NATIVE_REFUSAL"),
            message=payload.get("reason", "unspecified refusal"),
            locus="native_wdp.solve_native_genesis_descent",
            details=(("authority_effect", "None"),),
        ))

    if proc.returncode != 0 or payload.get("status") != "PASS":
        return _boundary_refusal(
            require_native,
            NativeWdpProtocolError(f"Unexpected response (exit {proc.returncode}): {payload!r}"),
            code="WDP_NATIVE_UNEXPECTED",
            locus="native_wdp.solve_native_genesis_descent",
        )

    try:
        if payload.get("authority_effect") != "None":
            raise NativeWdpProtocolError("native descent may not grant authority")
        common = {"status", "kind", "authority_effect"}
        if payload.get("kind") == "map":
            if set(payload) != common | {"prefix", "certificate"}:
                raise NativeWdpProtocolError("invalid map response fields")
            if type(payload["prefix"]) is not list or any(type(x) is not int for x in payload["prefix"]):
                raise NativeWdpProtocolError("invalid prefix")
            if tuple(payload["prefix"]) != trans.prefix:
                raise NativeWdpProtocolError("prefix changed")
            submitted = payload["certificate"]
            if type(submitted) is not list or any(x is not None and type(x) is not int for x in submitted):
                raise NativeWdpProtocolError("invalid map certificate")
            checked = trans.descent(mem)
            if checked[0] != "map" or tuple(submitted) != checked[1]:
                raise NativeWdpProtocolError("descent map failed finite replay")
            res = GenesisDescentResult(kind="map", prefix=trans.prefix,
                                       certificate=json.dumps(submitted), authority_effect="None", backend="rust")
        elif payload.get("kind") == "collision":
            if set(payload) != common | {"collision_first", "collision_second"}:
                raise NativeWdpProtocolError("invalid collision response fields")
            first, second = payload["collision_first"], payload["collision_second"]
            if type(first) is not list or type(second) is not list:
                raise NativeWdpProtocolError("collision words must be lists")
            if mem.run(first) != mem.run(second) or mem.run(trans.apply(first)) == mem.run(trans.apply(second)):
                raise NativeWdpProtocolError("collision failed direct replay")
            res = GenesisDescentResult(kind="collision", collision_first=tuple(first), collision_second=tuple(second),
                                       authority_effect="None", backend="rust")
        else:
            raise NativeWdpProtocolError("unknown descent result")
    except (ValueError, TypeError, KeyError, NativeWdpProtocolError) as error:
        return _boundary_refusal(require_native, NativeWdpProtocolError(str(error)),
                                 code="WDP_NATIVE_PROTOCOL", locus="native_wdp.solve_native_genesis_descent", cause=error)
    return Ok(res)
