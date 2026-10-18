"""test_majorana_multiqubit_noise.py — Unit Tests for Multi-Qubit Braided Clifford Operations with Noise.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e), Claim MAJ-C7/MAJ-C8, gemini_000.md.
"""

from __future__ import annotations

from fractions import Fraction
import sys
from pathlib import Path
import pytest

# Ensure ms_majorana/code is in sys.path
code_dir = Path(__file__).resolve().parent.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from majorana_braid_exact import ExactSignedPermutationMatrix
from majorana_multiqubit_noise import (
    LocalMajoranaNoise,
    MultiQubitBraidCircuit,
    MultiQubitNoisyBraidProposalPacket,
    MultiQubitNoisyBraidReceipt,
    MultiQubitNoisyBraidReferee,
)


class TestLocalMajoranaNoise:
    """Test suite for LocalMajoranaNoise Hamiltonian representation."""

    def test_zero_noise(self):
        noise = LocalMajoranaNoise.zero(8)
        assert noise.dim == 8
        assert noise.max_leakage() == Fraction(0, 1)
        assert noise.leakage_on_mode(1) == Fraction(0, 1)

    def test_single_pair_noise(self):
        noise = LocalMajoranaNoise.single_pair(4, 1, 2, Fraction(1, 10))
        assert noise.dim == 4
        # K[0][1] = 1/10, K[1][0] = -1/10
        assert noise.data[0][1] == Fraction(1, 10)
        assert noise.data[1][0] == Fraction(-1, 10)
        # Mode 1 leakage: 2 * |1/10| = 1/5
        assert noise.leakage_on_mode(1) == Fraction(1, 5)
        assert noise.leakage_on_mode(3) == Fraction(0, 1)
        assert noise.max_leakage() == Fraction(1, 5)

    def test_stray_couplings(self):
        couplings = [
            (1, 2, Fraction(1, 5)),
            (3, 4, Fraction(2, 5)),
        ]
        noise = LocalMajoranaNoise.stray_couplings(4, couplings)
        assert noise.leakage_on_mode(1) == Fraction(2, 5)
        assert noise.leakage_on_mode(3) == Fraction(4, 5)
        assert noise.max_leakage() == Fraction(4, 5)

    def test_validation_errors(self):
        with pytest.raises(ValueError, match="dim must be integer >= 2"):
            LocalMajoranaNoise(1, ())
        with pytest.raises(ValueError, match="dim must be integer >= 2"):
            LocalMajoranaNoise(True, ())

        with pytest.raises(ValueError, match="Data shape must be"):
            LocalMajoranaNoise(2, ((Fraction(0, 1),),))

        with pytest.raises(TypeError, match="Matrix entries must be Fraction or int"):
            LocalMajoranaNoise(2, ((0.0, 0), (0, 0)))

        with pytest.raises(ValueError, match="Diagonal entry at"):
            LocalMajoranaNoise(2, ((Fraction(1, 1), Fraction(0, 1)), (Fraction(0, 1), Fraction(0, 1))))

        with pytest.raises(ValueError, match="Matrix must be skew-symmetric"):
            LocalMajoranaNoise(2, ((Fraction(0, 1), Fraction(1, 1)), (Fraction(1, 1), Fraction(0, 1))))

        with pytest.raises(ValueError, match="out of range"):
            LocalMajoranaNoise.single_pair(4, 0, 1, Fraction(1, 1))

        with pytest.raises(ValueError, match="must be distinct"):
            LocalMajoranaNoise.single_pair(4, 2, 2, Fraction(1, 1))

        with pytest.raises(TypeError, match="epsilon must be Fraction or int"):
            LocalMajoranaNoise.single_pair(4, 1, 2, 0.5)

        with pytest.raises(ValueError, match="Self-coupling at mode"):
            LocalMajoranaNoise.stray_couplings(4, [(1, 1, Fraction(1, 1))])

        with pytest.raises(TypeError, match="Coupling epsilon must be Fraction or int"):
            LocalMajoranaNoise.stray_couplings(4, [(1, 2, 0.1)])

        noise = LocalMajoranaNoise.zero(4)
        with pytest.raises(ValueError, match="out of range"):
            noise.leakage_on_mode(5)

        u_wrong_dim = ExactSignedPermutationMatrix.identity(6)
        with pytest.raises(ValueError, match="Dimension mismatch"):
            noise.transform(u_wrong_dim)


