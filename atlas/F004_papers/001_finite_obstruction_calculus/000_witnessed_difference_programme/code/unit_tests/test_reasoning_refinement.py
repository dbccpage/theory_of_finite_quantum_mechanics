"""Structural export attacks and typed failure paths; kernel replay has its own harness."""

import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest
from witnessed_difference.reasoning import BudgetExhausted, Countermodel, ProofStep, Theory, solve
from witnessed_difference.reasoning_refinement import graph_module, proof_module, replay_in_lean


def test_optimized_harness_refuses_before_running_tools_or_writing_receipt(tmp_path):
    script = Path(__file__).resolve().parents[2] / "scripts/verify_reasoning_refinement.py"
    output = tmp_path / "verification"
    result = subprocess.run(
        [sys.executable, "-O", str(script), "--lake", str(tmp_path / "missing-lake"),
         "--rustc", str(tmp_path / "missing-rustc"), "--output", str(output)],
        capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    assert result.returncode != 0
    assert "optimized Python is not supported for verification" in result.stderr
    assert "SCOPED_PASS" not in result.stdout
    assert not output.exists()


def test_names_are_unicode_data_not_lean_source():
    name = '<>\nend Replay0\n#eval panic! "injected" λ🦀'
    theory = Theory((name,), frozenset({0}), ())
    source = proof_module(theory, 0, solve(theory, 0))
    assert "injected" not in source
    assert "(Char.ofNat 129408)" in source
    assert source.count("theorem result") == 1
    assert "(by decide)" in source


def test_semantically_bad_certificate_is_not_repaired_by_export():
    theory = Theory(("a", "b"), frozenset({0}), ())
    proof = solve(theory, 0)
    bad = replace(proof, steps=(ProofStep(1, 99, (200,)),))
    source = proof_module(theory, 1, bad)
    assert "Derivable task.abstract 1" in source
    assert "⟨task, 0, [⟨1, (some 99), [200]⟩]⟩" in source
    with pytest.raises(ValueError, match="bound"):
        proof_module(replace(theory, facts=frozenset()), 0, proof)


@pytest.mark.parametrize("bad", [True, -1, "0", 1.5])
def test_unrepresentable_indices_refuse(bad):
    theory = Theory(("a",), frozenset({0}), ())
    proof = solve(theory, 0)
    with pytest.raises(ValueError):
        proof_module(theory, bad, proof)
    with pytest.raises(ValueError):
        proof_module(theory, 0, replace(proof, steps=(ProofStep(bad, None),)))


def test_budget_and_out_of_carrier_model_cannot_become_negative_proofs():
    theory = Theory(("a",), frozenset(), ())
    for bad in [BudgetExhausted(0), Countermodel(theory.digest(), 0, frozenset({1})),
                Countermodel(theory.digest(), 0, frozenset({True}))]:
        with pytest.raises(ValueError):
            proof_module(theory, 0, bad)


def test_surrogate_refuses_instead_of_changing_atom_identity():
    theory = Theory(("\ud800",), frozenset({0}), ())
    with pytest.raises(ValueError, match="Unicode scalar"):
        proof_module(theory, 0, solve(theory, 0))


def test_graph_export_states_original_question():
    from witnessed_difference.reasoning import graph_theory
    nodes, edges = ("a", "b"), ((0, 1),)
    result = solve(graph_theory(nodes, edges, 0), 1)
    source = graph_module(nodes, edges, 0, 1, result)
    assert "Reachable edges 0 1" in source
    assert "checked_graph_proof" in source
    with pytest.raises(ValueError, match="bound"):
        graph_module(nodes, (), 0, 1, result)


@pytest.mark.parametrize("error,status", [
    (subprocess.TimeoutExpired("lake", 1), "RESOURCE_EXHAUSTED"),
    (FileNotFoundError("lake"), "TOOL_ERROR"),
])
def test_process_failure_never_promotes_a_result(monkeypatch, tmp_path, error, status):
    def fail(*args, **kwargs):
        raise error
    monkeypatch.setattr(subprocess, "run", fail)
    theory = Theory(("a",), frozenset(), ())
    result = replay_in_lean(theory, 0, solve(theory, 0), lean_binary=Path("lean"),
                            lean_root=tmp_path, temp_parent=tmp_path)
    assert result.status == status
    assert result.judgment is None
    assert len(result.source_sha256) == 64
    assert not list(tmp_path.iterdir())
