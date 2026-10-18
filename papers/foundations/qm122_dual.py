"""Exact Python dual of the named QM-122 report, dilation, and Gauss-integer witnesses.

Origin: papers/foundations/finite_ledger.md claim QM-122-C38, and lean4/H010Scale.lean theorem witnesses_are_the_special_case.
Claim: urn:omega:fqm:qm122:python-dual-of-named-lean-witnesses:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by papers/foundations/_code/qm_122/tests/test_qm122_dual.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 9; AST Sonar cognitive complexity max 9; AST nesting depth max 3; lizard 1.24.1 cyclomatic complexity max 9.
Scope Fence: This file does not prove Gleason uniqueness, does not recover M_n(C), and does not claim the two mix witnesses are a theorem for every Gaussian vector. It is not a Lean proof.

The exhibited vectors are lean4/H008PhaseBlindPresentation.lean psi1 and psi2.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from itertools import permutations
from typing import Mapping as TypingMapping


class Qm122DualError(ValueError):
    """One violated QM-122 dual invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: TypingMapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> Qm122DualError:
    return Qm122DualError(invariant, parameters)


def _exact_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an integer weight was required", role=role)
    if type(value) is int:
        return value
    raise _fail("value is not an exact integer", role=role, received=type(value).__name__)


def _require_report(value: object, role: str) -> bool:
    if type(value) is not bool:
        raise _fail("report is not a boolean", role=role, received=type(value).__name__)
    return value


Report = bool
Pair = tuple[bool, bool]


def _collapsed_report() -> Report:
    collapsed = False
    return collapsed


def collapse(q: object) -> Report:
    _require_report(q, "collapse")
    return _collapsed_report()


def toggle(q: object) -> Report:
    report = _require_report(q, "toggle")
    return not report


def has_two_sided_inverse(tau: Callable[[Report], Report]) -> bool:
    tau_table = {q: tau(q) for q in (False, True)}
    if any(type(image) is not bool for image in tau_table.values()):
        return False
    for inv_false in (False, True):
        for inv_true in (False, True):
            inv = {False: inv_false, True: inv_true}

            def inv_fn(q: Report, table: dict[bool, bool] = inv) -> Report:
                return table[q]

            if all(inv_fn(tau_table[q]) == q and tau_table[inv_fn(q)] == q for q in (False, True)):
                return True
    return False


def bool_reversibles() -> list[Callable[[Report], Report]]:
    maps: list[Callable[[Report], Report]] = []
    for f_false in (False, True):
        for f_true in (False, True):
            table = {False: f_false, True: f_true}

            def tau(q: Report, t: dict[bool, bool] = table) -> Report:
                return t[q]

            if has_two_sided_inverse(tau):
                maps.append(tau)
    return maps


PAIR_DOMAIN: tuple[Pair, ...] = tuple((a, b) for a in (False, True) for b in (False, True))


def _reversible_pair_maps() -> list[Callable[[Pair], Pair]]:
    maps: list[Callable[[Pair], Pair]] = []
    for outputs in permutations(PAIR_DOMAIN):
        table = dict(zip(PAIR_DOMAIN, outputs, strict=True))

        def pair_map(x: Pair, values: dict[Pair, Pair] = table) -> Pair:
            return values[x]

        maps.append(pair_map)
    return maps


def identity_dilations() -> list[Callable[[Pair], Pair]]:
    """Every reversible map that fixes the report coordinate."""
    return [dil for dil in _reversible_pair_maps() if all(dil(x)[0] == x[0] for x in PAIR_DOMAIN)]


def collapse_dilations() -> list[Callable[[Pair], Pair]]:
    """Reversible dilations whose prepared-ancilla slice collapses the report."""
    return [
        dil
        for dil in _reversible_pair_maps()
        if all(dil((q, False))[0] == collapse(q) for q in (False, True))
    ]


def _gauss(value: object, role: str) -> tuple[int, int]:
    if isinstance(value, tuple) and len(value) == 2:
        return (_exact_int(value[0], role + ".re"), _exact_int(value[1], role + ".im"))
    raise _fail("gaussian integer is not a pair", role=role, received=type(value).__name__)


def gmul(z: object, w: object) -> tuple[int, int]:
    ar, ai = _gauss(z, "left")
    br, bi = _gauss(w, "right")
    return (ar * br - ai * bi, ar * bi + ai * br)


def one_plus_i_not_unit() -> bool:
    """Exact mod-two obstruction: no residue w satisfies (1+i)w ≡ 1."""
    for x_mod_two in (0, 1):
        for y_mod_two in (0, 1):
            real, imag = gmul((1, 1), (x_mod_two, y_mod_two))
            if (real % 2, imag % 2) == (1, 0):
                return False
    return True


def _weight_at(value: Mapping[object, object], label: bool, role: str) -> int:
    for key in value:
        if type(key) is not bool:
            raise _fail("weight map key is not a report boolean", role=role, received=type(key).__name__)
    if label not in value:
        raise _fail("weight map misses a report", role=role, report=label)
    return _exact_int(value[label], role)


def _weight_map(value: object, role: str) -> dict[bool, int]:
    if not isinstance(value, Mapping):
        raise _fail("weight map is not a mapping", role=role, received=type(value).__name__)
    return {False: _weight_at(value, False, role), True: _weight_at(value, True, role)}


def _pair(value: object) -> Pair:
    if not isinstance(value, tuple) or len(value) != 2:
        raise _fail("pair is not a report pair", received=type(value).__name__)
    return (_require_report(value[0], "pair[0]"), _require_report(value[1], "pair[1]"))


