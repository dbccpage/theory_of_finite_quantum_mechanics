from __future__ import annotations
"""
Executable Python dual harness for W5.5 — separating predictions of exotic lifts.

Mirrors Lean `003_qm_separating_predictions.lean`:

1. Density free-parameter counts: complex d², real d(d+1)/2, quaternionic d(2d-1).
2. Complex composite local tomography identity; rebit 9≠10; quat 36≠28 at 2×2.
3. Shared classical ℓ¹ shadow can agree while composite LT diverges.
4. SEP-LP: ℓᵖ readout vs Born-ℓ² on Amp2 (2,1) — p=1,2,4 weights diverge.
5. SEP-CHSH classical: local CHSH ≤ 2 is lift-independent (non-separator).
6. SEP-CHSH-Q: Tsirelson square 8>4 named numeric (not ℂ/ℝ separator).
7. SEP-CHSH-FIELD: multipartite LT proxy (3 qubits) separates rebit/quat from
   complex; bipartite CHSH remains non-separator.
8. SEP-NETWORK: triangle bilocal Mermin-chain |N|≤8 unnorm; Renou-class named
   field scores separate ℂ/ℝ; continuum Renou numerics OPEN.

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum
from itertools import product

import pytest


class NamedLift(str, Enum):
    COMPLEX = "complexHilbert"
    REAL = "realHilbert"
    QUAT = "quaternionicHilbert"


def density_params(lift: NamedLift, d: int) -> int:
    if d <= 0:
        raise ValueError("d must be positive")
    if lift is NamedLift.COMPLEX:
        return d * d
    if lift is NamedLift.REAL:
        return d * (d + 1) // 2
    if lift is NamedLift.QUAT:
        return d * (2 * d - 1)
    raise ValueError(lift)


def local_prod(lift: NamedLift, d_a: int, d_b: int) -> int:
    return density_params(lift, d_a) * density_params(lift, d_b)


def composite_params(lift: NamedLift, d_a: int, d_b: int) -> int:
    return density_params(lift, d_a * d_b)


def test_single_qubit_param_separations():
    assert density_params(NamedLift.COMPLEX, 2) == 4
    assert density_params(NamedLift.REAL, 2) == 3
    assert density_params(NamedLift.QUAT, 2) == 6
    assert density_params(NamedLift.REAL, 2) != density_params(NamedLift.COMPLEX, 2)
    assert density_params(NamedLift.QUAT, 2) != density_params(NamedLift.COMPLEX, 2)
    assert density_params(NamedLift.REAL, 2) != density_params(NamedLift.QUAT, 2)


def test_complex_local_tomography_identity():
    for d_a, d_b in [(1, 1), (2, 2), (2, 3), (3, 5)]:
        assert local_prod(NamedLift.COMPLEX, d_a, d_b) == composite_params(
            NamedLift.COMPLEX, d_a, d_b
        )


def test_rebit_lt_fails_9_ne_10():
    assert local_prod(NamedLift.REAL, 2, 2) == 9
    assert composite_params(NamedLift.REAL, 2, 2) == 10
    assert local_prod(NamedLift.REAL, 2, 2) != composite_params(NamedLift.REAL, 2, 2)


def test_quat_lt_fails_36_ne_28():
    assert local_prod(NamedLift.QUAT, 2, 2) == 36
    assert composite_params(NamedLift.QUAT, 2, 2) == 28
    assert local_prod(NamedLift.QUAT, 2, 2) != composite_params(NamedLift.QUAT, 2, 2)


def test_shared_l1_shadow_while_composite_separates():
    """Diagonal ℓ¹ law can agree; composite LT is where rebit/complex diverge."""
    shadow = {"w0": 1, "w1": 1}
    assert shadow["w0"] == shadow["w1"]
    assert local_prod(NamedLift.COMPLEX, 2, 2) == composite_params(
        NamedLift.COMPLEX, 2, 2
    )
    assert local_prod(NamedLift.REAL, 2, 2) != composite_params(NamedLift.REAL, 2, 2)


@dataclass(frozen=True)
class SeparatingRow:
    lift: NamedLift
    single_qubit_params: int
    local_prod_22: int
    composite_22: int

    @property
    def lt_holds(self) -> bool:
        return self.local_prod_22 == self.composite_22


def row(lift: NamedLift) -> SeparatingRow:
    return SeparatingRow(
        lift=lift,
        single_qubit_params=density_params(lift, 2),
        local_prod_22=local_prod(lift, 2, 2),
        composite_22=composite_params(lift, 2, 2),
    )


def test_prediction_table_rows():
    assert row(NamedLift.COMPLEX).lt_holds is True
    assert row(NamedLift.REAL).lt_holds is False
    assert row(NamedLift.QUAT).lt_holds is False
    assert row(NamedLift.COMPLEX).single_qubit_params == 4
    assert row(NamedLift.REAL).single_qubit_params == 3
    assert row(NamedLift.QUAT).single_qubit_params == 6




class ReadoutLaw(str, Enum):
    ELL1 = "ell1"
    BORN_L2 = "bornL2"
    ELL4 = "ell4"


@dataclass(frozen=True)
class Amp2:
    a0: int
    a1: int


def unnorm_weights(law: ReadoutLaw, amp: Amp2) -> tuple[int, int]:
    if law is ReadoutLaw.ELL1:
        return (amp.a0, amp.a1)
    if law is ReadoutLaw.BORN_L2:
        return (amp.a0 * amp.a0, amp.a1 * amp.a1)
    if law is ReadoutLaw.ELL4:
        s0, s1 = amp.a0 * amp.a0, amp.a1 * amp.a1
        return (s0 * s0, s1 * s1)
    raise ValueError(law)


AMP21 = Amp2(2, 1)
AMP11 = Amp2(1, 1)


def test_sep_lp_born_ne_ell1_on_amp21():
    assert unnorm_weights(ReadoutLaw.ELL1, AMP21) == (2, 1)
    assert unnorm_weights(ReadoutLaw.BORN_L2, AMP21) == (4, 1)
    assert unnorm_weights(ReadoutLaw.ELL4, AMP21) == (16, 1)
    assert unnorm_weights(ReadoutLaw.BORN_L2, AMP21) != unnorm_weights(
        ReadoutLaw.ELL1, AMP21
    )
    assert unnorm_weights(ReadoutLaw.BORN_L2, AMP21) != unnorm_weights(
        ReadoutLaw.ELL4, AMP21
    )
    assert unnorm_weights(ReadoutLaw.ELL1, AMP21) != unnorm_weights(
        ReadoutLaw.ELL4, AMP21
    )


def test_sep_lp_support_shared_weights_diverge():
    assert AMP21.a0 > 0 and AMP21.a1 > 0
    assert unnorm_weights(ReadoutLaw.BORN_L2, AMP21) != unnorm_weights(
        ReadoutLaw.ELL1, AMP21
    )


def test_equal_amp_readouts_agree_nonseparator():
    """Equal amplitudes: all ℓᵖ laws give the same unnormalized weights."""
    assert unnorm_weights(ReadoutLaw.ELL1, AMP11) == (1, 1)
    assert unnorm_weights(ReadoutLaw.BORN_L2, AMP11) == (1, 1)
    assert unnorm_weights(ReadoutLaw.ELL4, AMP11) == (1, 1)




def s(b: bool) -> int:
    return 1 if b else -1


def chsh(a0: bool, a1: bool, b0: bool, b1: bool) -> int:
    return s(a0) * s(b0) + s(a0) * s(b1) + s(a1) * s(b0) - s(a1) * s(b1)


def test_classical_chsh_le_two_all_assignments():
    for a0, a1, b0, b1 in product([False, True], repeat=4):
        assert chsh(a0, a1, b0, b1) <= 2
        assert chsh(a0, a1, b0, b1) >= -2
    assert chsh(True, True, True, True) == 2


def test_classical_chsh_bound_lift_independent():
    """Classical CHSH ≤ 2 does not depend on NamedLift (non-separator)."""
    for _lift in NamedLift:
        for a0, a1, b0, b1 in product([False, True], repeat=4):
            assert chsh(a0, a1, b0, b1) <= 2



CLASSICAL_CHSH_SQUARE_BOUND = 4
TSIRELSON_CHSH_SQUARE = 8


def quantum_chsh_square_decl(lift: NamedLift) -> int | None:
    if lift is NamedLift.COMPLEX:
        return TSIRELSON_CHSH_SQUARE
    if lift is NamedLift.REAL:
        return TSIRELSON_CHSH_SQUARE
    if lift is NamedLift.QUAT:
        return None
    raise ValueError(lift)


def test_tsirelson_square_exceeds_classical():
    assert TSIRELSON_CHSH_SQUARE > CLASSICAL_CHSH_SQUARE_BOUND
    assert TSIRELSON_CHSH_SQUARE == 8
    assert CLASSICAL_CHSH_SQUARE_BOUND == 4


def test_quantum_chsh_decl_complex_and_real_not_separator():
    assert quantum_chsh_square_decl(NamedLift.COMPLEX) == 8
    assert quantum_chsh_square_decl(NamedLift.REAL) == 8
    assert quantum_chsh_square_decl(NamedLift.QUAT) is None
    assert quantum_chsh_square_decl(NamedLift.COMPLEX) == quantum_chsh_square_decl(
        NamedLift.REAL
    )


def test_quantum_host_exceeds_finL1_chsh_square():
    fin_l1_cap = CLASSICAL_CHSH_SQUARE_BOUND
    quantum_cap = TSIRELSON_CHSH_SQUARE
    assert quantum_cap > fin_l1_cap


def test_sep_chsh_quantum_package():
    assert TSIRELSON_CHSH_SQUARE > CLASSICAL_CHSH_SQUARE_BOUND
    assert quantum_chsh_square_decl(NamedLift.COMPLEX) == 8
    assert quantum_chsh_square_decl(NamedLift.REAL) == 8
    assert quantum_chsh_square_decl(NamedLift.QUAT) is None
    assert quantum_chsh_square_decl(NamedLift.COMPLEX) == quantum_chsh_square_decl(
        NamedLift.REAL
    )




def local_prod3(lift: NamedLift) -> int:
    """Three-factor local density-param product (qubits)."""
    p = density_params(lift, 2)
    return p * p * p


def composite_params3(lift: NamedLift) -> int:
    """Composite density params on three-qubit total dim 8."""
    return density_params(lift, 8)


class FieldBellScenario(str, Enum):
    BIPARTITE_CHSH = "bipartiteChsh"
    MULTIPARTITE_LT_PROXY3 = "multipartiteLtProxy3"
    RENOU_TRIANGLE_NETWORK = "renouTriangleNetwork"


def is_complex_vs_real_field_separator(scenario: FieldBellScenario) -> bool:
    if scenario is FieldBellScenario.BIPARTITE_CHSH:
        return False
    if scenario is FieldBellScenario.MULTIPARTITE_LT_PROXY3:
        return True
    if scenario is FieldBellScenario.RENOU_TRIANGLE_NETWORK:
        return True
    raise ValueError(scenario)



NETWORK_LOCAL_MERMIN_UNNORM_BOUND = 8
NETWORK_LOCAL_MERMIN_PHYSICAL_BOUND = 2
COMPLEX_NETWORK_FIELD_SCORE = 3
REAL_NETWORK_FIELD_SCORE = 2


def bilocal_E(
    a_bits: tuple[int, int], b_bits: tuple[int, int, int, int], c_bits: tuple[int, int]
) -> int:
    total = 0
    for l1, l2 in product([0, 1], repeat=2):
        a = 1 if a_bits[l1] else -1
        b = 1 if b_bits[l1 * 2 + l2] else -1
        c = 1 if c_bits[l2] else -1
        total += a * b * c
    return total


def bilocal_mermin_N(
    a0: tuple[int, int],
    a1: tuple[int, int],
    b0: tuple[int, int, int, int],
    b1: tuple[int, int, int, int],
    c0: tuple[int, int],
    c1: tuple[int, int],
) -> int:
    return (
        bilocal_E(a0, b0, c0)
        + bilocal_E(a0, b1, c1)
        + bilocal_E(a1, b0, c1)
        - bilocal_E(a1, b1, c0)
    )


def bilocal_fiber_contrib(a0: int, a1: int, c0: int, c1: int, b0: int, b1: int) -> int:
    return a0 * (c0 * b0 + c1 * b1) + a1 * (c1 * b0 - c0 * b1)


def test_complex_lt3_holds_64_eq_64():
    assert local_prod3(NamedLift.COMPLEX) == 64
    assert composite_params3(NamedLift.COMPLEX) == 64
    assert local_prod3(NamedLift.COMPLEX) == composite_params3(NamedLift.COMPLEX)


def test_rebit_lt3_fails_27_ne_36():
    assert local_prod3(NamedLift.REAL) == 27
    assert composite_params3(NamedLift.REAL) == 36
    assert local_prod3(NamedLift.REAL) != composite_params3(NamedLift.REAL)


def test_quat_lt3_fails_216_ne_120():
    assert local_prod3(NamedLift.QUAT) == 216
    assert composite_params3(NamedLift.QUAT) == 120
    assert local_prod3(NamedLift.QUAT) != composite_params3(NamedLift.QUAT)


def test_bipartite_chsh_not_field_separator():
    assert is_complex_vs_real_field_separator(FieldBellScenario.BIPARTITE_CHSH) is False
    assert quantum_chsh_square_decl(NamedLift.COMPLEX) == quantum_chsh_square_decl(
        NamedLift.REAL
    )


def test_multipartite_lt3_is_field_separator():
    assert (
        is_complex_vs_real_field_separator(FieldBellScenario.MULTIPARTITE_LT_PROXY3)
        is True
    )
    assert local_prod3(NamedLift.COMPLEX) == composite_params3(NamedLift.COMPLEX)
    assert local_prod3(NamedLift.REAL) != composite_params3(NamedLift.REAL)


def test_sep_chsh_field_package():
    assert is_complex_vs_real_field_separator(FieldBellScenario.BIPARTITE_CHSH) is False
    assert (
        is_complex_vs_real_field_separator(FieldBellScenario.MULTIPARTITE_LT_PROXY3)
        is True
    )
    assert local_prod3(NamedLift.COMPLEX) == 64
    assert local_prod3(NamedLift.REAL) == 27
    assert composite_params3(NamedLift.REAL) == 36
    assert local_prod3(NamedLift.QUAT) == 216
    assert composite_params3(NamedLift.QUAT) == 120


def test_bilocal_fiber_abs_le_two():
    for vals in product([-1, 1], repeat=6):
        c = bilocal_fiber_contrib(*vals)
        assert -2 <= c <= 2


def test_bilocal_mermin_unnorm_bound_by_enum():
    """Full 2^16 network-local strategies: |N| ≤ 8."""
    max_abs = 0
    for a0 in product([0, 1], repeat=2):
        for a1 in product([0, 1], repeat=2):
            for c0 in product([0, 1], repeat=2):
                for c1 in product([0, 1], repeat=2):
                    for b0 in product([0, 1], repeat=4):
                        for b1 in product([0, 1], repeat=4):
                            N = bilocal_mermin_N(a0, a1, b0, b1, c0, c1)
                            max_abs = max(max_abs, abs(N))
    assert max_abs == NETWORK_LOCAL_MERMIN_UNNORM_BOUND
    assert max_abs // 4 == NETWORK_LOCAL_MERMIN_PHYSICAL_BOUND


def test_bilocal_mermin_tight_plus_eight():
    ones2 = (1, 1)
    ones4 = (1, 1, 1, 1)
    assert bilocal_mermin_N(ones2, ones2, ones4, ones4, ones2, ones2) == 8


def test_renou_triangle_is_field_separator():
    assert (
        is_complex_vs_real_field_separator(FieldBellScenario.RENOU_TRIANGLE_NETWORK)
        is True
    )
    assert is_complex_vs_real_field_separator(FieldBellScenario.BIPARTITE_CHSH) is False


def test_network_field_scores_separate():
    assert COMPLEX_NETWORK_FIELD_SCORE > REAL_NETWORK_FIELD_SCORE
    assert REAL_NETWORK_FIELD_SCORE == NETWORK_LOCAL_MERMIN_PHYSICAL_BOUND
    assert COMPLEX_NETWORK_FIELD_SCORE > NETWORK_LOCAL_MERMIN_PHYSICAL_BOUND


def test_continuum_renou_numerics_marked_open():
    continuum_renou_numerics_open = True
    assert continuum_renou_numerics_open is True


def test_sep_network_package():
    assert is_complex_vs_real_field_separator(FieldBellScenario.BIPARTITE_CHSH) is False
    assert (
        is_complex_vs_real_field_separator(FieldBellScenario.RENOU_TRIANGLE_NETWORK)
        is True
    )
    assert NETWORK_LOCAL_MERMIN_UNNORM_BOUND == 8
    assert NETWORK_LOCAL_MERMIN_PHYSICAL_BOUND == 2
    ones2 = (1, 1)
    ones4 = (1, 1, 1, 1)
    assert bilocal_mermin_N(ones2, ones2, ones4, ones4, ones2, ones2) == 8
    assert COMPLEX_NETWORK_FIELD_SCORE > REAL_NETWORK_FIELD_SCORE


if __name__ == "__main__":
    pytest.main([__file__])
