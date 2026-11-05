"""Process adapter to the canonical Rust functional evaluators."""
from fractions import Fraction

from coda_application.domain.l1_quotient import QuotientCertificate, _no_tick
from witnessed_difference.native_functionals import (
    FunctionalEvaluationError, closure, decode, encode, evaluate, representative_mass,
)


def _matrix(rows, n_cols):
    if type(n_cols) is not int or n_cols < 0:
        raise ValueError("column count must be a nonnegative integer")
    result = []
    for row in rows:
        if type(row) is not dict or any(type(j) is not int or not 0 <= j < n_cols for j in row):
            raise ValueError("invalid sparse matrix coordinate")
        for value in row.values():
            encode(value)
        result.append([row.get(j, Fraction(0)) for j in range(n_cols)])
    return result


def _request(rows, n_cols, x):
    matrix = _matrix(rows, n_cols)
    if len(x) != len(matrix):
        raise ValueError("cochain and matrix row counts differ")
    return {"matrix": [[encode(v) for v in row] for row in matrix],
            "columns": n_cols, "delta": [encode(v) for v in x],
            "weights": ["1"] * len(x)}


class NativeFunctionalEvaluator:
    def mass(self, values, tick=_no_tick):
        return representative_mass(values, tick=tick)

    def solve(self, rows, n_cols, x, tick=_no_tick):
        request = _request(rows, n_cols, x)
        result = evaluate({**request, "operation": "solve_phi1", "max_pivots": 100000}, tick=tick)
        if any(type(result.get(key)) is not list or len(result[key]) != size
               for key, size in (("potential", n_cols), ("residual", len(x)), ("dual", len(x)))):
            raise FunctionalEvaluationError("native certificate dimensions differ")
        cert = QuotientCertificate(decode(result.get("value")), tuple(map(decode, result["potential"])),
                                   tuple(map(decode, result["residual"])), tuple(map(decode, result["dual"])),
                                   "omega_functional exact primal-dual")
        self._verify(cert, request, tick)
        return cert

    def _verify(self, cert, request, tick=_no_tick):
        result = evaluate({**request, "operation": "verify_phi1", "value": encode(cert.distance),
                           "potential": [encode(v) for v in cert.repair],
                           "residual": [encode(v) for v in cert.residual],
                           "dual": [encode(v) for v in cert.witness]}, tick=tick)
        if decode(result.get("value")) != cert.distance:
            raise FunctionalEvaluationError("verified value differs")

    def verify(self, certificate, rows, n_cols, x):
        try:
            self._verify(certificate, _request(rows, n_cols, x))
            return True
        except (ValueError, TypeError, FunctionalEvaluationError):
            return False

    def verify_repair(self, rows, n_cols, x, repair, witness, value, tick=_no_tick):
        request = _request(rows, n_cols, x)
        try:
            result = evaluate({**request, "operation": "evaluate_phi1",
                               "potential": [encode(v) for v in repair],
                               "dual": [encode(v) for v in witness]}, tick=tick)
            return decode(result.get("value")) == value
        except (ValueError, TypeError, FunctionalEvaluationError):
            return False

    def closure(self, d0, n_cols, d1, x, tick=_no_tick):
        return closure(_matrix(d0, n_cols), n_cols, _matrix(d1, len(x)), x, tick=tick)
