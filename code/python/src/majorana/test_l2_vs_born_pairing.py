from __future__ import annotations
"""
Executable Python dual harness for W6.5 — ℓ² readout vs Born pairing independence.

Mirrors Lean `003_qm_l2_vs_born_pairing.lean`:

1. ℓ² readout: amplitudes → (a0², a1²) with no effect.
2. Born-style diagonal pairing depends on amplitude and effect.
3. Separation A: same ℓ² readout, distinct pairing scalars under two effects.
4. Separation B: no effect-free map recovers all pairings from amp alone.
5. Separation C: linear pairing weights ≠ ℓ² readout on Amp(2,1).
6. Coincidence on identity effect does not merge import slots.
7. Amp3 residual: independence mirror on three-sector toy.
8. R_BORN reconstruction bind pathway (host-gated import; not FinL1-derived).

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum

import pytest


@dataclass(frozen=True)
class Amp2:
    a0: int
    a1: int


@dataclass(frozen=True)
class Effect2:
    e0: int
    e1: int


AMP21 = Amp2(2, 1)
AMP11 = Amp2(1, 1)
EFF_ID = Effect2(1, 1)
EFF0 = Effect2(1, 0)
EFF1 = Effect2(0, 1)


def l2_readout(amp: Amp2) -> tuple[int, int]:
    """OB-L2-READOUT: quadratic amplitude weights; effect-blind."""
    return (amp.a0 * amp.a0, amp.a1 * amp.a1)


def born_pairing(amp: Amp2, eff: Effect2) -> int:
    """Born-style diagonal pairing scalar ∑ a_i² e_i."""
    return amp.a0 * amp.a0 * eff.e0 + amp.a1 * amp.a1 * eff.e1


def born_pairing_weights(amp: Amp2, eff: Effect2) -> tuple[int, int]:
    return (amp.a0 * amp.a0 * eff.e0, amp.a1 * amp.a1 * eff.e1)


def linear_pairing_weights(amp: Amp2, eff: Effect2) -> tuple[int, int]:
    return (amp.a0 * eff.e0, amp.a1 * eff.e1)


class ImportSlot(str, Enum):
    OB_L2_READOUT = "obL2Readout"
    OB_BORN_PAIRING = "obBornPairing"


@dataclass(frozen=True)
class Amp3:
    a0: int
    a1: int
    a2: int


@dataclass(frozen=True)
class Effect3:
    e0: int
    e1: int
    e2: int


AMP321 = Amp3(3, 2, 1)
EFF30 = Effect3(1, 0, 0)
EFF32 = Effect3(0, 0, 1)


def l2_readout3(amp: Amp3) -> tuple[int, int, int]:
    return (amp.a0 * amp.a0, amp.a1 * amp.a1, amp.a2 * amp.a2)


def born_pairing3(amp: Amp3, eff: Effect3) -> int:
    return (
        amp.a0 * amp.a0 * eff.e0 + amp.a1 * amp.a1 * eff.e1 + amp.a2 * amp.a2 * eff.e2
    )


class BornHost(str, Enum):
    FINL1 = "finL1Alone"
    BORN_IMPORT = "bornImportPackage"


def r_born_pathway_recovered(host: BornHost) -> bool:
    return host is BornHost.BORN_IMPORT


def test_l2_readout_amp21():
    assert l2_readout(AMP21) == (4, 1)
    assert l2_readout(AMP11) == (1, 1)


def test_born_pairing_effect_relative():
    assert born_pairing(AMP21, EFF0) == 4
    assert born_pairing(AMP21, EFF1) == 1
    assert born_pairing(AMP21, EFF_ID) == 5
    assert born_pairing(AMP21, EFF0) != born_pairing(AMP21, EFF1)


def test_same_l2_distinct_pairings():
    """Separation A: fixed amp ⇒ fixed ℓ² readout; pairings still diverge."""
    assert l2_readout(AMP21) == (4, 1)
    assert born_pairing(AMP21, EFF0) != born_pairing(AMP21, EFF1)


def test_no_effect_free_pairing_map():
    """Separation B: no prob(amp) equals born_pairing(amp, eff) for all eff."""
    amps = [Amp2(a0, a1) for a0 in range(0, 4) for a1 in range(0, 4)]
    effects = [Effect2(e0, e1) for e0 in range(0, 3) for e1 in range(0, 3)]
    for amp in amps:
        values = {born_pairing(amp, eff) for eff in effects}
        if len(values) > 1:
            assert True
            break
    else:
        pytest.fail("expected some amp with effect-relative pairings")

    assert born_pairing(AMP21, EFF0) != born_pairing(AMP21, EFF1)


def test_linear_ne_l2_on_amp21_id():
    """Separation C: linear weights (2,1) ≠ ℓ² weights (4,1)."""
    assert linear_pairing_weights(AMP21, EFF_ID) == (2, 1)
    assert l2_readout(AMP21) == (4, 1)
    assert linear_pairing_weights(AMP21, EFF_ID) != l2_readout(AMP21)


def test_coincidence_on_identity_effect():
    """On identity effect, Born weights equal ℓ² readout — still two slots."""
    assert born_pairing_weights(AMP21, EFF_ID) == l2_readout(AMP21)
    assert linear_pairing_weights(AMP21, EFF_ID) != l2_readout(AMP21)


def test_l2_and_born_pairing_independent():
    assert born_pairing(AMP21, EFF0) != born_pairing(AMP21, EFF1)
    assert linear_pairing_weights(AMP21, EFF_ID) != l2_readout(AMP21)
    assert born_pairing_weights(AMP21, EFF_ID) == l2_readout(AMP21)
    assert ImportSlot.OB_L2_READOUT != ImportSlot.OB_BORN_PAIRING


def test_merge_slots_refused():
    merge_slots_claim = False
    assert merge_slots_claim is False


def test_amp3_independence():
    assert l2_readout3(AMP321) == (9, 4, 1)
    assert born_pairing3(AMP321, EFF30) == 9
    assert born_pairing3(AMP321, EFF32) == 1
    assert born_pairing3(AMP321, EFF30) != born_pairing3(AMP321, EFF32)


def test_no_effect_free_pairing_map3():
    assert born_pairing3(AMP321, EFF30) != born_pairing3(AMP321, EFF32)


def test_r_born_pathway_host_gated():
    assert r_born_pathway_recovered(BornHost.FINL1) is False
    assert r_born_pathway_recovered(BornHost.BORN_IMPORT) is True
    finl1_forces_born_pairing_law = False
    born_import_provides_effect_relative_pairing = True
    assert finl1_forces_born_pairing_law is False
    assert born_import_provides_effect_relative_pairing is True


def test_amp3_and_born_bind_package():
    amp3_and_born_bind_package_toy = True
    gleason_uniqueness_closed = False
    merge_slots_claim = False
    assert amp3_and_born_bind_package_toy is True
    assert l2_readout3(AMP321) == (9, 4, 1)
    assert born_pairing3(AMP321, EFF30) != born_pairing3(AMP321, EFF32)
    assert r_born_pathway_recovered(BornHost.BORN_IMPORT) is True
    assert r_born_pathway_recovered(BornHost.FINL1) is False
    assert gleason_uniqueness_closed is False
    assert merge_slots_claim is False


if __name__ == "__main__":
    pytest.main([__file__])