class TestMultiQubitBraidCircuit:
    """Test suite for MultiQubitBraidCircuit Clifford gate synthesis."""

    def test_initialization_and_validation(self):
        c = MultiQubitBraidCircuit(2)
        assert c.num_qubits == 2
        assert c.num_modes == 8

        with pytest.raises(ValueError, match="num_qubits must be integer >= 1"):
            MultiQubitBraidCircuit(0)
        with pytest.raises(ValueError, match="num_qubits must be integer >= 1"):
            MultiQubitBraidCircuit(True)

    def test_phase_gate(self):
        c = MultiQubitBraidCircuit(1)
        c.append_phase(1)
        mat = c.evaluate_matrix()
        assert mat.dim == 4
        assert mat.is_orthogonal() is True
        assert mat.determinant() == Fraction(1, 1)

        # Inverse phase
        c_inv = MultiQubitBraidCircuit(1)
        c_inv.append_phase(1, inverse=True)
        mat_inv = c_inv.evaluate_matrix()
        # S * S^{-1} == I
        prod = mat.multiply(mat_inv)
        assert prod == ExactSignedPermutationMatrix.identity(4)

    def test_hadamard_gate(self):
        c = MultiQubitBraidCircuit(1)
        c.append_hadamard(1)
        mat = c.evaluate_matrix()
        assert mat.dim == 4
        assert mat.is_orthogonal() is True
        assert mat.determinant() == Fraction(1, 1)

        # Inverse Hadamard
        c_inv = MultiQubitBraidCircuit(1)
        c_inv.append_hadamard(1, inverse=True)
        mat_inv = c_inv.evaluate_matrix()
        prod = mat.multiply(mat_inv)
        assert prod == ExactSignedPermutationMatrix.identity(4)

    def test_cnot_and_multi_qubit_circuit(self):
        c = MultiQubitBraidCircuit(2)
        c.append_phase(1)
        c.append_hadamard(2)
        c.append_cnot(1, 2)
        mat = c.evaluate_matrix()
        assert mat.dim == 8
        assert mat.is_orthogonal() is True
        assert mat.determinant() == Fraction(1, 1)

    def test_circuit_argument_validation(self):
        c = MultiQubitBraidCircuit(2)
        with pytest.raises(ValueError, match="qubit=0 out of range"):
            c.append_phase(0)
        with pytest.raises(ValueError, match="qubit=3 out of range"):
            c.append_hadamard(3)
        with pytest.raises(ValueError, match="Qubit index out of range"):
            c.append_cnot(0, 1)
        with pytest.raises(ValueError, match="must be distinct"):
            c.append_cnot(1, 1)
        with pytest.raises(ValueError, match="Adjacent swap requires"):
            c3 = MultiQubitBraidCircuit(3)
            c3.append_swap(1, 3)
        # Non-local CNOT is supported via topological SWAP routing
        c3.append_cnot(1, 3)
        mat3 = c3.evaluate_matrix()
        assert mat3.is_orthogonal() is True
        assert mat3.determinant() == Fraction(1, 1)


