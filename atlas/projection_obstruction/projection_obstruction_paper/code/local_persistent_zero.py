"""Finite, boundary-checked certificates for Proposition 5.20.

The independently supplied model fixes every Hamiltonian term and polynomial
readout. A certificate cannot remove a boundary term by omitting it. The result
concerns the declared polynomial, not every component of a quantum cumulant.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from itertools import combinations, product
from math import prod
from typing import Mapping

import sympy as sp
from polynomial_onset import OnsetCertificate, certify_onset, polynomial_lift, verify_onset


def _gaussian(value):
    value = sp.sympify(value) if type(value) is int else value
    if not isinstance(value, sp.Basic) or value.free_symbols:
        raise ValueError("exact Gaussian-rational entries required")
    real, imag = value.as_real_imag()
    if not isinstance(real, sp.Rational) or not isinstance(imag, sp.Rational):
        raise ValueError("exact Gaussian-rational entries required")
    return real + sp.I * imag


def _matrix(value):
    if not isinstance(value, sp.MatrixBase):
        raise ValueError("an explicit exact matrix is required")
    return sp.ImmutableMatrix(value.rows, value.cols, [_gaussian(x) for x in value])


@dataclass(frozen=True)
class LocalTerm:
    support: tuple[int, ...]
    operator: sp.ImmutableMatrix


@dataclass(frozen=True)
class LocalModel:
    dimensions: tuple[int, ...]
    region: tuple[int, ...]
    terms: tuple[LocalTerm, ...]
    basis: tuple[sp.ImmutableMatrix, ...]
    initial_region_state: sp.ImmutableMatrix
    readouts: tuple[Mapping[tuple[int, ...], sp.Rational], ...]
    degree: int


@dataclass(frozen=True)
class LocalZeroCertificate:
    model_digest: str
    generator: sp.ImmutableMatrix
    onset: OnsetCertificate


def _support(support, sites):
    if (not isinstance(support, tuple) or not support
            or any(type(i) is not int or i < 0 or i >= sites for i in support)
            or tuple(sorted(set(support))) != support):
        raise ValueError("nonempty sorted distinct in-range support required")


def _embed(operator, support, target, dimensions):
    """Explicit tensor placement; never truncate a crossing interaction."""
    dims = tuple(dimensions[i] for i in target)
    if prod(dims) > 64:
        raise ValueError("local boundary union exceeds the declared 64-dimensional budget")
    positions = tuple(target.index(i) for i in support)
    tuples = tuple(product(*(range(d) for d in dims)))

    def index(t):
        result = 0
        for position in positions:
            result = result * dims[position] + t[position]
        return result

    return sp.ImmutableMatrix(len(tuples), len(tuples), lambda i, j:
        operator[index(tuples[i]), index(tuples[j])]
        if all(tuples[i][k] == tuples[j][k] for k in range(len(dims)) if k not in positions)
        else 0)


def _encoded_matrix(matrix):
    return [[[str(sp.re(x)), str(sp.im(x))] for x in row] for row in matrix.tolist()]


def model_digest(model):
    payload = {"dimensions": model.dimensions, "region": model.region,
               "terms": [{"support": t.support, "operator": _encoded_matrix(t.operator)} for t in model.terms],
               "basis": [_encoded_matrix(b) for b in model.basis],
               "initial": _encoded_matrix(model.initial_region_state), "degree": model.degree,
               "readouts": [[[list(e), str(c)] for e, c in sorted(p.items())] for p in model.readouts]}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def checked_local_flow(model: LocalModel):
    """Replay Hermiticity, basis independence, identity, invariance and all crossings."""
    if (not isinstance(model.dimensions, tuple) or not model.dimensions
            or any(type(d) is not int or d < 1 for d in model.dimensions)):
        raise ValueError("positive finite site dimensions required")
    _support(model.region, len(model.dimensions))
    size = prod(model.dimensions[i] for i in model.region)
    if size > 8 or not model.basis or len(model.basis) > size * size:
        raise ValueError("local certificate basis exceeds its declared budget")
    basis = tuple(_matrix(b) for b in model.basis)
    if any(b.shape != (size, size) or b != b.H for b in basis):
        raise ValueError("basis must consist of Hermitian operators on the region")
    columns = sp.Matrix.hstack(*(b.reshape(size * size, 1) for b in basis))
    if columns.rank() != len(basis):
        raise ValueError("operator basis is dependent")
    identity = sp.eye(size).reshape(size * size, 1)
    if columns.row_join(identity).rank() != len(basis):
        raise ValueError("operator space does not contain identity")
    rho = _matrix(model.initial_region_state)
    if rho.shape != (size, size) or rho != rho.H or sp.trace(rho) != 1:
        raise ValueError("initial region state must be Hermitian with trace one")
    for k in range(1, size + 1):
        for indices in combinations(range(size), k):
            if rho.extract(indices, indices).det() < 0:
                raise ValueError("initial region state is not positive")
    region = set(model.region)
    local_h = sp.zeros(size)
    for term in model.terms:
        _support(term.support, len(model.dimensions))
        h = _matrix(term.operator)
        dimension = prod(model.dimensions[i] for i in term.support)
        if h.shape != (dimension, dimension) or h != h.H:
            raise ValueError("every term must be a Hermitian operator on its declared support")
        if set(term.support) <= region:
            local_h += _embed(h, term.support, model.region, model.dimensions)
        elif region.intersection(term.support):
            union = tuple(sorted(region.union(term.support)))
            boundary = _embed(h, term.support, union, model.dimensions)
            for b in basis:
                embedded = _embed(b, model.region, union, model.dimensions)
                if boundary * embedded != embedded * boundary:
                    raise ValueError("nonzero crossing commutator")
    rows = []
    for b in basis:
        derivative = sp.I * (local_h * b - b * local_h)
        if columns.row_join(derivative.reshape(size * size, 1)).rank() != len(basis):
            raise ValueError("operator space is not locally invariant")
        coefficients, parameters = columns.gauss_jordan_solve(derivative.reshape(size * size, 1))
        if parameters.rows or any(not isinstance(x, sp.Rational) for x in coefficients):
            raise ValueError("a unique real rational local generator is required")
        rows.append(list(coefficients))
    generator = sp.ImmutableMatrix(rows)
    initial = sp.ImmutableMatrix([sp.trace(b * rho) for b in basis])
    if type(model.degree) is not int or model.degree < 0:
        raise ValueError("nonnegative declared polynomial degree required")
    lift = polynomial_lift(generator, initial, model.readouts)
    if any(sum(e) > model.degree for p in model.readouts for e, c in p.items() if c):
        raise ValueError("polynomial exceeds the declared degree")
    return generator, initial, lift


def propose_local_zero(model: LocalModel) -> LocalZeroCertificate:
    generator, initial, _ = checked_local_flow(model)
    onset = certify_onset(generator, initial, model.readouts)
    if onset.first_onset is not None:
        raise ValueError("readout is not persistently zero")
    return LocalZeroCertificate(model_digest(model), generator, onset)


def verify_local_zero(model: LocalModel, certificate: LocalZeroCertificate) -> bool:
    try:
        generator, initial, _ = checked_local_flow(model)
        return (certificate.model_digest == model_digest(model)
                and certificate.generator == generator
                and certificate.onset.first_onset is None
                and verify_onset(generator, initial, model.readouts, certificate.onset))
    except (ValueError, TypeError, AttributeError, IndexError):
        return False


def encode_certificate(certificate: LocalZeroCertificate) -> dict:
    return {"schema_version": "po000.local_zero.v1", "model_digest": certificate.model_digest,
            "generator": [[str(x) for x in row] for row in certificate.generator.tolist()],
            "annihilator": [str(x) for x in certificate.onset.annihilator],
            "derivatives": [[str(x) for x in row] for row in certificate.onset.derivatives],
            "first_onset": certificate.onset.first_onset, "authority_effect": "None"}


def decode_certificate(payload: dict) -> LocalZeroCertificate:
    fields = {"schema_version", "model_digest", "generator", "annihilator", "derivatives", "first_onset", "authority_effect"}
    if (not isinstance(payload, dict) or set(payload) != fields
            or payload["schema_version"] != "po000.local_zero.v1"
            or payload["authority_effect"] != "None" or payload["first_onset"] is not None):
        raise ValueError("invalid local-zero envelope")

    def rational(text):
        from fractions import Fraction
        if not isinstance(text, str):
            raise ValueError("canonical rational string required")
        q = Fraction(text)
        if str(q) != text:
            raise ValueError("noncanonical rational string")
        return sp.Rational(q.numerator, q.denominator)

    return LocalZeroCertificate(payload["model_digest"],
        sp.ImmutableMatrix([[rational(x) for x in row] for row in payload["generator"]]),
        OnsetCertificate(tuple(rational(x) for x in payload["annihilator"]),
                         tuple(tuple(rational(x) for x in row) for row in payload["derivatives"]), None))
