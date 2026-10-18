"""Exact finite Euler arithmetic and adversarial cancellation certificates."""

from fractions import Fraction
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fermionic_hamiltonian import DiscreteFermionicHamiltonian, FermionicLattice
from hamiltonian_gin_bridge import HamiltonianGinBridge


def _synthetic_index(bridge, monkeypatch, amplitudes, name="ExactFixture"):
    """Isolate the index/auditor from the separately tested path generator."""
    model = DiscreteFermionicHamiltonian(FermionicLattice.linear_chain(2), num_up=1, num_down=0)
    rows = [{"path_indices": (0, 0), "signed_amplitude": w,
             "abs_weight": abs(w), "parity": 1 if w > 0 else -1}
            for w in map(Fraction, amplitudes)]
    monkeypatch.setattr(model, "generate_sample_paths", lambda **_: rows)
    return bridge.index_hamiltonian_paths(model, model_name=name)


def test_fraction_couplings_and_binary_float_inputs_are_distinct_exact_data():
    lattice = FermionicLattice.linear_chain(2)
    rational = DiscreteFermionicHamiltonian(lattice, t=Fraction(1, 10), u=0, num_up=1, num_down=0)
    binary = DiscreteFermionicHamiltonian(lattice, t=0.1, u=0, num_up=1, num_down=0)
    assert rational.matrix[0][1] == -Fraction(1, 10)
    assert binary.matrix[0][1] == -Fraction.from_float(0.1)
    assert rational.matrix != binary.matrix
    assert rational.exact_transfer_matrix(Fraction(1, 7), 3)[0][1] == Fraction(1, 210)


def test_tiny_negative_exchange_paths_are_not_dropped():
    model = DiscreteFermionicHamiltonian.create_free_triangle(t=Fraction(1, 10**30))
    paths = model.generate_sample_paths(beta=1, trotter_steps=3)
    negatives = [p for p in paths if p["parity"] == -1]
    assert len(paths) == 27
    assert len(negatives) == 6
    assert {p["signed_amplitude"] for p in negatives} == {-Fraction(1, 27 * 10**90)}


def test_path_sum_equals_independent_exact_matrix_cube():
    model = DiscreteFermionicHamiltonian(
        FermionicLattice.linear_chain(2), t=Fraction(2, 7), u=Fraction(3, 5), num_up=1, num_down=1)
    transfer = model.exact_transfer_matrix(Fraction(5, 11), 3)
    expected = sum((transfer[i][j] * transfer[j][k] * transfer[k][i]
                    for i in range(model.dim) for j in range(model.dim)
                    for k in range(model.dim)), Fraction(0))
    paths = model.generate_sample_paths(Fraction(5, 11), 3)
    assert sum((p["signed_amplitude"] for p in paths), Fraction(0)) == expected
    assert all(isinstance(p["signed_amplitude"], Fraction) for p in paths)
    totals = model.compute_partition_functions(Fraction(5, 11), 3)
    assert Fraction(totals["z_fermionic_rational"]) == expected
    assert Fraction(totals["z_bosonic_rational"]) == sum((p["abs_weight"] for p in paths), Fraction(0))


def test_tiny_unequal_weights_never_pair(monkeypatch):
    bridge = HamiltonianGinBridge()
    try:
        result = _synthetic_index(bridge, monkeypatch, [1, -1 - Fraction(1, 10**13), 2])
        assert result["matched_pairs"] == 0
        receipt = bridge.audit_sign_resolution("ExactFixture")
        assert receipt.terminal_route == "SplitBrainRefusal"
        assert receipt.exact_unpaired_negative_mass == 1 + Fraction(1, 10**13)
    finally:
        bridge.close()


def test_sub_float_negative_mass_still_refuses(monkeypatch):
    bridge = HamiltonianGinBridge()
    try:
        _synthetic_index(bridge, monkeypatch, [1, -Fraction(1, 10**600)])
        receipt = bridge.audit_sign_resolution("ExactFixture")
        assert receipt.exact_unpaired_negative_mass == Fraction(1, 10**600)
        assert receipt.terminal_route == "SplitBrainRefusal"
        assert not receipt.all_exact_cancellations
    finally:
        bridge.close()


