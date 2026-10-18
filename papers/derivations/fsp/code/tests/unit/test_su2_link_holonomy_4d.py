"""test_su2_link_holonomy_4d.py — Comprehensive Unit Tests for 4D SU(2) Gauge Theory & PFP Bridge.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e), Paper 011, gemini_000.md.
"""

from __future__ import annotations

from fractions import Fraction
import sys
from pathlib import Path
import pytest

code_dir = Path(__file__).resolve().parent.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from su2_link_holonomy_4d import ExactRationalSU2, Lattice4DCoord, Lattice4DSU2
from pfp_fsp_bridge import (
    FspLinkProposal,
    FspPfpProposalPacket,
    FspPfpReceipt,
    FspPfpReferee,
)


class TestExactRationalSU2:
    """Test suite for ExactRationalSU2 unit quaternion algebra."""

    def test_identity(self):
        ident = ExactRationalSU2.identity()
        assert ident.a0 == Fraction(1, 1)
        assert ident.a1 == Fraction(0, 1)
        assert ident.a2 == Fraction(0, 1)
        assert ident.a3 == Fraction(0, 1)
        assert ident.determinant() == Fraction(1, 1)
        assert ident.trace() == Fraction(2, 1)
        assert ident.is_unitary() is True

    def test_from_pythagorean_quadruple(self):
        u = ExactRationalSU2.from_pythagorean_quadruple(1, 2, 2, 0)
        assert u.a0 == Fraction(1, 3)
        assert u.a1 == Fraction(2, 3)
        assert u.a2 == Fraction(2, 3)
        assert u.a3 == Fraction(0, 3)
        assert u.determinant() == Fraction(1, 1)
        assert u.is_unitary() is True

    def test_multiplication_and_inverse(self):
        u1 = ExactRationalSU2.from_pythagorean_quadruple(1, 2, 2, 0)
        u2 = ExactRationalSU2.from_pythagorean_quadruple(2, 1, 0, 2)
        prod = u1.multiply(u2)
        assert prod.is_unitary() is True
        assert prod.determinant() == Fraction(1, 1)

        inv = u1.dagger()
        ident = u1.multiply(inv)
        assert ident.a0 == Fraction(1, 1)
        assert ident.a1 == Fraction(0, 1)
        assert ident.a2 == Fraction(0, 1)
        assert ident.a3 == Fraction(0, 1)

    def test_complex_conjugate(self):
        u = ExactRationalSU2.from_pythagorean_quadruple(1, 2, 2, 0)
        u_conj = u.complex_conjugate()
        assert u_conj.a0 == u.a0
        assert u_conj.a1 == -u.a1
        assert u_conj.a2 == u.a2
        assert u_conj.a3 == -u.a3
        assert u_conj.is_unitary() is True

    def test_zero_float_type_errors(self):
        with pytest.raises(TypeError, match="Component.*must be an exact Fraction or int"):
            ExactRationalSU2(1.0, Fraction(0, 1), Fraction(0, 1), Fraction(0, 1))

        with pytest.raises(TypeError, match="Component.*must be an exact Fraction or int"):
            ExactRationalSU2(True, Fraction(0, 1), Fraction(0, 1), Fraction(0, 1))

        with pytest.raises(TypeError, match="Invalid type"):
            ExactRationalSU2("1", Fraction(0, 1), Fraction(0, 1), Fraction(0, 1))

    def test_invalid_norm_error(self):
        with pytest.raises(ValueError, match="unit quaternion norm squared must equal 1"):
            ExactRationalSU2(Fraction(1, 2), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1))

    def test_invalid_quadruple(self):
        with pytest.raises(ValueError, match="Quadruple components cannot all be zero"):
            ExactRationalSU2.from_pythagorean_quadruple(0, 0, 0, 0)

        with pytest.raises(ValueError, match="not a perfect square"):
            ExactRationalSU2.from_pythagorean_quadruple(1, 1, 0, 0)

    def test_multiply_invalid_type(self):
        u = ExactRationalSU2.identity()
        with pytest.raises(TypeError, match="Expected ExactRationalSU2"):
            u.multiply("not_a_quaternion")


