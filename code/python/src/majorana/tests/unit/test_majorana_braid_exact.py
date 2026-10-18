"""test_majorana_braid_exact.py — Unit Tests for Majorana Anyon Braiding & PFP Bridge.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e), Claim MAJ-C7/MAJ-C8, gemini_000.md.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import pytest

code_dir = Path(__file__).resolve().parent.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from majorana_braid_exact import (
    ExactSignedPermutationMatrix,
    MajoranaBraidCircuit,
    MajoranaBraidGenerator,
)
from pfp_majorana_bridge import (
    MajoranaBraidProposalPacket,
    MajoranaBraidReceipt,
    MajoranaBraidReferee,
)


class TestExactSignedPermutationMatrix:
    """Test suite for exact signed permutation representation matrices."""

    def test_identity(self):
        ident = ExactSignedPermutationMatrix.identity(3)
        assert ident.dim == 3
        assert ident.determinant() == Fraction(1, 1)
        assert ident.is_orthogonal() is True

    def test_multiply_and_transpose(self):
        m1 = MajoranaBraidGenerator(3, 1).matrix
        m2 = MajoranaBraidGenerator(3, 2).matrix
        prod = m1.multiply(m2)
        assert prod.dim == 3
        assert prod.is_orthogonal() is True
        assert prod.determinant() == Fraction(1, 1)

        inv = prod.transpose()
        ident = prod.multiply(inv)
        assert ident == ExactSignedPermutationMatrix.identity(3)

    def test_invalid_matrix_args(self):
        with pytest.raises(ValueError, match="dim must be integer >= 2"):
            ExactSignedPermutationMatrix(1, ())
        with pytest.raises(ValueError, match="dim must be integer >= 2"):
            ExactSignedPermutationMatrix(True, ())

        with pytest.raises(ValueError, match="Data shape must be"):
            ExactSignedPermutationMatrix(2, ((Fraction(1, 1),),))

        with pytest.raises(TypeError, match="Matrix entries must be Fraction or int"):
            ExactSignedPermutationMatrix(2, ((1.0, 0), (0, 1)))

    def test_dimension_mismatch_multiplication(self):
        m1 = ExactSignedPermutationMatrix.identity(2)
        m2 = ExactSignedPermutationMatrix.identity(3)
        with pytest.raises(ValueError, match="Dimension mismatch"):
            m1.multiply(m2)

    def test_singular_determinant(self):
        zero_data = ((Fraction(0, 1), Fraction(0, 1)), (Fraction(0, 1), Fraction(0, 1)))
        mat = ExactSignedPermutationMatrix(2, zero_data)
        assert mat.determinant() == Fraction(0, 1)


class TestMajoranaBraidGeneratorAndCircuit:
    """Test suite for braid generator and braid circuit invariants."""

    def test_generator_creation_and_inverse(self):
        gen = MajoranaBraidGenerator(4, 1)
        inv = MajoranaBraidGenerator(4, 1, inverse=True)
        prod = gen.matrix.multiply(inv.matrix)
        assert prod == ExactSignedPermutationMatrix.identity(4)

    def test_invalid_generator_args(self):
        with pytest.raises(ValueError, match="num_modes must be >= 2"):
            MajoranaBraidGenerator(1, 1)
        with pytest.raises(ValueError, match="Braid index j must be in"):
            MajoranaBraidGenerator(4, 0)
        with pytest.raises(ValueError, match="Braid index j must be in"):
            MajoranaBraidGenerator(4, 4)

    def test_yang_baxter_relation(self):
        circuit = MajoranaBraidCircuit(4)
        assert circuit.verify_yang_baxter(1) is True
        assert circuit.verify_yang_baxter(2) is True

    def test_yang_baxter_out_of_range(self):
        circuit = MajoranaBraidCircuit(4)
        with pytest.raises(ValueError, match="Cannot verify Yang-Baxter"):
            circuit.verify_yang_baxter(0)
        with pytest.raises(ValueError, match="Cannot verify Yang-Baxter"):
            circuit.verify_yang_baxter(3)

    def test_far_commutativity(self):
        circuit = MajoranaBraidCircuit(4)
        assert circuit.verify_far_commutativity(1, 3) is True

    def test_far_commutativity_invalid(self):
        circuit = MajoranaBraidCircuit(4)
        with pytest.raises(ValueError, match="Indices must satisfy"):
            circuit.verify_far_commutativity(1, 2)

    def test_circuit_evaluation(self):
        circuit = MajoranaBraidCircuit(4)
        circuit.append(1).append(2).append(1)
        mat = circuit.evaluate_matrix()
        assert mat.is_orthogonal() is True
        assert mat.determinant() == Fraction(1, 1)

    def test_circuit_invalid_args(self):
        with pytest.raises(ValueError, match="num_modes must be integer >= 2"):
            MajoranaBraidCircuit(1)
        circuit = MajoranaBraidCircuit(3)
        with pytest.raises(ValueError, match="out of range"):
            circuit.append(3)


class TestPfpMajoranaBridge:
    """Test suite for PFP mediation of topological anyon braiding."""

    def test_pfp_braid_proposal_acceptance(self):
        referee = MajoranaBraidReferee(num_modes=4)
        packet = MajoranaBraidProposalPacket(
            round_id="rnd_maj_001",
            proposer_id="agent_anyon_proposer",
            num_modes=4,
            braid_sequence=((1, False), (2, False), (1, False)),
        )

        receipt = referee.evaluate_proposal(packet)
        assert receipt.is_accepted is True
        assert receipt.is_orthogonal is True
        assert receipt.is_proper_rotation is True
        assert receipt.yang_baxter_satisfied is True
        assert receipt.authority_effect == "None"
        assert len(receipt.canonical_receipt_digest()) == 64

    def test_pfp_refusal_mode_mismatch(self):
        referee = MajoranaBraidReferee(num_modes=4)
        packet = MajoranaBraidProposalPacket(
            round_id="rnd_maj_002",
            proposer_id="agent_anyon_proposer",
            num_modes=6,
            braid_sequence=((1, False),),
        )
        receipt = referee.evaluate_proposal(packet)
        assert receipt.is_accepted is False
        assert "REFUSAL: Mode mismatch" in receipt.status_reason

    def test_pfp_refusal_invalid_index(self):
        referee = MajoranaBraidReferee(num_modes=4)
        packet = MajoranaBraidProposalPacket(
            round_id="rnd_maj_003",
            proposer_id="agent_anyon_proposer",
            num_modes=4,
            braid_sequence=((5, False),),
        )
        receipt = referee.evaluate_proposal(packet)
        assert receipt.is_accepted is False
        assert "REFUSAL: Braid index 5 out of range" in receipt.status_reason

    def test_referee_invalid_num_modes(self):
        with pytest.raises(ValueError, match="num_modes must be integer >= 2"):
            MajoranaBraidReferee(1)

    def test_pfp_refusal_yang_baxter_violation(self, monkeypatch):
        referee = MajoranaBraidReferee(num_modes=4)
        packet = MajoranaBraidProposalPacket(
            round_id="rnd_maj_004",
            proposer_id="agent_anyon_proposer",
            num_modes=4,
            braid_sequence=((1, False),),
        )
        monkeypatch.setattr(MajoranaBraidCircuit, "verify_yang_baxter", lambda self, j: False)
        receipt = referee.evaluate_proposal(packet)
        assert receipt.is_accepted is False
        assert receipt.yang_baxter_satisfied is False
        assert "REFUSAL: Braid transformation violates" in receipt.status_reason