def test_zero_signed_quotient_is_not_a_positive_ensemble(monkeypatch):
    bridge = HamiltonianGinBridge()
    try:
        _synthetic_index(bridge, monkeypatch, [1, -1])
        receipt = bridge.audit_sign_resolution("ExactFixture")
        assert receipt.exact_signed_sum == receipt.exact_residual_mass == 0
        assert receipt.terminal_route == "ZeroResidualRefusal"
        assert receipt.gin_quotiented_average_sign == 0
        assert not receipt.all_exact_cancellations
    finally:
        bridge.close()


@pytest.mark.parametrize("mutation", ["duplicate", "cross_model", "sign", "weight", "rational", "missing", "same_sign"])
def test_pair_and_record_mutations_fail_closed(monkeypatch, mutation):
    bridge = HamiltonianGinBridge()
    try:
        _synthetic_index(bridge, monkeypatch, [1, -1, 2], "A")
        _synthetic_index(bridge, monkeypatch, [1, -1, 2], "B")
        assert bridge.audit_sign_resolution("A").terminal_route == "Repair"
        p = bridge.conn.execute("SELECT * FROM GinInvolutionPairs ORDER BY pair_id").fetchall()
        pos, neg = p[0]["cfg_pos_id"], p[0]["cfg_neg_id"]
        if mutation == "duplicate":
            bridge.conn.execute("INSERT INTO GinInvolutionPairs VALUES (900, ?, ?, 'duplicate', 1)", (pos, neg))
        elif mutation == "cross_model":
            bridge.conn.execute("UPDATE GinInvolutionPairs SET cfg_neg_id=? WHERE pair_id=?", (p[1]["cfg_neg_id"], p[0]["pair_id"]))
        elif mutation == "sign":
            bridge.conn.execute("UPDATE FermionConfigurations SET jw_sign=1 WHERE cfg_id=?", (neg,))
        elif mutation == "weight":
            bridge.conn.execute("UPDATE FermionConfigurations SET weight=1.0000000000001 WHERE cfg_id=?", (neg,))
        elif mutation == "rational":
            bridge.conn.execute("UPDATE ExactHamiltonianPathWeights SET numerator='2' WHERE cfg_id=?", (neg,))
        elif mutation == "missing":
            bridge.conn.execute("DELETE FROM FermionConfigurations WHERE cfg_id=?", (neg,))
        else:
            bridge.conn.execute("UPDATE GinInvolutionPairs SET cfg_neg_id=? WHERE pair_id=?", (pos + 2, p[0]["pair_id"]))
        receipt = bridge.audit_sign_resolution("A")
        assert receipt.terminal_route == "SplitBrainRefusal"
        assert receipt.integrity_errors
        assert not receipt.all_exact_cancellations
    finally:
        bridge.close()


def test_repeated_model_batches_are_disjoint_and_cannot_cross_pair(monkeypatch):
    bridge = HamiltonianGinBridge()
    try:
        a = _synthetic_index(bridge, monkeypatch, [1, -1, 2])
        b = _synthetic_index(bridge, monkeypatch, [1, -1, 2])
        assert a["ensemble_id"] != b["ensemble_id"]
        receipt = bridge.audit_sign_resolution("ExactFixture")
        assert receipt.terminal_route == "Repair"
        assert receipt.pairs_audited == 2
        pairs = bridge.conn.execute("SELECT * FROM GinInvolutionPairs ORDER BY pair_id").fetchall()
        bridge.conn.execute("UPDATE GinInvolutionPairs SET cfg_neg_id=? WHERE pair_id=?",
                            (pairs[1]["cfg_neg_id"], pairs[0]["pair_id"]))
        bridge.conn.execute("UPDATE GinInvolutionPairs SET cfg_neg_id=? WHERE pair_id=?",
                            (pairs[0]["cfg_neg_id"], pairs[1]["pair_id"]))
        assert bridge.audit_sign_resolution("ExactFixture").terminal_route == "SplitBrainRefusal"
    finally:
        bridge.close()
