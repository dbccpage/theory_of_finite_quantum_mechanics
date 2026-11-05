# -*- coding: utf-8 -*-
"""
Problem intake: structural validation, exact normalisation and the problem digest.

Every evaluation starts here. A malformed instance (wrong container types, float or
symbolic entries, a cochain that does not match the boundary, a coboundary pair with
d1 d0 != 0, overlap keys that are not label pairs) raises ``IntakeError``, which the
pipeline turns into a typed REFUSED terminal. The normalised snapshot is what the
layers evaluate and what the digest binds, so mutating a caller's matrix afterwards
cannot change evaluated evidence.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Dict, List, Mapping, Tuple

from sympy import Rational
from sympy.matrices import MatrixBase

from coda_application.domain._seal import digest

Row = Dict[int, Fraction]


class IntakeError(ValueError, TypeError):
    """The problem instance is malformed; evaluation refuses it by name.

    Both a ValueError (bad shape or value) and a TypeError (bad kind), so callers that
    catch either see a typed refusal."""


def exact(value: Any, where: str) -> Fraction:
    if isinstance(value, bool):
        raise IntakeError(f"{where}: bool is not an exact rational")
    if isinstance(value, Rational):  # sympy.Float, Symbol, sqrt(2), zoo are not Rationals
        return Fraction(int(value.p), int(value.q))
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    raise IntakeError(f"{where}: {value!r} ({type(value).__name__}) is not an exact rational")


def matrix_rows(mat: Any, name: str) -> Tuple[List[Row], Tuple[int, int]]:
    if not isinstance(mat, MatrixBase):
        raise IntakeError(f"{name} must be a sympy Matrix, got {type(mat).__name__}")
    rows: List[Row] = [dict() for _ in range(mat.rows)]
    for (i, j), value in mat.todok().items():
        v = exact(value, f"{name}[{i},{j}]")
        if v:
            rows[i][j] = v
    return rows, (mat.rows, mat.cols)


def _fracs(values: Any, where: str) -> Tuple[Fraction, ...]:
    if not isinstance(values, (tuple, list)):
        raise IntakeError(f"{where} must be a tuple of exact rationals")
    return tuple(exact(v, f"{where}[{i}]") for i, v in enumerate(values))


def _ints(values: Any, where: str) -> Tuple[int, ...]:
    if not isinstance(values, (tuple, list)) or any(isinstance(v, bool) or not isinstance(v, int) for v in values):
        raise IntakeError(f"{where} must be a tuple of ints")
    return tuple(int(v) for v in values)


def _pair(f: Fraction) -> List[int]:
    return [f.numerator, f.denominator]


def _sparse(rows: List[Row], shape: Tuple[int, int]) -> Dict[str, Any]:
    return {
        "shape": list(shape),
        "nz": sorted([i, j, v.numerator, v.denominator] for i, row in enumerate(rows) for j, v in row.items()),
    }


@dataclass(frozen=True)
class IntakeData:
    """Normalised exact snapshot of a well-formed problem instance."""

    problem_id: str
    sieve: Tuple[str, ...]
    coarse: Tuple[int, ...]
    fine: Tuple[int, ...]
    projection: Tuple[Tuple[int, int], ...]
    sections: Tuple[Tuple[str, Tuple[Fraction, ...]], ...]
    overlaps: Tuple[Tuple[Tuple[str, str], bool], ...]
    d0_rows: Tuple[Row, ...]
    d0_shape: Tuple[int, int]
    d1_rows: Tuple[Row, ...]
    d1_shape: Tuple[int, int]
    cochain: Tuple[Fraction, ...]
    enclosure: Tuple[Fraction, Fraction]
    digest: str

    def section(self, label: str):
        for name, values in self.sections:
            if name == label:
                return values
        return None


def intake(problem: Any) -> IntakeData:
    """Validate and normalise ``problem``; raise IntakeError with the reason if malformed."""
    pid = getattr(problem, "problem_id", None)
    if not isinstance(pid, str) or not pid.strip():
        raise IntakeError("problem_id must be a non-blank string")
    raw_data = getattr(problem, "raw_data", None)
    if type(raw_data) is not str:
        raise IntakeError("raw_data must be an explicit source-description string")
    sieve = problem.candidate_sieve
    if not isinstance(sieve, (tuple, list)) or any(not isinstance(c, str) for c in sieve):
        raise IntakeError("candidate_sieve must be a tuple of strings")
    coarse = _ints(problem.coarse_profile, "coarse_profile")
    fine = _ints(problem.fine_profile, "fine_profile")
    if len(set(fine)) != len(fine) or len(set(coarse)) != len(coarse):
        raise IntakeError("profile labels must be distinct within each declared carrier")
    if not isinstance(problem.projection_map, Mapping):
        raise IntakeError("projection_map must be a mapping of ints")
    projection = tuple(sorted(_ints((k, v), "projection_map entry") for k, v in problem.projection_map.items()))
    if not isinstance(problem.local_sections, Mapping):
        raise IntakeError("local_sections must be a mapping of labels to exact tuples")
    sections = []
    for label, values in problem.local_sections.items():
        if not isinstance(label, str):
            raise IntakeError("section labels must be strings")
        sections.append((label, _fracs(values, f"local_sections[{label!r}]")))
    if not isinstance(problem.overlaps, Mapping):
        raise IntakeError("overlaps must be a mapping of label pairs to bools")
    overlaps = []
    for key, compatible in problem.overlaps.items():
        if not (isinstance(key, tuple) and len(key) == 2 and all(isinstance(k, str) for k in key)):
            raise IntakeError(f"overlap key {key!r} is not a pair of section labels")
        if not isinstance(compatible, bool):
            raise IntakeError(f"overlap {key!r} compatibility must be a bool")
        overlaps.append((key, compatible))
    d0_rows, d0_shape = matrix_rows(problem.d0, "d0")
    d1_rows, d1_shape = matrix_rows(problem.d1, "d1")
    x_rows, x_shape = matrix_rows(problem.defect_cochain, "defect_cochain")
    if x_shape[1] != 1:
        raise IntakeError(f"defect_cochain must be a single column, got shape {x_shape}")
    if x_shape[0] != d0_shape[0]:
        raise IntakeError(f"defect_cochain has {x_shape[0]} entries but d0 has {d0_shape[0]} rows")
    if d1_shape[0] and d1_shape[1] != x_shape[0]:
        raise IntakeError(f"d1 has {d1_shape[1]} columns but the cochain has {x_shape[0]} entries")
    for r, row in enumerate(d1_rows):  # d1 d0 = 0: the two differentials form a complex
        acc: Dict[int, Fraction] = {}
        for i, a in row.items():
            for j, b in d0_rows[i].items():
                acc[j] = acc.get(j, Fraction(0)) + a * b
        if any(v for v in acc.values()):
            raise IntakeError(f"d1 d0 != 0 (row {r}): the differentials do not form a cochain complex")
    cochain = tuple(x_rows[i].get(0, Fraction(0)) for i in range(x_shape[0]))
    enc = problem.enclosure_interval
    if not isinstance(enc, tuple) or len(enc) != 2:
        raise IntakeError("enclosure_interval must be a pair of exact rationals")
    enclosure = (exact(enc[0], "enclosure lo"), exact(enc[1], "enclosure hi"))
    body = {
        "problem_id": pid,
        "raw_data": raw_data,
        "sieve": list(sieve),
        "coarse": list(coarse),
        "fine": list(fine),
        "projection": [list(p) for p in projection],
        "sections": sorted([label, [_pair(v) for v in values]] for label, values in sections),
        "overlaps": sorted([[list(k), c] for k, c in overlaps]),
        "d0": _sparse(d0_rows, d0_shape),
        "d1": _sparse(d1_rows, d1_shape),
        "cochain": [_pair(v) for v in cochain],
        "enclosure": [_pair(enclosure[0]), _pair(enclosure[1])],
    }
    return IntakeData(
        problem_id=pid,
        sieve=tuple(sieve),
        coarse=coarse,
        fine=fine,
        projection=projection,
        sections=tuple(sections),
        overlaps=tuple(overlaps),
        d0_rows=tuple(d0_rows),
        d0_shape=d0_shape,
        d1_rows=tuple(d1_rows),
        d1_shape=d1_shape,
        cochain=cochain,
        enclosure=enclosure,
        digest=digest(body),
    )
