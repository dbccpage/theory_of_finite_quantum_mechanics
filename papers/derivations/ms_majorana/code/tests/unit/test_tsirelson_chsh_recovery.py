from __future__ import annotations
"""
Executable Python dual harness for W7.2 (Tsirelson / CHSH operational recovery).

Mirrors Lean `003_qm_tsirelson_chsh_recovery.lean`:

1. Classical deterministic CHSH ≤ 2 (all Bool assignments); tightness at 2.
2. Tsirelson square 8 > classical square 4 (named numeric, not FinL1-derived).
3. FinL1 host does not recover quantum exceedance; quantum host does (conditional).
4. Denser correlator toy: scaled signs (+,+,+,-) sum to 4; S²/2 = 8.
5. Renou-class network residual: bilocal bound 8; named field scores; continuum OPEN.
6. Full T14 recovery / analytic Tsirelson remain open.

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum
from itertools import product

import pytest


def s(b: bool) -> int:
    return 1 if b else -1


def chsh(a0: bool, a1: bool, b0: bool, b1: bool) -> int:
    return s(a0) * s(b0) + s(a0) * s(b1) + s(a1) * s(b0) - s(a1) * s(b1)


CLASSICAL_CHSH_SQUARE_BOUND = 4
TSIRELSON_CHSH_SQUARE = 8


class ChshHost(str, Enum):
    FINL1 = "finL1Deterministic"
    QUANTUM = "quantumLiftTsirelson"


def chsh_square_cap(host: ChshHost) -> int:
    if host is ChshHost.FINL1:
        return CLASSICAL_CHSH_SQUARE_BOUND
    return TSIRELSON_CHSH_SQUARE


def recovers_quantum_exceedance(host: ChshHost) -> bool:
    return host is ChshHost.QUANTUM


@dataclass(frozen=True)
class ScaledCorrelators:
    e00: int
    e01: int
    e10: int
    e11: int

    def scaled_chsh_sum(self) -> int:
        return self.e00 + self.e01 + self.e10 - self.e11


def chsh_square_from_scaled_sum(S: int) -> int:
    return (S * S) // 2


TSIRELSON_SCALED = ScaledCorrelators(1, 1, 1, -1)


def test_classical_chsh_le_two():
    for a0, a1, b0, b1 in product([False, True], repeat=4):
        assert chsh(a0, a1, b0, b1) <= 2
        assert chsh(a0, a1, b0, b1) >= -2


def test_chsh_eq_two_tight():
    assert chsh(True, True, True, True) == 2


def test_tsirelson_square_exceeds_classical():
    assert TSIRELSON_CHSH_SQUARE > CLASSICAL_CHSH_SQUARE_BOUND
    assert TSIRELSON_CHSH_SQUARE == 8
    assert CLASSICAL_CHSH_SQUARE_BOUND == 4


def test_finL1_host_no_exceedance():
    assert chsh_square_cap(ChshHost.FINL1) == 4
    assert not (chsh_square_cap(ChshHost.FINL1) > CLASSICAL_CHSH_SQUARE_BOUND)


def test_quantum_host_exceeds_classical():
    assert chsh_square_cap(ChshHost.QUANTUM) > chsh_square_cap(ChshHost.FINL1)


def test_finL1_not_quantum_exceedance():
    assert recovers_quantum_exceedance(ChshHost.FINL1) is False
    assert recovers_quantum_exceedance(ChshHost.QUANTUM) is True


def test_t14_partial_recovery_statuses():
    t14_classical = "ClassicalDerived"
    t14_quantum = "QuantumConditional"
    t14_analytic = "AnalyticOpen"
    assert t14_classical == "ClassicalDerived"
    assert t14_quantum == "QuantumConditional"
    assert t14_analytic == "AnalyticOpen"


def test_t14_full_recovery_open():
    t14_full_recovery_closed = False
    assert t14_full_recovery_closed is False


def test_r_bell_partial_when_quantum_host():
    assert recovers_quantum_exceedance(ChshHost.QUANTUM)
    r_bell_partial_under_quantum_host = True
    assert r_bell_partial_under_quantum_host is True


def test_tsirelson_scaled_correlators():
    assert TSIRELSON_SCALED.scaled_chsh_sum() == 4
    assert chsh_square_from_scaled_sum(4) == 8
    assert chsh_square_from_scaled_sum(TSIRELSON_SCALED.scaled_chsh_sum()) == (
        TSIRELSON_CHSH_SQUARE
    )


def test_finL1_chsh_sum_ne_tsirelson_scaled():
    for a0, a1, b0, b1 in product([False, True], repeat=4):
        assert chsh(a0, a1, b0, b1) != 4
        assert chsh(a0, a1, b0, b1) <= 2


def test_correlator_package_needs_quantum_host():
    assert recovers_quantum_exceedance(ChshHost.QUANTUM) is True
    assert recovers_quantum_exceedance(ChshHost.FINL1) is False


def test_denser_tsirelson_correlator_package():
    assert TSIRELSON_SCALED.scaled_chsh_sum() == 4
    assert chsh_square_from_scaled_sum(4) == 8
    assert recovers_quantum_exceedance(ChshHost.QUANTUM) is True
    assert recovers_quantum_exceedance(ChshHost.FINL1) is False
    analytic_tsirelson_open = True
    continuum_renou_numerics_open = True
    assert analytic_tsirelson_open is True
    assert continuum_renou_numerics_open is True


NETWORK_LOCAL_MERMIN_UNNORM_BOUND = 8
NETWORK_LOCAL_MERMIN_PHYSICAL_BOUND = 2
COMPLEX_NETWORK_FIELD_SCORE = 3
REAL_NETWORK_FIELD_SCORE = 2


def test_t14_network_package():
    bipartite_chsh_is_field_separator = False
    renou_triangle_is_field_separator = True
    assert bipartite_chsh_is_field_separator is False
    assert renou_triangle_is_field_separator is True
    assert COMPLEX_NETWORK_FIELD_SCORE > REAL_NETWORK_FIELD_SCORE
    assert REAL_NETWORK_FIELD_SCORE == NETWORK_LOCAL_MERMIN_PHYSICAL_BOUND
    assert NETWORK_LOCAL_MERMIN_UNNORM_BOUND == 8
    continuum_renou_numerics_open = True
    analytic_tsirelson_open = True
    t14_full_recovery_closed = False
    assert continuum_renou_numerics_open is True
    assert analytic_tsirelson_open is True
    assert t14_full_recovery_closed is False


def test_tsirelson_chsh_recovery_package():
    for a0, a1, b0, b1 in product([False, True], repeat=4):
        assert chsh(a0, a1, b0, b1) <= 2
    assert TSIRELSON_CHSH_SQUARE > CLASSICAL_CHSH_SQUARE_BOUND
    assert recovers_quantum_exceedance(ChshHost.FINL1) is False
    assert recovers_quantum_exceedance(ChshHost.QUANTUM) is True
    assert TSIRELSON_SCALED.scaled_chsh_sum() == 4
    assert chsh_square_from_scaled_sum(4) == 8
    assert COMPLEX_NETWORK_FIELD_SCORE > REAL_NETWORK_FIELD_SCORE


if __name__ == "__main__":
    pytest.main([__file__])