class TestLattice4DCoord:
    """Test suite for 4D torus coordinates."""

    def test_coord_shifts(self):
        coord = Lattice4DCoord(0, 1, 0, 1, (2, 2, 2, 2))
        shifted = coord.shift(0, 1)
        assert shifted.x0 == 1
        assert shifted.x1 == 1

        wrapped = shifted.shift(0, 1)
        assert wrapped.x0 == 0

    def test_involution_reflection(self):
        coord = Lattice4DCoord(1, 0, 1, 0, (3, 2, 2, 2))
        refl = coord.involution_reflection()
        assert refl.x0 == (-1) % 3
        assert refl.x1 == 0
        assert refl.x2 == 1
        assert refl.x3 == 0

    def test_invalid_coord_args(self):
        with pytest.raises(ValueError, match="must be positive"):
            Lattice4DCoord(0, 0, 0, 0, (0, 2, 2, 2))

        with pytest.raises(ValueError, match="out of range"):
            Lattice4DCoord(3, 0, 0, 0, (2, 2, 2, 2))

        coord = Lattice4DCoord(0, 0, 0, 0, (2, 2, 2, 2))
        with pytest.raises(ValueError, match="Direction mu must be in"):
            coord.shift(4)


class TestLattice4DSU2:
    """Test suite for 4D SU(2) lattice gauge configuration."""

    def test_lattice_initialization(self):
        lattice = Lattice4DSU2((2, 2, 2, 2))
        assert lattice.volume == 16
        assert lattice.num_links == 64
        assert lattice.total_wilson_action() == Fraction(0, 1)

    def test_invalid_lattice_dims(self):
        with pytest.raises(ValueError, match="Lattice dims must be a 4-tuple"):
            Lattice4DSU2((2, 2, 2))
        with pytest.raises(ValueError, match="Lattice dims must be a 4-tuple"):
            Lattice4DSU2((2, -2, 2, 2))

    def test_plaquette_calculation(self):
        lattice = Lattice4DSU2((2, 2, 2, 2))
        coord = Lattice4DCoord(0, 0, 0, 0, (2, 2, 2, 2))

        plaq = lattice.plaquette(coord, 0, 1)
        assert plaq == ExactRationalSU2.identity()
        assert lattice.plaquette_action(coord, 0, 1) == Fraction(0, 1)

        u_pert = ExactRationalSU2.from_pythagorean_quadruple(1, 2, 2, 0)
        lattice.set_link(coord, 0, u_pert)
        assert lattice.get_link(coord, 0) == u_pert

        action_01 = lattice.plaquette_action(coord, 0, 1)
        assert action_01 > Fraction(0, 1)
        assert lattice.total_wilson_action() > Fraction(0, 1)

    def test_invalid_plaquette_directions(self):
        lattice = Lattice4DSU2((2, 2, 2, 2))
        coord = Lattice4DCoord(0, 0, 0, 0, (2, 2, 2, 2))
        with pytest.raises(ValueError, match="must be distinct"):
            lattice.plaquette(coord, 0, 0)
        with pytest.raises(ValueError, match="Directions must be in"):
            lattice.plaquette(coord, 0, 4)

    def test_set_link_invalid_type(self):
        lattice = Lattice4DSU2((2, 2, 2, 2))
        coord = Lattice4DCoord(0, 0, 0, 0, (2, 2, 2, 2))
        with pytest.raises(TypeError, match="Link must be ExactRationalSU2"):
            lattice.set_link(coord, 0, "invalid")

    def test_involution_symmetry_and_sign_balance(self):
        lattice = Lattice4DSU2((2, 2, 2, 2))
        coord = Lattice4DCoord(0, 1, 0, 1, (2, 2, 2, 2))
        u = ExactRationalSU2.from_pythagorean_quadruple(1, 2, 2, 0)
        lattice.set_link(coord, 1, u)

        res = lattice.verify_involution_sign_balance()
        assert res["is_action_invariant"] is True
        assert res["all_links_unitary"] is True
        assert res["sign_cancellation_certified"] is True
        assert res["authority_effect"] == "None"

    def test_rational_metropolis_step(self):
        lattice = Lattice4DSU2((2, 2, 2, 2))
        coord = Lattice4DCoord(0, 0, 0, 0, (2, 2, 2, 2))
        u_pert = ExactRationalSU2.from_pythagorean_quadruple(1, 2, 2, 0)

        lattice.set_link(coord, 0, u_pert)
        accepted, delta_s = lattice.rational_metropolis_step(
            coord, 0, ExactRationalSU2.identity(), Fraction(9, 10)
        )
        assert accepted is True
        assert delta_s < Fraction(0, 1)

        accepted, delta_s = lattice.rational_metropolis_step(
            coord, 0, u_pert, Fraction(1, 1)
        )
        assert accepted is False
        assert delta_s > Fraction(0, 1)

        accepted, delta_s = lattice.rational_metropolis_step(
            coord, 0, u_pert, Fraction(0, 1)
        )
        assert accepted is True

    def test_metropolis_invalid_threshold(self):
        lattice = Lattice4DSU2((2, 2, 2, 2))
        coord = Lattice4DCoord(0, 0, 0, 0, (2, 2, 2, 2))
        with pytest.raises(ValueError, match="Random threshold must be in"):
            lattice.rational_metropolis_step(coord, 0, ExactRationalSU2.identity(), Fraction(2, 1))