def dump_right(u: object, v: object, p: object) -> int:
    left = _weight_map(u, "dump.u")
    right = _weight_map(v, "dump.v")
    report, ancilla = _pair(p)
    if ancilla:
        return 0
    return left[report] * (right[False] + right[True])


def tensor(u: object, v: object, p: object) -> int:
    left = _weight_map(u, "tensor.u")
    right = _weight_map(v, "tensor.v")
    report, ancilla = _pair(p)
    return left[report] * right[ancilla]


def delta(i: object) -> dict[bool, int]:
    report = _require_report(i, "delta")
    if report:
        return {False: 0, True: 1}
    return {False: 1, True: 0}


def no_report_half_step() -> bool:
    for s_false in (False, True):
        for s_true in (False, True):
            sigma = {False: s_false, True: s_true}
            if all(sigma[sigma[q]] == toggle(q) for q in (False, True)):
                return False
    return True


def _gauss_at(value: Mapping[object, object], label: bool, role: str) -> tuple[int, int]:
    if label not in value:
        raise _fail("gaussian vector misses a report", role=role, report=label)
    return _gauss(value[label], role)


def _gauss_map(value: object, role: str) -> dict[bool, tuple[int, int]]:
    if not isinstance(value, Mapping):
        raise _fail("gaussian vector is not a mapping", role=role, received=type(value).__name__)
    return {False: _gauss_at(value, False, role), True: _gauss_at(value, True, role)}


def mix(v: object) -> dict[bool, tuple[int, int]]:
    parsed = _gauss_map(v, "mix")
    vf = parsed[False]
    vt = parsed[True]
    return {
        False: (vf[0] + vt[0], vf[1] + vt[1]),
        True: (vf[0] - vt[0], vf[1] - vt[1]),
    }


def nsq(z: object) -> int:
    real, imag = _gauss(z, "nsq")
    return real * real + imag * imag


def total_weight(v: object) -> int:
    parsed = _gauss_map(v, "total")
    return nsq(parsed[False]) + nsq(parsed[True])


def psi1() -> dict[bool, tuple[int, int]]:
    """H008 psi1: both reports are 1."""
    return {False: (1, 0), True: (1, 0)}


def psi2() -> dict[bool, tuple[int, int]]:
    """H008 psi2: false is 1 and true is -1."""
    return {False: (1, 0), True: (-1, 0)}


def _mix_total(witness: Mapping[bool, tuple[int, int]]) -> int:
    return total_weight(mix(witness))


def dump_disagrees_with_tensor() -> bool:
    u = {False: 1, True: 0}
    v = {False: 0, True: 1}
    return any(dump_right(u, v, point) != tensor(u, v, point) for point in PAIR_DOMAIN)


@dataclass(frozen=True)
class Qm122DualReceipt:
    """Measured counts for the named QM-122-C38 witnesses."""

    reversible_reports: int
    identity_dilations: int
    collapse_dilations: int
    one_plus_i_blocked: bool
    dump_disagrees: bool
    no_half_step: bool
    mix_psi1: int
    mix_psi2: int
    weight_psi1: int
    weight_psi2: int


def _require_count(actual: int, expected: int, invariant: str) -> None:
    if actual != expected:
        raise _fail(invariant, actual=actual, expected=expected)


def qm122_dual_receipt() -> Qm122DualReceipt:
    """Discharge QM-122-C38 on the named finite witnesses."""
    weight_1 = total_weight(psi1())
    weight_2 = total_weight(psi2())
    receipt = Qm122DualReceipt(
        len(bool_reversibles()),
        len(identity_dilations()),
        len(collapse_dilations()),
        one_plus_i_not_unit(),
        dump_disagrees_with_tensor(),
        no_report_half_step(),
        _mix_total(psi1()),
        _mix_total(psi2()),
        weight_1,
        weight_2,
    )
    _require_count(receipt.reversible_reports, 2, "reversible report count is not 2")
    _require_count(receipt.identity_dilations, 4, "identity dilation count is not 4")
    _require_count(receipt.collapse_dilations, 4, "collapse dilation count is not 4")
    if receipt.one_plus_i_blocked is not True:
        raise _fail("1+i was a unit residue")
    if receipt.dump_disagrees is not True:
        raise _fail("dumpRight agreed with tensor on the exhibited weights")
    if receipt.no_half_step is not True:
        raise _fail("a report half-step existed")
    if receipt.mix_psi1 != 2 * receipt.weight_psi1:
        raise _fail("mix did not double psi1", mix=receipt.mix_psi1, weight=receipt.weight_psi1)
    if receipt.mix_psi2 != 2 * receipt.weight_psi2:
        raise _fail("mix did not double psi2", mix=receipt.mix_psi2, weight=receipt.weight_psi2)
    if has_two_sided_inverse(collapse):
        raise _fail("collapse was reversible")
    return receipt


__all__ = [
    "PAIR_DOMAIN",
    "Qm122DualError",
    "Qm122DualReceipt",
    "bool_reversibles",
    "collapse",
    "collapse_dilations",
    "delta",
    "dump_disagrees_with_tensor",
    "dump_right",
    "gmul",
    "has_two_sided_inverse",
    "identity_dilations",
    "mix",
    "no_report_half_step",
    "nsq",
    "one_plus_i_not_unit",
    "psi1",
    "psi2",
    "qm122_dual_receipt",
    "tensor",
    "toggle",
    "total_weight",
]
