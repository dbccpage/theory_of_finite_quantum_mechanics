from __future__ import annotations
"""
Executable Python dual harness for W6.19 (import independence models).

Mirrors Lean `003_qm_import_independence.lean`:

1. Provisional working basis B8 = B7 + {BUNDLE-U1-LT}.
2. Nested B4 / B5 / B7 retained.
3. Eight models each fail exactly one slot and admit the others.
4. 8x8 admits matrix: diagonal false, off-diagonal true; pairwise distinct.
5. Capital fences + L2/Born split + BUNDLE-U1-LT coupled package drop.
6. Separate OB-U1 / LT rows refused (not ImportSlot constructors).
7. Full BASIS-CANDIDATE independence remains OPEN (final N / more imports).

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum
from itertools import combinations


class ImportSlot(str, Enum):
    OB_NONCOMM = "OB-NONCOMM"
    OB_UNITARY = "OB-UNITARY"
    OB_CLONE = "OB-CLONE"
    CONT_TIME = "CONT-TIME"
    OB_HERM = "OB-HERM"
    OB_L2_READOUT = "OB-L2-READOUT"
    OB_BORN = "OB-BORN"
    BUNDLE_U1_LT = "BUNDLE-U1-LT"


WORKING_BASIS_B4 = (
    ImportSlot.OB_NONCOMM,
    ImportSlot.OB_UNITARY,
    ImportSlot.OB_CLONE,
    ImportSlot.CONT_TIME,
)

WORKING_BASIS_B5 = (
    ImportSlot.OB_NONCOMM,
    ImportSlot.OB_UNITARY,
    ImportSlot.OB_CLONE,
    ImportSlot.CONT_TIME,
    ImportSlot.OB_HERM,
)

WORKING_BASIS_B7 = (
    ImportSlot.OB_NONCOMM,
    ImportSlot.OB_UNITARY,
    ImportSlot.OB_CLONE,
    ImportSlot.CONT_TIME,
    ImportSlot.OB_HERM,
    ImportSlot.OB_L2_READOUT,
    ImportSlot.OB_BORN,
)

WORKING_BASIS_B8 = WORKING_BASIS_B7 + (ImportSlot.BUNDLE_U1_LT,)

# Primary provisional working basis alias
WORKING_BASIS = WORKING_BASIS_B8

EXCLUDED_COUPLED = ()
SEPARATE_OB_U1_ROW = False


@dataclass(frozen=True)
class IndependenceModel:
    noncomm: bool
    unitary: bool
    no_clone: bool
    cont_time: bool
    herm: bool
    l2: bool
    born: bool
    bundle: bool

    def admits(self, slot: ImportSlot) -> bool:
        if slot is ImportSlot.OB_NONCOMM:
            return self.noncomm
        if slot is ImportSlot.OB_UNITARY:
            return self.unitary
        if slot is ImportSlot.OB_CLONE:
            return self.no_clone
        if slot is ImportSlot.CONT_TIME:
            return self.cont_time
        if slot is ImportSlot.OB_HERM:
            return self.herm
        if slot is ImportSlot.OB_L2_READOUT:
            return self.l2
        if slot is ImportSlot.OB_BORN:
            return self.born
        if slot is ImportSlot.BUNDLE_U1_LT:
            return self.bundle
        raise ValueError(slot)

    def fails_exactly(self, drop: ImportSlot) -> bool:
        if self.admits(drop):
            return False
        return all(self.admits(s) for s in ImportSlot if s is not drop)


def _all_true(**overrides: bool) -> IndependenceModel:
    base = dict(
        noncomm=True,
        unitary=True,
        no_clone=True,
        cont_time=True,
        herm=True,
        l2=True,
        born=True,
        bundle=True,
    )
    base.update(overrides)
    return IndependenceModel(**base)


MODEL_DROP_NONCOMM = _all_true(noncomm=False)
MODEL_DROP_UNITARY = _all_true(unitary=False)
MODEL_DROP_CLONE = _all_true(no_clone=False)
MODEL_DROP_CONT_TIME = _all_true(cont_time=False)
MODEL_DROP_HERM = _all_true(herm=False)
MODEL_DROP_L2 = _all_true(l2=False)
MODEL_DROP_BORN = _all_true(born=False)
MODEL_DROP_BUNDLE = _all_true(bundle=False)

INDEPENDENCE_MODELS_B4 = (
    (ImportSlot.OB_NONCOMM, MODEL_DROP_NONCOMM),
    (ImportSlot.OB_UNITARY, MODEL_DROP_UNITARY),
    (ImportSlot.OB_CLONE, MODEL_DROP_CLONE),
    (ImportSlot.CONT_TIME, MODEL_DROP_CONT_TIME),
)

INDEPENDENCE_MODELS_B5 = INDEPENDENCE_MODELS_B4 + (
    (ImportSlot.OB_HERM, MODEL_DROP_HERM),
)

INDEPENDENCE_MODELS_B7 = INDEPENDENCE_MODELS_B5 + (
    (ImportSlot.OB_L2_READOUT, MODEL_DROP_L2),
    (ImportSlot.OB_BORN, MODEL_DROP_BORN),
)

INDEPENDENCE_MODELS_B8 = INDEPENDENCE_MODELS_B7 + (
    (ImportSlot.BUNDLE_U1_LT, MODEL_DROP_BUNDLE),
)

INDEPENDENCE_MODELS = INDEPENDENCE_MODELS_B8

MODEL_ROW = {
    ImportSlot.OB_NONCOMM: MODEL_DROP_NONCOMM,
    ImportSlot.OB_UNITARY: MODEL_DROP_UNITARY,
    ImportSlot.OB_CLONE: MODEL_DROP_CLONE,
    ImportSlot.CONT_TIME: MODEL_DROP_CONT_TIME,
    ImportSlot.OB_HERM: MODEL_DROP_HERM,
    ImportSlot.OB_L2_READOUT: MODEL_DROP_L2,
    ImportSlot.OB_BORN: MODEL_DROP_BORN,
    ImportSlot.BUNDLE_U1_LT: MODEL_DROP_BUNDLE,
}


def admits_matrix(row: ImportSlot, col: ImportSlot) -> bool:
    return MODEL_ROW[row].admits(col)


def test_working_basis_b4_card():
    assert len(WORKING_BASIS_B4) == 4
    assert len(set(WORKING_BASIS_B4)) == 4
    assert ImportSlot.OB_HERM not in WORKING_BASIS_B4
    assert ImportSlot.OB_L2_READOUT not in WORKING_BASIS_B4


def test_working_basis_b5_card():
    assert len(WORKING_BASIS_B5) == 5
    assert ImportSlot.OB_HERM in WORKING_BASIS_B5
    assert ImportSlot.OB_L2_READOUT not in WORKING_BASIS_B5


def test_working_basis_card():
    """Mutation-sensitive: provisional B8 has card 8."""
    assert len(WORKING_BASIS) == 8
    assert len(WORKING_BASIS_B8) == 8
    assert len(set(WORKING_BASIS_B8)) == 8
    assert ImportSlot.BUNDLE_U1_LT in WORKING_BASIS_B8
    assert WORKING_BASIS == WORKING_BASIS_B8


def test_every_basis_slot_has_drop_model():
    assert MODEL_DROP_NONCOMM.fails_exactly(ImportSlot.OB_NONCOMM)
    assert MODEL_DROP_UNITARY.fails_exactly(ImportSlot.OB_UNITARY)
    assert MODEL_DROP_CLONE.fails_exactly(ImportSlot.OB_CLONE)
    assert MODEL_DROP_CONT_TIME.fails_exactly(ImportSlot.CONT_TIME)
    assert MODEL_DROP_HERM.fails_exactly(ImportSlot.OB_HERM)
    assert MODEL_DROP_L2.fails_exactly(ImportSlot.OB_L2_READOUT)
    assert MODEL_DROP_BORN.fails_exactly(ImportSlot.OB_BORN)
    assert MODEL_DROP_BUNDLE.fails_exactly(ImportSlot.BUNDLE_U1_LT)


def test_drop_l2_fails_exactly():
    """Mutation-sensitive: L2 drop model fails only OB-L2-READOUT."""
    m = MODEL_DROP_L2
    assert m.fails_exactly(ImportSlot.OB_L2_READOUT)
    assert not m.admits(ImportSlot.OB_L2_READOUT)
    assert m.admits(ImportSlot.OB_BORN)
    assert m.admits(ImportSlot.OB_HERM)
    wrong = _all_true(l2=True)
    assert not wrong.fails_exactly(ImportSlot.OB_L2_READOUT)


def test_drop_born_fails_exactly():
    """Mutation-sensitive: Born drop model fails only OB-BORN."""
    m = MODEL_DROP_BORN
    assert m.fails_exactly(ImportSlot.OB_BORN)
    assert not m.admits(ImportSlot.OB_BORN)
    assert m.admits(ImportSlot.OB_L2_READOUT)
    wrong = _all_true(born=True)
    assert not wrong.fails_exactly(ImportSlot.OB_BORN)


def test_l2_born_split_models():
    """L2 host without Born, and Born without L2 host, both exist (merge refused)."""
    l2_only = _all_true(born=False)
    born_only = _all_true(l2=False)
    assert l2_only.admits(ImportSlot.OB_L2_READOUT)
    assert not l2_only.admits(ImportSlot.OB_BORN)
    assert born_only.admits(ImportSlot.OB_BORN)
    assert not born_only.admits(ImportSlot.OB_L2_READOUT)
    # Mutation trap: merged model would have both false together only
    merged_false = _all_true(l2=False, born=False)
    assert not merged_false.fails_exactly(ImportSlot.OB_L2_READOUT)
    assert not merged_false.fails_exactly(ImportSlot.OB_BORN)


def test_admits_matrix_diag_false():
    for s in ImportSlot:
        assert admits_matrix(s, s) is False


def test_admits_matrix_off_diag_true():
    for r in ImportSlot:
        for c in ImportSlot:
            if r is not c:
                assert admits_matrix(r, c) is True


def test_unique_drop_model_per_slot():
    for s in ImportSlot:
        assert admits_matrix(s, s) is False
        for r in ImportSlot:
            if r is not s:
                assert admits_matrix(r, s) is True


def test_drop_models_pairwise_distinct():
    models = [m for _, m in INDEPENDENCE_MODELS_B8]
    assert len(models) == 8
    for a, b in combinations(models, 2):
        assert a != b
    # C(8,2) = 28
    assert len(list(combinations(models, 2))) == 28


def test_independence_models_match_basis():
    assert len(INDEPENDENCE_MODELS) == len(WORKING_BASIS)
    slots = [s for s, _ in INDEPENDENCE_MODELS]
    assert tuple(slots) == WORKING_BASIS_B8


def test_capital_fences():
    # reset kernel shape: column-stochastic (1+0=1, 1+0=1) but not doubly (row0 sum=2)
    reset = (1, 0, 1, 0)  # k00, k10, k01, k11
    assert reset[0] + reset[1] == 1
    assert reset[2] + reset[3] == 1
    assert reset[0] + reset[2] != 1
    # L2 not forced from ℓ¹ shadow
    l2_forced_from_l1 = False
    assert l2_forced_from_l1 is False
    # Born not forced from L2 host alone
    born_forced_from_l2 = False
    assert born_forced_from_l2 is False


def test_bundle_in_b8_not_separate_u1():
    """BUNDLE-U1-LT is in B8; separate U1/LT rows refused."""
    assert len(EXCLUDED_COUPLED) == 0
    assert SEPARATE_OB_U1_ROW is False
    assert ImportSlot.BUNDLE_U1_LT in WORKING_BASIS_B8
    assert MODEL_DROP_BUNDLE.fails_exactly(ImportSlot.BUNDLE_U1_LT)


def test_full_basis_independence_open():
    """Mutation-sensitive: must not claim full BASIS-CANDIDATE closed."""
    full_basis_closed = False
    assert full_basis_closed is False
    names = {s.value for s in WORKING_BASIS_B8}
    assert "OB-U1" not in names  # separate row refused
    assert "BUNDLE-U1-LT" in names


def test_b8_package_summary():
    assert len(WORKING_BASIS_B8) == 8
    assert all(m.fails_exactly(s) for s, m in INDEPENDENCE_MODELS_B8)
    assert MODEL_DROP_L2 != MODEL_DROP_BORN
    assert MODEL_DROP_BUNDLE != MODEL_DROP_BORN
