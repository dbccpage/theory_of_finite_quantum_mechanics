"""test_kitaev_chain_exact.py — Unit Tests for 1D Discrete Kitaev Chain & Majorana Zero Modes.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e), Claim MAJ-C6, gemini_000.md.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import pytest

code_dir = Path(__file__).resolve().parent.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from kitaev_chain_exact import KitaevChainExact, MajoranaBilinear


class TestMajoranaBilinear:
    """Test suite for MajoranaBilinear operators and Clifford commutators."""

    def test_bilinear_creation(self):
        b = MajoranaBilinear(1, 4)
        assert b.mode_a == 1
        assert b.mode_b == 4

    def test_bilinear_invalid_args(self):
        with pytest.raises(TypeError, match="must be integers"):
            MajoranaBilinear("1", 2)
        with pytest.raises(TypeError, match="cannot be boolean"):
            MajoranaBilinear(True, 2)
        with pytest.raises(ValueError, match="must be positive"):
            MajoranaBilinear(0, 2)
        with pytest.raises(ValueError, match="must be ordered a < b"):
            MajoranaBilinear(4, 2)
        with pytest.raises(ValueError, match="must be ordered a < b"):
            MajoranaBilinear(2, 2)

    def test_commutator_with_mode(self):
        b = MajoranaBilinear(2, 5)
        comm2 = b.commutator_with_mode(2)
        assert comm2 == (Fraction(2, 1), 5)

        comm5 = b.commutator_with_mode(5)
        assert comm5 == (Fraction(-2, 1), 2)

        assert b.commutator_with_mode(1) is None
        assert b.commutator_with_mode(3) is None


class TestKitaevChainExact:
    """Test suite for KitaevChainExact Hamiltonian and MZM isolation."""

    def test_sweet_spot_chain_4_sites(self):
        chain = KitaevChainExact(num_sites=4, t=1, mu=0, delta=1)
        assert chain.is_sweet_spot is True
        assert chain.num_modes == 8

        bulk_modes = chain.bulk_paired_modes()
        assert bulk_modes == {2, 3, 4, 5, 6, 7}

        assert chain.boundary_modes() == (1, 8)

        unpaired = chain.unpaired_zero_modes()
        assert unpaired == {1, 8}

        comm1 = chain.commutator_with_mode(1)
        comm8 = chain.commutator_with_mode(8)
        assert comm1 == {}
        assert comm8 == {}

        comm2 = chain.commutator_with_mode(2)
        assert 3 in comm2
        assert comm2[3] != Fraction(0, 1)

        res = chain.verify_mzm_isolation()
        assert res["is_sweet_spot"] is True
        assert res["mzm_topologically_protected"] is True
        assert res["left_commutator_zero"] is True
        assert res["right_commutator_zero"] is True
        assert res["unpaired_modes"] == [1, 8]
        assert res["authority_effect"] == "None"

    def test_non_sweet_spot_with_chemical_potential(self):
        chain = KitaevChainExact(num_sites=3, t=1, mu=Fraction(1, 2), delta=1)
        assert chain.is_sweet_spot is False

        assert 1 in chain.bulk_paired_modes()

        comm1 = chain.commutator_with_mode(1)
        assert 2 in comm1
        assert comm1[2] != Fraction(0, 1)

        res = chain.verify_mzm_isolation()
        assert res["is_sweet_spot"] is False
        assert res["left_commutator_zero"] is False
        assert res["mzm_topologically_protected"] is False

    def test_non_sweet_spot_delta_different_from_t(self):
        chain = KitaevChainExact(num_sites=3, t=Fraction(2, 1), mu=0, delta=Fraction(1, 1))
        assert chain.is_sweet_spot is False
        assert 1 in chain.bulk_paired_modes()

        res = chain.verify_mzm_isolation()
        assert res["left_commutator_zero"] is False
        assert res["mzm_topologically_protected"] is False

    def test_zero_float_type_errors(self):
        with pytest.raises(TypeError, match="Parameter.*must be exact Fraction or int"):
            KitaevChainExact(num_sites=3, t=1.0)
        with pytest.raises(TypeError, match="Parameter.*must be exact Fraction or int"):
            KitaevChainExact(num_sites=3, mu=True)

    def test_invalid_num_sites(self):
        with pytest.raises(ValueError, match="num_sites must be an integer >= 2"):
            KitaevChainExact(num_sites=1)
        with pytest.raises(ValueError, match="num_sites must be an integer >= 2"):
            KitaevChainExact(num_sites=True)

    def test_commutator_invalid_mode_index(self):
        chain = KitaevChainExact(num_sites=3)
        with pytest.raises(ValueError, match="out of range"):
            chain.commutator_with_mode(0)
        with pytest.raises(ValueError, match="out of range"):
            chain.commutator_with_mode(7)