class TestMultiQubitNoisyBraidReferee:
    """Test suite for MultiQubitNoisyBraidReferee PFP evaluation."""

    def test_packet_digest_and_receipt_evaluation(self):
        packet = MultiQubitNoisyBraidProposalPacket(
            round_id="round_001",
            proposer_id="agent_qubit_proposer",
            num_qubits=2,
            operations=(
                ("phase", (1, 0)),
                ("hadamard", (2, 0)),
                ("cnot", (1, 2)),
            ),
            noise_couplings=(
                (1, 2, Fraction(1, 100)),
            ),
            tolerance_epsilon=Fraction(1, 50),
        )
        digest = packet.canonical_digest()
        assert isinstance(digest, str)
        assert len(digest) == 64

        referee = MultiQubitNoisyBraidReferee()
        receipt = referee.evaluate(packet)
        assert receipt.is_accepted is True
        assert receipt.status_reason == "ACCEPTED_STABLE"
        assert receipt.num_qubits == 2
        assert receipt.num_modes == 8
        assert receipt.gate_count == 3
        assert receipt.is_so_dim is True
        assert receipt.determinant == Fraction(1, 1)
        assert receipt.authority_effect == "None"

    def test_rejection_on_excessive_noise(self):
        packet = MultiQubitNoisyBraidProposalPacket(
            round_id="round_noisy",
            proposer_id="agent_qubit_proposer",
            num_qubits=2,
            operations=(
                ("phase", (1, 0)),
            ),
            noise_couplings=(
                (1, 3, Fraction(1, 2)),
            ),
            tolerance_epsilon=Fraction(1, 10),
        )
        referee = MultiQubitNoisyBraidReferee()
        receipt = referee.evaluate(packet)
        assert receipt.is_accepted is False
        assert receipt.status_reason == "REFUSAL_NOISE_LEAKAGE"
        assert receipt.circuit_noise_defect > receipt.tolerance_epsilon

    def test_rejection_on_invalid_operation(self):
        packet = MultiQubitNoisyBraidProposalPacket(
            round_id="round_invalid",
            proposer_id="agent_qubit_proposer",
            num_qubits=2,
            operations=(
                ("magic_gate", (1,)),
            ),
            noise_couplings=(),
            tolerance_epsilon=Fraction(1, 10),
        )
        referee = MultiQubitNoisyBraidReferee()
        receipt = referee.evaluate(packet)
        assert receipt.is_accepted is False
        assert "REFUSAL_UNKNOWN_OP" in receipt.status_reason

    def test_rejection_on_invalid_qubits(self):
        # We can construct packet with 0 qubits by bypassing dataclass if needed, or pass 0
        packet = MultiQubitNoisyBraidProposalPacket(
            round_id="round_0q",
            proposer_id="agent_qubit_proposer",
            num_qubits=0,
            operations=(),
            noise_couplings=(),
            tolerance_epsilon=Fraction(1, 10),
        )
        referee = MultiQubitNoisyBraidReferee()
        receipt = referee.evaluate(packet)
        assert receipt.is_accepted is False
        assert receipt.status_reason == "REFUSAL_INVALID_QUBITS"

    def test_circuit_with_elementary_and_exceptions(self):
        c = MultiQubitBraidCircuit(1)
        c.append_elementary(1)
        c.append_elementary(1, inverse=True)
        mat = c.evaluate_matrix()
        assert mat.is_orthogonal() is True

        # Test stray_couplings out of bounds
        with pytest.raises(ValueError, match="out of range"):
            LocalMajoranaNoise.stray_couplings(4, [(0, 1, Fraction(1, 1))])

        referee = MultiQubitNoisyBraidReferee()
        # Circuit build exception
        bad_circuit_packet = MultiQubitNoisyBraidProposalPacket(
            round_id="round_bad_cnot",
            proposer_id="agent_qubit_proposer",
            num_qubits=2,
            operations=(("cnot", (1, 1)),),
            noise_couplings=(),
            tolerance_epsilon=Fraction(1, 10),
        )
        r1 = referee.evaluate(bad_circuit_packet)
        assert r1.is_accepted is False
        assert "REFUSAL_CIRCUIT_BUILD_FAILED" in r1.status_reason

        # Invalid noise exception
        bad_noise_packet = MultiQubitNoisyBraidProposalPacket(
            round_id="round_bad_noise",
            proposer_id="agent_qubit_proposer",
            num_qubits=1,
            operations=(),
            noise_couplings=((1, 1, Fraction(1, 1)),),
            tolerance_epsilon=Fraction(1, 10),
        )
        r2 = referee.evaluate(bad_noise_packet)
        assert r2.is_accepted is False
        assert "REFUSAL_INVALID_NOISE" in r2.status_reason

    def test_type_error_on_float_tolerance(self):
        with pytest.raises(TypeError, match="tolerance_epsilon must be Fraction or int"):
            MultiQubitNoisyBraidProposalPacket(
                round_id="round_float",
                proposer_id="agent_qubit_proposer",
                num_qubits=1,
                operations=(),
                noise_couplings=(),
                tolerance_epsilon=0.1,  # Forbidden float
            )

    def test_nonlocal_cnot_and_swap_4qubits(self):
        c4 = MultiQubitBraidCircuit(4)
        c4.append_hadamard(1)
        c4.append_cnot(1, 4)
        mat = c4.evaluate_matrix()
        assert mat.dim == 16
        assert mat.is_orthogonal() is True
        assert mat.determinant() == Fraction(1, 1)

    def test_correlated_cluster_couplings(self):
        couplings = LocalMajoranaNoise.correlated_cluster_couplings(
            num_qubits=4, lattice_l=8, budget=Fraction(1, 10), seed=42
        )
        assert len(couplings) == 120  # 16 * 15 / 2
        noise = LocalMajoranaNoise.stray_couplings(16, couplings)
        assert noise.dim == 16
        assert noise.max_leakage() > Fraction(0, 1)