class TestPfpFspBridge:
    """Test suite for PFP mediation of FSP 4D SU(2) updates."""

    def test_pfp_proposal_acceptance(self):
        lattice = Lattice4DSU2((2, 2, 2, 2))
        referee = FspPfpReferee(lattice)
        u_cand = ExactRationalSU2.from_pythagorean_quadruple(1, 2, 2, 0)

        proposal = FspLinkProposal(0, 0, 0, 0, 0, u_cand)
        packet = FspPfpProposalPacket(
            round_id="rnd_001",
            proposer_id="agent_fsp_proposer",
            lattice_dims=(2, 2, 2, 2),
            proposals=(proposal,),
            declared_initial_action=Fraction(0, 1),
            declared_delta_action=Fraction(1, 3),
        )

        receipt = referee.evaluate_proposal(packet, random_threshold=Fraction(0, 1))
        assert receipt.is_accepted is True
        assert receipt.unitarity_verified is True
        assert receipt.determinant_verified is True
        assert receipt.involution_pairing_verified is True
        assert receipt.authority_effect == "None"
        assert len(receipt.canonical_receipt_digest()) == 64

    def test_pfp_proposal_rejection_high_threshold(self):
        lattice = Lattice4DSU2((2, 2, 2, 2))
        referee = FspPfpReferee(lattice)
        u_cand = ExactRationalSU2.from_pythagorean_quadruple(1, 2, 2, 0)

        proposal = FspLinkProposal(0, 0, 0, 0, 0, u_cand)
        packet = FspPfpProposalPacket(
            round_id="rnd_002",
            proposer_id="agent_fsp_proposer",
            lattice_dims=(2, 2, 2, 2),
            proposals=(proposal,),
            declared_initial_action=Fraction(0, 1),
            declared_delta_action=Fraction(1, 3),
        )

        receipt = referee.evaluate_proposal(packet, random_threshold=Fraction(1, 1))
        assert receipt.is_accepted is False
        assert "REJECTED" in receipt.status_reason
        assert receipt.computed_final_action == Fraction(0, 1)

    def test_pfp_proposal_descending_action(self):
        lattice = Lattice4DSU2((2, 2, 2, 2))
        coord = Lattice4DCoord(0, 0, 0, 0, (2, 2, 2, 2))
        u_pert = ExactRationalSU2.from_pythagorean_quadruple(1, 2, 2, 0)
        lattice.set_link(coord, 0, u_pert)

        referee = FspPfpReferee(lattice)
        proposal = FspLinkProposal(0, 0, 0, 0, 0, ExactRationalSU2.identity())
        packet = FspPfpProposalPacket(
            round_id="rnd_003",
            proposer_id="agent_fsp_proposer",
            lattice_dims=(2, 2, 2, 2),
            proposals=(proposal,),
            declared_initial_action=lattice.total_wilson_action(),
            declared_delta_action=-Fraction(1, 3),
        )

        receipt = referee.evaluate_proposal(packet, random_threshold=Fraction(9, 10))
        assert receipt.is_accepted is True
        assert "ACCEPTED: Action descending" in receipt.status_reason

    def test_pfp_invalid_random_threshold(self):
        lattice = Lattice4DSU2((2, 2, 2, 2))
        referee = FspPfpReferee(lattice)
        packet = FspPfpProposalPacket(
            round_id="rnd_004",
            proposer_id="agent_fsp_proposer",
            lattice_dims=(2, 2, 2, 2),
            proposals=(),
            declared_initial_action=Fraction(0, 1),
            declared_delta_action=Fraction(0, 1),
        )
        with pytest.raises(ValueError, match="Random threshold must be in"):
            referee.evaluate_proposal(packet, random_threshold=Fraction(-1, 1))

    def test_pfp_refusal_unitarity_or_determinant(self):
        lattice = Lattice4DSU2((2, 2, 2, 2))
        referee = FspPfpReferee(lattice)
        class NonUnitarySU2:
            a0 = Fraction(1, 1)
            a1 = Fraction(0, 1)
            a2 = Fraction(0, 1)
            a3 = Fraction(0, 1)
            def is_unitary(self):
                return False
            def determinant(self):
                return Fraction(2, 1)

        proposal = FspLinkProposal(0, 0, 0, 0, 0, NonUnitarySU2())
        packet = FspPfpProposalPacket(
            round_id="rnd_005",
            proposer_id="agent_fsp_proposer",
            lattice_dims=(2, 2, 2, 2),
            proposals=(proposal,),
            declared_initial_action=Fraction(0, 1),
            declared_delta_action=Fraction(0, 1),
        )
        receipt = referee.evaluate_proposal(packet)
        assert receipt.is_accepted is False
        assert "REFUSAL" in receipt.status_reason
        assert receipt.unitarity_verified is False
        assert receipt.determinant_verified is False

    def test_pfp_refusal_involution_breach(self, monkeypatch):
        lattice = Lattice4DSU2((2, 2, 2, 2))
        referee = FspPfpReferee(lattice)
        proposal = FspLinkProposal(0, 0, 0, 0, 0, ExactRationalSU2.identity())
        packet = FspPfpProposalPacket(
            round_id="rnd_006",
            proposer_id="agent_fsp_proposer",
            lattice_dims=(2, 2, 2, 2),
            proposals=(proposal,),
            declared_initial_action=Fraction(0, 1),
            declared_delta_action=Fraction(0, 1),
        )
        monkeypatch.setattr(
            lattice,
            "verify_involution_sign_balance",
            lambda: {"sign_cancellation_certified": False},
        )
        receipt = referee.evaluate_proposal(packet)
        assert receipt.is_accepted is False
        assert "REFUSAL: Involution tau sign balance breached" in receipt.status_reason

    def test_local_staple_action_all_directions(self):
        lattice = Lattice4DSU2((2, 2, 2, 2))
        coord = Lattice4DCoord(0, 0, 0, 0, (2, 2, 2, 2))
        for mu in range(4):
            staple = lattice.local_staple_action(coord, mu)
            assert staple == Fraction(0, 1)
