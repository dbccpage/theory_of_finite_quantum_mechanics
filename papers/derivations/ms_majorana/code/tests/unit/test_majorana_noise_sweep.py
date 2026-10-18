"""test_majorana_noise_sweep.py — Unit Tests for Multi-Parameter Rational Noise Sweeps.

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

from majorana_noise_sweep import (
    DeterministicRationalNoiseGenerator,
    MultiQubitNoiseSweepReceipt,
    MultiQubitNoiseSweepRunner,
    NoiseSweepDataPoint,
)


class TestDeterministicRationalNoiseGenerator:
    """Test suite for deterministic rational noise generator."""

    def test_seed_validation(self):
        gen = DeterministicRationalNoiseGenerator(seed=12345)
        assert gen._state == 12345

        with pytest.raises(TypeError, match="seed must be an integer"):
            DeterministicRationalNoiseGenerator(seed="not_an_int")
        with pytest.raises(TypeError, match="seed must be an integer"):
            DeterministicRationalNoiseGenerator(seed=True)

    def test_next_int_in_range(self):
        gen = DeterministicRationalNoiseGenerator(seed=42)
        val = gen.next_int_in_range(5, 15)
        assert 5 <= val <= 15

        with pytest.raises(ValueError, match="min_val 10 > max_val 5"):
            gen.next_int_in_range(10, 5)

    def test_next_fraction(self):
        gen = DeterministicRationalNoiseGenerator(seed=42)
        frac = gen.next_fraction(max_denom=20, scale_bound=Fraction(1, 10))
        assert isinstance(frac, Fraction)
        assert abs(frac) <= Fraction(1, 10)

        with pytest.raises(ValueError, match="max_denom must be >= 1"):
            gen.next_fraction(max_denom=0)
        with pytest.raises(TypeError, match="scale_bound must be Fraction or int"):
            gen.next_fraction(scale_bound=0.1)

    def test_generate_skew_symmetric_matrix(self):
        gen = DeterministicRationalNoiseGenerator(seed=100)
        noise = gen.generate_skew_symmetric_matrix(
            dim=6,
            scale_bound=Fraction(1, 20),
            density=Fraction(1, 1),
        )
        assert noise.dim == 6
        for r in range(6):
            assert noise.data[r][r] == Fraction(0, 1)
            for c in range(r + 1, 6):
                assert noise.data[r][c] == -noise.data[c][r]
                assert abs(noise.data[r][c]) <= Fraction(1, 20)

    def test_density_zero_and_validations(self):
        gen = DeterministicRationalNoiseGenerator(seed=100)
        zero_noise = gen.generate_skew_symmetric_matrix(
            dim=4,
            density=Fraction(0, 1),
        )
        assert zero_noise.max_leakage() == Fraction(0, 1)

        with pytest.raises(ValueError, match="dim must be >= 2"):
            gen.generate_skew_symmetric_matrix(dim=1)
        with pytest.raises(ValueError, match="density must be in"):
            gen.generate_skew_symmetric_matrix(dim=4, density=Fraction(-1, 2))


class TestNoiseSweepDataPointAndReceipt:
    """Test suite for data points and receipts."""

    def test_data_point_validation(self):
        pt = NoiseSweepDataPoint(
            point_id="pt_01",
            num_qubits=2,
            num_modes=8,
            noise_scale=Fraction(1, 100),
            tolerance_epsilon=Fraction(1, 50),
            commutation_defect=Fraction(1, 100),
            max_leakage=Fraction(1, 50),
            is_accepted=True,
            status_reason="ACCEPTED_STABLE",
        )
        assert pt.point_id == "pt_01"
        assert pt.is_accepted is True

        with pytest.raises(TypeError, match="noise_scale must be Fraction or int"):
            NoiseSweepDataPoint(
                point_id="pt_bad",
                num_qubits=1,
                num_modes=4,
                noise_scale=0.1,  # float forbidden
                tolerance_epsilon=Fraction(1, 10),
                commutation_defect=Fraction(0, 1),
                max_leakage=Fraction(0, 1),
                is_accepted=True,
                status_reason="OK",
            )


class TestMultiQubitNoiseSweepRunner:
    """Test suite for MultiQubitNoiseSweepRunner grid sweeps."""

    def test_runner_sweep_execution(self):
        runner = MultiQubitNoiseSweepRunner(seed=42)
        receipt = runner.run_sweep(
            qubit_counts=(1, 2),
            noise_scales=(Fraction(1, 100), Fraction(1, 10)),
            tolerances=(Fraction(1, 50),),
            trials_per_config=1,
            density=Fraction(1, 1),
        )
        assert receipt.total_evaluations == 4
        assert receipt.sharp_boundary_verified is True
        assert receipt.authority_effect == "None"
        assert len(receipt.canonical_digest()) == 64
        assert len(receipt.data_points) == 4

    def test_runner_qubit_3_execution(self):
        runner = MultiQubitNoiseSweepRunner(seed=99)
        receipt = runner.run_sweep(
            qubit_counts=(3,),  # 12 modes
            noise_scales=(Fraction(1, 50),),
            tolerances=(Fraction(1, 20),),
            trials_per_config=1,
        )
        assert receipt.total_evaluations == 1
        assert receipt.sharp_boundary_verified is True

    def test_runner_argument_validations(self):
        runner = MultiQubitNoiseSweepRunner(seed=42)
        with pytest.raises(ValueError, match="qubit_counts must contain integers >= 1"):
            runner.run_sweep(qubit_counts=())
        with pytest.raises(ValueError, match="qubit_counts must contain integers >= 1"):
            runner.run_sweep(qubit_counts=(0,))
        with pytest.raises(ValueError, match="noise_scales cannot be empty"):
            runner.run_sweep(qubit_counts=(1,), noise_scales=())
        with pytest.raises(ValueError, match="tolerances cannot be empty"):
            runner.run_sweep(qubit_counts=(1,), tolerances=())
        with pytest.raises(ValueError, match="trials_per_config must be >= 1"):
            runner.run_sweep(qubit_counts=(1,), trials_per_config=0)
